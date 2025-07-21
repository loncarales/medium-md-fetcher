"""
Pytest configuration and shared fixtures
"""

import pytest

from src.medium_api_client.cache.memory_cache import MemoryCache
from src.medium_api_client.client import MediumAPIClient
from src.medium_api_client.models import Article


@pytest.fixture
def mock_api_key():
    return "test-api-key-12345"


@pytest.fixture
def client_with_cache(mock_api_key):
    cache = MemoryCache()
    return MediumAPIClient(api_key=mock_api_key, cache=cache)


@pytest.fixture
def sample_response():
    return {
        "id": "123abc",
        "title": "Test Article",
        "subtitle": "This is a test subtitle",
        "author": "Test Author",
        "published_at": "2023-10-01T12:00:00Z",
        "last_modified_at": "2023-10-01T12:00:00Z",
        "markdown": "This is a sample markdown content.",
        "tags": ["test", "article"],
        "topics": ["testing", "development"],
        "url": "https://medium.com/@test-author/test-article-123abc",
        "unique_slug": "test-article-123abc",
        "is_locked": False,
    }


@pytest.fixture
def sample_article_data(sample_response):
    article_data = sample_response
    return Article(**article_data)
