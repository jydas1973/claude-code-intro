"""
Tests for the Brave Search Research Agent.
"""

import pytest
from unittest.mock import AsyncMock, Mock, patch
from pydantic_ai.models.test import TestModel
from pydantic_ai.models.function import FunctionModel

from ..agent import research_agent, run_research
from ..dependencies import BraveSearchDependencies


class TestBraveSearchAgent:
    """Test suite for the Brave Search Research Agent."""
    
    def test_agent_creation(self):
        """Test that the agent is created successfully."""
        assert research_agent is not None
        assert research_agent.deps_type == BraveSearchDependencies
        assert len(research_agent.tools) == 1
        assert "search_web" in [tool.name for tool in research_agent.tools]
    
    def test_system_prompt_content(self):
        """Test that the system prompt contains key research elements."""
        system_prompt = research_agent.system_prompt
        assert "research assistant" in system_prompt.lower()
        assert "brave search" in system_prompt.lower()
        assert "web search" in system_prompt.lower()
        assert "source" in system_prompt.lower()
    
    @pytest.mark.asyncio
    async def test_agent_with_test_model(self):
        """Test agent execution with TestModel for rapid validation."""
        # Create mock dependencies
        mock_session = AsyncMock()
        mock_deps = BraveSearchDependencies(
            brave_api_key="test_key",
            session=mock_session,
            session_id="test_session"
        )
        
        # Use TestModel for validation without real API calls
        test_model = TestModel()
        
        with research_agent.override(model=test_model):
            result = await research_agent.run(
                "Research quantum computing breakthroughs",
                deps=mock_deps
            )
            
            # TestModel should return a string response
            assert isinstance(result.data, str)
            assert len(result.data) > 0
    
    @pytest.mark.asyncio
    async def test_agent_with_function_model(self):
        """Test agent behavior with FunctionModel for custom responses."""
        
        def custom_function_calls(messages, info):
            """Custom function to simulate agent behavior."""
            # Simulate a search tool call
            return [
                {
                    'tool_name': 'search_web',
                    'args': {'query': 'test query', 'max_results': 10},
                    'result': 'Mock search results for test query'
                }
            ]
        
        # Create mock dependencies
        mock_session = AsyncMock()
        mock_deps = BraveSearchDependencies(
            brave_api_key="test_key",
            session=mock_session,
            session_id="test_session"
        )
        
        # Use FunctionModel with custom behavior
        function_model = FunctionModel(custom_function_calls)
        
        with research_agent.override(model=function_model):
            result = await research_agent.run(
                "Test research query",
                deps=mock_deps
            )
            
            assert isinstance(result.data, str)
    
    @pytest.mark.asyncio
    async def test_search_web_tool_registration(self):
        """Test that the search_web tool is properly registered."""
        # Create mock dependencies
        mock_session = AsyncMock()
        mock_deps = BraveSearchDependencies(
            brave_api_key="test_key",
            session=mock_session,
            session_id="test_session"
        )
        
        # Mock the tool function to return a controlled response
        with patch('brave_search_agent.tools.brave_search_tool') as mock_search:
            mock_search.return_value = "Mock search results"
            
            # Get the search tool directly
            search_tool = next(tool for tool in research_agent.tools if tool.name == "search_web")
            
            # Create a mock context
            mock_ctx = Mock()
            mock_ctx.deps = mock_deps
            
            # Call the tool function directly
            result = await search_tool.function(mock_ctx, "test query", 5)
            
            assert result == "Mock search results"
            mock_search.assert_called_once_with(
                api_key="test_key",
                session=mock_session,
                query="test query",
                max_results=5
            )
    
    @pytest.mark.asyncio
    async def test_search_tool_parameter_validation(self):
        """Test search tool parameter validation."""
        # Create mock dependencies
        mock_session = AsyncMock()
        mock_deps = BraveSearchDependencies(
            brave_api_key="test_key",
            session=mock_session,
            session_id="test_session"
        )
        
        with patch('brave_search_agent.tools.brave_search_tool') as mock_search:
            mock_search.return_value = "Mock search results"
            
            # Get the search tool directly
            search_tool = next(tool for tool in research_agent.tools if tool.name == "search_web")
            
            # Create a mock context
            mock_ctx = Mock()
            mock_ctx.deps = mock_deps
            
            # Test max_results bounds - should clamp to valid range
            await search_tool.function(mock_ctx, "test query", 25)  # Above max
            mock_search.assert_called_with(
                api_key="test_key",
                session=mock_session,
                query="test query",
                max_results=20  # Should be clamped to 20
            )
            
            mock_search.reset_mock()
            
            await search_tool.function(mock_ctx, "test query", 0)  # Below min
            mock_search.assert_called_with(
                api_key="test_key",
                session=mock_session,
                query="test query", 
                max_results=1  # Should be clamped to 1
            )


class TestConvenienceFunctions:
    """Test suite for convenience functions."""
    
    @pytest.mark.asyncio
    async def test_run_research_function(self):
        """Test the run_research convenience function."""
        with patch('brave_search_agent.agent.BraveSearchDependencies.create') as mock_create:
            with patch('brave_search_agent.agent.research_agent.run') as mock_run:
                # Mock dependencies creation
                mock_deps = Mock()
                mock_deps.close = AsyncMock()
                mock_create.return_value = mock_deps
                
                # Mock agent run result
                mock_result = Mock()
                mock_result.data = "Test research result"
                mock_run.return_value = mock_result
                
                # Test the convenience function
                result = await run_research("test query", session_id="test_session")
                
                assert result == "Test research result"
                mock_create.assert_called_once_with(session_id="test_session")
                mock_run.assert_called_once_with("test query", deps=mock_deps)
                mock_deps.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_run_research_cleanup_on_error(self):
        """Test that dependencies are cleaned up even if research fails."""
        with patch('brave_search_agent.agent.BraveSearchDependencies.create') as mock_create:
            with patch('brave_search_agent.agent.research_agent.run') as mock_run:
                # Mock dependencies creation
                mock_deps = Mock()
                mock_deps.close = AsyncMock()
                mock_create.return_value = mock_deps
                
                # Mock agent run to raise an exception
                mock_run.side_effect = Exception("Test error")
                
                # Test that cleanup still happens
                with pytest.raises(Exception, match="Test error"):
                    await run_research("test query")
                
                mock_deps.close.assert_called_once()