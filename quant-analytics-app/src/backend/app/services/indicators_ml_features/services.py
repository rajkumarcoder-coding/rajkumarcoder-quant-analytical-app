import logging
from app.shared.utils.df_to_json import df_json_convertor
from app.projects.build_indicators_ml_features.project_output import \
    indicator_ml_features_module_output
from app.core_configs.exceptions import InfrastructureError
from app.shared.utils.error_wrapper import safe_execute
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.domain.market_ohlcv_data_classes.response_data_models import DataFrameJSONResponse

logger = logging.getLogger(__name__)


@safe_execute(
    exception_cls=InfrastructureError,  # safeguard ONLY
    message="indicators_ml_features service failed",
    reason="unhandled_service_error",
)
async def get_indicators_ml_features(config: MarketPriceConfig) -> DataFrameJSONResponse:
    logger.info(
        "Fetching market prices for indicators_ml_features",
        extra={
            "symbols": config.symbols,
            "period": config.period,
            "interval": config.interval,
        },
    )

    # get sanitized stock data
    ml_features = await indicator_ml_features_module_output(config)

    # json converter
    json_data = df_json_convertor(ml_features)

    return json_data
