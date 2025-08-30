"""
Dependencies for the Brave Search Research Agent.
"""

import httpx
from dataclasses import dataclass, field
from typing import Optional
from .settings import load_settings


@dataclass
class BraveSearchDependencies:
    """
    Dependencies for the Brave Search Research Agent.
    
    This dataclass contains all external dependencies needed by the agent,
    following PydanticAI best practices for dependency injection.
    """
    brave_api_key: str
    session: httpx.AsyncClient
    session_id: Optional[str] = None

    @classmethod  
    async def create(cls, session_id: Optional[str] = None) -> "BraveSearchDependencies":
        """
        Create dependencies with proper HTTP client setup.
        
        Args:
            session_id: Optional session identifier for tracking
            
        Returns:
            Configured dependencies instance
        """
        settings = load_settings()
        
        # Create HTTP client with reasonable defaults
        session = httpx.AsyncClient(
            timeout=30.0,
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
            headers={
                "Accept": "application/json",
                "User-Agent": "Brave-Search-Research-Agent/1.0"
            }
        )
        
        return cls(
            brave_api_key=settings.brave_api_key,
            session=session,
            session_id=session_id
        )
    
    async def close(self):
        """Close the HTTP client session."""
        await self.session.aclose()