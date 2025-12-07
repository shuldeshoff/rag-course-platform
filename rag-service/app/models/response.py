"""
Response models
"""
from pydantic import BaseModel
from typing import List, Optional

class Chunk(BaseModel):
    content: str
    score: float
    source: str
    metadata: dict = {}

class AskResponse(BaseModel):
    status: str
    answer: str
    chunks_used: Optional[List[Chunk]] = []
    response_time_ms: int

class ErrorResponse(BaseModel):
    status: str = "error"
    error: str
    error_code: str

class HealthResponse(BaseModel):
    status: str
    services: dict
    version: str

