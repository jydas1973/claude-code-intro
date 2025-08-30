"""
Tools for the Brave Search Research Agent.
"""

import logging
import asyncio
from typing import List, Dict, Any, Optional
from aiolimiter import AsyncLimiter

logger = logging.getLogger(__name__)

# Rate limiter: 1 query per second for Brave API free tier
search_rate_limiter = AsyncLimiter(1, 1)  # 1 request per 1 second


async def brave_search_tool(
    api_key: str,
    session,  # httpx.AsyncClient
    query: str,
    max_results: int = 10
) -> str:
    """
    Search the web using Brave Search API with rate limiting.
    
    This is a standalone tool function that can be used by the agent.
    It implements proper rate limiting, error handling, and result formatting.
    
    Args:
        api_key: Brave Search API key
        session: HTTP client session
        query: Search query string
        max_results: Maximum number of results to return (1-20)
    
    Returns:
        Formatted string with search results
    
    Raises:
        Exception: If search fails or API errors occur
    """
    if not api_key or not api_key.strip():
        return "Error: Brave API key is required"
    
    if not query or not query.strip():
        return "Error: Search query cannot be empty"
    
    # Ensure max_results is within valid range
    max_results = min(max(max_results, 1), 20)
    
    # Apply rate limiting (1 query/second for free tier)
    async with search_rate_limiter:
        try:
            logger.info(f"Searching Brave for: {query} (max_results: {max_results})")
            
            headers = {
                "X-Subscription-Token": api_key,
                "Accept": "application/json"
            }
            
            params = {
                "q": query,
                "count": max_results,
                "search_lang": "en"
            }
            
            response = await session.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers=headers,
                params=params
            )
            
            # Handle rate limiting
            if response.status_code == 429:
                logger.warning("Rate limit exceeded for Brave API")
                return "Error: Rate limit exceeded. Please try again in a moment."
            
            # Handle authentication errors
            if response.status_code == 401:
                logger.error("Invalid Brave API key")
                return "Error: Invalid Brave API key. Please check your configuration."
            
            # Handle other HTTP errors
            if response.status_code != 200:
                error_msg = f"Brave API returned {response.status_code}: {response.text[:200]}"
                logger.error(error_msg)
                return f"Error: {error_msg}"
            
            data = response.json()
            web_results = data.get("web", {}).get("results", [])
            
            if not web_results:
                return f"No search results found for query: {query}"
            
            # Format results as a readable string
            result_text = f"Search Results for '{query}':\n\n"
            
            for i, result in enumerate(web_results, 1):
                title = result.get("title", "No title")
                url = result.get("url", "No URL")
                description = result.get("description", "No description")
                
                result_text += f"{i}. **{title}**\n"
                result_text += f"   URL: {url}\n"
                result_text += f"   {description}\n\n"
            
            logger.info(f"Found {len(web_results)} results for query: {query}")
            return result_text
            
        except asyncio.TimeoutError:
            error_msg = "Search request timed out"
            logger.error(error_msg)
            return f"Error: {error_msg}"
        except Exception as e:
            error_msg = f"Search failed: {str(e)}"
            logger.error(f"Error during Brave search: {e}")
            return f"Error: {error_msg}"