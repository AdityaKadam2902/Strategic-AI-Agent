"""
Enterprise Configuration Management for Strategic Decision Intelligence Platform.

Implements the Settings pattern with environment-based configuration,
validation, and secure credential handling following 12-Factor App principles.
"""

import os
from functools import lru_cache
from typing import Optional

from pydantic import Field, field_validator, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path

ENV_FILE = Path(__file__).resolve().parent.parent.parent.parent / ".env"

class ApplicationSettings(BaseSettings):
    """
    Centralized application configuration with strict validation.

    All configuration is loaded from environment variables following
    the 12-Factor App methodology. No hardcoded values are permitted.
    """



# Find .env at project root (2 levels up from config.py)
    

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        validate_default=True,
    )

    # Application Metadata
    app_name: str = Field(
        default="strategic-decision-intelligence",
        description="Application identifier for service discovery",
    )
    app_version: str = Field(
        default="2.0.0",
        description="Semantic version following semver.org",
    )
    environment: str = Field(
        default="development",
        pattern="^(development|staging|production)$",
        description="Deployment environment identifier",
    )
    debug: bool = Field(
        default=False,
        description="Debug mode - NEVER enable in production",
    )

    # API Server Configuration
    api_host: str = Field(
        default="0.0.0.0",
        description="Network interface for HTTP server binding",
    )
    api_port: int = Field(
        default=8000,
        ge=1024,
        le=65535,
        description="HTTP server port number",
    )
    api_workers: int = Field(
        default=1,
        ge=1,
        le=16,
        description="Uvicorn worker process count",
    )
    api_timeout: int = Field(
        default=120,
        ge=10,
        le=300,
        description="Request timeout in seconds",
    )

    # LLM Provider Configuration
    llm_provider: str = Field(
        default="groq",
        pattern="^(groq|openai|anthropic|azure)$",
        description="LLM provider identifier",
    )
    llm_api_key: SecretStr = Field(
        ...,
        description="LLM provider API key - REQUIRED",
    )
    llm_model: str = Field(
        default="llama-3.3-70b-versatile",
        description="Model identifier for inference",
    )
    llm_temperature: float = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
        description="Sampling temperature for generation",
    )
    llm_max_tokens: int = Field(
        default=4096,
        ge=256,
        le=8192,
        description="Maximum tokens per response",
    )
    llm_timeout: int = Field(
        default=60,
        ge=10,
        le=120,
        description="LLM API timeout in seconds",
    )
    llm_max_retries: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Maximum retry attempts for failed requests",
    )

    # Security Configuration
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:5173",
        description="Comma-separated allowed CORS origins",
    )
    rate_limit_requests: int = Field(
        default=30,
        ge=1,
        le=1000,
        description="Rate limit requests per window",
    )
    rate_limit_window: int = Field(
        default=60,
        ge=10,
        le=3600,
        description="Rate limiting window in seconds",
    )

    # Caching Configuration
    cache_enabled: bool = Field(
        default=False,
        description="Enable Redis caching layer",
    )
    cache_ttl: int = Field(
        default=3600,
        ge=60,
        le=86400,
        description="Cache TTL in seconds",
    )
    redis_url: Optional[str] = Field(
        default=None,
        description="Redis connection URL",
    )

    # Observability Configuration
    log_level: str = Field(
        default="INFO",
        pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$",
        description="Python logging level",
    )
    log_format: str = Field(
        default="structured",
        pattern="^(structured|plain)$",
        description="Logging output format",
    )
    metrics_enabled: bool = Field(
        default=True,
        description="Enable Prometheus metrics endpoint",
    )
    tracing_enabled: bool = Field(
        default=False,
        description="Enable OpenTelemetry distributed tracing",
    )

    @field_validator("debug")
    @classmethod
    def validate_debug_mode(cls, v: bool, info) -> bool:
        """Prevent debug mode in production environments."""
        env = info.data.get("environment", "development")
        if env == "production" and v:
            raise ValueError("Debug mode cannot be enabled in production environment")
        return v

    @field_validator("llm_api_key")
    @classmethod
    def validate_api_key(cls, v: SecretStr) -> SecretStr:
        """Ensure API key is not empty or placeholder."""
        key = v.get_secret_value()
        if not key or key.strip() == "" or "your_" in key.lower():
            raise ValueError(
                "LLM_API_KEY is required. Please set a valid API key in your .env file. "
                "Get one at https://console.groq.com/keys"
            )
        return v

    @field_validator("redis_url")
    @classmethod
    def validate_redis_url(cls, v: Optional[str], info) -> Optional[str]:
        """Validate Redis URL when caching is enabled."""
        cache_enabled = info.data.get("cache_enabled", False)
        if cache_enabled and not v:
            raise ValueError("REDIS_URL is required when CACHE_ENABLED is true")
        return v

    def get_cors_origins_list(self) -> list[str]:
        """Parse CORS origins string into list."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == "production"

    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == "development"


@lru_cache(maxsize=1)
def get_settings() -> ApplicationSettings:
    """
    Get cached application settings instance.

    Uses LRU cache to prevent repeated environment parsing
    and validation during application lifecycle.

    Returns:
        ApplicationSettings: Validated configuration instance
    """
    return ApplicationSettings()


# Global settings instance for module-level access
settings = get_settings()
