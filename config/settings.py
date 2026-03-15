"""
Configuration settings for the Daily AI Newsletter Generator.

This module centralizes all configuration values for the pipeline,
including API endpoints, timeouts, and output settings.
"""

import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Date and Time Settings
CURRENT_DATE = datetime.now()
DATE_FORMAT = "%Y-%m-%d"
TIMEZONE = "UTC"

# API Settings
ARXIV_API_BASE_URL = "http://export.arxiv.org/api/query?"
ARXIV_CATEGORIES = ["cs.AI", "cs.LG", "cs.CL", "cs.CV"]
ARXIV_MAX_RESULTS = 20
ARXIV_TIMEOUT = 10

# Apify Settings
APIFY_API_BASE_URL = "https://api.apify.com/v2"
APIFY_TIMEOUT = 30

# Substack Settings
SUBSTACK_TIMEOUT = 10

# Article Filtering
HOURS_LOOKBACK = 24  # Fetch content from last 24 hours
SUBSTACK_HOURS_LOOKBACK = 168  # Substack uses 7-day lookback (weekly newsletters)
MAX_SOURCE_AGE_DAYS = 3  # Maximum age of sources: 2-3 days (evaluated sources)

# API Settings - Anthropic/Claude
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")  # Loaded from .env or environment
ENABLE_RELEVANCE_EVALUATION = bool(ANTHROPIC_API_KEY)  # Only enable if API key is set

# Summarization Settings
MAX_SUMMARY_TOKENS = 150
SUMMARY_STYLE = "bullet_points"

# Output Settings
OUTPUT_DIR = "output/newsletters"
OUTPUT_FILENAME_TEMPLATE = "{date}-ai-newsletter.md"

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# User Profile for Personalization
USER_PROFILE = {
    "name": "User",
    "interests": ["LLMs", "AI safety", "practical applications", "open-source AI"],
    "expertise_level": "intermediate",
    "learning_goal": "master AI developments daily"
}
