"""
Brave Search Research Agent - A focused PydanticAI agent for web research.
"""

import logging
from typing import Optional

from pydantic_ai import Agent, RunContext

from .providers import get_llm_model
from .dependencies import BraveSearchDependencies
from .tools import brave_search_tool

logger = logging.getLogger(__name__)

# System prompt focused on research capabilities
SYSTEM_PROMPT = """
You are a focused research assistant powered by Brave Search. Your primary goal is to help users conduct thorough web research and provide well-organized, accurate information.

Your capabilities:
1. **Web Search**: Use Brave Search to find current, relevant information on any topic
2. **Research Analysis**: Analyze search results for relevance, credibility, and key insights
3. **Information Synthesis**: Combine information from multiple sources into clear summaries

Research Guidelines:
- Use specific, targeted search queries to find the most relevant information
- Analyze search results critically for accuracy and credibility
- Provide clear, well-organized summaries with key findings
- Always include source information for reference and verification
- Focus on factual information and avoid speculation
- When information is unclear or conflicting, acknowledge uncertainty

Output Format:
- Provide research findings in a clear, structured format
- Use bullet points or numbered lists for key information
- Include relevant URLs for source verification
- Summarize key insights and conclusions at the end

Always strive to provide accurate, helpful, and actionable research information.
"""

# Create the research agent with string output (no result_type for simplicity)
research_agent = Agent(
    get_llm_model(),
    deps_type=BraveSearchDependencies,
    system_prompt=SYSTEM_PROMPT
)


@research_agent.tool
async def search_web(
    ctx: RunContext[BraveSearchDependencies],
    query: str,
    max_results: int = 10
) -> str:
    """
    Search the web using Brave Search API.
    
    Args:
        query: Search query to execute
        max_results: Maximum number of results to return (1-20, default 10)
    
    Returns:
        Formatted string with search results including titles, URLs, and descriptions
    """
    try:
        # Ensure max_results is within valid range
        max_results = min(max(max_results, 1), 20)
        
        logger.info(f"Agent executing search for: {query}")
        
        # Use the standalone tool function
        results = await brave_search_tool(
            api_key=ctx.deps.brave_api_key,
            session=ctx.deps.session,
            query=query,
            max_results=max_results
        )
        
        return results
        
    except Exception as e:
        error_msg = f"Web search failed: {str(e)}"
        logger.error(error_msg)
        return error_msg


async def run_research(
    query: str, 
    session_id: Optional[str] = None,
    max_results: int = 10
) -> str:
    """
    Convenience function to run a research query.
    
    Args:
        query: Research query to execute
        session_id: Optional session identifier
        max_results: Maximum search results to include
    
    Returns:
        Research response as string
    """
    deps = await BraveSearchDependencies.create(session_id=session_id)
    
    try:
        result = await research_agent.run(query, deps=deps)
        return result.data
    finally:
        await deps.close()


async def run_research_sync(
    query: str,
    session_id: Optional[str] = None, 
    max_results: int = 10
) -> str:
    """
    Synchronous convenience function to run a research query.
    
    Args:
        query: Research query to execute
        session_id: Optional session identifier  
        max_results: Maximum search results to include
        
    Returns:
        Research response as string
    """
    deps = await BraveSearchDependencies.create(session_id=session_id)
    
    try:
        result = research_agent.run_sync(query, deps=deps)
        return result.data
    finally:
        await deps.close()