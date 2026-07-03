"""
Strategic Decision Intelligence Platform - FastAPI Application.

Production-grade API with comprehensive middleware, error handling,
observability, and rate limiting.
"""

import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import configure_logging, get_logger
from app.core.exceptions import (
    ApplicationException,
    ValidationException,
    LLMProviderException,
)
from app.models import (
    DebateRequest,
    DebateResponse,
    HealthCheckResponse,
    ErrorResponse,
    FinancialSummary,
)
from app.state import DebateState
from app.services.graph_service import get_debate_service

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    configure_logging()
    logger.info(
        "application_startup",
        version=settings.app_version,
        environment=settings.environment,
    )

    # Validate critical configuration
    try:
        _ = settings.llm_api_key
        logger.info("configuration_validated")
    except Exception as e:
        logger.critical("configuration_validation_failed", error=str(e))
        raise

    yield

    logger.info("application_shutdown")


app = FastAPI(
    title="Strategic Decision Intelligence Platform",
    description="""
    Enterprise-grade multi-agent AI system for strategic business decision analysis.

    ## Features

    - **Multi-Agent Debate**: 6 specialized AI agents analyze decisions from multiple perspectives
    - **Parallel Execution**: Specialist agents run concurrently for optimal performance
    - **Structured Output**: Confidence scores, financial projections, and risk assessments
    - **Production Ready**: Rate limiting, observability, and comprehensive error handling

    ## Decision Flow

    1. **Input Validation**: Decision text validated for quality and completeness
    2. **Parallel Analysis**: Pro, Con, Financial, and Market agents execute simultaneously
    3. **Executive Synthesis**: Judge agent weighs all inputs and produces recommendation
    4. **Confidence Scoring**: Multi-factor confidence calculation with risk adjustment
    5. **Structured Response**: Complete analysis with actionable insights
    """,
    version=settings.app_version,
    docs_url="/docs" if not settings.is_production() else None,
    redoc_url="/redoc" if not settings.is_production() else None,
    lifespan=lifespan,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins_list(),
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Exception Handlers
@app.exception_handler(ApplicationException)
async def application_exception_handler(request: Request, exc: ApplicationException):
    """Handle application-specific exceptions."""
    logger.error(
        "application_error",
        error_code=exc.error_code,
        message=exc.message,
        path=request.url.path,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error_code=exc.error_code,
            message=exc.message,
            details=exc.details,
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
    logger.exception("unhandled_exception", request_id=request_id, path=request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error_code="INTERNAL_ERROR",
            message="An unexpected error occurred. Please try again later.",
            request_id=request_id,
        ).model_dump(),
    )


# Request ID Middleware
@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    """Attach unique request ID to each request."""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


# Routes
@app.get("/", include_in_schema=False)
async def root():
    """Root redirect to API documentation."""
    return {
        "service": "Strategic Decision Intelligence Platform",
        "version": settings.app_version,
        "documentation": "/docs",
        "health": "/health",
    }


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """System health check endpoint."""
    return HealthCheckResponse(
        status="healthy",
        version=settings.app_version,
        environment=settings.environment,
        dependencies={
            "llm_provider": settings.llm_provider,
            "llm_model": settings.llm_model,
        },
    )


@app.post("/api/v1/debate", response_model=DebateResponse)
async def run_debate(request: DebateRequest, req: Request):
    """
    Execute strategic decision analysis.

    Orchestrates multiple AI agents to analyze a strategic business decision
    from multiple perspectives and produce a comprehensive recommendation.

    - **decision**: Complete strategic question (20-1000 characters)
    - **industry_context**: Optional industry for targeted analysis
    """
    request_id = req.state.request_id
    logger.info(
        "debate_request_received",
        request_id=request_id,
        decision_preview=request.decision[:100],
    )

    # Initialize state
    initial_state: DebateState = {
        "decision": request.decision,
        "industry_context": request.industry_context,
        "request_id": request_id,
        "pro_output": None,
        "con_output": None,
        "financial_output": None,
        "market_output": None,
        "judge_output": None,
        "confidence_output": None,
        "agent_statuses": {},
        "errors": [],
        "started_at": None,
        "completed_at": None,
    }

    # Execute workflow
    service = get_debate_service()
    final_state = await service.execute(initial_state)

    # Validate outputs
    if not final_state.get("judge_output"):
        raise LLMProviderException("Judge output missing from final state")

    if not final_state.get("confidence_output"):
        raise LLMProviderException("Confidence output missing from final state")

    judge = final_state["judge_output"]
    confidence = final_state["confidence_output"]
    financial = final_state.get("financial_output")

    # Build response
    response = DebateResponse(
        request_id=request_id,
        decision=judge.final_decision,
        confidence_score=confidence.score,
        opportunities=judge.key_opportunities,
        risks=judge.key_risks,
        financial_summary=FinancialSummary(
            investment_required=financial.estimated_investment if financial else "Not analyzed",
            roi_projection=financial.roi_projection if financial else "Not analyzed",
            breakeven_timeline=financial.breakeven_timeline if financial else "Not analyzed",
            uncertainty_level=financial.uncertainty_level if financial else "high",
            key_financial_risks=financial.financial_risks if financial else [],
        ),
        reasoning_summary=judge.reasoning,
        conditions=judge.conditions,
        consensus_level=judge.consensus_level,
        priority_actions=judge.priority_actions,
        processing_time_ms=final_state.get("processing_time_ms"),
    )

    logger.info(
        "debate_response_generated",
        request_id=request_id,
        decision=response.decision,
        confidence=response.confidence_score,
        duration_ms=response.processing_time_ms,
    )

    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        workers=settings.api_workers,
        log_level=settings.log_level.lower(),
    )
