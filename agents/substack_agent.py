"""
Substack Newsletter Agent for fetching and processing AI newsletter posts.

This agent is responsible for:
- Fetching recent posts from AI-focused Substack newsletters
- Extracting post metadata (title, author, summary, URL, date)
- Normalizing metadata across different newsletters
- Filtering posts from the last 24 hours
"""

import logging
from typing import List, Dict, Any

from connectors.substack_connector import SubstackConnector
from config.settings import SUBSTACK_HOURS_LOOKBACK

logger = logging.getLogger(__name__)


class SubstackAgent:
    """Agent for fetching and processing Substack newsletter posts."""

    def __init__(self):
        """Initialize the SubstackAgent."""
        self.connector = SubstackConnector()

    def run(self, hours: int = None) -> List[Dict[str, Any]]:
        """
        Execute the Substack agent.

        This method:
        1. Fetches recent posts from configured AI Substack newsletters
        2. Extracts post metadata
        3. Filters posts from the last 7 days (or specified time period)

        Args:
            hours: Number of hours to look back (default: 168 = 7 days for weekly newsletters)

        Returns:
            List of post metadata dictionaries containing:
            - title: Post title
            - author: Newsletter author
            - summary: Post summary/excerpt
            - url: Post URL
            - publish_date: Publication datetime
            - newsletter_name: Name of the newsletter
            - source: "Substack"
        """
        # Use Substack-specific default (7 days) if hours not specified
        if hours is None:
            hours = SUBSTACK_HOURS_LOOKBACK

        logger.info("Starting Substack agent")

        posts = self.connector.fetch_recent_posts(hours=hours)

        logger.info(f"Fetched {len(posts)} posts from Substack newsletters")

        return posts

    def process_posts(self, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process and validate post data.

        Ensures all required fields are present and properly formatted.

        Args:
            posts: List of raw post data

        Returns:
            List of processed post metadata
        """
        processed = []

        for post in posts:
            try:
                # Validate required fields
                required_fields = ["title", "url", "publish_date"]
                if all(field in post for field in required_fields):
                    # Ensure summary exists (can be empty)
                    if "summary" not in post:
                        post["summary"] = ""

                    # Ensure source is set
                    if "source" not in post:
                        post["source"] = "Substack"

                    processed.append(post)
            except Exception as e:
                logger.warning(f"Failed to process post: {e}")

        return processed

    def extract_key_insights(self, posts: List[Dict[str, Any]]) -> List[str]:
        """
        Extract key insights/themes from post titles and summaries.

        Args:
            posts: List of posts

        Returns:
            List of extracted insights/themes
        """
        insights = []
        all_text = " ".join(
            [
                f"{post.get('title', '')} {post.get('summary', '')}"
                for post in posts
            ]
        )

        # Simple keyword extraction (can be enhanced with NLP)
        keywords = [
            "GPT",
            "Claude",
            "multimodal",
            "open source",
            "benchmark",
            "reasoning",
            "agents",
            "fine-tuning",
            "safety",
            "alignment",
        ]

        for keyword in keywords:
            if keyword.lower() in all_text.lower():
                insights.append(keyword)

        return list(set(insights))

    def filter_by_date(
        self, posts: List[Dict[str, Any]], hours: int = 24
    ) -> List[Dict[str, Any]]:
        """
        Filter posts to only those within a specified time window.

        Args:
            posts: List of posts to filter
            hours: Number of hours to look back

        Returns:
            Filtered list of posts
        """
        from datetime import datetime, timedelta

        cutoff = datetime.utcnow() - timedelta(hours=hours)
        filtered = []

        for post in posts:
            try:
                pub_date = datetime.fromisoformat(
                    post.get("publish_date", "").replace("Z", "+00:00")
                )
                if pub_date >= cutoff:
                    filtered.append(post)
            except Exception:
                # If date parsing fails, include the post
                filtered.append(post)

        return filtered
