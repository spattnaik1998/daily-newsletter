"""
Daily Pipeline for the AI Newsletter Generator.

This module orchestrates all agents in the correct order:
1. Run NewsCrawlerAgent
2. Run ArxivAgent
3. Run SubstackAgent
4. Run SummarizationAgent
5. Run NewsletterAgent
"""

import logging
from typing import Tuple, List, Dict, Any

from agents.news_agent import NewsCrawlerAgent
from agents.arxiv_agent import ArxivAgent
from agents.substack_agent import SubstackAgent
from agents.summarization_agent import SummarizationAgent
from agents.newsletter_agent import NewsletterAgent

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class DailyPipeline:
    """Orchestrates the daily newsletter generation pipeline."""

    def __init__(self):
        """Initialize the pipeline with all agents."""
        self.news_agent = NewsCrawlerAgent()
        self.arxiv_agent = ArxivAgent()
        self.substack_agent = SubstackAgent()
        self.summarization_agent = SummarizationAgent()
        self.newsletter_agent = NewsletterAgent()

    def run(self, hours: int = 24) -> Tuple[str, Dict[str, Any]]:
        """
        Execute the complete daily pipeline.

        Steps:
        1. Collect news articles
        2. Collect research papers
        3. Collect newsletter posts
        4. Summarize all content
        5. Generate final newsletter

        Args:
            hours: Number of hours to look back (default: 24)

        Returns:
            Tuple of (newsletter_markdown, metadata)
        """
        logger.info("=" * 60)
        logger.info("Starting Daily AI Newsletter Pipeline")
        logger.info("=" * 60)

        metadata = {
            "articles_count": 0,
            "papers_count": 0,
            "posts_count": 0,
            "themes": [],
        }

        # Step 1: Fetch news articles
        logger.info("\n[1/5] Fetching news articles...")
        articles = self.news_agent.run(hours=hours)
        articles = self.news_agent.process_articles(articles)
        articles = self.news_agent.filter_by_date(articles, hours=hours)
        metadata["articles_count"] = len(articles)
        logger.info(f"✓ Fetched {len(articles)} news articles")

        # Step 2: Fetch research papers
        logger.info("\n[2/5] Fetching research papers...")
        papers = self.arxiv_agent.run(hours=hours)
        papers = self.arxiv_agent.process_papers(papers)
        papers = self.arxiv_agent.filter_by_relevance(papers)
        metadata["papers_count"] = len(papers)
        logger.info(f"✓ Fetched {len(papers)} research papers")

        # Step 3: Fetch newsletter posts
        logger.info("\n[3/5] Fetching newsletter posts...")
        posts = self.substack_agent.run(hours=hours)
        posts = self.substack_agent.process_posts(posts)
        posts = self.substack_agent.filter_by_date(posts, hours=hours)
        metadata["posts_count"] = len(posts)
        logger.info(f"✓ Fetched {len(posts)} newsletter posts")

        # Step 4: Summarize content
        logger.info("\n[4/5] Summarizing content...")
        articles_bullets = self.summarization_agent.create_article_bullets(articles)
        papers_bullets = self.summarization_agent.create_paper_bullets(papers)
        posts_bullets = self.summarization_agent.create_post_bullets(posts)
        themes = self.summarization_agent.identify_themes(articles, papers, posts)
        metadata["themes"] = themes
        logger.info(f"✓ Created {len(articles_bullets)} article bullets")
        logger.info(f"✓ Created {len(papers_bullets)} paper bullets")
        logger.info(f"✓ Created {len(posts_bullets)} post bullets")
        logger.info(f"✓ Identified {len(themes)} themes")

        # Step 5: Generate newsletter
        logger.info("\n[5/5] Generating newsletter...")
        newsletter = self.newsletter_agent.generate(
            articles_bullets, papers_bullets, posts_bullets, themes
        )
        logger.info("✓ Newsletter generated successfully")

        logger.info("\n" + "=" * 60)
        logger.info("Pipeline completed successfully")
        logger.info("=" * 60)

        return newsletter, metadata

    def log_summary(self, metadata: Dict[str, Any]) -> None:
        """
        Log a summary of the pipeline results.

        Args:
            metadata: Pipeline metadata dictionary
        """
        logger.info("\nPipeline Summary:")
        logger.info(f"  - Articles: {metadata.get('articles_count', 0)}")
        logger.info(f"  - Papers: {metadata.get('papers_count', 0)}")
        logger.info(f"  - Posts: {metadata.get('posts_count', 0)}")
        logger.info(f"  - Themes: {len(metadata.get('themes', []))}")
