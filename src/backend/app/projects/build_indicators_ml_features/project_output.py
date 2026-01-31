import pandas as pd
from app.infrastecture.redis_cache.cache_module_output.cache_key import \
    module_output_data_cache_key
from app.infrastecture.redis_cache.cache_module_output.cache_data import \
    get_module_output_cached_dataframe
from app.pipeline.indicators_ml_features.pipeline_integration import build_ml_features_pipeline
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.core_configs.app_settings import settings
from app.shared.logic_validators.dataframe_validations import require_dataframe


# “Lambda’s work is: don’t execute now; execute only when I am explicitly called.”

async def indicator_ml_features_module_output(
        config: MarketPriceConfig,
) -> pd.DataFrame:
    cache_key = module_output_data_cache_key(
        f"{config.symbols}_indicator_ml_features",
        config.start,
        config.end,
        config.period,
        config.interval,
    )

    async def compute():
        return await build_ml_features_pipeline(config)

    ml_features = await get_module_output_cached_dataframe(
        cache_key=cache_key,
        compute_fn=compute,
        ttl_seconds=settings.REDIS_TTL_MARKET_RETURNS_SECONDS,
    )

    return require_dataframe(
        ml_features,
        context="indicator_ml_features_module_output",
    )
