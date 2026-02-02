import pandas as pd
from app.infrastecture.redis_cache.cache_module_output.cache_key import \
    module_output_data_cache_key
from app.infrastecture.redis_cache.cache_module_output.cache_data import \
    get_module_output_cached_dataframe
from app.infrastecture.redis_cache.cache_module_output.cache_data import \
    module_output_cache_service
from app.pipeline.portfolio_analyzer.timeseries_pipeline_integration import fetch_portfolio_analyzer
from app.domain.market_ohlcv_data_classes.portfolio_configs import PortfolioAnalyzeRequest
from app.core_configs.app_settings import settings
from app.shared.logic_validators.dataframe_validations import require_dataframe
from app.pipeline.portfolio_analyzer.portfolio_metrics_pipeline_integration import \
    portfolio_metrics_calculation


# “Lambda’s work is: don’t execute now; execute only when I am explicitly called.”

async def portfolio_analyzer_module_output(
        config: PortfolioAnalyzeRequest,
) -> pd.DataFrame:
    cache_key = module_output_data_cache_key(
        f"{config.market.symbols}_portfolio_analyzer",
        config.market.start,
        config.market.end,
        config.market.period,
        config.market.interval,
    )

    async def compute():
        return await fetch_portfolio_analyzer(config)

    portfolio_analyzer = await get_module_output_cached_dataframe(
        cache_key=cache_key,
        compute_fn=compute,
        ttl_seconds=settings.REDIS_TTL_MARKET_RETURNS_SECONDS,
    )

    return require_dataframe(
        portfolio_analyzer,
        context="portfolio_analyzer_module_output",
    )


async def portfolio_analyzer_metrics_module_output(
        config: PortfolioAnalyzeRequest,
):
    cache_key = module_output_data_cache_key(
        f"{config.market.symbols}_portfolio_analyzer_metrics",
        config.market.start,
        config.market.end,
        config.market.period,
        config.market.interval,
    )

    async def compute():
        return await portfolio_metrics_calculation(config)

    portfolio_metrics = await module_output_cache_service(
        cache_key=cache_key,
        compute_fn=compute,
        ttl_seconds=settings.REDIS_TTL_MARKET_RETURNS_SECONDS,
    )

    return portfolio_metrics
