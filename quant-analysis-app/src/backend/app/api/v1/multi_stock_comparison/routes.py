from fastapi import APIRouter
from typing import Optional
from datetime import date
from app.shared.http_input_validations.validate_demo_symbols import validate_demo_symbols
from app.shared.http_input_validations.comparison_input_validation import \
    validate_two_symbols_for_comparison
from app.services.multi_stock_comparison_engine.services import get_multi_stock_comparison_prices
from app.api.v1.multi_stock_comparison.res_schema import MultiSymbolMarketComparisonResponse
from app.domain.market_ohlcv_data_classes.build_data_configs import build_market_config
from app.api.v1.multi_stock_comparison.api_res_mapping import MARKET_PRICE_MAPPING
from app.shared.utils.api_json_refining import refine_symbol_based_api_output

router = APIRouter(prefix="/market", tags=["Market"])


@router.get("/{symbol}/comparison", response_model=MultiSymbolMarketComparisonResponse)
async def market_comparison_endpoint(symbol: str,
                                     start: Optional[date] = None,
                                     end: Optional[date] = None,
                                     period: Optional[str] = None,
                                     interval: str = "1d",
                                     ):
    demo_symbols = validate_demo_symbols(symbols=symbol)
    allowed_symbols = validate_two_symbols_for_comparison(demo_symbols)

    if period is None and start is None and end is None:
        period = "1mo"

    config = build_market_config(
        symbols=allowed_symbols,
        start=start,
        end=end,
        period=period,
        interval=interval,
    )

    result = await get_multi_stock_comparison_prices(config)

    response = refine_symbol_based_api_output(
        raw_output=result, symbols=demo_symbols, mapping=MARKET_PRICE_MAPPING,
    )

    return response
