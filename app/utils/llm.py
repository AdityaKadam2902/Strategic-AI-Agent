"""
LLM utilities and helper functions for Groq integration.
"""
import logging
import json
from typing import Type, TypeVar, Optional
from langchain_groq import ChatGroq
from pydantic import BaseModel
from app.config import settings

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)


def get_llm(temperature: Optional[float] = None) -> ChatGroq:
    """
    Get configured ChatGroq instance.
    
    Args:
        temperature: Optional temperature override
        
    Returns:
        Configured ChatGroq instance
    """
    return ChatGroq(
        groq_api_key=settings.groq_api_key,
        model_name=settings.groq_model,
        temperature=temperature if temperature is not None else settings.temperature,
        max_tokens=settings.max_tokens,
    )


def parse_json_response(response: str, model: Type[T]) -> T:
    """
    Parse JSON response from LLM and validate against Pydantic model.
    
    Args:
        response: Raw response string from LLM
        model: Pydantic model class to validate against
        
    Returns:
        Validated Pydantic model instance
        
    Raises:
        ValueError: If parsing or validation fails
    """
    try:
        # Try to find JSON in the response (handle markdown code blocks)
        response = response.strip()
        
        # Remove markdown code blocks if present
        if response.startswith("```json"):
            response = response[7:]
        elif response.startswith("```"):
            response = response[3:]
            
        if response.endswith("```"):
            response = response[:-3]
            
        response = response.strip()
        
        # Parse JSON
        data = json.loads(response)
        
        # Validate with Pydantic model
        return model(**data)
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        logger.error(f"Response was: {response[:500]}")
        raise ValueError(f"Failed to parse JSON response: {e}")
    except Exception as e:
        logger.error(f"Validation error: {e}")
        raise ValueError(f"Failed to validate response: {e}")


async def invoke_agent_with_retry(
    llm: ChatGroq,
    prompt: str,
    model: Type[T],
    max_retries: int = 2
) -> T:
    """
    Invoke LLM with retry logic and structured output parsing.
    
    Args:
        llm: ChatGroq instance
        prompt: Formatted prompt string
        model: Pydantic model for response validation
        max_retries: Maximum number of retry attempts
        
    Returns:
        Validated Pydantic model instance
        
    Raises:
        Exception: If all retries fail
    """
    for attempt in range(max_retries + 1):
        try:
            response = await llm.ainvoke(prompt)
            return parse_json_response(response.content, model)
            
        except Exception as e:
            if attempt < max_retries:
                logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                continue
            else:
                logger.error(f"All {max_retries + 1} attempts failed")
                raise


def format_agent_context(state: dict, agent_name: str) -> str:
    """
    Format context from state for agent prompts.
    
    Args:
        state: Current debate state
        agent_name: Name of the calling agent
        
    Returns:
        Formatted context string
    """
    context_parts = [f"Decision to evaluate: {state['decision']}"]
    
    # Add other agent outputs if available (for Judge agent)
    if agent_name == "Judge":
        if state.get('pro_output'):
            context_parts.append(f"\n--- PRO ARGUMENTS ---\n{state['pro_output'].model_dump_json(indent=2)}")
        if state.get('con_output'):
            context_parts.append(f"\n--- CON ARGUMENTS ---\n{state['con_output'].model_dump_json(indent=2)}")
        if state.get('financial_output'):
            context_parts.append(f"\n--- FINANCIAL ANALYSIS ---\n{state['financial_output'].model_dump_json(indent=2)}")
        if state.get('market_output'):
            context_parts.append(f"\n--- MARKET ANALYSIS ---\n{state['market_output'].model_dump_json(indent=2)}")
    
    return "\n".join(context_parts)
