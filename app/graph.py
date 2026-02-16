"""
LangGraph workflow definition for Strategic Debate Engine.
"""
import logging
from langgraph.graph import StateGraph, END
from app.state import DebateState
from app.agents.pro_agent import run_pro_agent
from app.agents.con_agent import run_con_agent
from app.agents.financial_agent import run_financial_agent
from app.agents.market_agent import run_market_agent
from app.agents.judge_agent import run_judge_agent
from app.agents.confidence import run_confidence_scorer

logger = logging.getLogger(__name__)


async def run_all_specialist_agents(state: DebateState) -> DebateState:
    """
    Run all four specialist agents in parallel.
    
    This function executes Pro, Con, Financial, and Market agents
    concurrently for better performance.
    """
    import asyncio
    
    # Run all agents concurrently
    results = await asyncio.gather(
        run_pro_agent(state),
        run_con_agent(state),
        run_financial_agent(state),
        run_market_agent(state),
        return_exceptions=True
    )
    
    # Merge all results into state
    updated_state = dict(state)
    for result in results:
        if isinstance(result, dict):
            updated_state.update(result)
        elif isinstance(result, Exception):
            logger.error(f"Agent failed: {result}")
            errors = updated_state.get('errors', [])
            errors.append(str(result))
            updated_state['errors'] = errors
    
    return updated_state


def build_debate_graph():
    """
    Build and compile the debate workflow graph.
    
    Workflow:
    1. Entry point receives decision
    2. All four specialist agents run in parallel (via run_all_specialist_agents)
    3. Judge Agent synthesizes all inputs
    4. Confidence Scorer calculates final score
    5. Return final state
    
    Returns:
        Compiled graph ready for execution
    """
    # Initialize graph with state schema
    workflow = StateGraph(DebateState)
    
    # Add nodes
    workflow.add_node("specialist_agents", run_all_specialist_agents)
    workflow.add_node("judge_agent", run_judge_agent)
    workflow.add_node("confidence_scorer", run_confidence_scorer)
    
    # Define workflow
    workflow.set_entry_point("specialist_agents")
    workflow.add_edge("specialist_agents", "judge_agent")
    workflow.add_edge("judge_agent", "confidence_scorer")
    workflow.add_edge("confidence_scorer", END)
    
    # Compile the graph
    app = workflow.compile()
    
    logger.info("Debate graph compiled successfully")
    return app


# Global graph instance
debate_graph = None


def get_debate_graph():
    """Get or create the debate graph instance."""
    global debate_graph
    if debate_graph is None:
        debate_graph = build_debate_graph()
    return debate_graph
