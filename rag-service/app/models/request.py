"""
Request models
"""
from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    user_id: int = Field(..., description="Moodle user ID")
    course_id: int = Field(..., description="Moodle course ID")
    question: str = Field(..., max_length=500, description="User question")

class IndexRequest(BaseModel):
    course_id: int
    title: str
    content: str
    metadata: dict = {}

