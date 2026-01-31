from fastapi import APIRouter
from typing import Optional
from datetime import date
from app.shared.http_input_validations.validate_demo_symbols import validate_demo_symbols
from app.services.technical_indicators_and_signals.services import get_technical_indicators
from app.api.v1.technical_indicators_and_signals.res_schema import IndicatorsAPIResponse
from app.api.v1.technical_indicators_and_signals.api_res_mapping import INDICATORS_MAPPING
from app.shared.utils.api_json_refining import refine_symbol_based_api_output
from app.domain.market_ohlcv_data_classes.build_data_configs import build_market_config

router = APIRouter(prefix="/market", tags=["Market"])


@router.get("/{symbol}/indicators", response_model=IndicatorsAPIResponse)
async def indicators_endpoint(symbol: str,
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

    result = await get_technical_indicators(config)

    response = refine_symbol_based_api_output(
        raw_output=result, symbols=demo_symbols, mapping=INDICATORS_MAPPING,
    )

    return response
