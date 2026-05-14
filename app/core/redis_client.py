import redis.asyncio as redis
from app.core.settings import settings

class RedisClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
            cls._instance.client = None
        return cls._instance

    async def connect(self):
        if self.client is None:
            self.client = await redis.from_url(settings.REDIS_URL, decode_responses=True)

    async def close(self):
        if self.client:
            await self.client.close()
            self.client = None

    async def get(self, key: str):
        if not self.client:
            await self.connect()
        return await self.client.get(key)

    async def set(self, key: str, value: str, expire: int = None):
        if not self.client:
            await self.connect()
        await self.client.set(key, value, ex=expire)

    async def delete(self, key: str):
        if not self.client:
            await self.connect()
        await self.client.delete(key)

    async def flushall(self):
        if not self.client:
            await self.connect()
        await self.client.flushall()

redis_client = RedisClient()
