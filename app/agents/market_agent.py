"""
Market Agent - Analyzes market dynamics, competition, and regulatory landscape.
"""
import logging
from app.models import MarketAgentOutput
from app.utils.llm import get_llm, invoke_agent_with_retry, format_agent_context

logger = logging.getLogger(__name__)

MARKET_AGENT_PROMPT = """You are a market research analyst evaluating the market landscape for the following business decision.

{context}

Your role:
- Assess market size and growth potential
- Analyze competitive landscape and positioning
- Identify regulatory and compliance concerns
- Evaluate market trends and dynamics
- Highlight entry barriers and macro risks

You must respond ONLY with valid JSON matching this exact structure:
{{
    "market_size": "Market size estimate with supporting rationale",
    "competition_analysis": "Competitive landscape overview",
    "regulatory_concerns": ["concern1", "concern2", "concern3"],
    "market_trends": ["trend1", "trend2", "trend3"],
    "entry_barriers": ["barrier1", "barrier2", "barrier3"],
    "macro_risks": ["risk1", "risk2", "risk3"]
}}

Provide 3-5 items for each list. Consider both opportunities and threats in the market.

Respond with JSON only, no additional text."""


async def run_market_agent(state: dict) -> dict:
    """
    Execute Market Agent analysis.
    
    Args:
        state: Current debate state
        
    Returns:
        Updated state with market_output
    """
    logger.info("Running Market Agent...")
    
    try:
        llm = get_llm(temperature=0.6)
        context = format_agent_context(state, "Market")
        prompt = MARKET_AGENT_PROMPT.format(context=context)
        
        output = await invoke_agent_with_retry(llm, prompt, MarketAgentOutput)
        
        logger.info(f"Market Agent completed with {len(output.macro_risks)} macro risks identified")
        return {"market_output": output}
        
    except Exception as e:
        logger.error(f"Market Agent failed: {e}")
        errors = state.get('errors', [])
        errors.append(f"Market Agent error: {str(e)}")
        return {"errors": errors}
