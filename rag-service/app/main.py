"""
FastAPI application entry point
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import time

from app.models.request import AskRequest
from app.models.response import AskResponse, HealthResponse, ErrorResponse
from app.api.auth import verify_token
from app.api.admin import router as admin_router
from app.services.qdrant_service import qdrant_service
from app.services.yandex_service import yandex_service
from app.services.rag_pipeline import rag_pipeline
from app.database.db import init_db
from app.utils.rate_limiter import rate_limit_user
from app.utils.cache import cache_service
from app.utils.logger import get_logger

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("startup", message="Initializing RAG Course Platform")
    init_db()
    logger.info("startup", message="Database initialized")
    yield
    # Shutdown
    logger.info("shutdown", message="Shutting down")

app = FastAPI(
    title="RAG Course Platform API",
    description="API for RAG-powered course assistant",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(admin_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "RAG Course Platform API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "ask": "/ask (POST, requires auth)",
            "docs": "/docs"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    services = {
        "api": "ok",
        "qdrant": "ok" if qdrant_service.check_health() else "error",
        "postgres": "ok"
    }
    
    # Check YandexGPT only if configured
    if yandex_service.api_key:
        yandex_ok = await yandex_service.check_health()
        services["yandex_gpt"] = "ok" if yandex_ok else "error"
    else:
        services["yandex_gpt"] = "not_configured"
    
    return HealthResponse(
        status="healthy",
        services=services,
        version="1.0.0"
    )

@app.post("/ask", response_model=AskResponse)
async def ask_question(
    request: AskRequest,
    token: str = Depends(verify_token)
):
    """
    Ask a question about the course using RAG pipeline
    Requires Bearer token authentication
    Rate limited per user
    """
    # Rate limiting
    await rate_limit_user(None, request.user_id)
    
    # Check cache
    cached = cache_service.get_answer_cache(request.question, request.course_id)
    if cached:
        logger.info(
            "cache_hit",
            user_id=request.user_id,
            course_id=request.course_id
        )
        return AskResponse(**cached)
    
    try:
        logger.info(
            "ask_question",
            user_id=request.user_id,
            course_id=request.course_id,
            question_length=len(request.question)
        )
        
        # Use full RAG pipeline
        answer, chunks, response_time_ms = await rag_pipeline.process(
            question=request.question,
            course_id=request.course_id,
            top_k=5
        )
        
        result = {
            "status": "success",
            "answer": answer,
            "chunks_used": chunks,
            "response_time_ms": response_time_ms
        }
        
        # Cache result
        cache_service.set_answer_cache(request.question, request.course_id, result)
        
        logger.info(
            "ask_success",
            user_id=request.user_id,
            course_id=request.course_id,
            response_time_ms=response_time_ms,
            chunks_count=len(chunks)
        )
        
        return AskResponse(**result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "ask_error",
            user_id=request.user_id,
            course_id=request.course_id,
            error=str(e)
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test-qdrant")
async def test_qdrant():
    """Test Qdrant connection"""
    try:
        collections = qdrant_service.client.get_collections()
        return {
            "status": "ok",
            "collections": [c.name for c in collections.collections]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/test-yandex")
async def test_yandex():
    """Test YandexGPT connection"""
    try:
        result = await yandex_service.generate("Скажи привет")
        return {"status": "ok", "response": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

