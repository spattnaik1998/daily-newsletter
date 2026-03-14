"""
Summarization Agent for condensing news, papers, and newsletter content.

This agent is responsible for:
- Summarizing news articles
- Summarizing research papers
- Summarizing newsletter insights
- Creating concise bullet-point summaries
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class SummarizationAgent:
    """Agent for summarizing content from various sources."""

    def __init__(self):
        """Initialize the SummarizationAgent."""
        self.max_summary_length = 150  # tokens/words

    def summarize_article(self, article: Dict[str, Any]) -> str:
        """
        Summarize a news article.

        Args:
            article: Article metadata dictionary

        Returns:
            Concise summary as string
        """
        try:
            # Use article text if available, otherwise use title
            text = article.get("article_text", "") or article.get("title", "")

            if len(text) > self.max_summary_length:
                # Simple extractive summarization
                sentences = text.split(". ")
                summary = ". ".join(sentences[: max(1, len(sentences) // 3)])
                return summary.strip()
            return text
        except Exception as e:
            logger.warning(f"Failed to summarize article: {e}")
            return article.get("title", "")

    def summarize_paper(self, paper: Dict[str, Any]) -> str:
        """
        Summarize a research paper.

        Args:
            paper: Paper metadata dictionary

        Returns:
            Concise summary (1-2 sentences)
        """
        try:
            abstract = paper.get("abstract", "")

            if not abstract:
                return paper.get("title", "")

            # Extract first 1-2 sentences from abstract
            sentences = abstract.split(". ")
            summary_sentences = sentences[:2]
            summary = ". ".join(summary_sentences)

            # Limit length
            if len(summary) > self.max_summary_length:
                words = summary.split()
                summary = " ".join(words[: self.max_summary_length])

            return summary.strip()
        except Exception as e:
            logger.warning(f"Failed to summarize paper: {e}")
            return paper.get("title", "")

    def summarize_post(self, post: Dict[str, Any]) -> str:
        """
        Summarize a Substack newsletter post.

        Args:
            post: Post metadata dictionary

        Returns:
            Concise summary
        """
        try:
            # Use summary if available, otherwise use title
            text = post.get("summary", "") or post.get("title", "")

            if len(text) > self.max_summary_length:
                # Truncate to max length
                words = text.split()
                text = " ".join(words[: self.max_summary_length])

            return text.strip()
        except Exception as e:
            logger.warning(f"Failed to summarize post: {e}")
            return post.get("title", "")

    def create_article_bullets(self, articles: List[Dict[str, Any]]) -> List[str]:
        """
        Convert articles into bullet points.

        Args:
            articles: List of article metadata

        Returns:
            List of bullet point strings
        """
        bullets = []

        for article in articles[:10]:  # Limit to top 10
            try:
                summary = self.summarize_article(article)
                title = article.get("title", "")
                url = article.get("url", "")

                # Create bullet with title and link
                bullet = f"**{title}** - {summary}"
                if url:
                    bullet = f"{bullet}\n  [Read more]({url})"

                bullets.append(bullet)
            except Exception as e:
                logger.warning(f"Failed to create bullet for article: {e}")

        return bullets

    def create_paper_bullets(self, papers: List[Dict[str, Any]]) -> List[str]:
        """
        Convert papers into bullet points.

        Args:
            papers: List of paper metadata

        Returns:
            List of bullet point strings
        """
        bullets = []

        for paper in papers[:10]:  # Limit to top 10
            try:
                summary = self.summarize_paper(paper)
                title = paper.get("title", "")
                arxiv_id = paper.get("arxiv_id", "")
                authors = paper.get("authors", [])

                # Create bullet with title and authors
                author_str = ", ".join(authors[:2]) if authors else "Unknown"
                bullet = f"**{title}** - {author_str}"

                if summary:
                    bullet = f"{bullet}\n  {summary}"

                if arxiv_id:
                    bullet = f"{bullet}\n  [arXiv:{arxiv_id}](https://arxiv.org/abs/{arxiv_id})"

                bullets.append(bullet)
            except Exception as e:
                logger.warning(f"Failed to create bullet for paper: {e}")

        return bullets

    def create_post_bullets(self, posts: List[Dict[str, Any]]) -> List[str]:
        """
        Convert newsletter posts into bullet points.

        Args:
            posts: List of post metadata

        Returns:
            List of bullet point strings
        """
        bullets = []

        for post in posts[:10]:  # Limit to top 10
            try:
                title = post.get("title", "")
                summary = self.summarize_post(post)
                url = post.get("url", "")
                newsletter = post.get("newsletter_name", "Unknown")

                # Create bullet with title and newsletter
                bullet = f"**{title}** - {newsletter}"

                if summary and summary != title:
                    bullet = f"{bullet}\n  {summary}"

                if url:
                    bullet = f"{bullet}\n  [Read full post]({url})"

                bullets.append(bullet)
            except Exception as e:
                logger.warning(f"Failed to create bullet for post: {e}")

        return bullets

    def identify_themes(
        self, articles: List[Dict], papers: List[Dict], posts: List[Dict]
    ) -> List[str]:
        """
        Identify emerging themes across all content.

        Args:
            articles: List of articles
            papers: List of papers
            posts: List of posts

        Returns:
            List of theme strings
        """
        themes = []

        # Collect all text
        all_text = ""
        for item in articles + papers + posts:
            all_text += f" {item.get('title', '')} {item.get('summary', '')} {item.get('abstract', '')}"

        # Look for common themes
        theme_keywords = {
            "Agentic AI": ["agent", "autonomous", "self-directed"],
            "Multimodal Models": ["multimodal", "vision", "image", "text"],
            "Robotics": ["robot", "robotics", "embodied"],
            "Synthetic Data": ["synthetic data", "synthetic", "generation"],
            "Open Source": ["open source", "open-source"],
            "Safety & Alignment": ["safety", "alignment", "interpretability"],
            "Fine-tuning": ["fine-tuning", "fine-tune", "adaptation"],
            "Reasoning": ["reasoning", "chain of thought", "thinking"],
        }

        all_text_lower = all_text.lower()

        for theme, keywords in theme_keywords.items():
            if any(kw.lower() in all_text_lower for kw in keywords):
                themes.append(theme)

        return themes
