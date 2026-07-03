"""
Custom Exception Hierarchy for Domain-Specific Error Handling.

Implements a structured exception taxonomy enabling precise error
classification, monitoring, and client-facing error responses.
"""

from typing import Optional


class ApplicationException(Exception):
    """Base exception for all application errors."""

    def __init__(
        self,
        message: str,
        error_code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: Optional[dict] = None,
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}


class ValidationException(ApplicationException):
    """Raised when input validation fails."""

    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=400,
            details=details,
        )


class ConfigurationException(ApplicationException):
    """Raised when application configuration is invalid."""

    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(
            message=message,
            error_code="CONFIGURATION_ERROR",
            status_code=500,
            details=details,
        )


class LLMProviderException(ApplicationException):
    """Raised when LLM provider API fails."""

    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(
            message=message,
            error_code="LLM_PROVIDER_ERROR",
            status_code=503,
            details=details,
        )


class AgentExecutionException(ApplicationException):
    """Raised when an AI agent fails to execute."""

    def __init__(self, message: str, agent_name: str, details: Optional[dict] = None):
        super().__init__(
            message=message,
            error_code="AGENT_EXECUTION_ERROR",
            status_code=500,
            details={"agent_name": agent_name, **(details or {})},
        )


class RateLimitException(ApplicationException):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded", details: Optional[dict] = None):
        super().__init__(
            message=message,
            error_code="RATE_LIMIT_EXCEEDED",
            status_code=429,
            details=details,
        )


class CacheException(ApplicationException):
    """Raised when cache operation fails."""

    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(
            message=message,
            error_code="CACHE_ERROR",
            status_code=500,
            details=details,
        )
