"""
Unit tests for domain models.
"""

import pytest
from pydantic import ValidationError

from app.models import DebateRequest, DebateResponse, DecisionVerdict


class TestDebateRequest:
    """Test cases for DebateRequest model."""

    def test_valid_request(self):
        """Test valid debate request creation."""
        request = DebateRequest(
            decision="Should we invest $2M in cloud infrastructure expansion?"
        )
        assert request.decision == "Should we invest $2M in cloud infrastructure expansion?"

    def test_decision_too_short(self):
        """Test validation rejects short decisions."""
        with pytest.raises(ValidationError) as exc_info:
            DebateRequest(decision="Short?")
        assert "min_length" in str(exc_info.value)

    def test_decision_no_punctuation(self):
        """Test validation requires proper punctuation."""
        with pytest.raises(ValidationError) as exc_info:
            DebateRequest(decision="This is a decision without punctuation")
        assert "punctuation" in str(exc_info.value).lower()

    def test_industry_context_optional(self):
        """Test industry context is optional."""
        request = DebateRequest(
            decision="Should we expand to European markets?",
            industry_context="SaaS"
        )
        assert request.industry_context == "SaaS"


class TestDebateResponse:
    """Test cases for DebateResponse model."""

    def test_valid_response(self):
        """Test valid debate response creation."""
        from app.models import FinancialSummary

        response = DebateResponse(
            request_id="test-123",
            decision=DecisionVerdict.PROCEED,
            confidence_score=75,
            opportunities=["Opportunity 1"],
            risks=["Risk 1"],
            financial_summary=FinancialSummary(
                investment_required="$1M",
                roi_projection="150% over 3 years",
                breakeven_timeline="18 months",
                uncertainty_level="medium",
            ),
            reasoning_summary="This is a well-reasoned decision based on market analysis.",
            consensus_level="high",
        )
        assert response.confidence_score == 75

    def test_confidence_score_range(self):
        """Test confidence score must be 0-100."""
        from app.models import FinancialSummary

        with pytest.raises(ValidationError):
            DebateResponse(
                request_id="test-123",
                decision=DecisionVerdict.PROCEED,
                confidence_score=150,
                opportunities=["Opp"],
                risks=["Risk"],
                financial_summary=FinancialSummary(
                    investment_required="$1M",
                    roi_projection="150%",
                    breakeven_timeline="18 months",
                    uncertainty_level="medium",
                ),
                reasoning_summary="Test reasoning.",
                consensus_level="high",
            )
