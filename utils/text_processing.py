"""
Text processing utilities for the Daily AI Newsletter Generator.

This module provides helper functions for:
- Text cleaning and normalization
- Truncation and ellipsis handling
- URL extraction and validation
- Basic NLP operations
"""

import logging
import re
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def clean_text(text: str) -> str:
    """
    Clean and normalize text.

    Args:
        text: Raw text string

    Returns:
        Cleaned text
    """
    if not text:
        return ""

    # Remove extra whitespace
    text = " ".join(text.split())

    # Remove special characters but keep basic punctuation
    text = re.sub(r"[^\w\s.,!?\-():\"]", "", text)

    return text.strip()


def truncate_text(text: str, max_length: int = 200, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length with ellipsis.

    Args:
        text: Text to truncate
        max_length: Maximum length in characters
        suffix: Suffix to add if truncated (default: "...")

    Returns:
        Truncated text
    """
    if not text:
        return ""

    if len(text) <= max_length:
        return text

    # Truncate and add suffix
    truncated = text[: max_length - len(suffix)]
    return truncated.rstrip() + suffix


def extract_urls(text: str) -> List[str]:
    """
    Extract URLs from text.

    Args:
        text: Text containing URLs

    Returns:
        List of URLs found
    """
    url_pattern = r"https?://[^\s)\"\'<>\[\]]+"
    urls = re.findall(url_pattern, text)
    return urls


def extract_sentences(text: str, max_sentences: int = 3) -> str:
    """
    Extract first N sentences from text.

    Args:
        text: Text to extract from
        max_sentences: Maximum number of sentences to extract

    Returns:
        Extracted sentences
    """
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]
    result = ". ".join(sentences[:max_sentences])

    if len(sentences) > max_sentences:
        result += "."

    return result


def normalize_date(date_string: str) -> str:
    """
    Normalize date string to YYYY-MM-DD format.

    Args:
        date_string: Date string in various formats

    Returns:
        Normalized date string
    """
    from datetime import datetime

    # Try common date formats
    formats = [
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%m/%d/%Y",
    ]

    for fmt in formats:
        try:
            date_obj = datetime.strptime(date_string.replace("Z", ""), fmt)
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            continue

    # If no format matches, return original
    return date_string


def create_markdown_link(text: str, url: str) -> str:
    """
    Create a markdown link.

    Args:
        text: Link text
        url: Link URL

    Returns:
        Markdown link string
    """
    return f"[{text}]({url})"


def capitalize_title(text: str) -> str:
    """
    Capitalize title using title case.

    Args:
        text: Title text

    Returns:
        Title-cased text
    """
    # Words to keep lowercase (articles, prepositions, etc.)
    lowercase_words = {"a", "an", "the", "and", "or", "but", "in", "on", "at", "to"}

    words = text.split()
    capitalized = []

    for i, word in enumerate(words):
        if i == 0 or word.lower() not in lowercase_words:
            capitalized.append(word.capitalize())
        else:
            capitalized.append(word.lower())

    return " ".join(capitalized)


def remove_duplicates(items: List[Dict[str, Any]], key: str = "title") -> List[Dict]:
    """
    Remove duplicate items from a list based on a key field.

    Args:
        items: List of item dictionaries
        key: Field to check for duplicates

    Returns:
        List with duplicates removed
    """
    seen = set()
    unique = []

    for item in items:
        item_key = item.get(key, "")
        if item_key not in seen:
            seen.add(item_key)
            unique.append(item)

    return unique


def merge_content(
    articles: List[Dict],
    papers: List[Dict],
    posts: List[Dict],
) -> List[Dict]:
    """
    Merge content from multiple sources into a single list.

    Args:
        articles: News articles
        papers: Research papers
        posts: Newsletter posts

    Returns:
        Merged list of content
    """
    content = []

    for item in articles:
        item["content_type"] = "article"
        content.append(item)

    for item in papers:
        item["content_type"] = "paper"
        content.append(item)

    for item in posts:
        item["content_type"] = "post"
        content.append(item)

    return content
