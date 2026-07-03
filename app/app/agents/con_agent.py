"""
Opposition Agent - Strategic Skeptic.

Identifies risks, challenges, and alternative approaches
to protect the organization from poor strategic decisions.
"""

from app.models import ConAgentOutput
from app.services.llm_service import LLMService
from app.agents.prompts import AgentPrompts, format_prompt
from app.core.logging import get_logger

logger = get_logger(__name__)


async def run_con_agent(state: dict) -> dict:
    """
    Execute Con Agent analysis.

    Args:
        state: Current debate state with decision and context

    Returns:
        State update with con_output or errors
    """
    logger.info("agent_execution_started", agent="con_agent", request_id=state.get("request_id"))

    try:
        llm = LLMService()
        prompt = format_prompt(
            AgentPrompts.CON_AGENT_PROMPT,
            decision=state["decision"],
            industry_context=state.get("industry_context"),
        )

        output = await llm.generate_structured(
            prompt=prompt,
            output_model=ConAgentOutput,
            temperature=0.7,
        )

        logger.info(
            "agent_execution_completed",
            agent="con_agent",
            risks_count=len(output.risks),
            alternatives_count=len(output.alternative_options),
        )

        return {"con_output": output}

    except Exception as e:
        logger.error("agent_execution_failed", agent="con_agent", error=str(e))
        errors = state.get("errors", [])
        errors.append(f"Con Agent: {str(e)}")
        return {"errors": errors}
