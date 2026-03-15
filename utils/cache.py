"""
Feed Cache - Simple file-based caching layer for RSS/API responses.

Caches HTTP responses from news sources, arXiv, and Substack with 6-hour TTL.
Stores JSON files in output/cache/ directory to avoid redundant API calls.
"""

import logging
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

# Cache TTL in seconds (6 hours)
CACHE_TTL_SECONDS = 6 * 60 * 60


class FeedCache:
    """Simple file-based cache for feed responses with TTL."""

    def __init__(self, cache_dir: str = "output/cache"):
        """
        Initialize the feed cache.

        Args:
            cache_dir: Directory to store cache files (default: output/cache)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = CACHE_TTL_SECONDS

    def _get_cache_path(self, key: str) -> Path:
        """
        Get the cache file path for a given key.

        Args:
            key: Cache key (usually a URL)

        Returns:
            Path to cache file
        """
        # Hash the key to create a filename
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.json"

    def get(self, url: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get cached data for a URL if it exists and is not expired.

        Args:
            url: URL or key to look up

        Returns:
            Cached data list or None if expired/missing
        """
        cache_path = self._get_cache_path(url)

        if not cache_path.exists():
            logger.debug(f"Cache miss for {url}")
            return None

        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cache_data = json.load(f)

            # Check if cache has expired
            cached_time = datetime.fromisoformat(cache_data.get("cached_at", ""))
            if datetime.utcnow() - cached_time > timedelta(seconds=self.ttl):
                logger.debug(f"Cache expired for {url}")
                cache_path.unlink()  # Delete expired cache
                return None

            logger.debug(f"Cache hit for {url}")
            return cache_data.get("data", [])

        except Exception as e:
            logger.warning(f"Error reading cache for {url}: {e}")
            return None

    def set(self, url: str, data: List[Dict[str, Any]]) -> bool:
        """
        Store data in cache for a URL.

        Args:
            url: URL or key to cache
            data: Data to cache (list of items)

        Returns:
            True if successful, False otherwise
        """
        cache_path = self._get_cache_path(url)

        try:
            cache_data = {
                "url": url,
                "cached_at": datetime.utcnow().isoformat(),
                "data": data,
                "count": len(data),
            }

            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=2)

            logger.debug(f"Cached {len(data)} items for {url}")
            return True

        except Exception as e:
            logger.warning(f"Error writing cache for {url}: {e}")
            return False

    def clear_expired(self) -> int:
        """
        Clear all expired cache files.

        Returns:
            Number of files deleted
        """
        if not self.cache_dir.exists():
            return 0

        deleted_count = 0
        cutoff_time = datetime.utcnow() - timedelta(seconds=self.ttl)

        try:
            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    with open(cache_file, "r", encoding="utf-8") as f:
                        cache_data = json.load(f)

                    cached_time = datetime.fromisoformat(cache_data.get("cached_at", ""))
                    if cached_time < cutoff_time:
                        cache_file.unlink()
                        deleted_count += 1
                except Exception:
                    pass

            if deleted_count > 0:
                logger.info(f"Cleared {deleted_count} expired cache files")

        except Exception as e:
            logger.warning(f"Error clearing expired cache: {e}")

        return deleted_count

    def clear_all(self) -> int:
        """
        Clear all cache files.

        Returns:
            Number of files deleted
        """
        if not self.cache_dir.exists():
            return 0

        deleted_count = 0
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    cache_file.unlink()
                    deleted_count += 1
                except Exception:
                    pass

            if deleted_count > 0:
                logger.info(f"Cleared {deleted_count} cache files")

        except Exception as e:
            logger.warning(f"Error clearing all cache: {e}")

        return deleted_count


# Global cache instance
_cache = None


def get_cache() -> FeedCache:
    """Get or create the global cache instance."""
    global _cache
    if _cache is None:
        _cache = FeedCache()
    return _cache
