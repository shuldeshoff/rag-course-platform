"""
Tests for indexing
"""
import pytest
import os
from app.services.indexer import indexer_service
from app.utils.parsers import DocumentParser
from app.utils.chunker import chunker

def test_parse_txt():
    """Test TXT parsing"""
    text = "Это тестовый текст.\nС несколькими строками."
    
    # Create temp file
    with open("/tmp/test.txt", "w", encoding="utf-8") as f:
        f.write(text)
    
    parsed = DocumentParser.parse("/tmp/test.txt")
    assert "тестовый текст" in parsed
    os.unlink("/tmp/test.txt")

def test_chunking():
    """Test text chunking"""
    text = "Это первое предложение. Это второе предложение. Это третье предложение. Это четвертое предложение."
    
    chunks = chunker.chunk(text, method="sentences")
    
    assert len(chunks) > 0
    assert all(isinstance(chunk, str) for chunk in chunks)

@pytest.mark.asyncio
async def test_index_text():
    """Test text indexing"""
    text = "RAG - это Retrieval-Augmented Generation. Это важная технология."
    
    result = await indexer_service.index_text(
        text=text,
        course_id=999,
        metadata={"test": True}
    )
    
    assert result["chunks_created"] > 0
    assert result["course_id"] == 999

