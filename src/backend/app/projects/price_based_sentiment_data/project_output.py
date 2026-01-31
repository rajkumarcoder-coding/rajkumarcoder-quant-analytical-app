from app.infrastecture.redis_cache.cache_module_output.cache_key import \
    module_output_data_cache_key
from app.infrastecture.redis_cache.cache_module_output.cache_data import \
    module_output_cache_service
from app.domain.market_ohlcv_data_classes.price_sentiment import PriceSentimentEngineRequest
from app.core_configs.app_settings import settings
from app.pipeline.price_sentiment_and_momentum.pipeline_integration import \
    fetch_price_based_sentiment_data


async def price_based_sentiment_module_output(
        config: PriceSentimentEngineRequest,
):
    cache_key = module_output_data_cache_key(
        f"{config.market.symbols}_price_based_sentiment_engine_metrics",
        config.market.start,
        config.market.end,
        config.market.period,
        config.market.interval,
    )

    async def compute():
        return await fetch_price_based_sentiment_data(config)

    price_sentiment_metrics = await module_output_cache_service(
        cache_key=cache_key,
        compute_fn=compute,
        ttl_seconds=settings.REDIS_TTL_MARKET_RETURNS_SECONDS,
    )

    return price_sentiment_metrics
