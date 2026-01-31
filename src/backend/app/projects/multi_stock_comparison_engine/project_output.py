import pandas as pd
from app.infrastecture.redis_cache.cache_module_output.cache_key import \
    module_output_data_cache_key
from app.infrastecture.redis_cache.cache_module_output.cache_data import \
    get_module_output_cached_dataframe
from app.infrastecture.redis_cache.cache_module_output.cache_data import \
    module_output_cache_service
from app.pipeline.multi_stock_comparison.timeseries_pipeline_integration import \
    fetch_multi_stock_comparison_data
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.core_configs.app_settings import settings
from app.shared.logic_validators.dataframe_validations import require_dataframe
from app.pipeline.multi_stock_comparison.matrics_pipeline_integration import \
    compare_multi_stock_metrics


# “Lambda’s work is: don’t execute now; execute only when I am explicitly called.”

async def multi_stock_comparison_returns_module_output(
        config: MarketPriceConfig,
) -> pd.DataFrame:
    cache_key = module_output_data_cache_key(
        f"{config.symbols}_multi_stock_comparisons_returns",
        config.start,
        config.end,
        config.period,
        config.interval,
    )

    async def compute():
        return await fetch_multi_stock_comparison_data(config)

    market_price_and_returns = await get_module_output_cached_dataframe(
        cache_key=cache_key,
        compute_fn=compute,
        ttl_seconds=settings.REDIS_TTL_MARKET_RETURNS_SECONDS,
    )

    return require_dataframe(
        market_price_and_returns,
        context="fetch_multi_stock_comparison_data_pipeline_output",
    )


async def multi_stock_comparison_metrics_module_output(
        config: MarketPriceConfig,
):
    cache_key = module_output_data_cache_key(
        f"{config.symbols}_multi_stock_comparisons_metrics",
        config.start,
        config.end,
        config.period,
        config.interval,
    )

    async def compute():
        return await compare_multi_stock_metrics(config)

    comparison_metrics = await module_output_cache_service(
        cache_key=cache_key,
        compute_fn=compute,
        ttl_seconds=settings.REDIS_TTL_MARKET_RETURNS_SECONDS,
    )

    return comparison_metrics
