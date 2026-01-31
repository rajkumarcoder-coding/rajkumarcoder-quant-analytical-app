import logging
from app.shared.utils.df_to_json import df_json_convertor
from app.projects.market_regime_risk_detection.project_output import \
    market_regime_risk_detection_module_output, market_regime_metrics_module_output
from app.core_configs.exceptions import InfrastructureError
from app.shared.utils.error_wrapper import safe_execute
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.domain.market_ohlcv_data_classes.response_data_models import DataFrameJSONResponse

logger = logging.getLogger(__name__)


@safe_execute(
    exception_cls=InfrastructureError,  # safeguard ONLY
    message="market_regime service failed",
    reason="unhandled_service_error",
)
async def get_market_regime(config: MarketPriceConfig) -> DataFrameJSONResponse:
    logger.info(
        "Fetching market prices for market_regime",
        extra={
            "symbols": config.symbols,
            "period": config.period,
            "interval": config.interval,
        },
    )

    # get sanitized stock data
    regime = await market_regime_risk_detection_module_output(config)
    metrics = await market_regime_metrics_module_output(config)

    # json converter
    json_data = df_json_convertor(regime, metrics)

    return json_data
