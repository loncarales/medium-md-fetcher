"""
Main API client implementation
Contains: MediumAPIClient class, primary API interaction logic
"""

import hashlib
import logging
from typing import Any, Dict, Optional
from urllib.parse import urlparse

import requests

from src.medium_api_client.cache.base import CacheInterface
from src.medium_api_client.cache.disk_cache import DiskCache
from src.medium_api_client.exceptions import ArticleNotFound, AuthenticationError, InvalidURLError, MediumAPIException
from src.medium_api_client.models import Article


class MediumAPIClient:
    def __init__(self, api_key: str, cache: Optional[CacheInterface] = None, logger=None):
        self.api_key = api_key
        self.base_url = "https://medium2.p.rapidapi.com"
        self.headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "medium2.p.rapidapi.com",
            "User-Agent": "MediumAPIClient/1.0",
        }
        self.cache = cache or DiskCache()
        self.logger = logger or logging.getLogger(__name__)

        # TODO: Initialize rate limiter (150 requests per month for a free tier)

        # Session for connection pooling
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_article_by_url(self, article_url: str) -> Optional[Article]:
        """
        Retrieve article content by Medium URL

        Args:
            article_url (str): Full Medium article URL

        Returns:
            Dict: Article data or None if error
        """
        try:
            # Extract article ID from URL
            article_id = self._extract_article_id(article_url)
            if not article_id:
                raise InvalidURLError(f"Cannot extract article ID from URL: {article_url}")
            # Article endpoints
            article_endpoint = f"{self.base_url}/article/{article_id}"
            article_markdown_endpoint = f"{self.base_url}/article/{article_id}/markdown"
            # Generate cache keys
            cache_key_info = self._generate_cache_key(article_endpoint)
            cache_key_markdown = self._generate_cache_key(article_markdown_endpoint)
            cache_key = cache_key_info + cache_key_markdown
            # Try to get from the cache first
            cached_article = self._get_from_cache(cache_key)
            # self.logger.info(f"Article cached content: {cached_article}")
            if cached_article:
                return Article(**cached_article)

            # Cache miss or force refresh - make API call
            article_data = self._fetch_article_from_api(article_endpoint)
            if article_data:
                article_markdown_data = self._fetch_article_from_api(article_markdown_endpoint)
                if article_markdown_data:
                    # Add markdown content to article info
                    article_data["markdown"] = article_markdown_data.get("markdown", "")
                # Store article info in a cache
                self.cache.set(cache_key, article_data)

                return Article(**article_data)

            return None
        except (InvalidURLError, AuthenticationError, ArticleNotFound):
            # Re-raise known exceptions
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            raise MediumAPIException(f"Failed to retrieve article from URL: {article_url}. Error: {str(e)}") from e

    def _get_from_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        try:
            cached_data = self.cache.get(cache_key)

            if cached_data:
                return cached_data

            return None

        except Exception as e:
            self.logger.error(f"Error retrieving from cache: {str(e)}")
            return None

    def _generate_cache_key(self, url: str) -> str:
        """
        Generate a cache key for URL

        Args:
            url: Article URL

        Returns:
            Cache key string
        """
        # Normalize URL (remove query parameters, fragments, etc.)
        parsed = urlparse(url)
        normalized_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

        # Create a hash of normalized URL
        return hashlib.md5(normalized_url.encode("utf-8")).hexdigest()

    def _extract_article_id(self, url: str) -> str:
        """
        Extract article ID from Medium URL

        Args:
            url (str): Medium article URL

        Returns:
            str: Article ID
        """
        # Medium URLs typically contain the article ID after the last dash
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.split("-")
        return path_parts[-1] if path_parts else None

    def _fetch_article_from_api(self, article_endpoint) -> Optional[Dict[str, Any]]:
        """
        Fetch article data from the API

        Args:
            article_endpoint: Article API endpoint URL

        Returns:
            Article data dictionary or None
        """
        try:
            # self.logger.debug(f"Making API request to: {article_endpoint}")
            response = self.session.get(article_endpoint, timeout=30)

            # Handle different response codes
            if response.status_code == 200:
                data = response.json()
                return data

            elif response.status_code == 401:
                raise AuthenticationError("Invalid API key or authentication failed")

            elif response.status_code == 403:
                raise AuthenticationError("Access forbidden. Check your subscription status.")

            elif response.status_code == 404:
                raise ArticleNotFound(f"Article not found: {article_endpoint}")

            else:
                self.logger.error(f"API request failed with status {response.status_code}: {response.text}")
                raise MediumAPIException(f"API request failed with status {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Network error during API request: {str(e)}")
            raise MediumAPIException(f"Network error: {str(e)}") from e

    def close(self):
        """
        Close the HTTP session
        Close the DiskCache connection.
        """
        if self.session:
            self.session.close()
        """Close the cache if it exists"""
        if self.cache:
            self.cache.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
