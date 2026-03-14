"""
Connector for fetching AI newsletter posts from Substack.

This module provides an interface to extract recent posts from
AI-focused Substack publications.
"""

import logging
from typing import List, Dict, Any
import requests

from config.settings import SUBSTACK_TIMEOUT

logger = logging.getLogger(__name__)


class SubstackConnector:
    """Fetches posts from Substack AI newsletters."""

    def __init__(self):
        """Initialize the SubstackConnector."""
        self.timeout = SUBSTACK_TIMEOUT

        # Popular AI Substack newsletters
        self.newsletters = [
            {
                "name": "Import AI",
                "subdomain": "importai",
                "url": "https://importai.substack.com",
            },
            {
                "name": "Latent Space",
                "subdomain": "latentspace",
                "url": "https://latentspace.substack.com",
            },
            {
                "name": "The Sequence",
                "subdomain": "thesequence",
                "url": "https://thesequence.substack.com",
            },
            {
                "name": "Ben's Bites",
                "subdomain": "bensbites",
                "url": "https://bensbites.substack.com",
            },
        ]

    def fetch_recent_posts(self, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Fetch recent posts from all configured AI Substack newsletters.

        Args:
            hours: Number of hours to look back (default: 24)

        Returns:
            List of post metadata dictionaries containing:
            - title: Post title
            - author: Newsletter author
            - summary: Post summary/excerpt
            - url: Post URL
            - publish_date: Publication datetime
            - newsletter_name: Name of the newsletter
        """
        posts = []

        for newsletter in self.newsletters:
            try:
                posts.extend(self._fetch_newsletter_posts(newsletter))
            except Exception as e:
                logger.error(
                    f"Failed to fetch posts from {newsletter['name']}: {e}"
                )

        return posts

    def _fetch_newsletter_posts(
        self, newsletter: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        """
        Fetch recent posts from a specific Substack newsletter.

        Args:
            newsletter: Newsletter metadata dictionary

        Returns:
            List of post metadata dictionaries
        """
        logger.info(f"Fetching posts from {newsletter['name']}")

        try:
            # This is a placeholder for Substack integration
            # In production, you would use either:
            # 1. Substack RSS feed if available
            # 2. Web scraping with BeautifulSoup
            # 3. Substack API if accessible
            posts = self._mock_fetch_posts(newsletter)
            return posts
        except Exception as e:
            logger.error(f"Failed to fetch from {newsletter['name']}: {e}")
            return []

    def _mock_fetch_posts(self, newsletter: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Mock fetch function for testing (replace with real implementation).

        Args:
            newsletter: Newsletter metadata

        Returns:
            List of mock post metadata
        """
        # This returns mock data for testing
        # Replace with actual web scraping or RSS parsing in production
        return []

    def fetch_from_rss(self, rss_url: str) -> List[Dict[str, Any]]:
        """
        Fetch posts from an RSS feed (if newsletter provides one).

        Args:
            rss_url: URL to the RSS feed

        Returns:
            List of post metadata dictionaries
        """
        try:
            import feedparser

            logger.info(f"Fetching from RSS: {rss_url}")
            feed = feedparser.parse(rss_url)

            posts = []
            for entry in feed.entries[:10]:  # Limit to 10 most recent
                post = {
                    "title": entry.get("title", ""),
                    "url": entry.get("link", ""),
                    "publish_date": entry.get("published", ""),
                    "summary": entry.get("summary", ""),
                    "author": entry.get("author", "Unknown"),
                }
                posts.append(post)

            return posts
        except Exception as e:
            logger.error(f"Failed to parse RSS feed: {e}")
            return []

    def fetch_from_web(self, newsletter_url: str) -> List[Dict[str, Any]]:
        """
        Fetch posts by scraping the newsletter website.

        Args:
            newsletter_url: Base URL of the newsletter

        Returns:
            List of post metadata dictionaries
        """
        try:
            from bs4 import BeautifulSoup

            logger.info(f"Scraping posts from {newsletter_url}")
            response = requests.get(newsletter_url, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            posts = []

            # This is a generic placeholder
            # Actual parsing would depend on the specific newsletter's HTML structure
            for article in soup.find_all("article")[:5]:
                try:
                    post = {
                        "title": article.get_text(strip=True)[:100],
                        "url": article.get("href", ""),
                        "summary": "",
                        "author": "Unknown",
                    }
                    posts.append(post)
                except Exception:
                    continue

            return posts
        except Exception as e:
            logger.error(f"Failed to scrape {newsletter_url}: {e}")
            return []
