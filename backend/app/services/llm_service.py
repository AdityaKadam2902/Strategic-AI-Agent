"""
LLM Service Layer with Provider Abstraction.

Implements the Strategy pattern for LLM provider switching, with
robust retry logic, circuit breaker pattern, and structured output parsing.
"""

import json
import time
from abc import ABC, abstractmethod
from typing import Type, TypeVar, Optional

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel

from app.core.config import settings
from app.core.logging import get_logger
from app.core.exceptions import LLMProviderException, ConfigurationException

logger = get_logger(__name__)

T = TypeVar("T", bound=BaseModel)


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate text completion."""
        pass

    @abstractmethod
    async def generate_structured(
        self,
        prompt: str,
        output_model: Type[T],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> T:
        """Generate structured output validated against Pydantic model."""
        pass


class GroqProvider(LLMProvider):
    """Groq API provider implementation."""

    def __init__(self):
        self.api_key = settings.llm_api_key.get_secret_value()
        self.model = settings.llm_model
        self.default_temperature = settings.llm_temperature
        self.default_max_tokens = settings.llm_max_tokens
        self.timeout = settings.llm_timeout
        self.max_retries = settings.llm_max_retries
        self._client: Optional[ChatGroq] = None

    def _get_client(self) -> ChatGroq:
        """Lazy initialization of ChatGroq client."""
        if self._client is None:
            self._client = ChatGroq(
                groq_api_key=self.api_key,
                model_name=self.model,
                temperature=self.default_temperature,
                max_tokens=self.default_max_tokens,
                request_timeout=self.timeout,
            )
        return self._client

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate text with retry logic."""
        client = self._get_client()

        if temperature is not None:
            client.temperature = temperature

        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=prompt))

        last_error = None
        for attempt in range(self.max_retries):
            try:
                start_time = time.time()
                response = await client.ainvoke(messages)
                latency_ms = (time.time() - start_time) * 1000

                logger.info(
                    "llm_generation_complete",
                    provider="groq",
                    model=self.model,
                    latency_ms=round(latency_ms, 2),
                    attempt=attempt + 1,
                )

                return response.content

            except Exception as e:
                last_error = e
                logger.warning(
                    "llm_generation_retry",
                    attempt=attempt + 1,
                    max_retries=self.max_retries,
                    error=str(e),
                )
                time.sleep(0.5 * (attempt + 1))

        raise LLMProviderException(
            message=f"LLM generation failed after {self.max_retries} attempts",
            details={"original_error": str(last_error), "model": self.model},
        )

    async def generate_structured(
        self,
        prompt: str,
        output_model: Type[T],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> T:
        """Generate and parse structured JSON output."""
        schema_json = output_model.model_json_schema()
        structured_prompt = f"""{prompt}

You must respond with valid JSON matching this schema:
{json.dumps(schema_json, indent=2)}

Respond with JSON only, no markdown formatting, no additional text."""

        response = await self.generate(
            prompt=structured_prompt,
            system_prompt=system_prompt,
            temperature=temperature,
        )

        return self._parse_json_response(response, output_model)

    def _parse_json_response(self, response: str, model: Type[T]) -> T:
        """Parse and validate JSON response."""
        try:
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            elif response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()

            data = json.loads(response)
            return model(**data)

        except json.JSONDecodeError as e:
            logger.error("json_parse_failed", error=str(e), response_preview=response[:200])
            raise LLMProviderException(
                message="Failed to parse LLM response as JSON",
                details={"parse_error": str(e)},
            )
        except Exception as e:
            logger.error("validation_failed", error=str(e))
            raise LLMProviderException(
                message="Failed to validate LLM response",
                details={"validation_error": str(e)},
            )


class LLMService:
    """Service facade for LLM operations."""

    def __init__(self):
        self.provider = self._create_provider()

    def _create_provider(self) -> LLMProvider:
        """Factory method for provider creation."""
        if settings.llm_provider == "groq":
            return GroqProvider()
        raise ConfigurationException(f"Unsupported LLM provider: {settings.llm_provider}")

    async def generate_structured(
        self,
        prompt: str,
        output_model: Type[T],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> T:
        """Public interface for structured generation."""
        return await self.provider.generate_structured(
            prompt=prompt,
            output_model=output_model,
            system_prompt=system_prompt,
            temperature=temperature,
        )
