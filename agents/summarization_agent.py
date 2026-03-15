"""
Summarization Agent for condensing news, papers, and newsletter content.

This agent uses Claude Haiku for intelligent summarization with fallback to
simple text extraction. Produces structured summaries with:
- One-line summary
- Key insight
- "Why this matters" statement
"""

import logging
from typing import List, Dict, Any, Optional
import anthropic

logger = logging.getLogger(__name__)


class SummarizationAgent:
    """Agent for summarizing content using Claude Haiku API with fallback."""

    def __init__(self):
        """Initialize the SummarizationAgent with Anthropic client."""
        try:
            self.client = anthropic.Anthropic()
            self.model = "claude-haiku-4-5-20251001"
            self.use_ai = True
        except Exception as e:
            logger.warning(f"Failed to initialize Claude Haiku: {e}. Falling back to text extraction.")
            self.client = None
            self.use_ai = False
        self.max_summary_length = 150

    def summarize_article(self, article: Dict[str, Any]) -> str:
        """
        Summarize a news article using Claude Haiku or fallback to text extraction.

        Args:
            article: Article metadata dictionary

        Returns:
            Structured summary with insight and "why it matters"
        """
        if self.use_ai:
            try:
                text = article.get("article_text", "") or article.get("title", "")
                if not text:
                    return article.get("title", "")

                prompt = f"""Summarize this news article in exactly 3 lines:
1. One-line summary (concise, under 15 words)
2. Key insight (1-2 sentences)
3. Why this matters (1 sentence explaining impact)

Article:
{text[:500]}

Respond ONLY with these 3 lines, numbered 1-3."""

                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=200,
                    messages=[{"role": "user", "content": prompt}],
                )

                summary_text = next(
                    (block.text for block in response.content if block.type == "text"),
                    None,
                )
                if summary_text:
                    return summary_text.strip()
            except Exception as e:
                logger.debug(f"Failed to summarize article with Claude: {e}")

        # Fallback to simple extraction
        return self._fallback_summarize_article(article)

    def _fallback_summarize_article(self, article: Dict[str, Any]) -> str:
        """Fallback article summarization using text extraction."""
        text = article.get("article_text", "") or article.get("title", "")
        if len(text) > self.max_summary_length:
            sentences = text.split(". ")
            summary = ". ".join(sentences[: max(1, len(sentences) // 3)])
            return summary.strip()
        return text

    def summarize_paper(self, paper: Dict[str, Any]) -> str:
        """
        Summarize a research paper using Claude Haiku or text extraction.

        Args:
            paper: Paper metadata dictionary

        Returns:
            Structured summary with insight and "why it matters"
        """
        if self.use_ai:
            try:
                abstract = paper.get("abstract", "")
                title = paper.get("title", "")
                if not abstract and not title:
                    return ""

                prompt = f"""Summarize this research paper in exactly 3 lines:
1. One-line summary (concise, under 15 words)
2. Key insight (1-2 sentences)
3. Why this matters (1 sentence explaining significance)

Title: {title}
Abstract:
{abstract[:500]}

Respond ONLY with these 3 lines, numbered 1-3."""

                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=200,
                    messages=[{"role": "user", "content": prompt}],
                )

                summary_text = next(
                    (block.text for block in response.content if block.type == "text"),
                    None,
                )
                if summary_text:
                    return summary_text.strip()
            except Exception as e:
                logger.debug(f"Failed to summarize paper with Claude: {e}")

        # Fallback to simple extraction
        return self._fallback_summarize_paper(paper)

    def _fallback_summarize_paper(self, paper: Dict[str, Any]) -> str:
        """Fallback paper summarization using abstract extraction."""
        abstract = paper.get("abstract", "")
        if not abstract:
            return paper.get("title", "")

        sentences = abstract.split(". ")
        summary_sentences = sentences[:2]
        summary = ". ".join(summary_sentences)

        if len(summary) > self.max_summary_length:
            words = summary.split()
            summary = " ".join(words[: self.max_summary_length])

        return summary.strip()

    def summarize_post(self, post: Dict[str, Any]) -> str:
        """
        Summarize a Substack post using Claude Haiku or text extraction.

        Args:
            post: Post metadata dictionary

        Returns:
            Structured summary with insight and "why it matters"
        """
        if self.use_ai:
            try:
                text = post.get("summary", "") or post.get("title", "")
                if not text:
                    return ""

                prompt = f"""Summarize this newsletter post in exactly 3 lines:
1. One-line summary (concise, under 15 words)
2. Key insight (1-2 sentences)
3. Why this matters (1 sentence explaining relevance)

Post:
{text[:500]}

Respond ONLY with these 3 lines, numbered 1-3."""

                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=200,
                    messages=[{"role": "user", "content": prompt}],
                )

                summary_text = next(
                    (block.text for block in response.content if block.type == "text"),
                    None,
                )
                if summary_text:
                    return summary_text.strip()
            except Exception as e:
                logger.debug(f"Failed to summarize post with Claude: {e}")

        # Fallback to simple extraction
        return self._fallback_summarize_post(post)

    def _fallback_summarize_post(self, post: Dict[str, Any]) -> str:
        """Fallback post summarization using text truncation."""
        text = post.get("summary", "") or post.get("title", "")
        if len(text) > self.max_summary_length:
            words = text.split()
            text = " ".join(words[: self.max_summary_length])
        return text.strip()

    def create_article_bullets(self, articles: List[Dict[str, Any]]) -> List[str]:
        """
        Convert articles into bullet points with AI-enhanced summaries.

        Args:
            articles: List of article metadata

        Returns:
            List of bullet point strings
        """
        bullets = []
        articles_to_process = articles[:10]  # Limit to top 10

        for article in articles_to_process:
            try:
                summary = self.summarize_article(article)
                title = article.get("title", "")
                url = article.get("url", "")

                # Create bullet with title, summary, and link
                bullet = f"**{title}**\n  {summary}"
                if url:
                    bullet = f"{bullet}\n  [Read more]({url})"

                bullets.append(bullet)
            except Exception as e:
                logger.warning(f"Failed to create bullet for article: {e}")

        return bullets

    def create_paper_bullets(self, papers: List[Dict[str, Any]]) -> List[str]:
        """
        Convert papers into bullet points with AI-enhanced summaries.
        Adds [Code Available] badge for papers with code.

        Args:
            papers: List of paper metadata

        Returns:
            List of bullet point strings
        """
        bullets = []
        papers_to_process = papers[:10]  # Limit to top 10

        for paper in papers_to_process:
            try:
                summary = self.summarize_paper(paper)
                title = paper.get("title", "")
                arxiv_id = paper.get("arxiv_id", "")
                authors = paper.get("authors", [])
                has_code = paper.get("has_code", False)
                github_url = paper.get("github_url")

                # Create bullet with title and authors
                author_str = ", ".join(authors[:2]) if authors else "Unknown"
                code_badge = " **[Code Available]**" if has_code else ""
                bullet = f"**{title}**{code_badge} - {author_str}"

                if summary:
                    bullet = f"{bullet}\n  {summary}"

                # Add links
                links = []
                if arxiv_id:
                    links.append(f"[arXiv:{arxiv_id}](https://arxiv.org/abs/{arxiv_id})")
                if github_url:
                    links.append(f"[GitHub]({github_url})")

                if links:
                    bullet = f"{bullet}\n  {' • '.join(links)}"

                bullets.append(bullet)
            except Exception as e:
                logger.warning(f"Failed to create bullet for paper: {e}")

        return bullets

    def create_post_bullets(self, posts: List[Dict[str, Any]]) -> List[str]:
        """
        Convert newsletter posts into bullet points with AI-enhanced summaries.

        Args:
            posts: List of post metadata

        Returns:
            List of bullet point strings
        """
        bullets = []
        posts_to_process = posts[:10]  # Limit to top 10

        for post in posts_to_process:
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
