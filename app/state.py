"""
State management for LangGraph debate workflow.
"""
from typing import Optional
from typing_extensions import TypedDict
from app.models import (
    ProAgentOutput,
    ConAgentOutput,
    FinancialAgentOutput,
    MarketAgentOutput,
    JudgeOutput,
    ConfidenceOutput
)


class DebateState(TypedDict):
    """
    Shared state object passed between all agents in the debate graph.
    
    This state flows through the entire LangGraph workflow and accumulates
    outputs from each agent.
    """
    # Input
    decision: str
    
    # Agent outputs
    pro_output: Optional[ProAgentOutput]
    con_output: Optional[ConAgentOutput]
    financial_output: Optional[FinancialAgentOutput]
    market_output: Optional[MarketAgentOutput]
    judge_output: Optional[JudgeOutput]
    confidence_output: Optional[ConfidenceOutput]
    
    # Error tracking
    errors: Optional[list]
