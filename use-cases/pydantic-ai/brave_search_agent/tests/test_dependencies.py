"""
Tests for dependency management.
"""

import pytest
import os
import httpx
from unittest.mock import patch, Mock, AsyncMock

from ..dependencies import BraveSearchDependencies


class TestBraveSearchDependencies:
    """Test suite for BraveSearchDependencies class."""
    
    def test_dependencies_creation(self):
        """Test basic dependencies creation."""
        mock_session = Mock()
        
        deps = BraveSearchDependencies(
            brave_api_key="test_api_key",
            session=mock_session,
            session_id="test_session"
        )
        
        assert deps.brave_api_key == "test_api_key"
        assert deps.session == mock_session
        assert deps.session_id == "test_session"
    
    def test_dependencies_optional_session_id(self):
        """Test dependencies creation with optional session_id."""
        mock_session = Mock()
        
        deps = BraveSearchDependencies(
            brave_api_key="test_api_key",
            session=mock_session
        )
        
        assert deps.brave_api_key == "test_api_key"
        assert deps.session == mock_session
        assert deps.session_id is None
    
    @pytest.mark.asyncio
    async def test_create_dependencies_method(self):
        """Test the create class method."""
        with patch.dict(os.environ, {
            "BRAVE_API_KEY": "test_api_key",
            "LLM_API_KEY": "test_llm_key"
        }):
            deps = await BraveSearchDependencies.create(session_id="test_session")
            
            assert deps.brave_api_key == "test_api_key"
            assert isinstance(deps.session, httpx.AsyncClient)
            assert deps.session_id == "test_session"
            
            # Clean up
            await deps.close()
    
    @pytest.mark.asyncio
    async def test_create_dependencies_without_session_id(self):
        """Test create method without session_id."""
        with patch.dict(os.environ, {
            "BRAVE_API_KEY": "test_api_key",
            "LLM_API_KEY": "test_llm_key"
        }):
            deps = await BraveSearchDependencies.create()
            
            assert deps.brave_api_key == "test_api_key"
            assert isinstance(deps.session, httpx.AsyncClient)
            assert deps.session_id is None
            
            # Clean up
            await deps.close()
    
    @pytest.mark.asyncio
    async def test_http_client_configuration(self):
        """Test that HTTP client is properly configured."""
        with patch.dict(os.environ, {
            "BRAVE_API_KEY": "test_api_key",
            "LLM_API_KEY": "test_llm_key"
        }):
            deps = await BraveSearchDependencies.create()
            
            # Check HTTP client configuration
            client = deps.session
            assert isinstance(client, httpx.AsyncClient)
            assert client.timeout.read == 30.0
            
            # Check headers
            expected_headers = {
                "Accept": "application/json",
                "User-Agent": "Brave-Search-Research-Agent/1.0"
            }
            for key, value in expected_headers.items():
                assert client.headers[key] == value
            
            # Check limits
            assert client._limits.max_keepalive_connections == 5
            assert client._limits.max_connections == 10
            
            # Clean up
            await deps.close()
    
    @pytest.mark.asyncio
    async def test_close_method(self):
        """Test the close method."""
        mock_session = AsyncMock()
        
        deps = BraveSearchDependencies(
            brave_api_key="test_api_key",
            session=mock_session,
            session_id="test_session"
        )
        
        await deps.close()
        
        # Verify that session.aclose() was called
        mock_session.aclose.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_with_settings_loading_error(self):
        """Test create method when settings loading fails."""
        with patch('brave_search_agent.dependencies.load_settings') as mock_load_settings:
            mock_load_settings.side_effect = ValueError("Settings loading failed")
            
            with pytest.raises(ValueError, match="Settings loading failed"):
                await BraveSearchDependencies.create()


class TestDependencyIntegration:
    """Test suite for dependency integration patterns."""
    
    @pytest.mark.asyncio
    async def test_context_manager_pattern(self):
        """Test using dependencies with context manager pattern."""
        with patch.dict(os.environ, {
            "BRAVE_API_KEY": "test_api_key", 
            "LLM_API_KEY": "test_llm_key"
        }):
            # Test context manager-like usage
            deps = await BraveSearchDependencies.create()
            
            try:
                # Use dependencies
                assert deps.brave_api_key == "test_api_key"
                assert deps.session is not None
                
            finally:
                # Always clean up
                await deps.close()
    
    @pytest.mark.asyncio
    async def test_multiple_dependencies_isolation(self):
        """Test that multiple dependency instances are isolated."""
        with patch.dict(os.environ, {
            "BRAVE_API_KEY": "test_api_key",
            "LLM_API_KEY": "test_llm_key"
        }):
            deps1 = await BraveSearchDependencies.create(session_id="session_1")
            deps2 = await BraveSearchDependencies.create(session_id="session_2")
            
            try:
                # Should have same API key but different sessions
                assert deps1.brave_api_key == deps2.brave_api_key
                assert deps1.session_id == "session_1"
                assert deps2.session_id == "session_2"
                assert deps1.session is not deps2.session
                
            finally:
                await deps1.close()
                await deps2.close()
    
    @pytest.mark.asyncio
    async def test_dependency_reuse(self):
        """Test dependency reuse patterns."""
        with patch.dict(os.environ, {
            "BRAVE_API_KEY": "test_api_key",
            "LLM_API_KEY": "test_llm_key"
        }):
            deps = await BraveSearchDependencies.create()
            
            try:
                # Dependencies should be reusable across multiple operations
                assert deps.brave_api_key == "test_api_key"
                
                # Session should be reusable
                session = deps.session
                assert session is not None
                
                # Multiple operations should work with same dependencies
                for i in range(3):
                    # Simulate multiple uses
                    assert deps.brave_api_key == "test_api_key"
                    assert deps.session is session  # Same session instance
                    
            finally:
                await deps.close()


class TestErrorHandling:
    """Test suite for dependency error handling."""
    
    @pytest.mark.asyncio
    async def test_close_with_already_closed_session(self):
        """Test close method when session is already closed."""
        mock_session = AsyncMock()
        mock_session.aclose.side_effect = Exception("Already closed")
        
        deps = BraveSearchDependencies(
            brave_api_key="test_api_key",
            session=mock_session
        )
        
        # Should not raise an exception
        try:
            await deps.close()
        except Exception:
            pytest.fail("close() should handle already closed sessions gracefully")
    
    @pytest.mark.asyncio
    async def test_create_with_invalid_settings(self):
        """Test create method with invalid settings."""
        with patch('brave_search_agent.dependencies.load_settings') as mock_load_settings:
            mock_settings = Mock()
            mock_settings.brave_api_key = ""  # Invalid empty key
            mock_load_settings.return_value = mock_settings
            
            # Should still create dependencies (validation happens at settings level)
            deps = await BraveSearchDependencies.create()
            
            assert deps.brave_api_key == ""
            assert isinstance(deps.session, httpx.AsyncClient)
            
            await deps.close()