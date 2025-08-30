"""
Tests for settings and configuration management.
"""

import pytest
import os
from unittest.mock import patch
from pydantic import ValidationError

from ..settings import Settings, load_settings


class TestSettings:
    """Test suite for Settings configuration class."""
    
    def test_settings_creation_with_valid_env(self):
        """Test settings creation with valid environment variables."""
        with patch.dict(os.environ, {
            "LLM_API_KEY": "test_llm_key",
            "BRAVE_API_KEY": "test_brave_key",
            "LLM_MODEL": "gpt-4",
            "LLM_PROVIDER": "openai"
        }):
            settings = Settings()
            
            assert settings.llm_api_key == "test_llm_key"
            assert settings.brave_api_key == "test_brave_key"
            assert settings.llm_model == "gpt-4"
            assert settings.llm_provider == "openai"
    
    def test_settings_defaults(self):
        """Test that default values are set correctly."""
        with patch.dict(os.environ, {
            "LLM_API_KEY": "test_llm_key",
            "BRAVE_API_KEY": "test_brave_key"
        }):
            settings = Settings()
            
            # Test default values
            assert settings.llm_provider == "openai"
            assert settings.llm_model == "gpt-4o"
            assert settings.llm_base_url == "https://api.openai.com/v1"
            assert settings.brave_search_url == "https://api.search.brave.com/res/v1/web/search"
            assert settings.app_env == "development"
            assert settings.log_level == "INFO"
            assert settings.debug is False
    
    def test_missing_llm_api_key(self):
        """Test validation error when LLM API key is missing."""
        with patch.dict(os.environ, {
            "BRAVE_API_KEY": "test_brave_key"
        }, clear=True):
            with pytest.raises(ValidationError) as exc_info:
                Settings()
            
            assert "llm_api_key" in str(exc_info.value).lower()
    
    def test_missing_brave_api_key(self):
        """Test validation error when Brave API key is missing."""
        with patch.dict(os.environ, {
            "LLM_API_KEY": "test_llm_key"
        }, clear=True):
            with pytest.raises(ValidationError) as exc_info:
                Settings()
            
            assert "brave_api_key" in str(exc_info.value).lower()
    
    def test_empty_api_keys_validation(self):
        """Test that empty API keys are rejected."""
        with patch.dict(os.environ, {
            "LLM_API_KEY": "",
            "BRAVE_API_KEY": "test_brave_key"
        }):
            with pytest.raises(ValidationError) as exc_info:
                Settings()
            
            assert "API key cannot be empty" in str(exc_info.value)
        
        with patch.dict(os.environ, {
            "LLM_API_KEY": "test_llm_key", 
            "BRAVE_API_KEY": "   "  # whitespace only
        }):
            with pytest.raises(ValidationError) as exc_info:
                Settings()
            
            assert "API key cannot be empty" in str(exc_info.value)
    
    def test_case_insensitive_env_vars(self):
        """Test that environment variables are case insensitive."""
        with patch.dict(os.environ, {
            "llm_api_key": "test_llm_key",  # lowercase
            "BRAVE_API_KEY": "test_brave_key",  # uppercase
            "Llm_Model": "gpt-3.5-turbo"  # mixed case
        }):
            settings = Settings()
            
            assert settings.llm_api_key == "test_llm_key"
            assert settings.brave_api_key == "test_brave_key"
            assert settings.llm_model == "gpt-3.5-turbo"
    
    def test_extra_env_vars_ignored(self):
        """Test that extra environment variables are ignored."""
        with patch.dict(os.environ, {
            "LLM_API_KEY": "test_llm_key",
            "BRAVE_API_KEY": "test_brave_key",
            "RANDOM_VAR": "should_be_ignored",
            "ANOTHER_VAR": "also_ignored"
        }):
            # Should not raise any errors about extra fields
            settings = Settings()
            
            assert settings.llm_api_key == "test_llm_key"
            assert settings.brave_api_key == "test_brave_key"
            assert not hasattr(settings, 'random_var')
            assert not hasattr(settings, 'another_var')


class TestLoadSettings:
    """Test suite for the load_settings function."""
    
    def test_load_settings_success(self):
        """Test successful settings loading."""
        with patch.dict(os.environ, {
            "LLM_API_KEY": "test_llm_key",
            "BRAVE_API_KEY": "test_brave_key"
        }):
            settings = load_settings()
            
            assert isinstance(settings, Settings)
            assert settings.llm_api_key == "test_llm_key"
            assert settings.brave_api_key == "test_brave_key"
    
    def test_load_settings_with_dotenv_call(self):
        """Test that load_dotenv is called when loading settings."""
        with patch('brave_search_agent.settings.load_dotenv') as mock_load_dotenv:
            with patch.dict(os.environ, {
                "LLM_API_KEY": "test_llm_key",
                "BRAVE_API_KEY": "test_brave_key"
            }):
                load_settings()
                
                # Verify load_dotenv was called
                assert mock_load_dotenv.call_count >= 1
    
    def test_load_settings_error_handling(self):
        """Test error handling in load_settings function."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError) as exc_info:
                load_settings()
            
            error_msg = str(exc_info.value)
            assert "Failed to load settings" in error_msg
            assert "Make sure to set" in error_msg
            assert ("LLM_API_KEY" in error_msg or "BRAVE_API_KEY" in error_msg)
    
    def test_load_settings_llm_key_specific_error(self):
        """Test specific error message for missing LLM API key."""
        with patch.dict(os.environ, {
            "BRAVE_API_KEY": "test_brave_key"
        }, clear=True):
            with pytest.raises(ValueError) as exc_info:
                load_settings()
            
            error_msg = str(exc_info.value)
            assert "LLM_API_KEY" in error_msg
            assert ".env file" in error_msg
    
    def test_load_settings_brave_key_specific_error(self):
        """Test specific error message for missing Brave API key."""
        with patch.dict(os.environ, {
            "LLM_API_KEY": "test_llm_key"
        }, clear=True):
            with pytest.raises(ValueError) as exc_info:
                load_settings()
            
            error_msg = str(exc_info.value)
            assert "BRAVE_API_KEY" in error_msg
            assert ".env file" in error_msg


class TestGlobalSettingsInstance:
    """Test suite for the global settings instance."""
    
    def test_global_settings_fallback(self):
        """Test that global settings falls back to test values when needed."""
        # This tests the fallback mechanism in the settings module
        from ..settings import settings
        
        # Should not raise an error, even if real env vars are not set
        assert settings is not None
        assert hasattr(settings, 'llm_api_key')
        assert hasattr(settings, 'brave_api_key')
    
    @pytest.mark.skipif(
        not (os.getenv('LLM_API_KEY') and os.getenv('BRAVE_API_KEY')),
        reason="Requires real API keys in environment"
    )
    def test_real_environment_settings(self):
        """Test with real environment variables if available."""
        from ..settings import settings
        
        # If real environment is set, should use real values
        if os.getenv('LLM_API_KEY') and os.getenv('BRAVE_API_KEY'):
            assert settings.llm_api_key != "test_key"
            assert settings.brave_api_key != "test_key"