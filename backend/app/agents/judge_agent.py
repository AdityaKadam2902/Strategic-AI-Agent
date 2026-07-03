"""
Executive Judge Agent - Strategic Synthesis.

Synthesizes inputs from all specialist agents to produce a final
recommendation with clear reasoning and priority actions.
"""

import json

from app.models import JudgeOutput
from app.services.llm_service import LLMService
from app.agents.prompts import AgentPrompts, format_prompt
from app.core.logging import get_logger

logger = get_logger(__name__)


async def run_judge_agent(state: dict) -> dict:
    """
    Execute Judge Agent synthesis.

    Args:
        state: Current debate state with all agent outputs

    Returns:
        State update with judge_output or errors
    """
    logger.info("agent_execution_started", agent="judge_agent", request_id=state.get("request_id"))

    try:
        llm = LLMService()

        # Format outputs for context
        pro_output = json.dumps(state.get("pro_output", {}).model_dump() if state.get("pro_output") else {}, indent=2)
        con_output = json.dumps(state.get("con_output", {}).model_dump() if state.get("con_output") else {}, indent=2)
        financial_output = json.dumps(state.get("financial_output", {}).model_dump() if state.get("financial_output") else {}, indent=2)
        market_output = json.dumps(state.get("market_output", {}).model_dump() if state.get("market_output") else {}, indent=2)

        prompt = format_prompt(
            AgentPrompts.JUDGE_AGENT_PROMPT,
            decision=state["decision"],
            pro_output=pro_output,
            con_output=con_output,
            financial_output=financial_output,
            market_output=market_output,
        )

        output = await llm.generate_structured(
            prompt=prompt,
            output_model=JudgeOutput,
            temperature=0.3,
        )

        logger.info(
            "agent_execution_completed",
            agent="judge_agent",
            decision=output.final_decision,
            consensus=output.consensus_level,
        )

        return {"judge_output": output}

    except Exception as e:
        logger.error("agent_execution_failed", agent="judge_agent", error=str(e))
        errors = state.get("errors", [])
        errors.append(f"Judge Agent: {str(e)}")
        return {"errors": errors}
