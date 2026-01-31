import pandas as pd
from app.infrastecture.redis_cache.cache_module_output.cache_key import \
    module_output_data_cache_key
from app.infrastecture.redis_cache.cache_module_output.cache_data import \
    get_module_output_cached_dataframe
from app.infrastecture.redis_cache.cache_module_output.cache_data import \
    module_output_cache_service
from app.pipeline.risk_and_volatility_analyzer.timeseries_pipeline_integration import \
    fetch_risk_analyzer
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.core_configs.app_settings import settings
from app.shared.logic_validators.dataframe_validations import require_dataframe
from app.pipeline.risk_and_volatility_analyzer.risk_metrics_pipeline_integration import \
    risk_metrics_calculation


# “Lambda’s work is: don’t execute now; execute only when I am explicitly called.”

async def risk_and_volatility_analyzer_module_output(
        config: MarketPriceConfig,
) -> pd.DataFrame:
    cache_key = module_output_data_cache_key(
        f"{config.symbols}_risk_and_volatility_analyzer",
        config.start,
        config.end,
        config.period,
        config.interval,
    )

    async def compute():
        return await fetch_risk_analyzer(config)

    risk_analyzer = await get_module_output_cached_dataframe(
        cache_key=cache_key,
        compute_fn=compute,
        ttl_seconds=settings.REDIS_TTL_MARKET_RETURNS_SECONDS,
    )

    return require_dataframe(
        risk_analyzer,
        context="technical_indicators_module_output",
    )


async def risk_analyzer_metrics_module_output(
        config: MarketPriceConfig,
):
    cache_key = module_output_data_cache_key(
        f"{config.symbols}_risk_analyzer_metrics",
        config.start,
        config.end,
        config.period,
        config.interval,
    )

    async def compute():
        return await risk_metrics_calculation(config)

    risk_metrics = await module_output_cache_service(
        cache_key=cache_key,
        compute_fn=compute,
        ttl_seconds=settings.REDIS_TTL_MARKET_RETURNS_SECONDS,
    )

    return risk_metrics
