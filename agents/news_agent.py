"""
News Crawler Agent for fetching and processing AI news articles.

This agent is responsible for:
- Triggering Apify crawls on AI news websites
- Extracting structured article metadata
- Filtering articles from the last 24 hours
- Returning results as JSON objects
"""

import logging
from typing import List, Dict, Any

from connectors.apify_connector import ApifyConnector

logger = logging.getLogger(__name__)


class NewsCrawlerAgent:
    """Agent for crawling and processing AI news articles."""

    def __init__(self):
        """Initialize the NewsCrawlerAgent."""
        self.connector = ApifyConnector()

    def run(self, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Execute the news crawling agent.

        This method:
        1. Triggers Apify crawls on configured news sources
        2. Extracts article metadata
        3. Filters articles from the specified time period

        Args:
            hours: Number of hours to look back (default: 24)

        Returns:
            List of article metadata dictionaries containing:
            - title: Article title
            - source: News source
            - author: Author name
            - url: Article URL
            - publication_date: Publication datetime
            - article_text: Article summary
        """
        logger.info("Starting news crawler agent")

        articles = self.connector.fetch_ai_news(hours=hours)

        logger.info(f"Crawled {len(articles)} articles from AI news sources")

        return articles

    def process_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process and validate article data.

        Args:
            articles: List of raw article data

        Returns:
            List of processed article metadata
        """
        processed = []

        for article in articles:
            try:
                # Validate required fields
                if all(
                    key in article
                    for key in ["title", "url", "publication_date"]
                ):
                    processed.append(article)
            except Exception as e:
                logger.warning(f"Failed to process article: {e}")

        return processed

    def filter_by_date(
        self, articles: List[Dict[str, Any]], hours: int = 24
    ) -> List[Dict[str, Any]]:
        """
        Filter articles to only those within a specified time window.

        Args:
            articles: List of articles to filter
            hours: Number of hours to look back

        Returns:
            Filtered list of articles
        """
        from datetime import datetime, timedelta

        cutoff = datetime.utcnow() - timedelta(hours=hours)
        filtered = []

        for article in articles:
            try:
                pub_date = datetime.fromisoformat(
                    article.get("publication_date", "").replace("Z", "+00:00")
                )
                if pub_date >= cutoff:
                    filtered.append(article)
            except Exception:
                # If date parsing fails, include the article
                filtered.append(article)

        return filtered
