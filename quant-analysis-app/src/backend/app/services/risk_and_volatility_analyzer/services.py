import logging
from app.shared.utils.df_to_json import df_json_convertor
from app.projects.risk_and_volatility_analyzer.project_output import \
    risk_and_volatility_analyzer_module_output, risk_analyzer_metrics_module_output
from app.core_configs.exceptions import InfrastructureError
from app.shared.utils.error_wrapper import safe_execute
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.domain.market_ohlcv_data_classes.response_data_models import DataFrameJSONResponse

logger = logging.getLogger(__name__)


@safe_execute(
    exception_cls=InfrastructureError,  # safeguard ONLY
    message="risk_analyzer service failed",
    reason="unhandled_service_error",
)
async def get_risk_analyzer(config: MarketPriceConfig) -> DataFrameJSONResponse:
    logger.info(
        "Fetching market prices for risk_analyzer",
        extra={
            "symbols": config.symbols,
            "period": config.period,
            "interval": config.interval,
        },
    )

    # get sanitized stock data
    risk_analyzer = await risk_and_volatility_analyzer_module_output(config)
    risk_metrics = await risk_analyzer_metrics_module_output(config)

    # json converter
    json_data = df_json_convertor(risk_analyzer, risk_metrics)

    return json_data
