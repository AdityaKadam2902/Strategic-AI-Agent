"""
Confidence Scorer - Calculates confidence score based on debate analysis.
"""
import logging
from app.models import ConfidenceOutput
from app.utils.llm import get_llm, invoke_agent_with_retry

logger = logging.getLogger(__name__)

CONFIDENCE_PROMPT = """You are a confidence assessment system analyzing a strategic decision debate.

Decision: {decision}

Judge's Final Decision: {final_decision}
Consensus Level: {consensus_level}
Number of Key Opportunities: {num_opportunities}
Number of Key Risks: {num_risks}
Financial Uncertainty: {financial_uncertainty}
Number of Regulatory Concerns: {num_regulatory}
Number of Alternative Options Suggested: {num_alternatives}

Your task is to calculate a confidence score (0-100) for this decision based on:

1. **Consensus Level** (30 points max):
   - high consensus = 30 points
   - medium consensus = 20 points
   - low consensus = 10 points

2. **Risk vs Opportunity Balance** (25 points max):
   - More opportunities than risks = 25 points
   - Equal opportunities and risks = 15 points
   - More risks than opportunities = 5 points

3. **Financial Certainty** (25 points max):
   - low uncertainty = 25 points
   - medium uncertainty = 15 points
   - high uncertainty = 5 points

4. **Regulatory/Market Clarity** (20 points max):
   - 0-2 regulatory concerns = 20 points
   - 3-4 regulatory concerns = 12 points
   - 5+ regulatory concerns = 5 points

Calculate the total score and provide breakdown.

You must respond ONLY with valid JSON matching this exact structure:
{{
    "score": 75,
    "factors": {{
        "consensus": 30,
        "risk_opportunity_balance": 15,
        "financial_certainty": 20,
        "regulatory_clarity": 10
    }},
    "explanation": "Brief explanation of how the score was calculated"
}}

The "score" field must be the sum of all factors and between 0-100.

Respond with JSON only, no additional text."""


async def run_confidence_scorer(state: dict) -> dict:
    """
    Calculate confidence score based on all debate outputs.
    
    Args:
        state: Current debate state with judge output
        
    Returns:
        Updated state with confidence_output
    """
    logger.info("Running Confidence Scorer...")
    
    try:
        judge_output = state.get('judge_output')
        financial_output = state.get('financial_output')
        market_output = state.get('market_output')
        con_output = state.get('con_output')
        
        if not judge_output:
            raise ValueError("Judge output is required for confidence scoring")
        
        # Prepare context for confidence calculation
        context = {
            'decision': state['decision'],
            'final_decision': judge_output.final_decision,
            'consensus_level': judge_output.consensus_level,
            'num_opportunities': len(judge_output.key_opportunities),
            'num_risks': len(judge_output.key_risks),
            'financial_uncertainty': financial_output.uncertainty_level if financial_output else 'high',
            'num_regulatory': len(market_output.regulatory_concerns) if market_output else 0,
            'num_alternatives': len(con_output.alternative_options) if con_output else 0
        }
        
        llm = get_llm(temperature=0.3)  # Low temp for consistent scoring
        prompt = CONFIDENCE_PROMPT.format(**context)
        
        output = await invoke_agent_with_retry(llm, prompt, ConfidenceOutput)
        
        # Validate score is in range
        if not 0 <= output.score <= 100:
            logger.warning(f"Confidence score {output.score} out of range, clamping to 0-100")
            output.score = max(0, min(100, output.score))
        
        logger.info(f"Confidence Scorer completed - Score: {output.score}/100")
        return {"confidence_output": output}
        
    except Exception as e:
        logger.error(f"Confidence Scorer failed: {e}")
        # Provide fallback confidence score
        fallback = ConfidenceOutput(
            score=50,
            factors={
                "consensus": 15,
                "risk_opportunity_balance": 12,
                "financial_certainty": 13,
                "regulatory_clarity": 10
            },
            explanation="Fallback score due to calculation error"
        )
        return {"confidence_output": fallback}
