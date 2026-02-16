"""
Financial Agent - Analyzes financial implications, costs, and ROI.
"""
import logging
from app.models import FinancialAgentOutput
from app.utils.llm import get_llm, invoke_agent_with_retry, format_agent_context

logger = logging.getLogger(__name__)

FINANCIAL_AGENT_PROMPT = """You are a financial analyst evaluating the economic implications of the following business decision.

{context}

Your role:
- Estimate investment requirements and cost structure
- Project ROI and revenue impact
- Identify financial risks and uncertainty factors
- Provide breakeven timeline estimates
- Assess overall financial viability

You must respond ONLY with valid JSON matching this exact structure:
{{
    "estimated_investment": "Estimated range or specific amount with reasoning",
    "roi_projection": "Expected ROI timeline and percentage estimates",
    "revenue_impact": "Projected revenue impact over time",
    "cost_structure": "Breakdown of major cost categories",
    "financial_risks": ["risk1", "risk2", "risk3"],
    "breakeven_timeline": "Estimated time to breakeven",
    "uncertainty_level": "low or medium or high"
}}

Be realistic with estimates. For uncertainty_level, use ONLY: "low", "medium", or "high".
Provide 3-5 financial risks.

Respond with JSON only, no additional text."""


async def run_financial_agent(state: dict) -> dict:
    """
    Execute Financial Agent analysis.
    
    Args:
        state: Current debate state
        
    Returns:
        Updated state with financial_output
    """
    logger.info("Running Financial Agent...")
    
    try:
        llm = get_llm(temperature=0.6)  # Slightly lower temp for financial analysis
        context = format_agent_context(state, "Financial")
        prompt = FINANCIAL_AGENT_PROMPT.format(context=context)
        
        output = await invoke_agent_with_retry(llm, prompt, FinancialAgentOutput)
        
        logger.info(f"Financial Agent completed - Uncertainty: {output.uncertainty_level}")
        return {"financial_output": output}
        
    except Exception as e:
        logger.error(f"Financial Agent failed: {e}")
        errors = state.get('errors', [])
        errors.append(f"Financial Agent error: {str(e)}")
        return {"errors": errors}
