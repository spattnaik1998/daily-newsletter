"""
Connector for fetching AI news articles from RSS feeds.

This module provides an interface to fetch real news articles from
major AI news sources using RSS feeds.
"""

import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta
import requests

from config.settings import APIFY_TIMEOUT

logger = logging.getLogger(__name__)


class ApifyConnector:
    """Fetches AI news articles from RSS feeds and web sources."""

    def __init__(self, api_token: str = None):
        """
        Initialize the ApifyConnector.

        Args:
            api_token: Apify API token (optional, for future Apify integration)
        """
        self.api_token = api_token or ""
        self.timeout = APIFY_TIMEOUT

        # Real AI news sources with RSS feeds
        self.news_sources = [
            {
                "name": "TechCrunch AI",
                "url": "https://techcrunch.com/category/artificial-intelligence/",
                "rss_url": "https://feeds.techcrunch.com/TechCrunch/AI",
            },
            {
                "name": "VentureBeat AI",
                "url": "https://venturebeat.com/category/ai/",
                "rss_url": "https://feeds.venturebeat.com/venturebeat/ai",
            },
            {
                "name": "The Verge AI",
                "url": "https://www.theverge.com/ai-artificial-intelligence",
                "rss_url": "https://www.theverge.com/ai-artificial-intelligence/index.xml",
            },
            {
                "name": "MIT Technology Review AI",
                "url": "https://www.technologyreview.com/artificial-intelligence/",
                "rss_url": "https://www.technologyreview.com/feed/?tag=artificial-intelligence",
            },
            {
                "name": "Hacker News",
                "url": "https://news.ycombinator.com/newest",
                "rss_url": "https://news.ycombinator.com/rss",
            },
        ]

    def fetch_ai_news(self, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Fetch recent AI news articles from multiple sources using RSS feeds.

        Args:
            hours: Number of hours to look back (default: 24)

        Returns:
            List of article metadata dictionaries containing:
            - title: Article title
            - source: News source name
            - author: Author name
            - url: Real article URL (clickable link)
            - publication_date: Publication datetime
            - article_text: Article summary
        """
        articles = []
        cutoff_date = datetime.utcnow() - timedelta(hours=hours)

        for source in self.news_sources:
            try:
                logger.info(f"Fetching from {source['name']}")
                articles.extend(self._fetch_from_rss(source, cutoff_date))
            except Exception as e:
                logger.error(f"Failed to fetch from {source['name']}: {e}")

        return articles

    def _fetch_from_rss(
        self, source: Dict[str, str], cutoff_date: datetime
    ) -> List[Dict[str, Any]]:
        """
        Fetch articles from a news source RSS feed.

        Args:
            source: Source metadata with RSS URL
            cutoff_date: Only return articles after this date

        Returns:
            List of article metadata dictionaries
        """
        try:
            import feedparser

            rss_url = source.get("rss_url")
            if not rss_url:
                return []

            logger.info(f"Fetching RSS: {rss_url}")
            feed = feedparser.parse(rss_url)

            articles = []

            # Parse feed entries
            for entry in feed.entries[:8]:  # Get up to 8 articles per source
                try:
                    # Parse publication date
                    pub_date_str = entry.get("published", "")
                    try:
                        pub_date = datetime.strptime(
                            pub_date_str[:19], "%Y-%m-%dT%H:%M:%S"
                        )
                    except (ValueError, TypeError):
                        pub_date = datetime.utcnow()

                    # Only include recent articles
                    if pub_date < cutoff_date:
                        continue

                    article = {
                        "title": entry.get("title", "No Title"),
                        "url": entry.get("link", source.get("url", "")),
                        "publication_date": pub_date_str,
                        "article_text": self._clean_summary(entry.get("summary", "")),
                        "author": entry.get("author", "Unknown"),
                        "source": source.get("name", "Unknown"),
                    }
                    articles.append(article)
                except Exception as e:
                    logger.warning(f"Failed to parse entry: {e}")
                    continue

            logger.info(f"Fetched {len(articles)} articles from {source['name']}")
            return articles

        except ImportError:
            logger.error("feedparser not installed. Install with: pip install feedparser")
            return []
        except Exception as e:
            logger.error(f"RSS fetch failed for {source['name']}: {e}")
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
