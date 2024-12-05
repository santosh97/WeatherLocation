from redis.asyncio import Redis
from app.config import settings

class RateLimiter:
    def __init__(self):
        self.redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)
        self.max_requests = settings.RATE_LIMIT_REQUESTS
        self.window = settings.RATE_LIMIT_WINDOW

    async def check_rate_limit(self, client_ip: str) -> bool:
        """Check if client has exceeded rate limit"""
        key = f"rate_limit:{client_ip}"
        
        # Get current count
        count = await self.redis.get(key)
        
        if count is None:
            # First request, set counter
            await self.redis.setex(key, self.window, 1)
            return True
            
        count = int(count)
        if count >= self.max_requests:
            return False
            
        # Increment counter
        await self.redis.incr(key)
        return True 