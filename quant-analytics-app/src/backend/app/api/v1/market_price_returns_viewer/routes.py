from fastapi import APIRouter
from typing import Optional
from datetime import date
from app.shared.http_input_validations.validate_demo_symbols import validate_demo_symbols
from app.services.market_price_returns_viewer.services import get_market_data_prices
from app.api.v1.market_price_returns_viewer.api_res_mapping import field_map
from app.domain.market_ohlcv_data_classes.build_data_configs import build_market_config
from app.shared.helper.render_api_response import map_dataframe_json_api_response
from app.api.v1.market_price_returns_viewer.res_schemas import \
    MultiSymbolMarketPriceResponse

router = APIRouter(prefix="/market", tags=["Market"])


@router.get("/{symbol}/price", response_model=MultiSymbolMarketPriceResponse)
async def market_prices_endpoint(symbol: str,
                                 start: Optional[date] = None,
                                 end: Optional[date] = None,
                                 period: Optional[str] = None,
                                 interval: str = "1d",
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
    )

    result = await get_market_data_prices(config)

    raw_res = {
        "daily_returns_data": result.data,
    }

    response = map_dataframe_json_api_response(raw_res, field_map, "daily_returns")

    return response
