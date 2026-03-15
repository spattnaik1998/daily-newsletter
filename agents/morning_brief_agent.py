"""
Morning Brief Agent - AI-powered morning news briefing in PA style.

This agent synthesizes daily AI news into an executive briefing
written like a personal assistant keeping the user ahead of the game.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import anthropic
from config.settings import USER_PROFILE

logger = logging.getLogger(__name__)


class MorningBriefAgent:
    """Generates an executive morning briefing in personal PA style."""

    def __init__(self):
        """Initialize the Morning Brief Agent."""
        self.client = anthropic.Anthropic()
        self.model = "claude-opus-4-6"

    def generate_brief(
        self,
        articles: List[Dict[str, Any]],
        papers: List[Dict[str, Any]],
        posts: List[Dict[str, Any]],
    ) -> str:
        """
        Generate a morning briefing from collected sources.

        Args:
            articles: List of news articles
            papers: List of research papers
            posts: List of newsletter posts

        Returns:
            Formatted morning brief as markdown
        """
        logger.info("Generating morning brief...")

        # Prepare source summaries
        articles_summary = self._prepare_articles_summary(articles)
        papers_summary = self._prepare_papers_summary(papers)
        posts_summary = self._prepare_posts_summary(posts)

        # Generate briefing with Claude
        briefing = self._generate_with_claude(
            articles_summary, papers_summary, posts_summary
        )

        return briefing

    def _prepare_articles_summary(self, articles: List[Dict[str, Any]]) -> str:
        """Prepare articles for briefing generation."""
        if not articles:
            return ""

        summary = "## Breaking AI News\n\n"
        for i, article in enumerate(articles[:10], 1):  # Top 10 articles
            summary += f"{i}. **{article.get('title', 'Untitled')}**\n"
            summary += f"   Source: {article.get('source', 'Unknown')}\n"
            summary += f"   {article.get('article_text', 'No summary available')}\n\n"

        return summary

    def _prepare_papers_summary(self, papers: List[Dict[str, Any]]) -> str:
        """Prepare papers for briefing generation."""
        if not papers:
            return ""

        summary = "## Latest Research\n\n"
        for i, paper in enumerate(papers[:8], 1):  # Top 8 papers
            summary += f"{i}. **{paper.get('title', 'Untitled')}**\n"
            summary += f"   {paper.get('abstract', 'No abstract available')[:200]}...\n\n"

        return summary

    def _prepare_posts_summary(self, posts: List[Dict[str, Any]]) -> str:
        """Prepare newsletter posts for briefing generation."""
        if not posts:
            return ""

        summary = "## Industry Insights\n\n"
        for i, post in enumerate(posts[:8], 1):  # Top 8 posts
            summary += f"{i}. **{post.get('title', 'Untitled')}** by {post.get('author', 'Unknown')}\n"
            summary += f"   {post.get('summary', 'No summary available')[:150]}...\n\n"

        return summary

    def _generate_with_claude(
        self, articles: str, papers: str, posts: str
    ) -> str:
        """
        Generate morning brief using Claude Opus 4.6.

        Args:
            articles: Prepared articles summary
            papers: Prepared papers summary
            posts: Prepared posts summary

        Returns:
            Generated morning brief
        """
        today = datetime.utcnow().strftime("%A, %B %d, %Y")

        # Build user context from profile
        user_name = USER_PROFILE.get("name", "User")
        interests = ", ".join(USER_PROFILE.get("interests", []))
        expertise = USER_PROFILE.get("expertise_level", "intermediate")
        learning_goal = USER_PROFILE.get("learning_goal", "stay informed")

        prompt = f"""You are a sharp, energetic personal assistant tasked with keeping {user_name}
ahead of the game in AI. Your job is to synthesize the day's most critical AI developments
into a compelling morning briefing that's authoritative, engaging, and actionable.

**About {user_name}:**
- Interests: {interests}
- Expertise Level: {expertise}
- Learning Goal: {learning_goal}

Prioritize developments related to their interests. Explain technical concepts at their level.
Write like you're delivering the morning news—confident, clear, and compelling.
{user_name} depends on you to surface what matters. Include:

1. **Opening Hook** - Start with the single most important development today (one paragraph max)
2. **The Three Things You Need to Know** - Three key takeaways that move the needle
3. **Deep Dive** - One in-depth analysis of the most significant trend
4. **Research That Matters** - 2-3 academic/research papers worth watching
5. **Closing Perspective** - Your take on where this leaves the industry today

Be direct. No fluff. Use vivid language. Make clear why each item matters to {user_name}'s goals.

Today's AI Landscape:
{articles}
{papers}
{posts}

Write the briefing in markdown format. Keep the tone personal but professional—like your
best source of AI intelligence is talking directly to {user_name}. This should take 2-3 minutes to read."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
            )

            brief = next(
                (block.text for block in response.content if block.type == "text"),
                "Failed to generate briefing",
            )

            # Format with date header
            formatted_brief = f"""# Good Morning: Your AI Briefing for {today}

{brief}

---
*Generated by your AI intelligence team • {datetime.utcnow().strftime("%I:%M %p UTC")}*
"""

            return formatted_brief

        except Exception as e:
            logger.error(f"Failed to generate brief with Claude: {e}")
            # Fallback to basic summary
            return self._fallback_brief(articles, papers, posts, today)

    def _fallback_brief(
        self, articles: str, papers: str, posts: str, date: str
    ) -> str:
        """
        Fallback brief if Claude API fails.

        Args:
            articles: Articles summary
            papers: Papers summary
            posts: Posts summary
            date: Formatted date string

        Returns:
            Fallback formatted brief
        """
        return f"""# Your AI Briefing for {date}

## Key Developments Today

{articles}
{papers}
{posts}

---
*Your daily AI intelligence briefing*
"""
