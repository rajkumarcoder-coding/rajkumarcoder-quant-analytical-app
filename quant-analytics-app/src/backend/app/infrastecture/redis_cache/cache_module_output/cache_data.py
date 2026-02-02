import pandas as pd
from typing import Dict
import inspect
from typing import Callable, TypeVar, Awaitable, Union
from app.providers.redis_database.cache_services import get_cached_object, set_cached_object
from app.providers.redis_database.strategies import RedisClients
from app.core_configs.app_settings import settings

T = TypeVar("T")
ComputeFn = Callable[[], Union[T, Awaitable[T]]]


async def module_output_cache_service(
        cache_key: str,
        compute_fn: ComputeFn[T],
        ttl_seconds: int = settings.REDIS_TTL_SECONDS,
) -> T:
    redis_client = RedisClients.fail_open()
    # 1. Try cache
    cached = await get_cached_object(
        key=cache_key,
        redis_client=redis_client,
    )
    if cached is not None:
        return cached

    # 2. Compute business logic (sync or async)
    result = compute_fn()
    if inspect.isawaitable(result):
        result = await result

    # 3. Store in cache
    await set_cached_object(
        key=cache_key,
        value=result,
        redis_client=redis_client,
        ttl=ttl_seconds,
    )

    return result


async def get_module_output_cached_dataframe(
        cache_key: str,
        compute_fn: ComputeFn[pd.DataFrame],
        ttl_seconds: int,
) -> pd.DataFrame:
    return await module_output_cache_service(
        cache_key=cache_key,
        compute_fn=compute_fn,
        ttl_seconds=ttl_seconds,
    )


async def get_module_output_cached_matrics(
        cache_key: str,
        compute_fn: ComputeFn[Dict[str, Dict[str, float]]],
        ttl_seconds: int,
) -> Dict[str, Dict[str, float]]:
    return await module_output_cache_service(
        cache_key=cache_key,
        compute_fn=compute_fn,
        ttl_seconds=ttl_seconds,
    )
