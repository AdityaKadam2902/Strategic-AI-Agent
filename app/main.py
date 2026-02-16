"""
FastAPI application for Strategic Debate Engine.
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings, validate_config
from app.models import DebateRequest, DebateResponse
from app.graph import get_debate_graph
from app.state import DebateState

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    # Startup
    logger.info("Starting Strategic Debate Engine...")
    try:
        validate_config()
        logger.info(f"Configuration validated - Model: {settings.groq_model}")
        # Pre-compile the graph
        get_debate_graph()
        logger.info("Debate graph pre-compiled and ready")
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Strategic Debate Engine...")


# Initialize FastAPI app
app = FastAPI(
    title="Strategic Debate Engine",
    description="Multi-agent AI system for strategic business decision analysis",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "Strategic Debate Engine",
        "version": "1.0.0",
        "status": "operational",
        "model": settings.groq_model,
        "endpoints": {
            "debate": "POST /debate",
            "health": "GET /health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model": settings.groq_model,
        "service": "Strategic Debate Engine"
    }


@app.post("/debate", response_model=DebateResponse)
async def run_debate(request: DebateRequest):
    """
    Run a strategic debate on a business decision.
    
    This endpoint orchestrates multiple AI agents to analyze a strategic
    decision from different perspectives and produce a comprehensive verdict
    with confidence scoring.
    
    Args:
        request: DebateRequest containing the decision to analyze
        
    Returns:
        DebateResponse with final decision, confidence score, and analysis
        
    Raises:
        HTTPException: If the debate process fails
    """
    logger.info(f"Starting debate for decision: {request.decision[:100]}...")
    
    try:
        # Initialize state
        initial_state: DebateState = {
            "decision": request.decision,
            "pro_output": None,
            "con_output": None,
            "financial_output": None,
            "market_output": None,
            "judge_output": None,
            "confidence_output": None,
            "errors": []
        }
        
        # Get debate graph
        graph = get_debate_graph()
        
        # Execute the debate workflow
        logger.info("Executing debate graph...")
        final_state = await graph.ainvoke(initial_state)
        
        # Check for errors
        if final_state.get('errors'):
            logger.warning(f"Debate completed with errors: {final_state['errors']}")
        
        # Validate we have required outputs
        if not final_state.get('judge_output'):
            raise ValueError("Judge output missing from final state")
        
        if not final_state.get('confidence_output'):
            raise ValueError("Confidence output missing from final state")
        
        judge_output = final_state['judge_output']
        confidence_output = final_state['confidence_output']
        financial_output = final_state.get('financial_output')
        
        # Construct response
        response = DebateResponse(
            decision=judge_output.final_decision,
            confidence_score=confidence_output.score,
            opportunities=judge_output.key_opportunities,
            risks=judge_output.key_risks,
            financial_summary={
                "investment": financial_output.estimated_investment if financial_output else "Not analyzed",
                "roi_projection": financial_output.roi_projection if financial_output else "Not analyzed",
                "breakeven": financial_output.breakeven_timeline if financial_output else "Not analyzed",
                "uncertainty": financial_output.uncertainty_level if financial_output else "high"
            },
            reasoning_summary=judge_output.reasoning
        )
        
        logger.info(f"Debate completed - Decision: {response.decision}, Confidence: {response.confidence_score}%")
        return response
        
    except Exception as e:
        logger.error(f"Debate failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Debate process failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level=settings.log_level.lower()
    )
