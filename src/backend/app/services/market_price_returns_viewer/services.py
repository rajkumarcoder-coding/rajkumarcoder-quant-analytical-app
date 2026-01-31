import logging
from app.shared.utils.df_to_json import df_json_convertor
from app.projects.market_price_returns_viewer.project_output import \
    market_price_and_returns_project_output
from app.core_configs.exceptions import InfrastructureError
from app.shared.utils.error_wrapper import safe_execute
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.domain.market_ohlcv_data_classes.response_data_models import DataFrameJSONResponse

logger = logging.getLogger(__name__)


@safe_execute(
    exception_cls=InfrastructureError,  # safeguard ONLY
    message="Market price service failed",
    reason="unhandled_service_error",
)
async def get_market_data_prices(config: MarketPriceConfig) -> DataFrameJSONResponse:
    logger.info(
        "Fetching market prices for market price and return viewer",
        extra={
            "symbols": config.symbols,
            "period": config.period,
            "interval": config.interval,
        },
    )

    # get sanitized stock data
    prices_and_returns = await market_price_and_returns_project_output(config)

    # json converter
    json_data = df_json_convertor(prices_and_returns)

    return json_data
