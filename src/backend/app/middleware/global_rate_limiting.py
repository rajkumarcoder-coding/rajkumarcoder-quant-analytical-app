import time
import logging
from fastapi import Request
from fastapi.responses import JSONResponse
import redis.asyncio as redis
from app.providers.redis_database.strategies import RedisClients
from app.core_configs.rate_limiting_configs import RateLimitConfig

logger = logging.getLogger(__name__)
_last_redis_error = 0

RATE_LIMIT = RateLimitConfig.GLOBAL_RATE_LIMIT
WINDOW_SECONDS = RateLimitConfig.GLOBAL_WINDOW_SECONDS


def should_log(interval: int = 60) -> bool:
    global _last_redis_error
    now = time.time()
    if now - _last_redis_error > interval:
        _last_redis_error = now
        return True
    return False


async def global_rate_limit_middleware(request: Request, call_next):
    try:
        client_ip = request.client.host if request.client else "unknown"
        key = f"global_rate:{client_ip}"

        redis_client: redis.Redis = RedisClients.fail_open()

        count = await redis_client.incr(key)

        # Set TTL only once
        if count == 1:
            await redis_client.expire(key, WINDOW_SECONDS)

        if count > RATE_LIMIT:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests"},
            )

    except redis.RedisError:
        # FAIL OPEN
        if should_log():
            logger.warning("Redis unavailable, rate limiting skipped")

    return await call_next(request)
