import logging
from app.shared.utils.df_to_json import df_json_convertor
from app.projects.earnings_event_price_impact.project_output import \
    earnings_event_price_impact_module_output
from app.core_configs.exceptions import InfrastructureError
from app.shared.utils.error_wrapper import safe_execute
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.domain.market_ohlcv_data_classes.response_data_models import DataFrameJSONResponse

logger = logging.getLogger(__name__)


@safe_execute(
    exception_cls=InfrastructureError,  # safeguard ONLY
    message="earnings_event_price_impact service failed",
    reason="unhandled_service_error",
)
async def get_earnings_event_price_impact(config: MarketPriceConfig) -> DataFrameJSONResponse:
    logger.info(
        "Fetching market prices for earnings_event_price_impact",
        extra={
            "symbols": config.symbols,
            "period": config.period,
            "interval": config.interval,
        },
    )

    # get sanitized stock data
    earnings_event_price_impact = await earnings_event_price_impact_module_output(config)

    # json converter
    json_data = df_json_convertor(earnings_event_price_impact)

    return json_data
