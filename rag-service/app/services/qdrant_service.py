"""
Qdrant service for vector operations
"""
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from app.config import settings
import uuid

class QdrantService:
    def __init__(self):
        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT
        )
        self.collection_name = settings.QDRANT_COLLECTION
        self._ensure_collection()
    
    def _ensure_collection(self):
        """Create collection if not exists"""
        from app.services.embedder import embedder_service
        collections = self.client.get_collections().collections
        if not any(c.name == self.collection_name for c in collections):
            vector_size = embedder_service.dimension
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
    
    def search(self, vector: list, course_id: int, limit: int = 5):
        """Search for similar vectors"""
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=vector,
                query_filter={
                    "must": [
                        {"key": "course_id", "match": {"value": course_id}}
                    ]
                },
                limit=limit
            )
            return results
        except Exception as e:
            print(f"Qdrant search error: {e}")
            return []
    
    def insert(self, vector: list, course_id: int, content: str, metadata: dict):
        """Insert vector into collection"""
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "course_id": course_id,
                "content": content,
                "metadata": metadata
            }
        )
        self.client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )
    
    def check_health(self) -> bool:
        """Check if Qdrant is healthy"""
        try:
            self.client.get_collections()
            return True
        except:
            return False

qdrant_service = QdrantService()

