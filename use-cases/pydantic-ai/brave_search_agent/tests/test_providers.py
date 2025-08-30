"""
Tests for LLM provider configuration.
"""

import pytest
import os
from unittest.mock import patch, Mock
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from ..providers import get_llm_model, get_model_info, validate_llm_configuration


class TestGetLLMModel:
    """Test suite for get_llm_model function."""
    
    def test_get_llm_model_default(self):
        """Test get_llm_model with default settings."""
        with patch.dict(os.environ, {
            "LLM_API_KEY": "test_api_key",
            "BRAVE_API_KEY": "test_brave_key",
            "LLM_MODEL": "gpt-4o",
            "LLM_BASE_URL": "https://api.openai.com/v1"
        }):
            model = get_llm_model()
            
            assert isinstance(model, OpenAIModel)
            assert model.name == "gpt-4o"
            assert isinstance(model.provider, OpenAIProvider)
    
    def test_get_llm_model_with_override(self):
        """Test get_llm_model with model choice override."""
        with patch.dict(os.environ, {
            "LLM_API_KEY": "test_api_key",
            "BRAVE_API_KEY": "test_brave_key", 
            "LLM_MODEL": "gpt-4o",
        }):
            # Override the default model
            model = get_llm_model(model_choice="gpt-3.5-turbo")
            
            assert isinstance(model, OpenAIModel)
            assert model.name == "gpt-3.5-turbo"
    
    def test_get_llm_model_provider_configuration(self):
        """Test that provider is configured correctly."""
        with patch.dict(os.environ, {
            "LLM_API_KEY": "test_api_key_123",
            "BRAVE_API_KEY": "test_brave_key",
            "LLM_BASE_URL": "https://custom.openai.endpoint.com/v1"
        }):
            model = get_llm_model()
            
            provider = model.provider
            assert isinstance(provider, OpenAIProvider)
            # Note: We can't directly test the API key or base_url from the provider
            # as they're internal to the OpenAI provider implementation
    
    def test_get_llm_model_settings_loading_error(self):
        """Test get_llm_model when settings loading fails."""
        with patch('brave_search_agent.providers.load_settings') as mock_load_settings:
            mock_load_settings.side_effect = ValueError("Settings error")
            
            with pytest.raises(ValueError, match="Settings error"):
                get_llm_model()


class TestGetModelInfo:
    """Test suite for get_model_info function."""
    
    def test_get_model_info_returns_dict(self):
        """Test that get_model_info returns a dictionary with expected keys."""
        with patch.dict(os.environ, {
            "LLM_API_KEY": "test_api_key",
            "BRAVE_API_KEY": "test_brave_key",
            "LLM_PROVIDER": "openai",
            "LLM_MODEL": "gpt-4o",
            "LLM_BASE_URL": "https://api.openai.com/v1",
            "APP_ENV": "testing",
            "DEBUG": "true"
        }):
            info = get_model_info()
            
            assert isinstance(info, dict)
            
            # Check all expected keys are present
            expected_keys = {
                "llm_provider", "llm_model", "llm_base_url", "app_env", "debug"
            }
            assert set(info.keys()) == expected_keys
            
            # Check values
            assert info["llm_provider"] == "openai"
            assert info["llm_model"] == "gpt-4o"
            assert info["llm_base_url"] == "https://api.openai.com/v1"
            assert info["app_env"] == "testing"
            assert info["debug"] is True
    
    def test_get_model_info_with_defaults(self):
        """Test get_model_info with default values."""
        with patch.dict(os.environ, {
            "LLM_API_KEY": "test_api_key",
            "BRAVE_API_KEY": "test_brave_key"
        }):
            info = get_model_info()
            
            # Check default values
            assert info["llm_provider"] == "openai"
            assert info["llm_model"] == "gpt-4o"
            assert info["llm_base_url"] == "https://api.openai.com/v1"
            assert info["app_env"] == "development"
            assert info["debug"] is False


class TestValidateLLMConfiguration:
    """Test suite for validate_llm_configuration function."""
    
    def test_validate_llm_configuration_success(self):
        """Test successful LLM configuration validation."""
        with patch.dict(os.environ, {
            "LLM_API_KEY": "test_api_key",
            "BRAVE_API_KEY": "test_brave_key",
        }):
            result = validate_llm_configuration()
            assert result is True
    
    def test_validate_llm_configuration_failure(self):
        """Test LLM configuration validation failure."""
        # Clear environment to cause validation failure
        with patch.dict(os.environ, {}, clear=True):
            result = validate_llm_configuration()
            assert result is False
    
    def test_validate_llm_configuration_exception_handling(self):
        """Test that validation handles exceptions gracefully."""
        with patch('brave_search_agent.providers.get_llm_model') as mock_get_model:
            mock_get_model.side_effect = Exception("Model creation failed")
            
            # Should return False, not raise exception
            result = validate_llm_configuration()
            assert result is False
    
    def test_validate_llm_configuration_prints_error(self, capsys):
        """Test that validation prints error message on failure."""
        with patch('brave_search_agent.providers.get_llm_model') as mock_get_model:
            mock_get_model.side_effect = Exception("Test error message")
            
            result = validate_llm_configuration()
            
            assert result is False
            captured = capsys.readouterr()
            assert "LLM configuration validation failed" in captured.out
            assert "Test error message" in captured.out


class TestProviderIntegration:
    """Test suite for provider integration patterns."""
    
    def test_provider_model_creation_consistency(self):
        """Test that multiple calls return consistent models."""
        with patch.dict(os.environ, {
            "LLM_API_KEY": "test_api_key",
            "BRAVE_API_KEY": "test_brave_key",
            "LLM_MODEL": "gpt-4o"
        }):
            model1 = get_llm_model()
            model2 = get_llm_model()
            
            # Should be equivalent models
            assert model1.name == model2.name
            assert type(model1.provider) == type(model2.provider)
    
    def test_different_model_override_creates_different_models(self):
        """Test that different model choices create different models."""
        with patch.dict(os.environ, {
            "LLM_API_KEY": "test_api_key",
            "BRAVE_API_KEY": "test_brave_key",
            "LLM_MODEL": "gpt-4o"
        }):
            model_default = get_llm_model()
            model_override = get_llm_model("gpt-3.5-turbo")
            
            assert model_default.name == "gpt-4o"
            assert model_override.name == "gpt-3.5-turbo"
    
    def test_settings_dependency(self):
        """Test that provider functions depend on settings correctly."""
        with patch('brave_search_agent.providers.load_settings') as mock_load_settings:
            mock_settings = Mock()
            mock_settings.llm_model = "custom-model"
            mock_settings.llm_base_url = "https://custom.api.com/v1"
            mock_settings.llm_api_key = "custom_key"
            mock_settings.llm_provider = "custom"
            mock_settings.app_env = "custom_env"
            mock_settings.debug = True
            mock_load_settings.return_value = mock_settings
            
            # Test get_llm_model uses settings
            model = get_llm_model()
            assert model.name == "custom-model"
            
            # Test get_model_info uses settings
            info = get_model_info()
            assert info["llm_provider"] == "custom"
            assert info["llm_model"] == "custom-model"
            assert info["llm_base_url"] == "https://custom.api.com/v1"
            assert info["app_env"] == "custom_env"
            assert info["debug"] is True