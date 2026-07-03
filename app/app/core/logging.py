"""
Enterprise Logging Configuration with Structured Output.

Implements structured logging using structlog for JSON-formatted logs
suitable for log aggregation systems (ELK, Datadog, CloudWatch).
"""

import logging
import sys
from typing import Any

import structlog
from structlog.processors import JSONRenderer, TimeStamper
from structlog.stdlib import BoundLogger

from app.core.config import settings


def configure_logging() -> None:
    """
    Configure application-wide logging with structured output.

    Sets up both standard library logging and structlog for
    consistent JSON-formatted log output across all modules.
    """
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper()),
    )

    # Suppress noisy third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    # Configure structlog processors based on environment
    shared_processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        TimeStamper(fmt="iso"),
    ]

    if settings.log_format == "structured":
        # Production: JSON formatted logs
        processors = shared_processors + [
            structlog.processors.dict_tracebacks,
            JSONRenderer(),
        ]
    else:
        # Development: Human-readable logs
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(colors=True),
        ]

    structlog.configure(
        processors=processors,
        wrapper_class=BoundLogger,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> BoundLogger:
    """
    Get a structured logger instance.

    Args:
        name: Module or component identifier

    Returns:
        BoundLogger: Configured structured logger
    """
    return structlog.get_logger(name)
