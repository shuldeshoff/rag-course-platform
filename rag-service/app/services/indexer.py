"""
Document indexing service
"""
import os
from typing import List, Dict
from app.utils.parsers import DocumentParser
from app.utils.chunker import chunker
from app.services.embedder import embedder_service
from app.services.qdrant_service import qdrant_service

class IndexerService:
    def __init__(self):
        self.parser = DocumentParser()
        self.chunker = chunker
        self.embedder = embedder_service
        self.qdrant = qdrant_service
    
    async def index_document(
        self,
        file_path: str,
        course_id: int,
        metadata: Dict = None
    ) -> Dict:
        """
        Index a document: parse, chunk, embed, store
        """
        if metadata is None:
            metadata = {}
        
        # 1. Parse document
        text = self.parser.parse(file_path)
        
        if not text.strip():
            raise ValueError("Document is empty or could not be parsed")
        
        # 2. Chunk text
        chunks = self.chunker.chunk(text, method="sentences")
        
        if not chunks:
            raise ValueError("No chunks created from document")
        
        # 3. Create embeddings
        embeddings = self.embedder.embed_batch(chunks)
        
        # 4. Store in Qdrant
        filename = os.path.basename(file_path)
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_metadata = {
                **metadata,
                "filename": filename,
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
            
            self.qdrant.insert(
                vector=embedding,
                course_id=course_id,
                content=chunk,
                metadata=chunk_metadata
            )
        
        return {
            "filename": filename,
            "chunks_created": len(chunks),
            "total_characters": len(text),
            "course_id": course_id
        }
    
    async def index_text(
        self,
        text: str,
        course_id: int,
        metadata: Dict = None
    ) -> Dict:
        """
        Index raw text directly
        """
        if metadata is None:
            metadata = {}
        
        # 1. Clean text
        text = DocumentParser.clean_text(text)
        
        # 2. Chunk
        chunks = self.chunker.chunk(text, method="sentences")
        
        # 3. Embed
        embeddings = self.embedder.embed_batch(chunks)
        
        # 4. Store
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_metadata = {
                **metadata,
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
            
            self.qdrant.insert(
                vector=embedding,
                course_id=course_id,
                content=chunk,
                metadata=chunk_metadata
            )
        
        return {
            "chunks_created": len(chunks),
            "total_characters": len(text),
            "course_id": course_id
        }

indexer_service = IndexerService()

