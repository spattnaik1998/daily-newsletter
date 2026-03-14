"""
Connector for fetching AI newsletter posts from Substack.

This module provides an interface to extract recent posts from
AI-focused Substack publications using RSS feeds.
"""

import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta
import requests

from config.settings import SUBSTACK_TIMEOUT

logger = logging.getLogger(__name__)


class SubstackConnector:
    """Fetches posts from Substack AI newsletters using RSS feeds."""

    def __init__(self):
        """Initialize the SubstackConnector."""
        self.timeout = SUBSTACK_TIMEOUT

        # Popular AI Substack newsletters with RSS feed URLs
        self.newsletters = [
            {
                "name": "Import AI",
                "subdomain": "importai",
                "url": "https://importai.substack.com",
                "rss_url": "https://importai.substack.com/feed",
            },
            {
                "name": "Latent Space",
                "subdomain": "latentspace",
                "url": "https://latentspace.substack.com",
                "rss_url": "https://latentspace.substack.com/feed",
            },
            {
                "name": "The Sequence",
                "subdomain": "thesequence",
                "url": "https://thesequence.substack.com",
                "rss_url": "https://thesequence.substack.com/feed",
            },
            {
                "name": "Ben's Bites",
                "subdomain": "bensbites",
                "url": "https://bensbites.substack.com",
                "rss_url": "https://bensbites.substack.com/feed",
            },
        ]

    def fetch_recent_posts(self, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Fetch recent posts from all configured AI Substack newsletters.

        Uses RSS feeds for real-time data fetching.

        Args:
            hours: Number of hours to look back (default: 24)

        Returns:
            List of post metadata dictionaries containing:
            - title: Post title
            - author: Newsletter author
            - summary: Post summary/excerpt
            - url: Post URL (real Substack link)
            - publish_date: Publication datetime
            - newsletter_name: Name of the newsletter
            - source: "Substack"
        """
        posts = []
        cutoff_date = datetime.utcnow() - timedelta(hours=hours)

        for newsletter in self.newsletters:
            try:
                logger.info(f"Fetching from {newsletter['name']} RSS feed")
                posts.extend(self._fetch_from_rss(newsletter, cutoff_date))
            except Exception as e:
                logger.error(f"Failed to fetch from {newsletter['name']}: {e}")

        return posts

    def _fetch_from_rss(
        self, newsletter: Dict[str, str], cutoff_date: datetime
    ) -> List[Dict[str, Any]]:
        """
        Fetch posts from Substack RSS feed.

        Args:
            newsletter: Newsletter metadata with RSS URL
            cutoff_date: Only return posts after this date

        Returns:
            List of post metadata dictionaries
        """
        try:
            import feedparser

            rss_url = newsletter.get("rss_url")
            if not rss_url:
                return []

            logger.info(f"Fetching RSS: {rss_url}")
            feed = feedparser.parse(rss_url)

            posts = []

            # Parse feed entries
            for entry in feed.entries[:5]:  # Limit to 5 most recent
                try:
                    # Parse publication date
                    pub_date_str = entry.get("published", "")
                    try:
                        pub_date = datetime.strptime(
                            pub_date_str[:19], "%Y-%m-%dT%H:%M:%S"
                        )
                    except (ValueError, TypeError):
                        pub_date = datetime.utcnow()

                    # Only include recent posts
                    if pub_date < cutoff_date:
                        continue

                    post = {
                        "title": entry.get("title", "No Title"),
                        "url": entry.get("link", newsletter.get("url", "")),
                        "publish_date": pub_date_str,
                        "summary": self._clean_summary(
                            entry.get("summary", "")
                        ),
                        "author": newsletter.get("name", "Unknown"),
                        "newsletter_name": newsletter.get("name", "Unknown"),
                        "source": "Substack",
                    }
                    posts.append(post)
                except Exception as e:
                    logger.warning(f"Failed to parse entry: {e}")
                    continue

            logger.info(f"Fetched {len(posts)} posts from {newsletter['name']}")
            return posts

        except ImportError:
            logger.error("feedparser not installed. Install with: pip install feedparser")
            return []
        except Exception as e:
            logger.error(f"RSS fetch failed for {newsletter['name']}: {e}")
            return []

    def _clean_summary(self, summary: str) -> str:
        """
        Clean HTML from summary text.

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

            # Limit to first 200 chars
            if len(clean_text) > 200:
                clean_text = clean_text[:197] + "..."

            return clean_text.strip()
        except Exception:
            # Fallback: just return truncated raw text
            return summary[:200].strip()

    def fetch_from_web(self, newsletter_url: str) -> List[Dict[str, Any]]:
        """
        Alternative: Fetch posts by web scraping (if RSS unavailable).

        Args:
            newsletter_url: Base URL of the newsletter

        Returns:
            List of post metadata dictionaries
        """
        try:
            from bs4 import BeautifulSoup

            logger.info(f"Scraping posts from {newsletter_url}")
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(
                newsletter_url, timeout=self.timeout, headers=headers
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            posts = []

            # Find post links (Substack uses specific structure)
            post_elements = soup.find_all("a", {"data-testid": "post-preview-title"})

            for element in post_elements[:5]:
                try:
                    title = element.get_text(strip=True)
                    url = element.get("href", "")

                    if url and not url.startswith("http"):
                        url = newsletter_url.rstrip("/") + url

                    post = {
                        "title": title,
                        "url": url,
                        "summary": "",
                        "author": "Unknown",
                        "source": "Substack",
                    }
                    posts.append(post)
                except Exception as e:
                    logger.warning(f"Failed to parse post element: {e}")
                    continue

            return posts
        except Exception as e:
            logger.error(f"Web scraping failed: {e}")
            return []
