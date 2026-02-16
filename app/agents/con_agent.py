"""
Con Agent - Argues against the strategic decision.
"""
import logging
from app.models import ConAgentOutput
from app.utils.llm import get_llm, invoke_agent_with_retry, format_agent_context

logger = logging.getLogger(__name__)

CON_AGENT_PROMPT = """You are a strategic skeptic tasked with making the strongest possible case AGAINST the following business decision.

{context}

Your role:
- Identify critical risks and potential downsides
- Highlight implementation challenges and resource constraints
- Question assumptions and identify blindspots
- Suggest alternative approaches that might be safer or more effective
- Be critical but constructive - focus on protecting the organization

You must respond ONLY with valid JSON matching this exact structure:
{{
    "arguments": ["argument1", "argument2", "argument3"],
    "risks": ["risk1", "risk2", "risk3"],
    "challenges": ["challenge1", "challenge2", "challenge3"],
    "alternative_options": ["alternative1", "alternative2"]
}}

Provide 3-5 items for each list. Be specific and identify concrete risks.

Respond with JSON only, no additional text."""


async def run_con_agent(state: dict) -> dict:
    """
    Execute Con Agent analysis.
    
    Args:
        state: Current debate state
        
    Returns:
        Updated state with con_output
    """
    logger.info("Running Con Agent...")
    
    try:
        llm = get_llm(temperature=0.7)
        context = format_agent_context(state, "Con")
        prompt = CON_AGENT_PROMPT.format(context=context)
        
        output = await invoke_agent_with_retry(llm, prompt, ConAgentOutput)
        
        logger.info(f"Con Agent completed with {len(output.risks)} risks identified")
        return {"con_output": output}
        
    except Exception as e:
        logger.error(f"Con Agent failed: {e}")
        errors = state.get('errors', [])
        errors.append(f"Con Agent error: {str(e)}")
        return {"errors": errors}
