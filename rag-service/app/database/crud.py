"""
CRUD operations for database
"""
from sqlalchemy.orm import Session
from app.models.database import RequestLog
from typing import List, Optional

def create_request_log(
    db: Session,
    user_id: int,
    course_id: int,
    question: str,
    answer: Optional[str] = None,
    chunks_used: Optional[dict] = None,
    response_time_ms: Optional[int] = None,
    status: str = "success",
    error_message: Optional[str] = None
) -> RequestLog:
    """Create request log entry"""
    log = RequestLog(
        user_id=user_id,
        course_id=course_id,
        question=question,
        answer=answer,
        chunks_used=chunks_used,
        response_time_ms=response_time_ms,
        status=status,
        error_message=error_message
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def get_user_requests(
    db: Session,
    user_id: int,
    limit: int = 50
) -> List[RequestLog]:
    """Get user request history"""
    return db.query(RequestLog)\
        .filter(RequestLog.user_id == user_id)\
        .order_by(RequestLog.created_at.desc())\
        .limit(limit)\
        .all()

def get_course_stats(db: Session, course_id: int) -> dict:
    """Get statistics for course"""
    total = db.query(RequestLog)\
        .filter(RequestLog.course_id == course_id)\
        .count()
    
    success = db.query(RequestLog)\
        .filter(
            RequestLog.course_id == course_id,
            RequestLog.status == "success"
        )\
        .count()
    
    return {
        "total_requests": total,
        "successful_requests": success,
        "error_rate": (total - success) / total if total > 0 else 0
    }

