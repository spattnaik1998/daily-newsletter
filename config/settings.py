"""
Configuration settings for the Daily AI Newsletter Generator.

This module centralizes all configuration values for the pipeline,
including API endpoints, timeouts, and output settings.
"""

from datetime import datetime

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

# Summarization Settings
MAX_SUMMARY_TOKENS = 150
SUMMARY_STYLE = "bullet_points"

# Output Settings
OUTPUT_DIR = "output/newsletters"
OUTPUT_FILENAME_TEMPLATE = "{date}-ai-newsletter.md"

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
