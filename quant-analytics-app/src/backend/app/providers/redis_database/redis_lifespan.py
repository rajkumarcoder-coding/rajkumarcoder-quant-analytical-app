import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from redis.asyncio import Redis

from app.core_configs.app_settings import settings

logger = logging.getLogger(__name__)

# ---- module-level state (set during lifespan) ----
redis_fail_fast: Optional[Redis] = None
redis_fail_open: Optional[Redis] = None


# ---- runtime getters (CRITICAL FIX) ----
def get_redis_fail_fast() -> Redis:
    if redis_fail_fast is None:
        raise RuntimeError("Fail-fast Redis not initialized")
    return redis_fail_fast


def get_redis_fail_open() -> Optional[Redis]:
    return redis_fail_open


@asynccontextmanager
async def redis_lifespan(app: FastAPI):
    _ = app  # explicitly unused
    global redis_fail_fast, redis_fail_open

    # ---------- FAIL-FAST REDIS ----------
    redis_fail_fast = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
        decode_responses=settings.REDIS_DECODE_RESPONSES,
        max_connections=settings.REDIS_MAX_CONNECTIONS,
    )

    try:
        await redis_fail_fast.ping()
        logger.info("Fail-fast Redis connected")
    except Exception as e:
        logger.critical("Fail-fast Redis unavailable — aborting startup", exc_info=e)
        raise RuntimeError("Fail-fast Redis required") from e

    # ---------- FAIL-OPEN REDIS ----------
    try:
        redis_fail_open = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses=settings.REDIS_DECODE_RESPONSES,
            max_connections=settings.REDIS_MAX_CONNECTIONS,
        )
        await redis_fail_open.ping()
        logger.info("Fail-open Redis connected")
    except Exception as e:
        redis_fail_open = None
        logger.warning(
            "Fail-open Redis unavailable — running without cache",
            exc_info=e,
        )

    yield

    # ---------- SHUTDOWN ----------
    try:
        if redis_fail_fast:
            await redis_fail_fast.close()
            logger.info("redis fail fast connection closed and disposed")
    except Exception as e:
        logger.error("Error closing fail-fast Redis", exc_info=e)

    try:
        if redis_fail_open is not None:
            await redis_fail_open.close()
            logger.info("redis fail open connection closed and disposed")
    except Exception as e:
        logger.error("Error closing fail-open Redis", exc_info=e)
