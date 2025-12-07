"""
Tests for RAG pipeline
"""
import pytest
from app.services.embedder import embedder_service
from app.services.qdrant_service import qdrant_service

def test_embedder_single():
    """Test single text embedding"""
    text = "Что такое RAG?"
    embedding = embedder_service.embed(text)
    
    assert isinstance(embedding, list)
    assert len(embedding) == embedder_service.dimension
    assert all(isinstance(x, float) for x in embedding)

def test_embedder_batch():
    """Test batch embeddings"""
    texts = ["RAG", "YandexGPT", "Machine Learning"]
    embeddings = embedder_service.embed_batch(texts)
    
    assert len(embeddings) == 3
    assert all(len(emb) == embedder_service.dimension for emb in embeddings)

def test_qdrant_insert_and_search():
    """Test Qdrant insert and search"""
    # Insert test data
    text = "RAG - это Retrieval-Augmented Generation"
    embedding = embedder_service.embed(text)
    
    qdrant_service.insert(
        vector=embedding,
        course_id=999,
        content=text,
        metadata={"source": "test", "test": True}
    )
    
    # Search
    results = qdrant_service.search(
        vector=embedding,
        course_id=999,
        limit=1
    )
    
    assert len(results) > 0
    assert results[0].payload["content"] == text

