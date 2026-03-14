"""
FastAPI Backend Server for Daily AI Newsletter Generator.

This server provides REST API endpoints for the frontend to:
- Fetch the latest newsletter
- Access newsletter archive
- Trigger newsletter generation
- Manage schedule and settings
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

from fastapi import FastAPI, HTTPException, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Daily AI Newsletter API",
    description="API for the Daily AI Newsletter Generator",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
OUTPUT_DIR = Path("output/newsletters")
NEWSLETTERS_DIR = OUTPUT_DIR
DATE_FORMAT = "%Y-%m-%d"


# Pydantic models
class NewsletterResponse(BaseModel):
    """Response model for newsletter data."""
    date: str
    content: str
    metadata: Dict[str, Any]
    generated_at: str


class StatsResponse(BaseModel):
    """Response model for statistics."""
    date: str
    articles: int
    papers: int
    posts: int
    themes: List[str]


class GenerationStatus(BaseModel):
    """Response model for generation status."""
    status: str
    message: str
    job_id: Optional[str] = None


class ArchiveItem(BaseModel):
    """Response model for archive items."""
    date: str
    filename: str
    size: int


class ArchiveResponse(BaseModel):
    """Response model for archive list."""
    items: List[ArchiveItem]
    total: int
    page: int
    limit: int


# Helper functions
def get_newsletter_file(date: str) -> Optional[Path]:
    """Get the path to a newsletter file by date."""
    filename = f"{date}-ai-newsletter.md"
    filepath = NEWSLETTERS_DIR / filename
    if filepath.exists():
        return filepath
    return None


def get_morning_brief_file(date: str) -> Optional[Path]:
    """Get the path to a morning brief file by date."""
    filename = f"{date}-morning-brief.md"
    filepath = NEWSLETTERS_DIR / filename
    if filepath.exists():
        return filepath
    return None


def get_latest_morning_brief() -> Optional[Dict[str, Any]]:
    """Get the most recent morning brief."""
    if not NEWSLETTERS_DIR.exists():
        return None

    files = sorted(NEWSLETTERS_DIR.glob("*-morning-brief.md"), reverse=True)
    if not files:
        return None

    latest_file = files[0]
    date_str = latest_file.stem.replace("-morning-brief", "")

    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            content = f.read()

        return {
            "date": date_str,
            "content": content,
            "generated_at": datetime.fromtimestamp(latest_file.stat().st_mtime).isoformat()
        }
    except Exception as e:
        logger.error(f"Error reading morning brief: {e}")
        return None


def parse_newsletter_metadata(content: str) -> Dict[str, Any]:
    """Extract metadata from newsletter markdown content."""
    metadata = {
        "articles": 0,
        "papers": 0,
        "posts": 0,
        "themes": []
    }

    lines = content.split('\n')
    current_section = None

    for line in lines:
        if '## Major AI News' in line:
            current_section = 'articles'
        elif '## Important Research Papers' in line:
            current_section = 'papers'
        elif '## Insights from AI Newsletters' in line:
            current_section = 'posts'
        elif '## Emerging Themes' in line:
            current_section = 'themes'
        elif line.startswith('* **') and current_section == 'themes':
            # Extract theme
            theme = line.replace('* **', '').replace('**', '').strip()
            if theme:
                metadata['themes'].append(theme)
        elif line.startswith('* **') and current_section in ['articles', 'papers', 'posts']:
            if current_section == 'articles':
                metadata['articles'] += 1
            elif current_section == 'papers':
                metadata['papers'] += 1
            elif current_section == 'posts':
                metadata['posts'] += 1

    return metadata


def get_latest_newsletter() -> Optional[Dict[str, Any]]:
    """Get the most recent newsletter."""
    if not NEWSLETTERS_DIR.exists():
        return None

    files = sorted(NEWSLETTERS_DIR.glob("*-ai-newsletter.md"), reverse=True)
    if not files:
        return None

    latest_file = files[0]
    date_str = latest_file.stem.replace("-ai-newsletter", "")

    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            content = f.read()

        metadata = parse_newsletter_metadata(content)

        return {
            "date": date_str,
            "content": content,
            "metadata": metadata,
            "generated_at": datetime.fromtimestamp(latest_file.stat().st_mtime).isoformat()
        }
    except Exception as e:
        logger.error(f"Error reading newsletter: {e}")
        return None


def run_pipeline():
    """Run the newsletter generation pipeline."""
    try:
        from pipeline.daily_pipeline import DailyPipeline

        logger.info("Starting newsletter generation...")
        pipeline = DailyPipeline()
        newsletter, metadata = pipeline.run(hours=24)

        # Save newsletter and morning brief
        today_date = datetime.now().strftime(DATE_FORMAT)
        NEWSLETTERS_DIR.mkdir(parents=True, exist_ok=True)

        # Save newsletter
        filename = f"{today_date}-ai-newsletter.md"
        filepath = NEWSLETTERS_DIR / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(newsletter)
        logger.info(f"Newsletter generated successfully: {filepath}")

        # Save morning brief if available
        if metadata.get("morning_brief"):
            brief_filename = f"{today_date}-morning-brief.md"
            brief_filepath = NEWSLETTERS_DIR / brief_filename
            with open(brief_filepath, 'w', encoding='utf-8') as f:
                f.write(metadata["morning_brief"])
            logger.info(f"Morning brief generated successfully: {brief_filepath}")

        return True
    except Exception as e:
        logger.error(f"Error generating newsletter: {e}")
        return False


# API Routes
@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "running",
        "name": "Daily AI Newsletter API",
        "version": "1.0.0"
    }


@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/newsletter/latest", response_model=Optional[NewsletterResponse])
async def get_latest_newsletter_endpoint():
    """Get the latest generated newsletter."""
    newsletter = get_latest_newsletter()
    if not newsletter:
        raise HTTPException(status_code=404, detail="No newsletter found")
    return newsletter


@app.get("/api/newsletter/{date}", response_model=Optional[NewsletterResponse])
async def get_newsletter_by_date(date: str):
    """Get a newsletter by specific date (YYYY-MM-DD)."""
    filepath = get_newsletter_file(date)
    if not filepath:
        raise HTTPException(status_code=404, detail=f"Newsletter for {date} not found")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        metadata = parse_newsletter_metadata(content)

        return {
            "date": date,
            "content": content,
            "metadata": metadata,
            "generated_at": datetime.fromtimestamp(filepath.stat().st_mtime).isoformat()
        }
    except Exception as e:
        logger.error(f"Error reading newsletter: {e}")
        raise HTTPException(status_code=500, detail="Error reading newsletter")


@app.get("/api/newsletter/archive", response_model=ArchiveResponse)
async def get_archive(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100)):
    """Get newsletter archive with pagination."""
    if not NEWSLETTERS_DIR.exists():
        return ArchiveResponse(items=[], total=0, page=page, limit=limit)

    files = sorted(NEWSLETTERS_DIR.glob("*-ai-newsletter.md"), reverse=True)
    total = len(files)

    # Pagination
    start = (page - 1) * limit
    end = start + limit
    paginated_files = files[start:end]

    items = []
    for filepath in paginated_files:
        date_str = filepath.stem.replace("-ai-newsletter", "")
        items.append(
            ArchiveItem(
                date=date_str,
                filename=filepath.name,
                size=filepath.stat().st_size
            )
        )

    return ArchiveResponse(items=items, total=total, page=page, limit=limit)


@app.get("/api/newsletter/stats", response_model=StatsResponse)
async def get_latest_stats():
    """Get statistics for the latest newsletter."""
    newsletter = get_latest_newsletter()
    if not newsletter:
        raise HTTPException(status_code=404, detail="No newsletter found")

    return StatsResponse(
        date=newsletter["date"],
        articles=newsletter["metadata"].get("articles", 0),
        papers=newsletter["metadata"].get("papers", 0),
        posts=newsletter["metadata"].get("posts", 0),
        themes=newsletter["metadata"].get("themes", [])
    )


@app.post("/api/newsletter/generate", response_model=GenerationStatus)
async def generate_newsletter(background_tasks: BackgroundTasks):
    """Trigger newsletter generation (runs in background)."""
    background_tasks.add_task(run_pipeline)

    return GenerationStatus(
        status="generating",
        message="Newsletter generation started",
        job_id="bg-task-1"
    )


@app.get("/api/newsletter/{date}/download")
async def download_newsletter(date: str, format: str = Query("md", pattern="^(md|txt)$")):
    """Download newsletter in specified format."""
    filepath = get_newsletter_file(date)
    if not filepath:
        raise HTTPException(status_code=404, detail=f"Newsletter for {date} not found")

    filename = f"ai-newsletter-{date}.{format}"

    return FileResponse(
        path=filepath,
        filename=filename,
        media_type="text/markdown" if format == "md" else "text/plain"
    )


@app.get("/api/morning-brief/latest")
async def get_latest_morning_brief_endpoint():
    """Get the latest generated morning brief."""
    brief = get_latest_morning_brief()
    if not brief:
        raise HTTPException(status_code=404, detail="No morning brief found")
    return brief


@app.get("/api/morning-brief/{date}")
async def get_morning_brief_by_date(date: str):
    """Get a morning brief by specific date (YYYY-MM-DD)."""
    filepath = get_morning_brief_file(date)
    if not filepath:
        raise HTTPException(status_code=404, detail=f"Morning brief for {date} not found")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        return {
            "date": date,
            "content": content,
            "generated_at": datetime.fromtimestamp(filepath.stat().st_mtime).isoformat()
        }
    except Exception as e:
        logger.error(f"Error reading morning brief: {e}")
        raise HTTPException(status_code=500, detail="Error reading morning brief")


@app.get("/api/morning-brief/{date}/download")
async def download_morning_brief(date: str):
    """Download morning brief as markdown."""
    filepath = get_morning_brief_file(date)
    if not filepath:
        raise HTTPException(status_code=404, detail=f"Morning brief for {date} not found")

    filename = f"morning-brief-{date}.md"

    return FileResponse(
        path=filepath,
        filename=filename,
        media_type="text/markdown"
    )


@app.get("/api/settings")
async def get_settings():
    """Get current settings."""
    return {
        "max_source_age_days": 3,
        "enable_relevance_evaluation": True,
        "enable_news": True,
        "enable_papers": True,
        "enable_posts": True,
        "schedule": {
            "enabled": True,
            "time": "07:00",
            "timezone": "UTC"
        }
    }


@app.put("/api/settings")
async def update_settings(settings: Dict[str, Any]):
    """Update settings (placeholder)."""
    logger.info(f"Settings update requested: {settings}")
    return {
        "status": "success",
        "message": "Settings updated",
        "data": settings
    }


@app.get("/api/settings/sources")
async def get_sources():
    """Get configured sources."""
    return {
        "news": {
            "enabled": True,
            "sources": ["TechCrunch AI", "VentureBeat AI", "MIT Technology Review", "The Verge AI", "Hacker News"]
        },
        "papers": {
            "enabled": True,
            "categories": ["cs.AI", "cs.LG", "cs.CL", "cs.CV"]
        },
        "posts": {
            "enabled": True,
            "newsletters": ["Import AI", "Latent Space", "The Sequence", "Ben's Bites"]
        }
    }


@app.put("/api/settings/sources")
async def update_sources(sources: Dict[str, Any]):
    """Update sources configuration (placeholder)."""
    logger.info(f"Sources update requested: {sources}")
    return {
        "status": "success",
        "message": "Sources updated",
        "data": sources
    }


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


if __name__ == "__main__":
    import uvicorn

    print("Starting Daily AI Newsletter API Server...")
    print("Available at: http://localhost:8000")
    print("API docs: http://localhost:8000/docs")

    uvicorn.run(app, host="0.0.0.0", port=8000)
