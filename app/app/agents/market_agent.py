"""
Market Intelligence Agent - Competitive Landscape Analyst.

Evaluates market size, competition, regulatory concerns, and
macroeconomic risks for strategic decision context.
"""

from app.models import MarketAgentOutput
from app.services.llm_service import LLMService
from app.agents.prompts import AgentPrompts, format_prompt
from app.core.logging import get_logger

logger = get_logger(__name__)


async def run_market_agent(state: dict) -> dict:
    """
    Execute Market Agent analysis.

    Args:
        state: Current debate state with decision and context

    Returns:
        State update with market_output or errors
    """
    logger.info("agent_execution_started", agent="market_agent", request_id=state.get("request_id"))

    try:
        llm = LLMService()
        prompt = format_prompt(
            AgentPrompts.MARKET_AGENT_PROMPT,
            decision=state["decision"],
            industry_context=state.get("industry_context"),
        )

        output = await llm.generate_structured(
            prompt=prompt,
            output_model=MarketAgentOutput,
            temperature=0.6,
        )

        logger.info(
            "agent_execution_completed",
            agent="market_agent",
            trends_count=len(output.market_trends),
            regulatory_count=len(output.regulatory_concerns),
        )

        return {"market_output": output}

    except Exception as e:
        logger.error("agent_execution_failed", agent="market_agent", error=str(e))
        errors = state.get("errors", [])
        errors.append(f"Market Agent: {str(e)}")
        return {"errors": errors}
