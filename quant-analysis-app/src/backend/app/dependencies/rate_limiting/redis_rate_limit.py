import logging
import time
from fastapi import Request, HTTPException
import redis

logger = logging.getLogger(__name__)

_last_redis_error = 0

from app.providers.redis_database.strategies import RedisClients


async def redis_rate_limit(limit: int, window: int):
    async def dependency(request: Request):
        # 🔑 IMPORTANT: include path + IP to avoid collisions
        client_ip = request.client.host
        route = request.url.path
        key = f"rate:{client_ip}:{route}"

        redis_client: redis.Redis = RedisClients.fail_open()

        current = await redis_client.incr(key)

        # 🔥 CRITICAL: set TTL only on first hit
        if current == 1:
            await redis_client.expire(key, window)

        if current > limit:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded ({limit}/{window}s)",
            )

    return dependency


def should_log(interval: int = 60) -> bool:
    """
    Throttle infrastructure error logs to avoid log spam.
    """
    global _last_redis_error
    now = time.time()
    if now - _last_redis_error > interval:
        _last_redis_error = now
        return True
    return False


async def redis_rate_limit_fail_open(limit: int, window: int):
    """
    Redis-based rate limiting with fail-open behavior.
    If Redis is unavailable, requests are allowed to proceed.
    """

    async def dependency(request: Request):
        try:
            # Proxy-safe client IP resolution
            client_ip = (
                    request.headers.get("x-forwarded-for", "").split(",")[0]
                    or (request.client.host if request.client else "unknown")
            )

            route = request.scope.get("path")
            key = f"rate:{client_ip}:{route}"

            redis_client: redis.Redis = RedisClients.fail_open()

            current = await redis_client.incr(key)

            # Set TTL only on first request
            if current == 1:
                await redis_client.expire(key, window)

            if current > limit:
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded",
                )

        except redis.exceptions.RedisError as e:
            # 🔥 FAIL OPEN + LOG THROTTLING
            if should_log():
                logger.warning(
                    "Redis unavailable → rate limiting temporarily disabled",
                )
            return  # allow request

    return dependency
