"""
LangGraph Workflow Orchestration Service.

Manages the multi-agent debate workflow with parallel execution,
error handling, and state management.
"""

import asyncio
import time

from langgraph.graph import StateGraph, END

from app.state import DebateState
from app.agents.pro_agent import run_pro_agent
from app.agents.con_agent import run_con_agent
from app.agents.financial_agent import run_financial_agent
from app.agents.market_agent import run_market_agent
from app.agents.judge_agent import run_judge_agent
from app.agents.confidence import run_confidence_scorer
from app.core.logging import get_logger
from app.core.exceptions import AgentExecutionException

logger = get_logger(__name__)


class DebateGraphService:
    """Service for managing debate workflow execution."""

    def __init__(self):
        self._graph = None

    def _build_graph(self):
        """Build and compile the debate workflow graph."""
        workflow = StateGraph(DebateState)

        # Add nodes
        workflow.add_node("specialist_agents", self._run_specialists_parallel)
        workflow.add_node("judge_agent", self._run_judge_wrapper)
        workflow.add_node("confidence_scorer", self._run_confidence_wrapper)

        # Define edges
        workflow.set_entry_point("specialist_agents")
        workflow.add_edge("specialist_agents", "judge_agent")
        workflow.add_edge("judge_agent", "confidence_scorer")
        workflow.add_edge("confidence_scorer", END)

        return workflow.compile()

    async def _run_specialists_parallel(self, state: DebateState) -> DebateState:
        """Run all four specialist agents concurrently."""
        logger.info(
            "specialist_agents_parallel_execution",
            request_id=state.get("request_id"),
        )

        results = await asyncio.gather(
            run_pro_agent(state),
            run_con_agent(state),
            run_financial_agent(state),
            run_market_agent(state),
            return_exceptions=True,
        )

        updated_state = dict(state)
        for result in results:
            if isinstance(result, dict):
                updated_state.update(result)
            elif isinstance(result, Exception):
                logger.error("specialist_agent_failed", error=str(result))
                errors = updated_state.get("errors", [])
                errors.append(str(result))
                updated_state["errors"] = errors

        return updated_state

    async def _run_judge_wrapper(self, state: DebateState) -> DebateState:
        """Wrapper for judge agent with error context."""
        try:
            return await run_judge_agent(state)
        except Exception as e:
            logger.error("judge_agent_failed", error=str(e))
            raise AgentExecutionException("Judge synthesis failed", "judge_agent")

    async def _run_confidence_wrapper(self, state: DebateState) -> DebateState:
        """Wrapper for confidence scorer with fallback."""
        try:
            return await run_confidence_scorer(state)
        except Exception as e:
            logger.error("confidence_scorer_failed", error=str(e))
            from app.models import ConfidenceOutput
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

    async def execute(self, initial_state: DebateState) -> DebateState:
        """
        Execute the complete debate workflow.

        Args:
            initial_state: Starting state with decision and request_id

        Returns:
            Final state with all agent outputs
        """
        if self._graph is None:
            self._graph = self._build_graph()

        start_time = time.time()
        logger.info("debate_workflow_started", request_id=initial_state.get("request_id"))

        final_state = await self._graph.ainvoke(initial_state)

        duration_ms = int((time.time() - start_time) * 1000)
        logger.info(
            "debate_workflow_completed",
            request_id=initial_state.get("request_id"),
            duration_ms=duration_ms,
            errors_count=len(final_state.get("errors", [])),
        )

        final_state["processing_time_ms"] = duration_ms
        return final_state


# Singleton instance
_debate_service = None


def get_debate_service() -> DebateGraphService:
    """Get or create debate service singleton."""
    global _debate_service
    if _debate_service is None:
        _debate_service = DebateGraphService()
    return _debate_service
