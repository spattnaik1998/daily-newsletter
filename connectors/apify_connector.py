"""
Connector for fetching AI news articles from RSS feeds.

This module provides an interface to fetch real news articles from
major AI news sources using RSS feeds.

STRICT ENFORCEMENT: Only articles from the last 2-3 days are included.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import requests
from email.utils import parsedate_to_datetime
import time
from time import mktime
from calendar import timegm

from config.settings import APIFY_TIMEOUT

logger = logging.getLogger(__name__)

# Maximum article age: 3 days
MAX_ARTICLE_AGE_DAYS = 3


class ApifyConnector:
    """Fetches AI news articles from RSS feeds with strict recency enforcement."""

    def __init__(self, api_token: str = None):
        """
        Initialize the ApifyConnector.

        Args:
            api_token: Apify API token (optional, for future Apify integration)
        """
        self.api_token = api_token or ""
        self.timeout = APIFY_TIMEOUT
        self.max_age_days = MAX_ARTICLE_AGE_DAYS
        self.min_timestamp = (datetime.utcnow() - timedelta(days=self.max_age_days)).timestamp()

        # Premium AI news sources - strict recency requirement
        self.news_sources = [
            {
                "name": "TechCrunch AI",
                "url": "https://techcrunch.com/category/artificial-intelligence/",
                "rss_url": "https://feeds.techcrunch.com/TechCrunch/AI",
                "priority": 1,
            },
            {
                "name": "VentureBeat AI",
                "url": "https://venturebeat.com/category/ai/",
                "rss_url": "https://feeds.venturebeat.com/venturebeat/ai",
                "priority": 1,
            },
            {
                "name": "MIT Technology Review",
                "url": "https://www.technologyreview.com/artificial-intelligence/",
                "rss_url": "https://www.technologyreview.com/feed/?tag=artificial-intelligence",
                "priority": 1,
            },
            {
                "name": "The Verge",
                "url": "https://www.theverge.com/ai-artificial-intelligence",
                "rss_url": "https://www.theverge.com/ai-artificial-intelligence/index.xml",
                "priority": 1,
            },
            {
                "name": "Ars Technica",
                "url": "https://arstechnica.com/",
                "rss_url": "https://feeds.arstechnica.com/arstechnica/index",
                "priority": 1,
            },
            {
                "name": "Nature Machine Intelligence",
                "url": "https://www.nature.com/natmachintell/",
                "rss_url": "https://www.nature.com/natmachintell/current_issue/rss/",
                "priority": 2,
            },
            {
                "name": "AI News",
                "url": "https://www.artificial-intelligence.news/",
                "rss_url": "https://www.artificial-intelligence.news/feed/",
                "priority": 1,
            },
            {
                "name": "Synced Review",
                "url": "https://syncedreview.com/",
                "rss_url": "https://syncedreview.com/feed/",
                "priority": 2,
            },
            {
                "name": "Hacker News",
                "url": "https://news.ycombinator.com/",
                "rss_url": "https://news.ycombinator.com/rss",
                "priority": 2,
            },
        ]

    def fetch_ai_news(self, hours: int = 72) -> List[Dict[str, Any]]:
        """
        Fetch recent AI news articles with STRICT 2-3 day maximum age enforcement.

        Args:
            hours: Number of hours to look back (default: 72 = 3 days)

        Returns:
            List of article metadata dictionaries - ONLY articles from last 2-3 days
        """
        articles = []
        # STRICT: Override with max 3 days
        max_age_seconds = 3 * 24 * 60 * 60
        cutoff_timestamp = datetime.utcnow().timestamp() - max_age_seconds

        logger.info(f"STRICT ENFORCEMENT: Only fetching articles newer than {datetime.utcfromtimestamp(cutoff_timestamp)}")

        for source in self.news_sources:
            try:
                logger.info(f"Fetching from {source['name']} (max age: 3 days)")
                fetched = self._fetch_from_rss(source, cutoff_timestamp)
                articles.extend(fetched)
                logger.info(f"  → Got {len(fetched)} recent articles from {source['name']}")
            except Exception as e:
                logger.error(f"Failed to fetch from {source['name']}: {e}")

        logger.info(f"Total articles after strict filtering: {len(articles)}")
        return articles

    def _parse_timestamp(self, date_str: str) -> Optional[float]:
        """
        Parse date string and convert to Unix timestamp.
        RETURNS NONE IF UNPARSEABLE - no fallback to current time!

        Args:
            date_str: Date string in various formats

        Returns:
            Unix timestamp (seconds since epoch) or None if unparseable
        """
        if not date_str:
            return None

        # Try email format first (most reliable)
        try:
            dt = parsedate_to_datetime(date_str)
            return dt.timestamp()
        except (TypeError, ValueError):
            pass

        # Try ISO formats
        formats = [
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
        ]

        for fmt in formats:
            try:
                # Handle timezone info
                dt_str = date_str
                if date_str.endswith('Z'):
                    dt_str = date_str[:-1] + '+00:00'

                dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
                return dt.timestamp()
            except (ValueError, TypeError):
                continue

        # Try common formats
        formats_no_tz = [
            "%a, %d %b %Y %H:%M:%S",
            "%d %b %Y %H:%M:%S",
        ]

        for fmt in formats_no_tz:
            try:
                dt = datetime.strptime(date_str[:25], fmt)
                return dt.timestamp()
            except (ValueError, TypeError):
                continue

        # If we get here, we couldn't parse it - RETURN NONE
        logger.warning(f"UNPARSEABLE DATE - REJECTING: {date_str}")
        return None

    def _fetch_from_rss(
        self, source: Dict[str, str], cutoff_timestamp: float
    ) -> List[Dict[str, Any]]:
        """
        Fetch articles from RSS feed with STRICT timestamp enforcement.
        ONLY articles published in last 3 days are returned.

        Args:
            source: Source metadata with RSS URL
            cutoff_timestamp: Unix timestamp cutoff (only include articles after this)

        Returns:
            List of article metadata dictionaries (ONLY recent articles)
        """
        try:
            import feedparser

            rss_url = source.get("rss_url")
            if not rss_url:
                logger.warning(f"No RSS URL for {source.get('name')}")
                return []

            logger.info(f"Fetching RSS: {rss_url}")
            feed = feedparser.parse(rss_url)

            if not feed.entries:
                logger.warning(f"No entries found in {source.get('name')}")
                return []

            articles = []
            rejected_count = 0

            # Check all entries (not just first 15)
            for entry in feed.entries:
                try:
                    # Try to get publication date - multiple field names
                    pub_date_str = entry.get("published") or entry.get("updated") or ""

                    if not pub_date_str:
                        logger.debug(f"REJECT: No date field for: {entry.get('title', 'unknown')[:60]}")
                        rejected_count += 1
                        continue

                    # Parse to timestamp
                    pub_timestamp = self._parse_timestamp(pub_date_str)

                    if pub_timestamp is None:
                        logger.debug(f"REJECT: Unparseable date: {pub_date_str[:50]}")
                        rejected_count += 1
                        continue

                    # STRICT ENFORCEMENT: Reject if older than 3 days
                    if pub_timestamp < cutoff_timestamp:
                        age_days = (datetime.utcnow().timestamp() - pub_timestamp) / (24 * 3600)
                        logger.debug(
                            f"REJECT: Too old ({age_days:.1f} days): {entry.get('title', 'unknown')[:60]}"
                        )
                        rejected_count += 1
                        continue

                    # Validate required fields
                    title = entry.get("title", "").strip()
                    url = entry.get("link", "").strip()

                    if not title or not url:
                        logger.debug("REJECT: Missing title or URL")
                        rejected_count += 1
                        continue

                    # ACCEPT: Article passed all checks
                    article = {
                        "title": title,
                        "url": url,
                        "publication_date": datetime.utcfromtimestamp(pub_timestamp).isoformat(),
                        "article_text": self._clean_summary(entry.get("summary", "")),
                        "author": entry.get("author", "Unknown").strip(),
                        "source": source.get("name", "Unknown"),
                    }
                    articles.append(article)
                    logger.debug(f"ACCEPT: {title[:60]}")

                except Exception as e:
                    logger.warning(f"Error parsing entry: {e}")
                    rejected_count += 1
                    continue

            logger.info(
                f"{source.get('name')}: {len(articles)} RECENT, "
                f"{rejected_count} rejected (too old/invalid)"
            )
            return articles

        except ImportError:
            logger.error("feedparser not installed. Install with: pip install feedparser")
            return []
        except Exception as e:
            logger.error(f"RSS fetch FAILED for {source['name']}: {e}")
            return []

    def _clean_summary(self, summary: str) -> str:
        """
        Clean HTML from summary text and truncate.

        Args:
            summary: Raw summary with possible HTML

        Returns:
            Cleaned text
        """
        try:
            from html.parser import HTMLParser

            class HTMLStripper(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.reset()
                    self.strict = False
                    self.convert_charrefs = True
                    self.text = []

                def handle_data(self, d):
                    self.text.append(d)

                def get_data(self):
                    return "".join(self.text)

            stripper = HTMLStripper()
            stripper.feed(summary)
            clean_text = stripper.get_data()

            # Limit to first 250 chars
            if len(clean_text) > 250:
                clean_text = clean_text[:247] + "..."

            return clean_text.strip()
        except Exception:
            # Fallback: just return truncated raw text
            return summary[:250].strip()
