"""
Configuration management for Brave Search Research Agent using pydantic-settings.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator, ConfigDict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # LLM Configuration
    llm_provider: str = Field(default="openai", description="LLM provider")
    llm_api_key: str = Field(..., description="API key for the LLM provider")
    llm_model: str = Field(default="gpt-4o", description="Model name to use")
    llm_base_url: str = Field(
        default="https://api.openai.com/v1", 
        description="Base URL for the LLM API"
    )
    
    # Brave Search Configuration
    brave_api_key: str = Field(..., description="Brave Search API key")
    brave_search_url: str = Field(
        default="https://api.search.brave.com/res/v1/web/search",
        description="Brave Search API endpoint"
    )
    
    # Application Configuration
    app_env: str = Field(default="development", description="Application environment")
    log_level: str = Field(default="INFO", description="Logging level")
    debug: bool = Field(default=False, description="Enable debug mode")
    
    @field_validator("llm_api_key", "brave_api_key")
    @classmethod
    def validate_api_keys(cls, v):
        """Ensure API keys are not empty."""
        if not v or v.strip() == "":
            raise ValueError("API key cannot be empty")
        return v


def load_settings() -> Settings:
    """Load settings with proper error handling and environment loading."""
    # Load environment variables from .env file
    load_dotenv()
    
    try:
        return Settings()
    except Exception as e:
        error_msg = f"Failed to load settings: {e}"
        if "llm_api_key" in str(e).lower():
            error_msg += "\nMake sure to set LLM_API_KEY in your .env file"
        if "brave_api_key" in str(e).lower():
            error_msg += "\nMake sure to set BRAVE_API_KEY in your .env file"
        raise ValueError(error_msg) from e


# Global settings instance for easy access
try:
    settings = load_settings()
except Exception:
    # For testing, create settings with dummy values if real environment is not set
    import os
    os.environ.setdefault("LLM_API_KEY", "test_key")
    os.environ.setdefault("BRAVE_API_KEY", "test_key")
    settings = Settings()