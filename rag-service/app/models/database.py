"""
Database models
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.database.db import Base

class RequestLog(Base):
    __tablename__ = "requests_log"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    course_id = Column(Integer, nullable=False, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text)
    chunks_used = Column(JSON)
    response_time_ms = Column(Integer)
    status = Column(String(20))
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

