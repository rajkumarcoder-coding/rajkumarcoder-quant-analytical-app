import logging
from app.shared.utils.df_to_json import df_json_convertor
from app.projects.portfolio_return_analyzer.project_output import portfolio_analyzer_module_output, \
    portfolio_analyzer_metrics_module_output
from app.core_configs.exceptions import InfrastructureError
from app.shared.utils.error_wrapper import safe_execute
from app.domain.market_ohlcv_data_classes.portfolio_configs import PortfolioAnalyzeRequest
from app.domain.market_ohlcv_data_classes.response_data_models import DataFrameJSONResponse

logger = logging.getLogger(__name__)


@safe_execute(
    exception_cls=InfrastructureError,  # safeguard ONLY
    message="portfolio_returns service failed",
    reason="unhandled_service_error",
)
async def get_portfolio_returns(config: PortfolioAnalyzeRequest) -> DataFrameJSONResponse:
    logger.info(
        "Fetching market prices for portfolio_returns",
        extra={
            "symbols": config.market.symbols,
            "period": config.market.period,
            "interval": config.market.interval,
        },
    )

    # get sanitized stock data
    portfolio_returns = await portfolio_analyzer_module_output(config)
    portfolio_metrics = await portfolio_analyzer_metrics_module_output(config)

    # json converter
    json_data = df_json_convertor(portfolio_returns, portfolio_metrics)

    return json_data
