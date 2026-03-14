"""
Connector for fetching AI news articles using Apify crawlers.

This module provides an interface to the Apify API to crawl and extract
article data from major AI news websites.
"""

import logging
from typing import List, Dict, Any
import requests

from config.settings import APIFY_API_BASE_URL, APIFY_TIMEOUT

logger = logging.getLogger(__name__)


class ApifyConnector:
    """Fetches AI news articles using Apify actors."""

    def __init__(self, api_token: str = None):
        """
        Initialize the ApifyConnector.

        Args:
            api_token: Apify API token (can also be set via environment)
        """
        self.base_url = APIFY_API_BASE_URL
        self.api_token = api_token or ""
        self.timeout = APIFY_TIMEOUT

        # Suggested news sources to crawl
        self.news_sources = [
            "https://techcrunch.com/category/artificial-intelligence/",
            "https://venturebeat.com/category/ai/",
            "https://www.theverge.com/ai-artificial-intelligence",
        ]

    def fetch_ai_news(self, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Fetch recent AI news articles from multiple sources.

        Args:
            hours: Number of hours to look back (default: 24)

        Returns:
            List of article metadata dictionaries containing:
            - title: Article title
            - source: News source URL
            - author: Author name
            - url: Article URL
            - publication_date: Publication datetime
            - article_text: Article content summary
        """
        articles = []

        for source in self.news_sources:
            try:
                articles.extend(self._crawl_source(source))
            except Exception as e:
                logger.error(f"Failed to crawl source {source}: {e}")

        return articles

    def _crawl_source(self, source_url: str) -> List[Dict[str, Any]]:
        """
        Crawl a single news source.

        Args:
            source_url: URL of the source to crawl

        Returns:
            List of article metadata dictionaries
        """
        logger.info(f"Crawling news source: {source_url}")

        try:
            # This is a placeholder for Apify integration
            # In production, you would call the actual Apify API with proper authentication
            articles = self._mock_crawl_source(source_url)
            return articles
        except Exception as e:
            logger.error(f"Crawl failed for {source_url}: {e}")
            return []

    def _mock_crawl_source(self, source_url: str) -> List[Dict[str, Any]]:
        """
        Mock crawl function for testing (replace with real Apify API call).

        Args:
            source_url: URL of the source

        Returns:
            List of mock article metadata
        """
        # This returns mock data for testing
        # Replace with actual Apify API calls in production
        return []

    def trigger_actor(self, actor_id: str, input_data: Dict[str, Any]) -> str:
        """
        Trigger an Apify actor to start a crawl.

        Args:
            actor_id: Apify actor ID
            input_data: Input data for the actor

        Returns:
            Run ID of the started actor
        """
        if not self.api_token:
            logger.warning("Apify API token not set. Cannot trigger actor.")
            return None

        url = f"{self.base_url}/acts/{actor_id}/runs"
        headers = {"Authorization": f"Bearer {self.api_token}"}

        try:
            response = requests.post(
                url, json=input_data, headers=headers, timeout=self.timeout
            )
            response.raise_for_status()
            run_id = response.json().get("data", {}).get("id")
            logger.info(f"Actor run triggered: {run_id}")
            return run_id
        except requests.RequestException as e:
            logger.error(f"Failed to trigger actor: {e}")
            return None

    def get_run_status(self, actor_id: str, run_id: str) -> Dict[str, Any]:
        """
        Get the status of an Apify actor run.

        Args:
            actor_id: Apify actor ID
            run_id: Run ID to check

        Returns:
            Status dictionary or None if request fails
        """
        if not self.api_token:
            logger.warning("Apify API token not set.")
            return None

        url = f"{self.base_url}/acts/{actor_id}/runs/{run_id}"
        headers = {"Authorization": f"Bearer {self.api_token}"}

        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json().get("data")
        except requests.RequestException as e:
            logger.error(f"Failed to get run status: {e}")
            return None

    def get_run_results(self, actor_id: str, run_id: str) -> List[Dict[str, Any]]:
        """
        Get results from a completed Apify actor run.

        Args:
            actor_id: Apify actor ID
            run_id: Run ID

        Returns:
            List of result items
        """
        if not self.api_token:
            logger.warning("Apify API token not set.")
            return []

        url = f"{self.base_url}/acts/{actor_id}/runs/{run_id}/dataset/items"
        headers = {"Authorization": f"Bearer {self.api_token}"}

        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to get run results: {e}")
            return []
