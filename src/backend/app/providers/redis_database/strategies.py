from typing import Optional
from redis.asyncio import Redis

from app.providers.redis_database.redis_lifespan import (
    get_redis_fail_fast,
    get_redis_fail_open,
)


class RedisClients:
    """
    Centralized access to Redis clients with explicit failure semantics.
    """

    @staticmethod
    def fail_fast() -> Redis:
        return get_redis_fail_fast()

    @staticmethod
    def fail_open() -> Optional[Redis]:
        return get_redis_fail_open()
