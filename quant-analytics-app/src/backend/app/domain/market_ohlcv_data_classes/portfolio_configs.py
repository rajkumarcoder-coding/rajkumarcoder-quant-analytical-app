from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError as PydanticValidationError
from typing import Dict
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.domain.market_ohlcv_data_classes.build_data_configs import build_market_config
from app.core_configs.exceptions import ValidationError as AppValidationError


class PortfolioConfig(BaseModel):
    weights: Dict[str, float] = Field(
        ...,
        description="Symbols → weight mapping (must sum to 1.0)",
        examples=[{"AAPL": 0.4, "MSFT": 0.3, "GOOGL": 0.3}],
    )
    initial_capital: int = 100_000


class PortfolioAnalyzeRequest(BaseModel):
    market: MarketPriceConfig
    portfolio: PortfolioConfig


def build_portfolio_config(**kwargs) -> PortfolioConfig:
    try:
        return PortfolioConfig(**kwargs)

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


def portfolio_analyze_endpoint(payload: dict):
    market_config = build_market_config(
        symbols=payload.get("symbols"),  # required → validated downstream
        start=payload.get("start"),
        end=payload.get("end"),
        period=payload.get("period"),
        interval=payload.get("interval", "1d"),
    )

    portfolio_config = build_portfolio_config(
        weights=payload.get("weights"),
        initial_capital=payload.get("initial_capital"),  # required → validated downstream
    )

    return PortfolioAnalyzeRequest(market=market_config, portfolio=portfolio_config)
