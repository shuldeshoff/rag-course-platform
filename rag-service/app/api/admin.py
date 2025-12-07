"""
Admin API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import Optional
import os
import tempfile
from app.api.auth import verify_token
from app.services.indexer import indexer_service
from app.models.request import IndexRequest

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/index/file")
async def index_file(
    course_id: int = Form(...),
    title: str = Form(...),
    file: UploadFile = File(...),
    module_number: Optional[int] = Form(None),
    token: str = Depends(verify_token)
):
    """
    Index a document file (PDF, DOCX, TXT)
    Requires admin authentication
    """
    # Validate file type
    allowed_extensions = ['.pdf', '.docx', '.txt']
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {allowed_extensions}"
        )
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_path = tmp_file.name
    
    try:
        # Index document
        metadata = {
            "title": title,
            "source": file.filename,
            "type": "file"
        }
        if module_number:
            metadata["module"] = module_number
        
        result = await indexer_service.index_document(
            file_path=tmp_path,
            course_id=course_id,
            metadata=metadata
        )
        
        return {
            "status": "success",
            "message": f"Document indexed successfully",
            **result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Clean up temp file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

@router.post("/index/text")
async def index_text(
    request: IndexRequest,
    token: str = Depends(verify_token)
):
    """
    Index raw text content
    Requires admin authentication
    """
    try:
        result = await indexer_service.index_text(
            text=request.content,
            course_id=request.course_id,
            metadata={
                "title": request.title,
                "source": "direct_input",
                **request.metadata
            }
        )
        
        return {
            "status": "success",
            "message": "Text indexed successfully",
            **result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/{course_id}")
async def get_course_stats(
    course_id: int,
    token: str = Depends(verify_token)
):
    """
    Get indexing statistics for a course
    """
    try:
        # Query Qdrant for course documents
        from app.services.qdrant_service import qdrant_service
        
        # Get collection info
        collection_info = qdrant_service.client.get_collection(
            collection_name=qdrant_service.collection_name
        )
        
        return {
            "course_id": course_id,
            "total_vectors": collection_info.points_count,
            "collection": qdrant_service.collection_name
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

