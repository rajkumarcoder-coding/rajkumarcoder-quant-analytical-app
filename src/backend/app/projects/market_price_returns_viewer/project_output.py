import pandas as pd
from app.infrastecture.redis_cache.cache_module_output.cache_key import \
    module_output_data_cache_key
from app.infrastecture.redis_cache.cache_module_output.cache_data import \
    get_module_output_cached_dataframe
from app.pipeline.market_price_return_viewer.pipeline_integration import \
    fetch_market_prices_and_returns
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.core_configs.app_settings import settings
from app.shared.logic_validators.dataframe_validations import require_dataframe


# “Lambda’s work is: don’t execute now; execute only when I am explicitly called.”

async def market_price_and_returns_project_output(
        config: MarketPriceConfig,
) -> pd.DataFrame:
    cache_key = module_output_data_cache_key(
        f"{config.symbols}_market_prices_and_returns",
        config.start,
        config.end,
        config.period,
        config.interval,
    )

    async def compute():
        return await fetch_market_prices_and_returns(config)

    market_price_and_returns = await get_module_output_cached_dataframe(
        cache_key=cache_key,
        compute_fn=compute,
        ttl_seconds=settings.REDIS_TTL_MARKET_RETURNS_SECONDS,
    )

    return require_dataframe(
        market_price_and_returns,
        context="market_price_and_returns_pipeline_output",
    )
