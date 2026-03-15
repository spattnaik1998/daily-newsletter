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
from urllib.parse import urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from agents.news_agent import NewsCrawlerAgent
from agents.arxiv_agent import ArxivAgent
from agents.substack_agent import SubstackAgent
from agents.summarization_agent import SummarizationAgent
from agents.newsletter_agent import NewsletterAgent
from agents.relevance_evaluator import RelevanceEvaluator
from agents.morning_brief_agent import MorningBriefAgent
from config.settings import SUBSTACK_HOURS_LOOKBACK

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def _normalize_url(url: str) -> str:
    """
    Normalize a URL by removing tracking parameters and trailing slashes.

    Args:
        url: URL to normalize

    Returns:
        Normalized URL
    """
    try:
        parsed = urlparse(url)
        # Remove trailing slash from path
        path = parsed.path.rstrip("/")
        # Remove common tracking parameters
        query_params = parse_qs(parsed.query)
        tracking_params = {"utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"}
        filtered_params = {k: v for k, v in query_params.items() if k.lower() not in tracking_params}

        # Reconstruct query string
        query_str = "&".join(f"{k}={v[0]}" for k, v in sorted(filtered_params.items())) if filtered_params else ""
        normalized = f"{parsed.scheme}://{parsed.netloc}{path}"
        if query_str:
            normalized = f"{normalized}?{query_str}"
        return normalized.lower()
    except Exception:
        return url.lower()


def _jaccard_similarity(title1: str, title2: str) -> float:
    """
    Calculate Jaccard similarity between two titles.

    Args:
        title1: First title
        title2: Second title

    Returns:
        Similarity score between 0 and 1
    """
    words1 = set(title1.lower().split())
    words2 = set(title2.lower().split())

    if not words1 or not words2:
        return 0.0

    intersection = len(words1 & words2)
    union = len(words1 | words2)
    return intersection / union if union > 0 else 0.0


def _deduplicate_by_url(
    articles: List[Dict[str, Any]], papers: List[Dict[str, Any]], posts: List[Dict[str, Any]]
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Deduplicate items across sources by URL and title similarity.

    Args:
        articles: News articles
        papers: Research papers
        posts: Newsletter posts

    Returns:
        Tuple of deduplicated (articles, papers, posts)
    """
    # Normalize URLs and track seen items
    seen_urls = set()
    seen_items = []

    deduped_articles = []
    deduped_papers = []
    deduped_posts = []

    # Helper to check and add item
    def add_if_new(item: Dict[str, Any], item_type: str) -> bool:
        """Check if item is new and add if so."""
        url = item.get("url", "") or item.get("arxiv_id", "")
        if not url:
            return True

        normalized = _normalize_url(url) if url.startswith("http") else url

        # Check for exact URL match
        if normalized in seen_urls:
            return False

        # Check for title similarity (70% threshold)
        title = item.get("title", "").lower()
        for seen_item in seen_items:
            if seen_item.get("type") == item_type:
                if _jaccard_similarity(title, seen_item.get("title", "").lower()) > 0.7:
                    return False

        # This is a new item
        seen_urls.add(normalized)
        seen_items.append({"url": normalized, "title": title, "type": item_type})
        return True

    # Process articles
    for article in articles:
        if add_if_new(article, "article"):
            deduped_articles.append(article)

    # Process papers
    for paper in papers:
        if add_if_new(paper, "paper"):
            deduped_papers.append(paper)

    # Process posts
    for post in posts:
        if add_if_new(post, "post"):
            deduped_posts.append(post)

    # Log deduplication results
    original_count = len(articles) + len(papers) + len(posts)
    deduped_count = len(deduped_articles) + len(deduped_papers) + len(deduped_posts)
    if original_count > deduped_count:
        logger.info(f"Deduplicated: {original_count} → {deduped_count} items ({original_count - deduped_count} duplicates removed)")

    return deduped_articles, deduped_papers, deduped_posts


class DailyPipeline:
    """Orchestrates the daily newsletter generation pipeline."""

    def __init__(self, use_relevance_eval: bool = True):
        """
        Initialize the pipeline with all agents.

        Args:
            use_relevance_eval: Whether to use LLM-based relevance evaluation (default: True)
        """
        self.news_agent = NewsCrawlerAgent()
        self.arxiv_agent = ArxivAgent()
        self.substack_agent = SubstackAgent()
        self.summarization_agent = SummarizationAgent()
        self.newsletter_agent = NewsletterAgent()
        self.morning_brief_agent = MorningBriefAgent()
        self.use_relevance_eval = use_relevance_eval

        # Initialize relevance evaluator if enabled
        if self.use_relevance_eval:
            try:
                self.relevance_evaluator = RelevanceEvaluator()
                logger.info("✓ Relevance evaluator initialized with Claude API")
            except ValueError as e:
                logger.warning(f"Relevance evaluator disabled: {e}")
                logger.warning("Falling back to basic filtering only")
                self.use_relevance_eval = False
                self.relevance_evaluator = None
        else:
            self.relevance_evaluator = None

    def run(self, hours: int = 24) -> Tuple[str, Dict[str, Any]]:
        """
        Execute the complete daily pipeline.

        Steps:
        1. Collect news articles
        2. Collect research papers
        3. Collect newsletter posts
        4. Summarize all content
        5. Generate morning brief
        6. Generate final newsletter

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
            "parallel_fetch_time": 0,
        }

        # Steps 1-3: Fetch data sources in parallel
        logger.info("\n[1-3/6] Fetching content from all sources (parallel)...")
        start_fetch = time.time()

        with ThreadPoolExecutor(max_workers=3) as executor:
            # Submit all fetch tasks
            news_future = executor.submit(self._fetch_and_process_news, hours)
            papers_future = executor.submit(self._fetch_and_process_papers, hours)
            posts_future = executor.submit(self._fetch_and_process_posts, hours)

            # Gather results as they complete
            articles = news_future.result()
            papers = papers_future.result()
            posts = posts_future.result()

        fetch_time = time.time() - start_fetch
        metadata["parallel_fetch_time"] = fetch_time
        metadata["articles_count"] = len(articles)
        metadata["papers_count"] = len(papers)
        metadata["posts_count"] = len(posts)

        logger.info(f"✓ Fetched {len(articles)} news articles")
        logger.info(f"✓ Fetched {len(papers)} research papers")
        logger.info(f"✓ Fetched {len(posts)} newsletter posts")
        logger.info(f"  (completed in {fetch_time:.1f}s)")

        # Step 4: Deduplicate content across sources
        logger.info("\n[4/7] Deduplicating content across sources...")
        articles, papers, posts = _deduplicate_by_url(articles, papers, posts)
        metadata["articles_count"] = len(articles)
        metadata["papers_count"] = len(papers)
        metadata["posts_count"] = len(posts)

        # Step 5: Summarize content
        logger.info("\n[5/7] Summarizing content...")
        articles_bullets = self.summarization_agent.create_article_bullets(articles)
        papers_bullets = self.summarization_agent.create_paper_bullets(papers)
        posts_bullets = self.summarization_agent.create_post_bullets(posts)
        themes = self.summarization_agent.identify_themes(articles, papers, posts)
        metadata["themes"] = themes
        logger.info(f"✓ Created {len(articles_bullets)} article bullets")
        logger.info(f"✓ Created {len(papers_bullets)} paper bullets")
        logger.info(f"✓ Created {len(posts_bullets)} post bullets")
        logger.info(f"✓ Identified {len(themes)} themes")

        # Step 6: Generate morning brief
        logger.info("\n[6/7] Generating executive morning brief...")
        try:
            morning_brief = self.morning_brief_agent.generate_brief(
                articles, papers, posts
            )
            metadata["morning_brief"] = morning_brief
            logger.info("✓ Morning brief generated successfully")
        except Exception as e:
            logger.warning(f"Failed to generate morning brief: {e}")
            metadata["morning_brief"] = ""

        # Step 7: Generate newsletter
        logger.info("\n[7/7] Generating newsletter...")
        newsletter = self.newsletter_agent.generate(
            articles_bullets,
            papers_bullets,
            posts_bullets,
            themes,
            morning_brief=metadata.get("morning_brief"),
        )
        logger.info("✓ Newsletter generated successfully")

        logger.info("\n" + "=" * 60)
        logger.info("Pipeline completed successfully")
        logger.info("=" * 60)

        return newsletter, metadata

    def _fetch_and_process_news(self, hours: int) -> List[Dict[str, Any]]:
        """Fetch and process news articles (runs in parallel)."""
        articles = self.news_agent.run(hours=hours)
        articles = self.news_agent.process_articles(articles)
        articles = self.news_agent.filter_by_date(articles, hours=hours)

        # Apply relevance evaluation
        if self.use_relevance_eval and self.relevance_evaluator:
            articles, _ = self.relevance_evaluator.evaluate_sources(articles, "news")

        return articles

    def _fetch_and_process_papers(self, hours: int) -> List[Dict[str, Any]]:
        """Fetch and process papers (runs in parallel)."""
        papers = self.arxiv_agent.run(hours=hours)
        papers = self.arxiv_agent.process_papers(papers)
        papers = self.arxiv_agent.filter_by_relevance(papers)

        # Annotate with PapersWithCode availability
        papers = self.arxiv_agent.annotate_with_code(papers)
        papers = self.arxiv_agent.sort_by_code_availability(papers)

        # Apply relevance evaluation
        if self.use_relevance_eval and self.relevance_evaluator:
            papers, _ = self.relevance_evaluator.evaluate_sources(papers, "papers")

        return papers

    def _fetch_and_process_posts(self, hours: int = None) -> List[Dict[str, Any]]:
        """Fetch and process posts (runs in parallel)."""
        posts = self.substack_agent.run()  # Uses SUBSTACK_HOURS_LOOKBACK (168h)
        posts = self.substack_agent.process_posts(posts)
        posts = self.substack_agent.filter_by_date(posts, hours=SUBSTACK_HOURS_LOOKBACK)

        # Apply relevance evaluation
        if self.use_relevance_eval and self.relevance_evaluator:
            posts, _ = self.relevance_evaluator.evaluate_sources(posts, "posts")

        return posts

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
        if metadata.get("parallel_fetch_time"):
            logger.info(f"  - Parallel fetch time: {metadata['parallel_fetch_time']:.1f}s")
