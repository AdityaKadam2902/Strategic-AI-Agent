"""
Proposition Agent - Strategic Advocate.

Generates arguments in favor of the strategic decision with
quantified impacts and specific success factors.
"""

from app.models import ProAgentOutput
from app.services.llm_service import LLMService
from app.agents.prompts import AgentPrompts, format_prompt
from app.core.logging import get_logger

logger = get_logger(__name__)


async def run_pro_agent(state: dict) -> dict:
    """
    Execute Pro Agent analysis.

    Args:
        state: Current debate state with decision and context

    Returns:
        State update with pro_output or errors
    """
    logger.info("agent_execution_started", agent="pro_agent", request_id=state.get("request_id"))

    try:
        llm = LLMService()
        prompt = format_prompt(
            AgentPrompts.PRO_AGENT_PROMPT,
            decision=state["decision"],
            industry_context=state.get("industry_context"),
        )

        output = await llm.generate_structured(
            prompt=prompt,
            output_model=ProAgentOutput,
            temperature=0.7,
        )

        logger.info(
            "agent_execution_completed",
            agent="pro_agent",
            arguments_count=len(output.arguments),
            opportunities_count=len(output.opportunities),
        )

        return {"pro_output": output}

    except Exception as e:
        logger.error("agent_execution_failed", agent="pro_agent", error=str(e))
        errors = state.get("errors", [])
        errors.append(f"Pro Agent: {str(e)}")
        return {"errors": errors}
