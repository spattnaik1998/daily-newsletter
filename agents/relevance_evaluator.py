"""
Relevance Evaluator Agent using Claude API for robust source evaluation.

This agent is responsible for:
- Evaluating source relevance to AI topics using LLM
- Validating source dates (2-3 days old max)
- Scoring relevance for ranking
- Filtering out low-relevance or outdated sources
"""

import logging
import os
import json
import re
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
from anthropic import Anthropic

logger = logging.getLogger(__name__)


class RelevanceEvaluator:
    """Agent for evaluating source relevance using Claude API."""

    def __init__(self):
        """Initialize the RelevanceEvaluator with Claude client."""
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable not set. "
                "Please set your Anthropic API key to use relevance evaluation."
            )

        self.client = Anthropic(api_key=api_key)
        self.model = "claude-opus-4-6"
        self.max_age_days = 3  # Maximum age of sources: 2-3 days

    def evaluate_sources(
        self, sources: List[Dict[str, Any]], source_type: str
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Evaluate and filter sources by relevance and date.

        Args:
            sources: List of source dictionaries with metadata
            source_type: Type of source ('news', 'papers', or 'posts')

        Returns:
            Tuple of (relevant_sources, filtered_out_sources)
        """
        logger.info(f"Evaluating {len(sources)} {source_type} sources for relevance")

        # Step 1: Filter by date first (quick check)
        date_filtered = self._filter_by_date(sources, source_type)
        logger.info(f"✓ Date filter: {len(date_filtered)}/{len(sources)} sources within 2-3 days")

        if not date_filtered:
            logger.warning("No sources within acceptable date range")
            return [], sources

        # Step 2: Evaluate relevance with Claude (batch processing)
        relevant_sources = []
        filtered_out = []

        # Process in batches to avoid overwhelming the API
        batch_size = 10
        for i in range(0, len(date_filtered), batch_size):
            batch = date_filtered[i : i + batch_size]
            relevant_batch = self._evaluate_batch_relevance(batch, source_type)
            relevant_sources.extend(relevant_batch)

        # Collect filtered sources
        relevant_ids = {id(s) for s in relevant_sources}
        filtered_out = [s for s in date_filtered if id(s) not in relevant_ids]

        logger.info(f"✓ Relevance evaluation: {len(relevant_sources)} relevant sources")
        logger.info(f"✓ Filtered out: {len(filtered_out)} low-relevance sources")

        return relevant_sources, filtered_out

    def _filter_by_date(
        self, sources: List[Dict[str, Any]], source_type: str
    ) -> List[Dict[str, Any]]:
        """
        Filter sources to only those within 2-3 days old.

        Args:
            sources: List of sources
            source_type: Type of source ('news', 'papers', or 'posts')

        Returns:
            Filtered list of sources within acceptable date range
        """
        now = datetime.utcnow()
        cutoff = now - timedelta(days=self.max_age_days)
        filtered = []

        date_key = self._get_date_key(source_type)

        for source in sources:
            try:
                date_str = source.get(date_key, "")
                if not date_str:
                    logger.debug(f"Source missing {date_key}: {source.get('title', 'unknown')}")
                    continue

                # Parse ISO format date
                source_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))

                if source_date >= cutoff:
                    filtered.append(source)
                else:
                    age_days = (now - source_date).days
                    logger.debug(
                        f"Source too old ({age_days} days): {source.get('title', 'unknown')}"
                    )
            except Exception as e:
                logger.debug(f"Error parsing date for source: {e}")
                # Include source if date parsing fails (better safe than sorry)
                filtered.append(source)

        return filtered

    def _evaluate_batch_relevance(
        self, sources: List[Dict[str, Any]], source_type: str
    ) -> List[Dict[str, Any]]:
        """
        Evaluate batch of sources for AI relevance using Claude.

        Args:
            sources: Batch of sources to evaluate
            source_type: Type of source

        Returns:
            List of sources deemed relevant
        """
        if not sources:
            return []

        # Prepare batch evaluation prompt
        sources_text = self._format_sources_for_eval(sources, source_type)

        prompt = f"""Evaluate the following {source_type} sources for relevance to AI/ML topics.

Sources:
{sources_text}

For each source, determine if it's relevant to artificial intelligence, machine learning, or related AI topics (e.g., LLMs, neural networks, AI research, AI applications, AI news, etc.).

Return a JSON object with this format:
{{
  "evaluations": [
    {{"index": 0, "relevant": true, "reason": "brief reason"}},
    {{"index": 1, "relevant": false, "reason": "brief reason"}}
  ]
}}

Be inclusive but filter out:
- Off-topic content (sports, politics, weather, etc.)
- Promotional content without technical merit
- Duplicate or low-quality sources
- Non-AI related topics

Only return the JSON object, no additional text."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )

            # Parse Claude's response
            response_text = response.content[0].text

            # Extract JSON from response
            result = None
            try:
                result = json.loads(response_text)
            except json.JSONDecodeError:
                # Try to extract JSON if there's extra text
                # Look for JSON starting with { and ending with }
                json_match = re.search(r"\{[\s\S]*\}", response_text)
                if json_match:
                    try:
                        result = json.loads(json_match.group())
                    except json.JSONDecodeError as e:
                        logger.error(f"JSON parsing error: {e}. Response: {response_text[:200]}")
                        return sources
                else:
                    logger.error(f"No JSON object found in Claude response: {response_text[:200]}")
                    return sources

            if not result:
                logger.error("Empty result from Claude")
                return sources

            # Filter based on evaluations
            relevant = []
            evaluations = result.get("evaluations", [])

            for eval_item in evaluations:
                idx = eval_item.get("index", -1)
                if 0 <= idx < len(sources) and eval_item.get("relevant"):
                    relevant.append(sources[idx])
                    logger.debug(
                        f"Relevant: {sources[idx].get('title', 'unknown')} - {eval_item.get('reason', '')}"
                    )

            return relevant

        except Exception as e:
            logger.error(f"Error evaluating batch relevance: {e}")
            # Return all sources if evaluation fails (don't discard content)
            return sources

    def _format_sources_for_eval(
        self, sources: List[Dict[str, Any]], source_type: str
    ) -> str:
        """
        Format sources into readable text for Claude evaluation.

        Args:
            sources: List of sources
            source_type: Type of source

        Returns:
            Formatted text representation
        """
        formatted = []

        for idx, source in enumerate(sources):
            if source_type == "papers":
                text = (
                    f"{idx}. Title: {source.get('title', 'N/A')}\n"
                    f"   Abstract: {source.get('abstract', 'N/A')[:200]}...\n"
                    f"   Authors: {', '.join(source.get('authors', [])[:3])}"
                )
            elif source_type == "posts":
                text = (
                    f"{idx}. Title: {source.get('title', 'N/A')}\n"
                    f"   Newsletter: {source.get('newsletter_name', 'N/A')}\n"
                    f"   Summary: {source.get('summary', 'N/A')[:200]}..."
                )
            else:  # news
                text = (
                    f"{idx}. Title: {source.get('title', 'N/A')}\n"
                    f"   Source: {source.get('source', 'N/A')}\n"
                    f"   Summary: {source.get('article_text', 'N/A')[:200]}..."
                )

            formatted.append(text)

        return "\n".join(formatted)

    def _get_date_key(self, source_type: str) -> str:
        """
        Get the date field key for each source type.

        Args:
            source_type: Type of source

        Returns:
            Date field key name
        """
        date_keys = {
            "news": "publication_date",
            "papers": "submission_date",
            "posts": "publish_date",
        }
        return date_keys.get(source_type, "publication_date")

    def get_relevance_score(self, source: Dict[str, Any], source_type: str) -> float:
        """
        Get a relevance score for a single source (0-1 scale).

        Args:
            source: Source dictionary
            source_type: Type of source

        Returns:
            Relevance score between 0 and 1
        """
        try:
            date_key = self._get_date_key(source_type)
            date_str = source.get(date_key, "")

            if not date_str:
                return 0.0

            source_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            now = datetime.utcnow()
            age_hours = (now - source_date).total_seconds() / 3600

            # Score based on age: newer is better
            # Max 3 days (72 hours), score decreases linearly
            if age_hours > 72:
                return 0.0

            # Linear scale: 1.0 at 0 hours, 0.0 at 72 hours
            return max(0.0, 1.0 - (age_hours / 72.0))

        except Exception as e:
            logger.debug(f"Error calculating relevance score: {e}")
            return 0.5  # Default neutral score
