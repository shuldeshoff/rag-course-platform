"""
Rate limiting middleware using Redis
"""
from fastapi import HTTPException, Request
from redis import Redis
from app.config import settings
import time

class RateLimiter:
    def __init__(self):
        self.redis = Redis(
            host=getattr(settings, 'REDIS_HOST', 'localhost'),
            port=getattr(settings, 'REDIS_PORT', 6379),
            db=0,
            decode_responses=True
        )
        self.max_requests = 10  # requests per window
        self.window_seconds = 60  # time window
    
    def check_rate_limit(self, key: str) -> bool:
        """Check if request is within rate limit"""
        try:
            current = int(time.time())
            window_start = current - self.window_seconds
            
            # Remove old entries
            self.redis.zremrangebyscore(key, 0, window_start)
            
            # Count requests in current window
            request_count = self.redis.zcard(key)
            
            if request_count >= self.max_requests:
                return False
            
            # Add current request
            self.redis.zadd(key, {str(current): current})
            self.redis.expire(key, self.window_seconds)
            
            return True
        except Exception as e:
            # If Redis fails, allow request
            print(f"Rate limit check failed: {e}")
            return True
    
    def get_user_key(self, user_id: int) -> str:
        """Get rate limit key for user"""
        return f"ratelimit:user:{user_id}"
    
    def get_course_key(self, course_id: int) -> str:
        """Get rate limit key for course"""
        return f"ratelimit:course:{course_id}"

rate_limiter = RateLimiter()

async def rate_limit_user(request: Request, user_id: int):
    """Rate limit middleware for user"""
    key = rate_limiter.get_user_key(user_id)
    
    if not rate_limiter.check_rate_limit(key):
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later."
        )

