import pandas as pd
from app.providers.redis_database.strategies import RedisClients
from app.providers.market_ohlcv.yfinance_providers import YFinanceProvider
from app.shared.utils.normalize_df import normalize_df
from app.infrastecture.redis_cache.cache_market_ohlcv.cache_key import \
    market_ohlcv_cache_key
from app.providers.redis_database.cache_services import \
    get_cached_dataframe, set_cached_object
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.core_configs.app_settings import settings
from app.shared.logic_validators.dataframe_validations import require_dataframe


async def fetch_sanitize_market_ohlcv_prices(
        config: MarketPriceConfig
) -> pd.DataFrame:
    redis_client = RedisClients.fail_open()
    cache_key = market_ohlcv_cache_key(
        f"{config.symbols}_prices",
        config.symbols,
        config.start,
        config.end,
        config.period,
        config.interval,
    )

    cached_df = await get_cached_dataframe(cache_key, redis_client=redis_client)
    if cached_df is not None:
        return cached_df

    price_provider = YFinanceProvider()
    df = price_provider.fetch_prices(config)

    # copy from yfinance raw data
    raw_df = df.copy()

    sanitized_market_price_df = normalize_df(raw_df)

    # 3. Store in cache
    await set_cached_object(
        cache_key, sanitized_market_price_df, redis_client=redis_client,
        ttl=settings.REDIS_TTL_OHLCV_SECONDS,
    )

    return require_dataframe(
        sanitized_market_price_df, context="fetch_sanitize_market_data_prices",
    )
