from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError as PydanticValidationError
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.domain.market_ohlcv_data_classes.build_data_configs import build_market_config
from app.core_configs.exceptions import ValidationError as AppValidationError


class PriceSentimentConfig(BaseModel):
    lookback: int = 20


class PriceSentimentEngineRequest(BaseModel):
    market: MarketPriceConfig
    price_sentiment: PriceSentimentConfig


def build_price_sentiment_config(**kwargs) -> PriceSentimentConfig:
    try:
        return PriceSentimentConfig(**kwargs)

    except PydanticValidationError as e:
        raise AppValidationError(
            message="Invalid portfolio configuration",
            reason="portfolio_config_validation_failed",
            context=jsonable_encoder(
                {
                    "input": kwargs,
                    "errors": e.errors(),
                },
            ),
        ) from e


def build_price_sentiment_endpoint(payload: dict) -> PriceSentimentEngineRequest:
    market_config = build_market_config(
        symbols=payload.get("symbols"),  # required → validated downstream
        start=payload.get("start"),
        end=payload.get("end"),
        period=payload.get("period"),
        interval=payload.get("interval", "1d"),
    )

    price_sentiment_config = build_price_sentiment_config(
        lookback=payload.get("lookback"),  # required → validated downstream
    )

    return PriceSentimentEngineRequest(
        market=market_config, price_sentiment=price_sentiment_config,
    )
