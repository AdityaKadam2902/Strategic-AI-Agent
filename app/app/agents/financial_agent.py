"""
Financial Analysis Agent - Economic Evaluator.

Analyzes investment requirements, ROI projections, cost structures,
and financial risks with realistic estimates and clear assumptions.
"""

from app.models import FinancialAgentOutput
from app.services.llm_service import LLMService
from app.agents.prompts import AgentPrompts, format_prompt
from app.core.logging import get_logger

logger = get_logger(__name__)


async def run_financial_agent(state: dict) -> dict:
    """
    Execute Financial Agent analysis.

    Args:
        state: Current debate state with decision and context

    Returns:
        State update with financial_output or errors
    """
    logger.info("agent_execution_started", agent="financial_agent", request_id=state.get("request_id"))

    try:
        llm = LLMService()
        prompt = format_prompt(
            AgentPrompts.FINANCIAL_AGENT_PROMPT,
            decision=state["decision"],
            industry_context=state.get("industry_context"),
        )

        output = await llm.generate_structured(
            prompt=prompt,
            output_model=FinancialAgentOutput,
            temperature=0.5,
        )

        logger.info(
            "agent_execution_completed",
            agent="financial_agent",
            uncertainty=output.uncertainty_level,
            investment=output.estimated_investment[:50],
        )

        return {"financial_output": output}

    except Exception as e:
        logger.error("agent_execution_failed", agent="financial_agent", error=str(e))
        errors = state.get("errors", [])
        errors.append(f"Financial Agent: {str(e)}")
        return {"errors": errors}
