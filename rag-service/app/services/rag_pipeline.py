"""
RAG Pipeline orchestration
"""
import time
from typing import Tuple, List
from app.services.retriever import retriever_service
from app.services.generator import generator_service
from app.models.response import Chunk

class RAGPipeline:
    def __init__(self):
        self.retriever = retriever_service
        self.generator = generator_service
    
    async def process(
        self, 
        question: str, 
        course_id: int,
        top_k: int = 5
    ) -> Tuple[str, List[Chunk], int]:
        """
        Process question through full RAG pipeline
        
        Returns: (answer, chunks_used, response_time_ms)
        """
        start_time = time.time()
        
        # 1. Retrieve relevant chunks
        chunks = await self.retriever.retrieve(
            question=question,
            course_id=course_id,
            top_k=top_k
        )
        
        # 2. Generate answer with context
        answer = await self.generator.generate_with_context(
            question=question,
            chunks=chunks
        )
        
        # 3. Calculate response time
        response_time_ms = int((time.time() - start_time) * 1000)
        
        return answer, chunks, response_time_ms

rag_pipeline = RAGPipeline()

