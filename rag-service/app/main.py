"""
FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="RAG Course Platform API",
    description="API for RAG-powered course assistant",
    version="1.0.0"
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
    return {"message": "RAG Course Platform API"}

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "services": {
            "api": "ok"
        },
        "version": "1.0.0"
    }

