import pickle
import pandas as pd
from typing import Optional, TypeVar
import redis.exceptions
from app.core_configs.app_settings import settings

T = TypeVar("T")


async def get_cached_object(
        key: str,
        *,
        redis_client,
) -> Optional[T]:
    """
    Cache read utility.

    - Fail-fast behavior depends on redis_client passed
    - Fail-open supported by passing fail-open redis client
    """
    if redis_client is None:
        return None  # fail-open path

    try:
        raw = await redis_client.get(key)
        if raw is None:
            return None
        return pickle.loads(raw)

    except redis.exceptions.RedisError:
        # Fail-open semantics: cache must never break pipeline
        return None


async def get_cached_dataframe(
        key: str,
        *,
        redis_client,
) -> Optional[pd.DataFrame]:
    return await get_cached_object(
        key,
        redis_client=redis_client,
    )


async def set_cached_object(
        key: str,
        value: T,
        *,
        redis_client,
        ttl: int = settings.REDIS_TTL_SECONDS,
) -> None:
    """
    Cache write utility.

    - Fail-fast or fail-open behavior is caller-controlled
    """
    if redis_client is None:
        return  # fail-open path

    try:
        await redis_client.setex(
            key,
            ttl or settings.REDIS_TTL_SECONDS,
            pickle.dumps(value),
        )
    except redis.exceptions.RedisError:
        # fail-open for cache writes
        pass
