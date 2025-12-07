"""
Retriever service for finding relevant chunks
"""
from typing import List
from app.services.embedder import embedder_service
from app.services.qdrant_service import qdrant_service
from app.models.response import Chunk

class RetrieverService:
    def __init__(self):
        self.embedder = embedder_service
        self.qdrant = qdrant_service
    
    async def retrieve(self, question: str, course_id: int, top_k: int = 5) -> List[Chunk]:
        """
        Retrieve relevant chunks for question
        """
        # 1. Create embedding for question
        question_embedding = self.embedder.embed(question)
        
        # 2. Search in Qdrant
        results = self.qdrant.search(
            vector=question_embedding,
            course_id=course_id,
            limit=top_k
        )
        
        # 3. Convert to Chunk objects
        chunks = []
        for result in results:
            chunks.append(Chunk(
                content=result.payload.get("content", ""),
                score=result.score,
                source=result.payload.get("metadata", {}).get("source", "unknown"),
                metadata=result.payload.get("metadata", {})
            ))
        
        return chunks

retriever_service = RetrieverService()

