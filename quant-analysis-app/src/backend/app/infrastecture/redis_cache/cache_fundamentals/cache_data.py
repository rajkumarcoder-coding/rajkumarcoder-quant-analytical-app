from typing import Dict, Any
from app.providers.redis_database.strategies import RedisClients
from app.providers.market_ohlcv.yfinance_providers import YFinanceProvider
from app.infrastecture.redis_cache.cache_fundamentals.cache_key import \
    market_fundamentals_cache_key
from app.providers.redis_database.cache_services import \
    get_cached_object, set_cached_object
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.core_configs.app_settings import settings


async def fetch_sanitize_market_fundamentals(
        config: MarketPriceConfig
) -> Dict[str, Any]:
    redis_client = RedisClients.fail_open()
    cache_key = market_fundamentals_cache_key(
        f"{config.symbols}_fundamentals_market_prices",
        config.symbols,
    )

    cached_data = await get_cached_object(cache_key, redis_client=redis_client)
    if cached_data is not None:
        return cached_data

    fundamental_provider = YFinanceProvider()
    data = fundamental_provider.fetch_fundamentals(config.symbols)

    # copy from yfinance raw data
    raw_data = data.copy()

    # 3. Store in cache
    await set_cached_object(
        cache_key, raw_data, redis_client=redis_client,
        ttl=settings.REDIS_TTL_OHLCV_SECONDS,
    )

    return raw_data
