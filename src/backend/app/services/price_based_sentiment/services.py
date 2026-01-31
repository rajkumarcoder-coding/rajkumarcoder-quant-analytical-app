import logging
from app.projects.price_based_sentiment_data.project_output import \
    price_based_sentiment_module_output
from app.core_configs.exceptions import InfrastructureError
from app.shared.utils.error_wrapper import safe_execute
from app.domain.market_ohlcv_data_classes.price_sentiment import PriceSentimentEngineRequest
from app.domain.market_ohlcv_data_classes.response_data_models import MetricsJSONResponse

logger = logging.getLogger(__name__)


@safe_execute(
    exception_cls=InfrastructureError,  # safeguard ONLY
    message="price_sentiment service failed",
    reason="unhandled_service_error",
)
async def get_price_sentiment(config: PriceSentimentEngineRequest) -> MetricsJSONResponse:
    logger.info(
        "Fetching market prices for price_sentiment",
        extra={
            "symbols": config.market.symbols,
            "period": config.market.period,
            "interval": config.market.interval,
        },
    )

    # get sanitized stock data
    price_sentiment = await price_based_sentiment_module_output(config)

    return price_sentiment
