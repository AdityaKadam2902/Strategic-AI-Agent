"""
Pydantic models for request/response schemas and agent outputs.
"""
from typing import List, Dict, Optional
from pydantic import BaseModel, Field


# ============================================================================
# API Request/Response Models
# ============================================================================

class DebateRequest(BaseModel):
    """Request model for debate endpoint."""
    decision: str = Field(
        ...,
        description="The strategic decision to debate",
        min_length=10,
        max_length=500
    )


class DebateResponse(BaseModel):
    """Response model for debate endpoint."""
    decision: str = Field(..., description="Final decision verdict")
    confidence_score: int = Field(..., description="Confidence score 0-100", ge=0, le=100)
    opportunities: List[str] = Field(..., description="List of opportunities identified")
    risks: List[str] = Field(..., description="List of risks identified")
    financial_summary: Dict[str, str] = Field(..., description="Financial analysis summary")
    reasoning_summary: str = Field(..., description="Executive summary of reasoning")


# Agent Output Models

class ProAgentOutput(BaseModel):
    """Structured output from Pro Agent."""
    arguments: List[str] = Field(..., description="Arguments in favor of the decision")
    opportunities: List[str] = Field(..., description="Opportunities identified")
    strategic_benefits: List[str] = Field(..., description="Strategic benefits")
    success_factors: List[str] = Field(..., description="Key success factors")


class ConAgentOutput(BaseModel):
    """Structured output from Con Agent."""
    arguments: List[str] = Field(..., description="Arguments against the decision")
    risks: List[str] = Field(..., description="Risks identified")
    challenges: List[str] = Field(..., description="Implementation challenges")
    alternative_options: List[str] = Field(..., description="Alternative approaches")


class FinancialAgentOutput(BaseModel):
    """Structured output from Financial Agent."""
    estimated_investment: str = Field(..., description="Estimated initial investment required")
    roi_projection: str = Field(..., description="ROI projection timeline")
    revenue_impact: str = Field(..., description="Expected revenue impact")
    cost_structure: str = Field(..., description="Cost structure breakdown")
    financial_risks: List[str] = Field(..., description="Financial risks")
    breakeven_timeline: str = Field(..., description="Estimated breakeven timeline")
    uncertainty_level: str = Field(..., description="Financial uncertainty level: low/medium/high")


class MarketAgentOutput(BaseModel):
    """Structured output from Market Agent."""
    market_size: str = Field(..., description="Target market size estimate")
    competition_analysis: str = Field(..., description="Competitive landscape")
    regulatory_concerns: List[str] = Field(..., description="Regulatory and compliance concerns")
    market_trends: List[str] = Field(..., description="Relevant market trends")
    entry_barriers: List[str] = Field(..., description="Market entry barriers")
    macro_risks: List[str] = Field(..., description="Macroeconomic risks")


class JudgeOutput(BaseModel):
    """Structured output from Judge Agent."""
    final_decision: str = Field(
        ..., 
        description="Final verdict: 'Proceed', 'Proceed with conditions', or 'Do not proceed'"
    )
    key_opportunities: List[str] = Field(..., description="Top 3-5 opportunities")
    key_risks: List[str] = Field(..., description="Top 3-5 risks")
    conditions: List[str] = Field(default_factory=list, description="Conditions if applicable")
    reasoning: str = Field(..., description="Concise executive summary of reasoning")
    consensus_level: str = Field(
        ..., 
        description="Level of consensus among agents: high/medium/low"
    )


class ConfidenceOutput(BaseModel):
    """Structured output from Confidence Scorer."""
    score: int = Field(..., description="Confidence score 0-100", ge=0, le=100)
    factors: Dict[str, int] = Field(..., description="Score breakdown by factor")
    explanation: str = Field(..., description="Explanation of confidence calculation")
