import pandas as pd
from app.infrastecture.redis_cache.cache_module_output.cache_key import \
    module_output_data_cache_key
from app.infrastecture.redis_cache.cache_module_output.cache_data import \
    get_module_output_cached_dataframe
from app.infrastecture.redis_cache.cache_module_output.cache_data import \
    module_output_cache_service
from app.pipeline.technical_indicators_and_signals.timeseries_pipeline_integration import \
    fetch_technical_indicators
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.core_configs.app_settings import settings
from app.shared.logic_validators.dataframe_validations import require_dataframe
from app.pipeline.technical_indicators_and_signals.signals_pipeline_integration import \
    technical_indicators_signals


# “Lambda’s work is: don’t execute now; execute only when I am explicitly called.”

async def technical_indicators_module_output(
        config: MarketPriceConfig,
) -> pd.DataFrame:
    cache_key = module_output_data_cache_key(
        f"{config.symbols}_technical_indicators",
        config.start,
        config.end,
        config.period,
        config.interval,
    )

    async def compute():
        return await fetch_technical_indicators(config)

    technical_indicators = await get_module_output_cached_dataframe(
        cache_key=cache_key,
        compute_fn=compute,
        ttl_seconds=settings.REDIS_TTL_MARKET_RETURNS_SECONDS,
    )

    return require_dataframe(
        technical_indicators,
        context="technical_indicators_module_output",
    )


async def technical_indicators_signals_module_output(
        config: MarketPriceConfig,
):
    cache_key = module_output_data_cache_key(
        f"{config.symbols}_technical_indicators_signals",
        config.start,
        config.end,
        config.period,
        config.interval,
    )

    async def compute():
        return await technical_indicators_signals(config)

    indicators_signals = await module_output_cache_service(
        cache_key=cache_key,
        compute_fn=compute,
        ttl_seconds=settings.REDIS_TTL_MARKET_RETURNS_SECONDS,
    )

    return indicators_signals
