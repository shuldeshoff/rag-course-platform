"""
Text chunking strategies
"""
from typing import List
from app.config import settings

class TextChunker:
    def __init__(
        self, 
        chunk_size: int = None, 
        chunk_overlap: int = None
    ):
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP
    
    def chunk_by_sentences(self, text: str) -> List[str]:
        """
        Split text into chunks by sentences
        Tries to keep chunks around target size
        """
        import re
        
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            # If adding this sentence exceeds chunk_size
            if current_length + sentence_length > self.chunk_size and current_chunk:
                # Save current chunk
                chunks.append(' '.join(current_chunk))
                
                # Start new chunk with overlap
                overlap_sentences = []
                overlap_length = 0
                for s in reversed(current_chunk):
                    if overlap_length + len(s) <= self.chunk_overlap:
                        overlap_sentences.insert(0, s)
                        overlap_length += len(s)
                    else:
                        break
                
                current_chunk = overlap_sentences
                current_length = overlap_length
            
            current_chunk.append(sentence)
            current_length += sentence_length
        
        # Add last chunk
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def chunk_by_characters(self, text: str) -> List[str]:
        """Simple character-based chunking with overlap"""
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + self.chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence or word boundary
            if end < text_length:
                # Look for sentence end
                last_sentence = max(
                    chunk.rfind('.'),
                    chunk.rfind('!'),
                    chunk.rfind('?')
                )
                if last_sentence > self.chunk_size * 0.5:
                    chunk = chunk[:last_sentence + 1]
                else:
                    # Fall back to word boundary
                    last_space = chunk.rfind(' ')
                    if last_space > self.chunk_size * 0.5:
                        chunk = chunk[:last_space]
            
            chunks.append(chunk.strip())
            start += len(chunk) - self.chunk_overlap
        
        return chunks
    
    def chunk(self, text: str, method: str = "sentences") -> List[str]:
        """Chunk text using specified method"""
        if method == "sentences":
            return self.chunk_by_sentences(text)
        elif method == "characters":
            return self.chunk_by_characters(text)
        else:
            raise ValueError(f"Unknown chunking method: {method}")

chunker = TextChunker()

