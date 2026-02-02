import logging
from app.shared.utils.df_to_json import df_json_convertor
from app.projects.technical_indicators_and_signals.project_output import \
    technical_indicators_module_output, technical_indicators_signals_module_output
from app.core_configs.exceptions import InfrastructureError
from app.shared.utils.error_wrapper import safe_execute
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.domain.market_ohlcv_data_classes.response_data_models import DataFrameJSONResponse

logger = logging.getLogger(__name__)


@safe_execute(
    exception_cls=InfrastructureError,  # safeguard ONLY
    message="technical_indicators_and_signals service failed",
    reason="unhandled_service_error",
)
async def get_technical_indicators(config: MarketPriceConfig) -> DataFrameJSONResponse:
    logger.info(
        "Fetching market prices for technical_indicators_and_signals",
        extra={
            "symbols": config.symbols,
            "period": config.period,
            "interval": config.interval,
        },
    )

    # get sanitized stock data
    technical_indicators = await technical_indicators_module_output(config)
    signals = await technical_indicators_signals_module_output(config)

    # json converter
    json_data = df_json_convertor(technical_indicators, signals)

    return json_data
