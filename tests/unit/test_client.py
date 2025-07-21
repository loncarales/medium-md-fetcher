"""
Unit tests for MediumAPIClient
"""

from unittest.mock import Mock, patch

import pytest

from src.medium_api_client.client import MediumAPIClient
from src.medium_api_client.exceptions import AuthenticationError


class TestMediumAPIClient:
    def test_client_initialization(self, mock_api_key):
        client = MediumAPIClient(api_key=mock_api_key)
        assert client.api_key == mock_api_key

    def test_get_article_success(self, client_with_cache, sample_response, sample_article_data):
        test_url = "https://medium.com/@test-author/test-article-123abc"

        # Create a mock for the _fetch_article_from_api method
        original_fetch = client_with_cache._fetch_article_from_api
        mock_fetch = Mock()

        def side_effect(endpoint):
            if endpoint.endswith("/markdown"):
                return {"markdown": "Test markdown content"}
            return sample_response

        mock_fetch.side_effect = side_effect
        client_with_cache._fetch_article_from_api = mock_fetch

        result = client_with_cache.get_article_by_url(test_url)

        # Verify the result
        assert result.title == sample_article_data.title
        assert result.markdown == "Test markdown content"

        # Verify both API calls were made with correct URLs
        assert mock_fetch.call_count == 2
        calls = mock_fetch.call_args_list
        assert calls[0][0][0] == "https://medium2.p.rapidapi.com/article/123abc"
        assert calls[1][0][0] == "https://medium2.p.rapidapi.com/article/123abc/markdown"

        # Restore the original method
        client_with_cache._fetch_article_from_api = original_fetch

    def test_get_article_unauthorized(self, client_with_cache):
        test_url = "https://medium.com/@test-author/test-article-123abc"

        # Mock the internal method to raise AuthenticationError on the first call
        mock_fetch = Mock(side_effect=AuthenticationError("Access forbidden. Check your subscription status."))
        client_with_cache._fetch_article_from_api = mock_fetch

        with pytest.raises(AuthenticationError) as exc_info:
            client_with_cache.get_article_by_url(test_url)

        assert "Access forbidden" in str(exc_info.value)
        # Verify only the first call was made before exception
        assert mock_fetch.call_count == 1

    @patch("requests.Session.get")
    def test_fetch_article_from_api(self, mock_get, client_with_cache, sample_article_data):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = sample_article_data
        api_url = "https://medium2.p.rapidapi.com/article/123abc"

        result = client_with_cache._fetch_article_from_api(api_url)

        assert result == sample_article_data
        mock_get.assert_called_once_with(api_url, timeout=30)
