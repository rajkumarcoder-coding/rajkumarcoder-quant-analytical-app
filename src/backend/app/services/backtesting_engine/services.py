import logging
from app.shared.utils.df_to_json import df_json_convertor
from app.projects.backtesting_engine.project_output import backtesting_engine_module_output, \
    backtesting_engine_metrics_module_output
from app.core_configs.exceptions import InfrastructureError
from app.shared.utils.error_wrapper import safe_execute
from app.domain.market_ohlcv_data_classes.backtesting_engine import BacktestingEngineRequest
from app.domain.market_ohlcv_data_classes.response_data_models import DataFrameJSONResponse

logger = logging.getLogger(__name__)


@safe_execute(
    exception_cls=InfrastructureError,  # safeguard ONLY
    message="backtesting_engine service failed",
    reason="unhandled_service_error",
)
async def get_backtesting_engine(config: BacktestingEngineRequest) -> DataFrameJSONResponse:
    logger.info(
        "Fetching market prices for backtesting_engine",
        extra={
            "symbols": config.market.symbols,
            "period": config.market.period,
            "interval": config.market.interval,
        },
    )

    # get sanitized stock data
    backtesting_engine = await backtesting_engine_module_output(config)
    backtesting_metrics = await backtesting_engine_metrics_module_output(config)

    # json converter
    json_data = df_json_convertor(backtesting_engine, backtesting_metrics)

    return json_data
