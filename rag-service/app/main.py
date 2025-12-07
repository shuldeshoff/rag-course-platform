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
from app.services.qdrant_service import qdrant_service
from app.services.yandex_service import yandex_service
from app.database.db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("🚀 Initializing RAG Course Platform...")
    init_db()
    print("✅ Database initialized")
    yield
    # Shutdown
    print("👋 Shutting down...")

app = FastAPI(
    title="RAG Course Platform API",
    description="API for RAG-powered course assistant",
    version="1.0.0",
    lifespan=lifespan
)

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
    Ask a question about the course
    Requires Bearer token authentication
    """
    start_time = time.time()
    
    try:
        # Для MVP без RAG - просто отправляем в YandexGPT
        answer = await yandex_service.generate(request.question)
        
        response_time = int((time.time() - start_time) * 1000)
        
        return AskResponse(
            status="success",
            answer=answer,
            chunks_used=[],
            response_time_ms=response_time
        )
    
    except Exception as e:
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

