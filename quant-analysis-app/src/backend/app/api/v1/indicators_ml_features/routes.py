from fastapi import APIRouter
from typing import Optional
from datetime import date
from app.shared.http_input_validations.validate_demo_symbols import validate_demo_symbols
from app.services.indicators_ml_features.services import get_indicators_ml_features
from app.domain.market_ohlcv_data_classes.build_data_configs import build_market_config
from app.api.v1.indicators_ml_features.res_models import MLFeature

router = APIRouter(prefix="/market", tags=["Market"])


@router.get("/{symbol}/ml/features", response_model=MLFeature)
async def ml_features_endpoint(symbol: str,
                               start: Optional[date] = None,
                               end: Optional[date] = None,
                               period: Optional[str] = None,
                               interval: str = "1d",
                               rolling_window: int = 20,
                               trading_date: int = 252,
                               ):
    demo_symbols = validate_demo_symbols(symbols=symbol)

    if period is None and start is None and end is None:
        period = "1mo"

    config = build_market_config(
        symbols=demo_symbols,
        start=start,
        end=end,
        period=period,
        interval=interval,
        rolling_window=rolling_window,
        trading_date=trading_date,
    )

    response = await get_indicators_ml_features(config)

    return response
