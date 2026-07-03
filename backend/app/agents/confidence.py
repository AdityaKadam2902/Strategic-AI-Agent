"""
Confidence Scoring Engine - Risk-Adjusted Assessment.

Calculates confidence scores based on multi-factor analysis including
consensus level, risk-opportunity balance, financial certainty, and
regulatory clarity with transparent scoring rationale.
"""

from app.models import ConfidenceOutput, JudgeOutput, FinancialAgentOutput, MarketAgentOutput, ConAgentOutput
from app.services.llm_service import LLMService
from app.agents.prompts import AgentPrompts, format_prompt
from app.core.logging import get_logger

logger = get_logger(__name__)


async def run_confidence_scorer(state: dict) -> dict:
    """
    Calculate confidence score based on all debate outputs.

    Args:
        state: Current debate state with judge output

    Returns:
        State update with confidence_output
    """
    logger.info("agent_execution_started", agent="confidence_scorer", request_id=state.get("request_id"))

    try:
        judge_output = state.get("judge_output")
        financial_output = state.get("financial_output")
        market_output = state.get("market_output")
        con_output = state.get("con_output")

        if not judge_output:
            raise ValueError("Judge output is required for confidence scoring")

        context = {
            "decision": state["decision"],
            "final_decision": judge_output.final_decision,
            "consensus_level": judge_output.consensus_level,
            "num_opportunities": len(judge_output.key_opportunities),
            "num_risks": len(judge_output.key_risks),
            "financial_uncertainty": financial_output.uncertainty_level if financial_output else "high",
            "num_regulatory": len(market_output.regulatory_concerns) if market_output else 0,
            "num_alternatives": len(con_output.alternative_options) if con_output else 0,
        }

        llm = LLMService()
        prompt = format_prompt(
            AgentPrompts.CONFIDENCE_PROMPT,
            decision=state["decision"],
            **context
        )

        output = await llm.generate_structured(
            prompt=prompt,
            output_model=ConfidenceOutput,
            temperature=0.1,
        )

        # Validate score range
        if not 0 <= output.score <= 100:
            logger.warning("confidence_score_out_of_range", score=output.score)
            output.score = max(0, min(100, output.score))

        logger.info(
            "agent_execution_completed",
            agent="confidence_scorer",
            score=output.score,
            risk_adjusted=output.risk_adjusted_score,
        )

        return {"confidence_output": output}

    except Exception as e:
        logger.error("agent_execution_failed", agent="confidence_scorer", error=str(e))
        # Fallback scoring
        fallback = ConfidenceOutput(
            score=50,
            factors={
                "consensus": 15,
                "risk_opportunity_balance": 12,
                "financial_certainty": 13,
                "regulatory_clarity": 10,
            },
            explanation="Fallback score due to calculation error",
            risk_adjusted_score=45,
        )
        return {"confidence_output": fallback}
