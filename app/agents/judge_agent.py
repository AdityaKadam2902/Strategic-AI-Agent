"""
Judge Agent - Synthesizes all arguments and produces final verdict.
"""
import logging
from app.models import JudgeOutput
from app.utils.llm import get_llm, invoke_agent_with_retry, format_agent_context

logger = logging.getLogger(__name__)

JUDGE_AGENT_PROMPT = """You are an executive decision-maker synthesizing arguments from multiple advisors to reach a final strategic verdict.

{context}

You have received input from:
1. Pro advocate (arguments FOR the decision)
2. Con skeptic (arguments AGAINST the decision)
3. Financial analyst (economic implications)
4. Market analyst (competitive and regulatory landscape)

Your role:
- Weigh all arguments objectively
- Identify the most critical opportunities and risks (top 3-5 each)
- Make a clear final decision: "Proceed", "Proceed with conditions", or "Do not proceed"
- If "Proceed with conditions", specify what those conditions are
- Assess the level of consensus among the advisors
- Provide concise executive reasoning (2-3 paragraphs maximum)

You must respond ONLY with valid JSON matching this exact structure:
{{
    "final_decision": "Proceed OR Proceed with conditions OR Do not proceed",
    "key_opportunities": ["opportunity1", "opportunity2", "opportunity3"],
    "key_risks": ["risk1", "risk2", "risk3"],
    "conditions": ["condition1", "condition2"],
    "reasoning": "Executive summary explaining the decision and key factors",
    "consensus_level": "high OR medium OR low"
}}

For final_decision, use EXACTLY one of: "Proceed", "Proceed with conditions", "Do not proceed"
For consensus_level, use ONLY: "high", "medium", or "low"
If final_decision is NOT "Proceed with conditions", set conditions to empty array []

Be decisive and concise. Focus on what matters most.

Respond with JSON only, no additional text."""


async def run_judge_agent(state: dict) -> dict:
    """
    Execute Judge Agent synthesis and decision.
    
    Args:
        state: Current debate state with all agent outputs
        
    Returns:
        Updated state with judge_output
    """
    logger.info("Running Judge Agent...")
    
    try:
        llm = get_llm(temperature=0.5)  # Lower temp for more consistent decisions
        context = format_agent_context(state, "Judge")
        prompt = JUDGE_AGENT_PROMPT.format(context=context)
        
        output = await invoke_agent_with_retry(llm, prompt, JudgeOutput)
        
        logger.info(f"Judge Agent decision: {output.final_decision} (Consensus: {output.consensus_level})")
        return {"judge_output": output}
        
    except Exception as e:
        logger.error(f"Judge Agent failed: {e}")
        errors = state.get('errors', [])
        errors.append(f"Judge Agent error: {str(e)}")
        return {"errors": errors}
