from fastapi import APIRouter
from typing import Optional
from datetime import date
from app.shared.http_input_validations.validate_demo_symbols import validate_demo_symbols
from app.services.backtesting_engine.services import get_backtesting_engine
from app.domain.market_ohlcv_data_classes.backtesting_engine import backtesting_analysis_endpoint
from app.shared.helper.render_api_response import map_backtesting_response
from app.api.v1.backtesting_engine.res_schema import BacktestingStrategyResponse

router = APIRouter(prefix="/market", tags=["Market"])


@router.get("/{symbol}/backtesting", response_model=BacktestingStrategyResponse)
async def backtesting_endpoint(symbol: str,
                               start: Optional[date] = None,
                               end: Optional[date] = None,
                               period: Optional[str] = None,
                               interval: str = "1d",
                               rolling_window: int = 20,
                               trading_date: int = 252,
                               fast_window: int = 20,
                               slow_window: int = 50,
                               initial_capital: float = 100_000,
                               ):
    demo_symbols = validate_demo_symbols(symbols=symbol)

    if period is None and start is None and end is None:
        period = "1mo"

    payload = {
        "symbols": demo_symbols,
        "start": start,
        "end": end,
        "period": period,
        "interval": interval,
        "rolling_window": rolling_window,
        "trading_date": trading_date,
        "fast_window": fast_window,
        "slow_window": slow_window,
        "initial_capital": initial_capital,
    }

    config = backtesting_analysis_endpoint(payload=payload)

    result = await get_backtesting_engine(config)

    data = result.data
    metrics = result.metrics

    raw_res = {
        "backtesting_data": data,
        "backtesting_analysis": metrics,
    }

    response = map_backtesting_response(raw_res)

    return response
