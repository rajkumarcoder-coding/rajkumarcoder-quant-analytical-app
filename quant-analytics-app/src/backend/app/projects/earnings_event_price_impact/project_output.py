import pandas as pd
from app.infrastecture.redis_cache.cache_module_output.cache_key import \
    module_output_data_cache_key
from app.infrastecture.redis_cache.cache_module_output.cache_data import \
    get_module_output_cached_dataframe
from app.pipeline.earnings_event_price_impact.timeseries_pipeline_integration import \
    fetch_earnings_events_price_impact_data
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.core_configs.app_settings import settings
from app.shared.logic_validators.dataframe_validations import require_dataframe


# “Lambda’s work is: don’t execute now; execute only when I am explicitly called.”

async def earnings_event_price_impact_module_output(
        config: MarketPriceConfig,
) -> pd.DataFrame:
    cache_key = module_output_data_cache_key(
        f"{config.symbols}_earnings_event_price_impact",
        config.start,
        config.end,
        config.period,
        config.interval,
    )

    async def compute():
        return await fetch_earnings_events_price_impact_data(config)

    earning_events_impacts_data = await get_module_output_cached_dataframe(
        cache_key=cache_key,
        compute_fn=compute,
        ttl_seconds=settings.REDIS_TTL_MARKET_RETURNS_SECONDS,
    )

    return require_dataframe(
        earning_events_impacts_data,
        context="earnings_event_price_impact_module_output",
    )
