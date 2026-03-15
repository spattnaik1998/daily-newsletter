"""
FastAPI backend for the Daily AI Newsletter Generator frontend.

Provides REST API endpoints for:
- Newsletter generation and retrieval
- Pipeline statistics
- User profile management
- Settings management
- Archive browsing
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import json
from typing import Optional, Dict, Any, List
import asyncio
import logging

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.daily_pipeline import DailyPipeline
from config.settings import USER_PROFILE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Daily AI Newsletter API",
    description="REST API for the Daily AI Newsletter Generator",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
pipeline: Optional[DailyPipeline] = None
is_generating = False
last_generation_time = 0
last_stats = {
    "execution_time": 0,
    "cache_hit_rate": 0,
    "articles_fetched": 0,
    "papers_fetched": 0,
    "posts_fetched": 0,
    "duplicates_removed": 0,
    "fetch_time": 0,
    "last_run": "Never",
    "status": "idle"
}

# Newsletters directory
NEWSLETTERS_DIR = Path(__file__).parent.parent / "output" / "newsletters"


@app.on_event("startup")
async def startup():
    """Initialize the pipeline on startup."""
    global pipeline
    logger.info("Initializing Daily AI Newsletter Pipeline...")
    try:
        pipeline = DailyPipeline(use_relevance_eval=True)
        logger.info("✓ Pipeline initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize pipeline: {e}")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "pipeline_ready": pipeline is not None
    }


@app.post("/api/newsletter/generate")
async def generate_newsletter(background_tasks: BackgroundTasks):
    """
    Generate a new newsletter.

    Returns immediately with generation status.
    Backend task runs in background.
    """
    global is_generating, pipeline, last_generation_time, last_stats

    if is_generating:
        return {
            "status": "error",
            "message": "Newsletter generation already in progress",
            "data": None
        }

    if pipeline is None:
        raise HTTPException(status_code=500, detail="Pipeline not initialized")

    is_generating = True
    last_stats["status"] = "running"

    async def _generate_in_background():
        global is_generating, last_generation_time, last_stats
        try:
            logger.info("Starting newsletter generation...")
            start_time = datetime.utcnow()

            # Run pipeline
            newsletter_content, metadata = pipeline.run(hours=24)

            # Save newsletter
            today = start_time.strftime("%Y-%m-%d")
            newsletter_path = NEWSLETTERS_DIR / f"{today}-ai-newsletter.md"
            newsletter_path.parent.mkdir(parents=True, exist_ok=True)

            with open(newsletter_path, 'w', encoding='utf-8') as f:
                f.write(newsletter_content)

            logger.info(f"✓ Newsletter saved to {newsletter_path}")

            # Update stats
            end_time = datetime.utcnow()
            execution_time = (end_time - start_time).total_seconds()
            last_generation_time = execution_time
            last_stats = {
                "execution_time": execution_time,
                "cache_hit_rate": metadata.get("cache_hit_rate", 0),
                "articles_fetched": metadata.get("articles_count", 0),
                "papers_fetched": metadata.get("papers_count", 0),
                "posts_fetched": metadata.get("posts_count", 0),
                "duplicates_removed": metadata.get("duplicates_removed", 0),
                "fetch_time": metadata.get("parallel_fetch_time", 0),
                "last_run": start_time.isoformat(),
                "status": "completed"
            }

            is_generating = False
            logger.info(f"✓ Generation completed in {execution_time:.2f}s")

        except Exception as e:
            logger.error(f"Error generating newsletter: {e}")
            last_stats["status"] = "error"
            is_generating = False

    background_tasks.add_task(_generate_in_background)

    return {
        "status": "success",
        "message": "Newsletter generation started",
        "data": {
            "generation_started": datetime.utcnow().isoformat(),
            "check_status_at": "/api/newsletter/status"
        }
    }


@app.get("/api/newsletter/status")
async def newsletter_status():
    """Get the current generation status."""
    return {
        "status": "success",
        "data": {
            "is_generating": is_generating,
            "last_status": last_stats.get("status", "idle"),
            "last_execution_time": last_generation_time,
            "last_run": last_stats.get("last_run", "Never")
        }
    }


@app.get("/api/newsletter/latest")
async def get_latest_newsletter():
    """Get the latest generated newsletter."""
    try:
        # Find most recent newsletter file
        newsletter_files = sorted(
            NEWSLETTERS_DIR.glob("*-ai-newsletter.md"),
            reverse=True
        )

        if not newsletter_files:
            return {
                "status": "error",
                "message": "No newsletters found",
                "data": None
            }

        latest_file = newsletter_files[0]

        with open(latest_file, 'r', encoding='utf-8') as f:
            content = f.read()

        return {
            "status": "success",
            "data": {
                "content": content,
                "date": latest_file.stem.split('-ai-')[0],
                "file_path": str(latest_file),
                "created_at": datetime.fromtimestamp(latest_file.stat().st_mtime).isoformat()
            }
        }

    except Exception as e:
        logger.error(f"Error retrieving latest newsletter: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/newsletter/archive")
async def get_newsletter_archive(limit: int = 30):
    """Get list of archived newsletters."""
    try:
        newsletter_files = sorted(
            NEWSLETTERS_DIR.glob("*-ai-newsletter.md"),
            reverse=True
        )[:limit]

        newsletters = []
        for file in newsletter_files:
            newsletters.append({
                "date": file.stem.split('-ai-')[0],
                "file_path": str(file),
                "created_at": datetime.fromtimestamp(file.stat().st_mtime).isoformat(),
                "size_kb": file.stat().st_size / 1024
            })

        return {
            "status": "success",
            "data": newsletters
        }

    except Exception as e:
        logger.error(f"Error retrieving archive: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/newsletter/{date}")
async def get_newsletter_by_date(date: str):
    """Get newsletter for specific date (format: YYYY-MM-DD)."""
    try:
        newsletter_path = NEWSLETTERS_DIR / f"{date}-ai-newsletter.md"

        if not newsletter_path.exists():
            raise HTTPException(status_code=404, detail=f"No newsletter found for {date}")

        with open(newsletter_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return {
            "status": "success",
            "data": {
                "content": content,
                "date": date,
                "created_at": datetime.fromtimestamp(newsletter_path.stat().st_mtime).isoformat()
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving newsletter for {date}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_pipeline_stats():
    """Get current pipeline statistics."""
    return {
        "status": "success",
        "data": last_stats
    }


@app.get("/api/user-profile")
async def get_user_profile():
    """Get current user profile."""
    return {
        "status": "success",
        "data": USER_PROFILE
    }


@app.post("/api/user-profile")
async def update_user_profile(profile: Dict[str, Any]):
    """Update user profile."""
    try:
        # Validate profile
        required_fields = ["name", "interests", "expertise_level", "learning_goal"]
        if not all(field in profile for field in required_fields):
            raise HTTPException(status_code=400, detail="Missing required fields")

        # Save to settings (in real app, would persist to database)
        logger.info(f"User profile updated: {profile['name']}")

        return {
            "status": "success",
            "message": "Profile updated successfully",
            "data": profile
        }

    except Exception as e:
        logger.error(f"Error updating profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/settings")
async def update_settings(settings: Dict[str, Any]):
    """Update pipeline settings."""
    try:
        logger.info(f"Settings updated: {settings}")

        return {
            "status": "success",
            "message": "Settings saved successfully",
            "data": settings
        }

    except Exception as e:
        logger.error(f"Error updating settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/morning-brief/latest")
async def get_latest_morning_brief():
    """Get the latest morning brief."""
    try:
        # For now, return from latest newsletter metadata
        newsletter_files = sorted(
            NEWSLETTERS_DIR.glob("*-ai-newsletter.md"),
            reverse=True
        )

        if not newsletter_files:
            return {
                "status": "error",
                "message": "No morning brief available",
                "data": None
            }

        # In a real implementation, would extract morning brief from newsletter
        return {
            "status": "success",
            "data": {
                "content": "Morning brief content would be here",
                "generated_at": datetime.utcnow().isoformat()
            }
        }

    except Exception as e:
        logger.error(f"Error retrieving morning brief: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Root endpoint
@app.get("/")
async def root():
    """API information endpoint."""
    return {
        "name": "Daily AI Newsletter Generator API",
        "version": "1.0.0",
        "description": "REST API for automated AI news curation",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "newsletter": "/api/newsletter",
            "stats": "/api/stats",
            "profile": "/api/user-profile",
            "settings": "/api/settings"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
