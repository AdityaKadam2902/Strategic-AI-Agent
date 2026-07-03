"""
Domain Models and Data Transfer Objects.

Implements the domain model layer using Pydantic v2 for strict
validation, serialization, and OpenAPI schema generation.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


# ============================================================================
# Enums
# ============================================================================

class DecisionVerdict(str, Enum):
    """Standardized decision outcomes."""
    PROCEED = "Proceed"
    PROCEED_WITH_CONDITIONS = "Proceed with Conditions"
    DO_NOT_PROCEED = "Do Not Proceed"


class ConsensusLevel(str, Enum):
    """Consensus classification among advisory agents."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class UncertaintyLevel(str, Enum):
    """Financial uncertainty classification."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class AgentStatus(str, Enum):
    """Agent execution status tracking."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


# ============================================================================
# API Request/Response Models
# ============================================================================

class DebateRequest(BaseModel):
    """Request model for strategic decision analysis.

    Validates input decision text with length constraints
    to prevent abuse and ensure quality input.
    """
    decision: str = Field(
        ...,
        min_length=20,
        max_length=1000,
        description="Strategic business decision to analyze. Must be a complete, actionable question.",
        examples=["Should we invest $2M in expanding our cloud infrastructure to support enterprise clients?"],
    )

    industry_context: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Optional industry context for more targeted analysis (e.g., 'SaaS', 'Fintech', 'Healthcare')",
    )

    @field_validator("decision")
    @classmethod
    def validate_decision_quality(cls, v: str) -> str:
        """Ensure decision text contains a question or directive."""
        v = v.strip()
        if not any(v.endswith(p) for p in ["?", ".", "!"]):
            raise ValueError("Decision must end with proper punctuation")
        if len(v.split()) < 5:
            raise ValueError("Decision must contain at least 5 words for meaningful analysis")
        return v


class DebateResponse(BaseModel):
    """Response model containing complete strategic analysis.

    Provides structured output with decision verdict, confidence metrics,
    and comprehensive analysis suitable for executive review.
    """
    request_id: str = Field(
        ...,
        description="Unique identifier for this analysis request",
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="UTC timestamp of analysis completion",
    )
    decision: DecisionVerdict = Field(
        ...,
        description="Final strategic recommendation",
    )
    confidence_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Overall confidence score (0-100) based on multi-factor analysis",
    )
    opportunities: List[str] = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Identified strategic opportunities ranked by impact",
    )
    risks: List[str] = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Identified strategic risks ranked by severity",
    )
    financial_summary: "FinancialSummary" = Field(
        ...,
        description="Consolidated financial analysis summary",
    )
    reasoning_summary: str = Field(
        ...,
        min_length=50,
        max_length=2000,
        description="Executive summary of reasoning and key factors",
    )
    conditions: List[str] = Field(
        default_factory=list,
        description="Required conditions if decision is 'Proceed with Conditions'",
    )
    consensus_level: ConsensusLevel = Field(
        ...,
        description="Level of consensus among advisory agents",
    )
    agent_execution_status: Dict[str, AgentStatus] = Field(
        default_factory=dict,
        description="Status of each agent in the analysis pipeline",
    )
    processing_time_ms: Optional[int] = Field(
        default=None,
        description="Total processing time in milliseconds",
    )


class FinancialSummary(BaseModel):
    """Consolidated financial analysis output."""
    investment_required: str = Field(
        ...,
        description="Estimated initial investment with rationale",
    )
    roi_projection: str = Field(
        ...,
        description="Projected return on investment timeline and percentage",
    )
    breakeven_timeline: str = Field(
        ...,
        description="Estimated time to break even",
    )
    uncertainty_level: UncertaintyLevel = Field(
        ...,
        description="Financial uncertainty classification",
    )
    key_financial_risks: List[str] = Field(
        default_factory=list,
        max_length=5,
        description="Top financial risks identified",
    )


class HealthCheckResponse(BaseModel):
    """System health check response."""
    status: str = Field(default="healthy")
    version: str = Field(...)
    environment: str = Field(...)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    dependencies: Dict[str, str] = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    """Standardized error response format."""
    error_code: str = Field(...)
    message: str = Field(...)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = Field(default=None)
    details: Optional[Dict[str, Any]] = Field(default=None)


# ============================================================================
# Agent Output Models (Internal)
# ============================================================================

class ProAgentOutput(BaseModel):
    """Output from the Proposition (Pro) Agent."""
    arguments: List[str] = Field(..., min_length=1, max_length=8)
    opportunities: List[str] = Field(..., min_length=1, max_length=8)
    strategic_benefits: List[str] = Field(..., min_length=1, max_length=8)
    success_factors: List[str] = Field(..., min_length=1, max_length=8)
    competitive_advantages: List[str] = Field(default_factory=list, max_length=5)


class ConAgentOutput(BaseModel):
    """Output from the Opposition (Con) Agent."""
    arguments: List[str] = Field(..., min_length=1, max_length=8)
    risks: List[str] = Field(..., min_length=1, max_length=8)
    challenges: List[str] = Field(..., min_length=1, max_length=8)
    alternative_options: List[str] = Field(..., min_length=1, max_length=5)
    mitigation_strategies: List[str] = Field(default_factory=list, max_length=5)


class FinancialAgentOutput(BaseModel):
    """Output from the Financial Analysis Agent."""
    estimated_investment: str = Field(..., max_length=500)
    roi_projection: str = Field(..., max_length=500)
    revenue_impact: str = Field(..., max_length=500)
    cost_structure: str = Field(..., max_length=500)
    financial_risks: List[str] = Field(..., min_length=1, max_length=6)
    breakeven_timeline: str = Field(..., max_length=200)
    uncertainty_level: UncertaintyLevel = Field(...)
    cash_flow_impact: Optional[str] = Field(default=None, max_length=500)


class MarketAgentOutput(BaseModel):
    """Output from the Market Intelligence Agent."""
    market_size: str = Field(..., max_length=500)
    competition_analysis: str = Field(..., max_length=1000)
    regulatory_concerns: List[str] = Field(..., min_length=0, max_length=8)
    market_trends: List[str] = Field(..., min_length=1, max_length=8)
    entry_barriers: List[str] = Field(..., min_length=1, max_length=6)
    macro_risks: List[str] = Field(..., min_length=1, max_length=6)
    customer_demand_signal: Optional[str] = Field(default=None, max_length=500)


class JudgeOutput(BaseModel):
    """Output from the Executive Judge Agent."""
    final_decision: DecisionVerdict = Field(...)
    key_opportunities: List[str] = Field(..., min_length=1, max_length=6)
    key_risks: List[str] = Field(..., min_length=1, max_length=6)
    conditions: List[str] = Field(default_factory=list, max_length=6)
    reasoning: str = Field(..., min_length=50, max_length=1500)
    consensus_level: ConsensusLevel = Field(...)
    priority_actions: List[str] = Field(default_factory=list, max_length=5)


class ConfidenceOutput(BaseModel):
    """Output from the Confidence Scoring Engine."""
    score: int = Field(..., ge=0, le=100)
    factors: Dict[str, int] = Field(...)
    explanation: str = Field(..., max_length=1000)
    risk_adjusted_score: Optional[int] = Field(default=None, ge=0, le=100)


# Update forward references
DebateResponse.model_rebuild()
