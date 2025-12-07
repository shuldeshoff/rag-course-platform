"""
Caching service using Redis
"""
from redis import Redis
from app.config import settings
import json
import hashlib

class CacheService:
    def __init__(self):
        self.redis = Redis(
            host=getattr(settings, 'REDIS_HOST', 'localhost'),
            port=getattr(settings, 'REDIS_PORT', 6379),
            db=1,
            decode_responses=True
        )
        self.ttl = 3600  # 1 hour default TTL
    
    def _make_key(self, prefix: str, *args) -> str:
        """Create cache key from arguments"""
        data = json.dumps(args, sort_keys=True)
        hash_key = hashlib.md5(data.encode()).hexdigest()
        return f"{prefix}:{hash_key}"
    
    def get(self, key: str):
        """Get cached value"""
        try:
            value = self.redis.get(key)
            if value:
                return json.loads(value)
        except Exception as e:
            print(f"Cache get error: {e}")
        return None
    
    def set(self, key: str, value, ttl: int = None):
        """Set cached value"""
        try:
            ttl = ttl or self.ttl
            self.redis.setex(key, ttl, json.dumps(value))
        except Exception as e:
            print(f"Cache set error: {e}")
    
    def delete(self, key: str):
        """Delete cached value"""
        try:
            self.redis.delete(key)
        except Exception as e:
            print(f"Cache delete error: {e}")
    
    def get_answer_cache(self, question: str, course_id: int):
        """Get cached answer for question"""
        key = self._make_key("answer", course_id, question.lower().strip())
        return self.get(key)
    
    def set_answer_cache(self, question: str, course_id: int, answer: dict):
        """Cache answer for question"""
        key = self._make_key("answer", course_id, question.lower().strip())
        self.set(key, answer, ttl=1800)  # 30 minutes

cache_service = CacheService()

