"""
Unit tests for configuration management.
"""

import pytest
from pydantic import ValidationError

from app.core.config import ApplicationSettings


class TestApplicationSettings:
    """Test cases for application settings."""

    def test_valid_settings(self, monkeypatch):
        """Test valid settings creation."""
        monkeypatch.setenv("LLM_API_KEY", "gsk_test_key_12345")
        monkeypatch.setenv("ENVIRONMENT", "development")

        settings = ApplicationSettings()
        assert settings.environment == "development"
        assert settings.llm_provider == "groq"

    def test_production_debug_rejection(self, monkeypatch):
        """Test debug mode rejected in production."""
        monkeypatch.setenv("LLM_API_KEY", "gsk_test_key_12345")
        monkeypatch.setenv("ENVIRONMENT", "production")
        monkeypatch.setenv("DEBUG", "true")

        with pytest.raises(ValidationError) as exc_info:
            ApplicationSettings()
        assert "Debug mode cannot be enabled" in str(exc_info.value)

    def test_invalid_api_key(self, monkeypatch):
        """Test placeholder API key rejected."""
        monkeypatch.setenv("LLM_API_KEY", "your_api_key_here")

        with pytest.raises(ValidationError) as exc_info:
            ApplicationSettings()
        assert "LLM_API_KEY is required" in str(exc_info.value)
