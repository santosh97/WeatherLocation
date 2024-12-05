import json
from redis.asyncio import Redis
from app.config import settings

class CacheService:
    def __init__(self):
        self.redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)
        self.ttl = settings.REDIS_CACHE_TTL

    async def get(self, key: str) -> dict:
        """Get cached data"""
        data = await self.redis.get(key)
        return json.loads(data) if data else None

    async def set(self, key: str, value: dict) -> bool:
        """Cache data with TTL"""
        try:
            await self.redis.setex(
                key,
                self.ttl,
                json.dumps(value)
            )
            return True
        except Exception:
            return False 