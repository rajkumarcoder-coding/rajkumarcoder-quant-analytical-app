from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError as PydanticValidationError
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.domain.market_ohlcv_data_classes.build_data_configs import build_market_config
from app.core_configs.exceptions import ValidationError as AppValidationError


class BacktestingConfig(BaseModel):
    fast_window: int = 20
    slow_window: int = 50
    initial_capital: int = 10000,


class BacktestingEngineRequest(BaseModel):
    market: MarketPriceConfig
    backtesting: BacktestingConfig


def build_backtesting_config(**kwargs) -> BacktestingConfig:
    try:
        return BacktestingConfig(**kwargs)

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


def backtesting_analysis_endpoint(payload: dict):
    market_config = build_market_config(
        symbols=payload.get("symbols"),  # required → validated downstream
        start=payload.get("start"),
        end=payload.get("end"),
        period=payload.get("period"),
        interval=payload.get("interval", "1d"),
    )

    backtesting_config = build_backtesting_config(
        fast_window=payload.get("fast_window"),
        slow_window=payload.get("slow_window"),
        initial_capital=payload.get("initial_capital"),  # required → validated downstream
    )

    return BacktestingEngineRequest(market=market_config, backtesting=backtesting_config)
