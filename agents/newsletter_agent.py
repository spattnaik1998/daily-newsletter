"""
Newsletter Agent for generating the final markdown newsletter.

This agent is responsible for:
- Combining all processed content into a tiered format
- Organizing content by impact and importance
- Generating clean markdown output
- Formatting the newsletter for readability
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from config.settings import DATE_FORMAT

logger = logging.getLogger(__name__)


class NewsletterAgent:
    """Agent for generating the final AI newsletter with tiered format."""

    def __init__(self):
        """Initialize the NewsletterAgent."""
        self.date = datetime.now().strftime(DATE_FORMAT)

    def generate(
        self,
        articles_bullets: List[str],
        papers_bullets: List[str],
        posts_bullets: List[str],
        themes: List[str],
        morning_brief: Optional[str] = None,
    ) -> str:
        """
        Generate the complete newsletter in tiered markdown format.

        Prioritizes high-impact content:
        1. Lead Story (most important development)
        2. Must Read Today (top 3 items)
        3. AI News Briefing (full news section)
        4. Research Spotlight (featured paper)
        5. Community Insights (newsletter perspectives)
        6. Emerging Themes (detected patterns)
        7. Full Papers Digest (complete research list)

        Args:
            articles_bullets: Bullet points for news articles
            papers_bullets: Bullet points for research papers
            posts_bullets: Bullet points for newsletter posts
            themes: List of emerging themes
            morning_brief: Optional executive morning brief

        Returns:
            Complete newsletter as markdown string
        """
        logger.info("Generating newsletter")

        newsletter = self._create_header()

        # Include morning brief if provided
        if morning_brief:
            newsletter += self._create_morning_brief_section(morning_brief)

        # Lead Story - single most important item
        if articles_bullets:
            lead_story = self._extract_lead_story(articles_bullets)
            if lead_story:
                newsletter += self._create_lead_story_section(lead_story)

        # Must Read Today - top 3 items across sources
        top_items = self._get_top_items(articles_bullets, papers_bullets, posts_bullets, count=3)
        if top_items:
            newsletter += self._create_must_read_section(top_items)

        # AI News Briefing
        if articles_bullets:
            newsletter += self._create_section("AI News Briefing", articles_bullets)

        # Research Spotlight
        if papers_bullets:
            spotlight_paper = self._extract_spotlight_paper(papers_bullets)
            if spotlight_paper:
                newsletter += self._create_research_spotlight_section(spotlight_paper)

            # Full papers list
            newsletter += self._create_section("Full Research Papers", papers_bullets)

        # Community Insights
        if posts_bullets:
            newsletter += self._create_section("What the Community Is Talking About", posts_bullets)

        # Emerging Themes
        if themes:
            newsletter += self._create_themes_section(themes)

        newsletter += self._create_footer()

        return newsletter

    def _create_header(self) -> str:
        """
        Create the newsletter header.

        Returns:
            Header markdown string
        """
        header = f"""# Daily AI Newsletter

**Date:** {self.date}

---

"""
        return header

    def _create_morning_brief_section(self, brief: str) -> str:
        """Create the morning brief section."""
        return f"{brief}\n\n---\n\n"

    def _extract_lead_story(self, articles_bullets: List[str]) -> Optional[str]:
        """
        Extract the first (most important) article as lead story.

        Args:
            articles_bullets: List of article bullets

        Returns:
            Lead story or None
        """
        return articles_bullets[0] if articles_bullets else None

    def _extract_spotlight_paper(self, papers_bullets: List[str]) -> Optional[str]:
        """
        Extract the first paper (prioritizes papers with code) as spotlight.

        Args:
            papers_bullets: List of paper bullets

        Returns:
            Spotlight paper or None
        """
        return papers_bullets[0] if papers_bullets else None

    def _get_top_items(
        self, articles: List[str], papers: List[str], posts: List[str], count: int = 3
    ) -> List[str]:
        """
        Get top items from all sources for "Must Read" section.

        Prioritizes articles, then papers, then posts.

        Args:
            articles: News articles
            papers: Research papers
            posts: Newsletter posts
            count: Number of items to return

        Returns:
            Top items from each category
        """
        top_items = []

        # Add up to count items total, prioritizing articles
        for item in articles[:count]:
            if len(top_items) < count:
                top_items.append(item)

        for item in papers[:count - len(top_items)]:
            if len(top_items) < count:
                top_items.append(item)

        for item in posts[:count - len(top_items)]:
            if len(top_items) < count:
                top_items.append(item)

        return top_items

    def _create_lead_story_section(self, lead_story: str) -> str:
        """
        Create the lead story section.

        Args:
            lead_story: The lead story bullet

        Returns:
            Section markdown
        """
        section = """## 📰 Lead Story

The single most important AI development today:

"""
        # Remove bullet marker if present
        clean_story = lead_story.lstrip("* ").lstrip("- ")
        section += f"{clean_story}\n\n---\n\n"
        return section

    def _create_must_read_section(self, items: List[str]) -> str:
        """
        Create the "Must Read Today" section.

        Args:
            items: Top items from all sources

        Returns:
            Section markdown
        """
        section = """## ⭐ Must Read Today

Top 3 most important developments:

"""
        for i, item in enumerate(items, 1):
            # Remove bullet marker if present
            clean_item = item.lstrip("* ").lstrip("- ")
            section += f"{i}. {clean_item}\n\n"

        section += "---\n\n"
        return section

    def _create_research_spotlight_section(self, spotlight_paper: str) -> str:
        """
        Create the research spotlight section featuring one paper.

        Args:
            spotlight_paper: The featured paper bullet

        Returns:
            Section markdown
        """
        section = """## 🔬 Research Spotlight

Featured research paper worth deep-diving into:

"""
        # Remove bullet marker if present
        clean_paper = spotlight_paper.lstrip("* ").lstrip("- ")
        section += f"{clean_paper}\n\n---\n\n"
        return section

    def _create_section(self, title: str, bullets: List[str]) -> str:
        """
        Create a newsletter section with bullet points.

        Args:
            title: Section title
            bullets: List of bullet point strings

        Returns:
            Section markdown string
        """
        # Add emoji based on section title
        emoji_map = {
            "AI News Briefing": "📢",
            "Full Research Papers": "📚",
            "What the Community Is Talking About": "💬",
        }
        emoji = emoji_map.get(title, "")
        section_title = f"{emoji} {title}".strip()

        section = f"## {section_title}\n\n"

        for bullet in bullets:
            section += f"* {bullet}\n\n"

        section += "---\n\n"

        return section

    def _create_themes_section(self, themes: List[str]) -> str:
        """
        Create the emerging themes section.

        Args:
            themes: List of themes

        Returns:
            Themes section markdown string
        """
        section = "## Emerging Themes\n\n"

        section += "Key themes appearing across today's content:\n\n"

        for theme in themes:
            section += f"* **{theme}**\n"

        section += "\n---\n\n"

        return section

    def _create_footer(self) -> str:
        """
        Create the newsletter footer.

        Returns:
            Footer markdown string
        """
        footer = """## How to Subscribe

This newsletter is generated daily at 7:00 AM UTC.

Subscribe to the individual sources for more information:
* [Import AI](https://importai.substack.com)
* [Latent Space](https://latentspace.substack.com)
* [The Sequence](https://thesequence.substack.com)
* [Ben's Bites](https://bensbites.substack.com)

---

*Generated by Daily AI Newsletter Generator*
"""
        return footer

    def save_newsletter(self, content: str, output_path: str) -> bool:
        """
        Save the newsletter to a markdown file.

        Args:
            content: Newsletter markdown content
            output_path: Path to save the file

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info(f"Newsletter saved to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save newsletter: {e}")
            return False
