"""
Connector for fetching AI research papers from arXiv.

This module provides an interface to the arXiv API to retrieve
recently submitted papers in AI-related categories.
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
import requests

from config.settings import ARXIV_API_BASE_URL, ARXIV_CATEGORIES, ARXIV_MAX_RESULTS, ARXIV_TIMEOUT

logger = logging.getLogger(__name__)


class ArxivConnector:
    """Fetches recent papers from arXiv API."""

    def __init__(self):
        """Initialize the ArxivConnector."""
        self.base_url = ARXIV_API_BASE_URL
        self.timeout = ARXIV_TIMEOUT
        self.categories = ARXIV_CATEGORIES
        self.max_results = ARXIV_MAX_RESULTS

    def fetch_recent_papers(self, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Fetch recent papers from arXiv in AI categories.

        Args:
            hours: Number of hours to look back (default: 24)

        Returns:
            List of paper metadata dictionaries containing:
            - title: Paper title
            - authors: List of author names
            - abstract: Paper abstract
            - pdf_url: URL to PDF
            - submission_date: Submission datetime
            - arxiv_id: arXiv ID
        """
        papers = []
        cutoff_date = datetime.utcnow() - timedelta(hours=hours)

        for category in self.categories:
            try:
                papers.extend(self._fetch_category(category, cutoff_date))
            except Exception as e:
                logger.error(f"Failed to fetch papers from category {category}: {e}")

        return papers

    def _fetch_category(self, category: str, cutoff_date: datetime) -> List[Dict[str, Any]]:
        """
        Fetch papers from a specific arXiv category.

        Args:
            category: arXiv category code (e.g., 'cs.AI')
            cutoff_date: Only return papers submitted after this date

        Returns:
            List of paper metadata dictionaries
        """
        logger.info(f"Fetching papers from category: {category}")

        # Build query: recent papers in category
        query = f"cat:{category} AND submittedDate:[{cutoff_date.strftime('%Y%m%d0000')} TO 9999999999]"
        params = {
            "search_query": query,
            "start": 0,
            "max_results": self.max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return self._parse_arxiv_response(response.text)
        except requests.RequestException as e:
            logger.error(f"Request failed for category {category}: {e}")
            return []

    def _parse_arxiv_response(self, xml_content: str) -> List[Dict[str, Any]]:
        """
        Parse XML response from arXiv API.

        Args:
            xml_content: XML response content

        Returns:
            List of parsed paper metadata
        """
        papers = []
        try:
            import xml.etree.ElementTree as ET

            root = ET.fromstring(xml_content)
            namespace = {"atom": "http://www.w3.org/2005/Atom"}

            for entry in root.findall("atom:entry", namespace):
                paper = self._extract_paper_metadata(entry, namespace)
                if paper:
                    papers.append(paper)
        except Exception as e:
            logger.error(f"Failed to parse arXiv response: {e}")

        return papers

    def _extract_paper_metadata(self, entry, namespace: Dict) -> Dict[str, Any]:
        """
        Extract paper metadata from an arXiv entry element.

        Args:
            entry: XML entry element
            namespace: XML namespace dictionary

        Returns:
            Paper metadata dictionary or None if parsing fails
        """
        try:
            title = entry.find("atom:title", namespace).text.strip()
            authors = [
                author.find("atom:name", namespace).text
                for author in entry.findall("atom:author", namespace)
            ]
            abstract = entry.find("atom:summary", namespace).text.strip()
            arxiv_id = entry.find("atom:id", namespace).text.split("/abs/")[-1]
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            published = entry.find("atom:published", namespace).text

            return {
                "title": title,
                "authors": authors,
                "abstract": abstract,
                "pdf_url": pdf_url,
                "arxiv_id": arxiv_id,
                "submission_date": published,
                "source": "arXiv",
            }
        except Exception as e:
            logger.error(f"Failed to extract paper metadata: {e}")
            return None
