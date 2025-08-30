"""
Tests for Brave Search tools functionality.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, Mock, patch
import httpx

from ..tools import brave_search_tool, search_rate_limiter


class TestBraveSearchTool:
    """Test suite for the brave_search_tool function."""
    
    @pytest.mark.asyncio
    async def test_successful_search(self):
        """Test successful search with mock HTTP response."""
        # Mock HTTP session
        mock_session = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "web": {
                "results": [
                    {
                        "title": "Test Result 1",
                        "url": "https://example.com/1",
                        "description": "First test result"
                    },
                    {
                        "title": "Test Result 2", 
                        "url": "https://example.com/2",
                        "description": "Second test result"
                    }
                ]
            }
        }
        mock_session.get.return_value = mock_response
        
        # Test the search tool
        result = await brave_search_tool(
            api_key="test_api_key",
            session=mock_session,
            query="test query",
            max_results=5
        )
        
        # Verify the result format
        assert isinstance(result, str)
        assert "Search Results for 'test query'" in result
        assert "Test Result 1" in result
        assert "https://example.com/1" in result
        assert "First test result" in result
        assert "Test Result 2" in result
        
        # Verify API call was made correctly
        mock_session.get.assert_called_once()
        call_args = mock_session.get.call_args
        assert "https://api.search.brave.com/res/v1/web/search" in call_args[0]
        assert call_args[1]["headers"]["X-Subscription-Token"] == "test_api_key"
        assert call_args[1]["params"]["q"] == "test query"
        assert call_args[1]["params"]["count"] == 5
    
    @pytest.mark.asyncio
    async def test_empty_api_key(self):
        """Test handling of empty API key."""
        mock_session = AsyncMock()
        
        result = await brave_search_tool("", mock_session, "test query")
        assert "Error: Brave API key is required" == result
        
        result = await brave_search_tool("   ", mock_session, "test query")
        assert "Error: Brave API key is required" == result
    
    @pytest.mark.asyncio
    async def test_empty_query(self):
        """Test handling of empty query."""
        mock_session = AsyncMock()
        
        result = await brave_search_tool("test_key", mock_session, "")
        assert "Error: Search query cannot be empty" == result
        
        result = await brave_search_tool("test_key", mock_session, "   ")
        assert "Error: Search query cannot be empty" == result
    
    @pytest.mark.asyncio
    async def test_max_results_bounds(self):
        """Test that max_results is properly bounded."""
        mock_session = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"web": {"results": []}}
        mock_session.get.return_value = mock_response
        
        # Test upper bound
        await brave_search_tool("test_key", mock_session, "test", max_results=25)
        call_args = mock_session.get.call_args
        assert call_args[1]["params"]["count"] == 20  # Should be clamped to 20
        
        mock_session.reset_mock()
        
        # Test lower bound
        await brave_search_tool("test_key", mock_session, "test", max_results=0)
        call_args = mock_session.get.call_args
        assert call_args[1]["params"]["count"] == 1  # Should be clamped to 1
    
    @pytest.mark.asyncio
    async def test_rate_limit_error(self):
        """Test handling of 429 rate limit error."""
        mock_session = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.text = "Rate limit exceeded"
        mock_session.get.return_value = mock_response
        
        result = await brave_search_tool("test_key", mock_session, "test query")
        
        assert "Error: Rate limit exceeded" in result
        assert "Please try again in a moment" in result
    
    @pytest.mark.asyncio 
    async def test_auth_error(self):
        """Test handling of 401 authentication error."""
        mock_session = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_session.get.return_value = mock_response
        
        result = await brave_search_tool("invalid_key", mock_session, "test query")
        
        assert "Error: Invalid Brave API key" in result
        assert "Please check your configuration" in result
    
    @pytest.mark.asyncio
    async def test_other_http_errors(self):
        """Test handling of other HTTP errors."""
        mock_session = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal server error"
        mock_session.get.return_value = mock_response
        
        result = await brave_search_tool("test_key", mock_session, "test query")
        
        assert "Error: Brave API returned 500" in result
        assert "Internal server error" in result
    
    @pytest.mark.asyncio
    async def test_no_results(self):
        """Test handling when no results are returned."""
        mock_session = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"web": {"results": []}}
        mock_session.get.return_value = mock_response
        
        result = await brave_search_tool("test_key", mock_session, "obscure query")
        
        assert "No search results found for query: obscure query" == result
    
    @pytest.mark.asyncio
    async def test_timeout_error(self):
        """Test handling of request timeout."""
        mock_session = AsyncMock()
        mock_session.get.side_effect = asyncio.TimeoutError()
        
        result = await brave_search_tool("test_key", mock_session, "test query")
        
        assert "Error: Search request timed out" == result
    
    @pytest.mark.asyncio
    async def test_general_exception(self):
        """Test handling of general exceptions."""
        mock_session = AsyncMock()
        mock_session.get.side_effect = Exception("Connection error")
        
        result = await brave_search_tool("test_key", mock_session, "test query")
        
        assert "Error: Search failed: Connection error" == result


class TestRateLimiting:
    """Test suite for rate limiting functionality."""
    
    @pytest.mark.asyncio
    async def test_rate_limiting_exists(self):
        """Test that rate limiter is properly configured."""
        assert search_rate_limiter is not None
        assert search_rate_limiter.max_rate == 1  # 1 request
        assert search_rate_limiter.time_period == 1  # per 1 second
    
    @pytest.mark.asyncio
    async def test_rate_limiting_behavior(self):
        """Test that rate limiting actually delays requests."""
        mock_session = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"web": {"results": []}}
        mock_session.get.return_value = mock_response
        
        # Record timing for multiple requests
        start_time = asyncio.get_event_loop().time()
        
        # Make 3 requests - should be rate limited
        tasks = [
            brave_search_tool("test_key", mock_session, f"query {i}")
            for i in range(3)
        ]
        
        await asyncio.gather(*tasks)
        
        end_time = asyncio.get_event_loop().time()
        elapsed_time = end_time - start_time
        
        # Should take at least 2 seconds (3 requests with 1/second limit)
        assert elapsed_time >= 2.0


class TestSearchResponseParsing:
    """Test suite for search response parsing and formatting."""
    
    @pytest.mark.asyncio
    async def test_result_formatting(self):
        """Test that results are properly formatted."""
        mock_session = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "web": {
                "results": [
                    {
                        "title": "AI Research Paper",
                        "url": "https://arxiv.org/paper/123",
                        "description": "Latest advances in artificial intelligence research"
                    }
                ]
            }
        }
        mock_session.get.return_value = mock_response
        
        result = await brave_search_tool("test_key", mock_session, "AI research")
        
        # Check formatting elements
        assert "Search Results for 'AI research':" in result
        assert "1. **AI Research Paper**" in result
        assert "URL: https://arxiv.org/paper/123" in result
        assert "Latest advances in artificial intelligence research" in result
    
    @pytest.mark.asyncio
    async def test_missing_fields(self):
        """Test handling of missing result fields."""
        mock_session = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "web": {
                "results": [
                    {
                        # Missing title, url, description
                    },
                    {
                        "title": "Valid Result",
                        # Missing url, description
                    }
                ]
            }
        }
        mock_session.get.return_value = mock_response
        
        result = await brave_search_tool("test_key", mock_session, "test")
        
        # Should handle missing fields gracefully
        assert "No title" in result
        assert "No URL" in result
        assert "No description" in result
        assert "Valid Result" in result