import redis

from app.providers.redis_database.strategies import RedisClients

REFRESH_PREFIX = "refresh"

redis_client: redis.Redis = RedisClients.fail_fast()


async def store_refresh_token(user_id: str, token: str, ttl_seconds: int):
    key = f"{REFRESH_PREFIX}:{user_id}"
    await redis_client.setex(key, ttl_seconds, token)


async def get_refresh_token(user_id: str) -> str | None:
    return await redis_client.get(f"{REFRESH_PREFIX}:{user_id}")


async def revoke_refresh_token(user_id: str):
    await redis_client.delete(f"{REFRESH_PREFIX}:{user_id}")
