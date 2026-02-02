import logging
from app.shared.utils.df_to_json import df_json_convertor
from app.projects.multi_stock_comparison_engine.project_output import (
    multi_stock_comparison_metrics_module_output,
    multi_stock_comparison_returns_module_output
)
from app.core_configs.exceptions import InfrastructureError
from app.shared.utils.error_wrapper import safe_execute
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.domain.market_ohlcv_data_classes.response_data_models import DataFrameJSONResponse

logger = logging.getLogger(__name__)


@safe_execute(
    exception_cls=InfrastructureError,  # safeguard ONLY
    message="Multi stock comparison service failed",
    reason="unhandled_service_error",
)
async def get_multi_stock_comparison_prices(config: MarketPriceConfig) -> DataFrameJSONResponse:
    logger.info(
        "Fetching market prices for multi stock comparison",
        extra={
            "symbols": config.symbols,
            "period": config.period,
            "interval": config.interval,
        },
    )

    # get sanitized stock data
    prices_and_returns = await multi_stock_comparison_returns_module_output(config)

    metrics = await multi_stock_comparison_metrics_module_output(config)

    # json converter
    json_data = df_json_convertor(prices_and_returns, metrics)

    return json_data
