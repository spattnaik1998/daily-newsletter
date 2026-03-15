"""
arXiv Research Agent for fetching and processing AI research papers.

This agent is responsible for:
- Querying the arXiv API for recent papers
- Fetching papers from AI categories (cs.AI, cs.LG, cs.CL, cs.CV)
- Extracting and normalizing paper metadata
- Filtering papers from the last 24 hours
"""

import logging
from typing import List, Dict, Any
import requests

from connectors.arxiv_connector import ArxivConnector

logger = logging.getLogger(__name__)


class ArxivAgent:
    """Agent for fetching and processing arXiv research papers."""

    def __init__(self):
        """Initialize the ArxivAgent."""
        self.connector = ArxivConnector()

    def run(self, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Execute the arXiv agent.

        This method:
        1. Queries arXiv API for papers in AI categories
        2. Extracts paper metadata
        3. Filters papers from the last 24 hours

        Args:
            hours: Number of hours to look back (default: 24)

        Returns:
            List of paper metadata dictionaries containing:
            - title: Paper title
            - authors: List of author names
            - abstract: Paper abstract
            - pdf_url: URL to PDF
            - arxiv_id: arXiv identifier
            - submission_date: Submission datetime
            - source: "arXiv"
        """
        logger.info("Starting arXiv agent")

        papers = self.connector.fetch_recent_papers(hours=hours)

        logger.info(f"Fetched {len(papers)} papers from arXiv")

        return papers

    def process_papers(self, papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process and validate paper data.

        Ensures all required fields are present and properly formatted.

        Args:
            papers: List of raw paper data

        Returns:
            List of processed paper metadata
        """
        processed = []

        for paper in papers:
            try:
                # Validate required fields
                required_fields = ["title", "abstract", "arxiv_id", "submission_date"]
                if all(field in paper for field in required_fields):
                    # Normalize authors list
                    if isinstance(paper.get("authors"), str):
                        paper["authors"] = [paper["authors"]]

                    processed.append(paper)
            except Exception as e:
                logger.warning(f"Failed to process paper: {e}")

        return processed

    def filter_by_relevance(
        self, papers: List[Dict[str, Any]], keywords: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Filter papers by relevance keywords in title/abstract.

        Args:
            papers: List of papers to filter
            keywords: List of keywords to search for

        Returns:
            Filtered list of papers
        """
        if not keywords:
            # Default keywords for AI newsletter
            keywords = [
                "learning",
                "neural",
                "model",
                "training",
                "algorithm",
                "network",
                "deep",
                "agent",
                "language",
                "vision",
            ]

        filtered = []
        keywords_lower = [k.lower() for k in keywords]

        for paper in papers:
            title_abstract = (
                f"{paper.get('title', '')} {paper.get('abstract', '')}".lower()
            )
            if any(kw in title_abstract for kw in keywords_lower):
                filtered.append(paper)

        return filtered

    def annotate_with_code(self, papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Annotate papers with PapersWithCode availability.

        Checks if each paper has code available on paperswithcode.com.

        Args:
            papers: List of papers to annotate

        Returns:
            Papers with added has_code and github_url fields
        """
        annotated = []
        pwc_api = "https://paperswithcode.com/api/v1/papers/"

        for paper in papers:
            try:
                arxiv_id = paper.get("arxiv_id", "")
                if not arxiv_id:
                    paper["has_code"] = False
                    annotated.append(paper)
                    continue

                # Query PapersWithCode API
                try:
                    response = requests.get(
                        f"{pwc_api}?arxiv_id={arxiv_id}",
                        timeout=5
                    )
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("results") and len(data["results"]) > 0:
                            paper["has_code"] = True
                            # Extract GitHub URL if available
                            for result in data["results"]:
                                if result.get("github_url"):
                                    paper["github_url"] = result["github_url"]
                                    break
                        else:
                            paper["has_code"] = False
                    else:
                        paper["has_code"] = False
                except requests.RequestException:
                    # If API call fails, mark as unknown
                    paper["has_code"] = False

                annotated.append(paper)
            except Exception as e:
                logger.debug(f"Failed to annotate paper {paper.get('arxiv_id', 'unknown')}: {e}")
                paper["has_code"] = False
                annotated.append(paper)

        return annotated

    def sort_by_code_availability(self, papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sort papers to put those with code at the top.

        Args:
            papers: List of papers (must be pre-annotated with has_code)

        Returns:
            Sorted list with code-available papers first
        """
        papers_with_code = [p for p in papers if p.get("has_code", False)]
        papers_without_code = [p for p in papers if not p.get("has_code", False)]
        return papers_with_code + papers_without_code

    def get_summary_stats(self, papers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate summary statistics for the papers.

        Args:
            papers: List of papers

        Returns:
            Dictionary with statistics
        """
        papers_with_code = sum(1 for p in papers if p.get("has_code", False))
        return {
            "total_papers": len(papers),
            "papers_with_code": papers_with_code,
            "unique_authors": len(set(a for p in papers for a in p.get("authors", []))),
            "categories_covered": len(
                set(p.get("source", "") for p in papers if p.get("source"))
            ),
        }
