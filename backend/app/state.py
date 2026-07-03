"""
State Management for LangGraph Debate Workflow.

Defines the typed state dictionary that flows through the multi-agent
orchestration graph, ensuring type safety across agent boundaries.
"""

from typing import Optional, TypedDict, List

from app.models import (
    ProAgentOutput,
    ConAgentOutput,
    FinancialAgentOutput,
    MarketAgentOutput,
    JudgeOutput,
    ConfidenceOutput,
    AgentStatus,
)


class AgentExecutionState(TypedDict, total=False):
    """Individual agent execution tracking."""
    status: AgentStatus
    started_at: Optional[str]
    completed_at: Optional[str]
    error_message: Optional[str]


class DebateState(TypedDict):
    """
    Shared state object passed between all agents in the debate graph.

    This immutable-style state flows through the entire LangGraph workflow
    and accumulates outputs from each agent. Each agent receives the full
    state and returns a partial update.
    """
    # Input
    decision: str
    industry_context: Optional[str]
    request_id: str

    # Agent outputs
    pro_output: Optional[ProAgentOutput]
    con_output: Optional[ConAgentOutput]
    financial_output: Optional[FinancialAgentOutput]
    market_output: Optional[MarketAgentOutput]
    judge_output: Optional[JudgeOutput]
    confidence_output: Optional[ConfidenceOutput]

    # Execution tracking
    agent_statuses: dict[str, AgentExecutionState]
    errors: List[str]
    started_at: Optional[str]
    completed_at: Optional[str]
