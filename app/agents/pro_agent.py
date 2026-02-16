"""
Pro Agent - Argues in favor of the strategic decision.
"""
import logging
from app.models import ProAgentOutput
from app.utils.llm import get_llm, invoke_agent_with_retry, format_agent_context

logger = logging.getLogger(__name__)

PRO_AGENT_PROMPT = """You are a strategic advocate tasked with making the strongest possible case FOR the following business decision.

{context}

Your role:
- Identify compelling arguments in favor of this decision
- Highlight strategic opportunities and competitive advantages
- Outline success factors and enabling conditions
- Be persuasive but grounded in business reality
- Focus on growth, innovation, and competitive positioning

You must respond ONLY with valid JSON matching this exact structure:
{{
    "arguments": ["argument1", "argument2", "argument3"],
    "opportunities": ["opportunity1", "opportunity2", "opportunity3"],
    "strategic_benefits": ["benefit1", "benefit2", "benefit3"],
    "success_factors": ["factor1", "factor2", "factor3"]
}}

Provide 3-5 items for each list. Be specific and actionable.

Respond with JSON only, no additional text."""


async def run_pro_agent(state: dict) -> dict:
    """
    Execute Pro Agent analysis.
    
    Args:
        state: Current debate state
        
    Returns:
        Updated state with pro_output
    """
    logger.info("Running Pro Agent...")
    
    try:
        llm = get_llm(temperature=0.7)
        context = format_agent_context(state, "Pro")
        prompt = PRO_AGENT_PROMPT.format(context=context)
        
        output = await invoke_agent_with_retry(llm, prompt, ProAgentOutput)
        
        logger.info(f"Pro Agent completed with {len(output.arguments)} arguments")
        return {"pro_output": output}
        
    except Exception as e:
        logger.error(f"Pro Agent failed: {e}")
        errors = state.get('errors', [])
        errors.append(f"Pro Agent error: {str(e)}")
        return {"errors": errors}
