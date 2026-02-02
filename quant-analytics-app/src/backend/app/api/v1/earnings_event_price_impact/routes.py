from fastapi import APIRouter
from typing import Optional
from datetime import date
from app.shared.http_input_validations.validate_demo_symbols import validate_demo_symbols
from app.services.eranings_event_price_impact.services import get_earnings_event_price_impact
from app.domain.market_ohlcv_data_classes.build_data_configs import build_market_config
from app.api.v1.earnings_event_price_impact.validate_earnings_data_range import \
    validate_earnings_data_range
from app.api.v1.earnings_event_price_impact.api_res_mapping import field_map
from app.shared.helper.render_api_response import map_dataframe_json_api_response
from app.api.v1.earnings_event_price_impact.res_schema import EarningsImpactResponse

router = APIRouter(prefix="/market", tags=["Market"])


@router.get("/{symbol}/earnings/impact", response_model=EarningsImpactResponse)
async def earnings_impact_endpoint(symbol: str,
                                   start: Optional[date] = None,
                                   end: Optional[date] = None,
                                   period: Optional[str] = None,
                                   interval: str = "1d",
                                   rolling_window: int = 20,
                                   ):
    demo_symbols = validate_demo_symbols(symbols=symbol)

    if period is None and start is None and end is None:
        period = "5y"

    validate_earnings_data_range(
        period=period,
        start=start,
        end=end,
    )

    config = build_market_config(
        symbols=demo_symbols,
        start=start,
        end=end,
        period=period,
        interval=interval,
        rolling_window=rolling_window,
    )

    result = await get_earnings_event_price_impact(config)

    raw_res = {
        "earnings_impact_data": result.data,
    }

    response = map_dataframe_json_api_response(raw_res, field_map, "earnings_impact")

    return response
