from fastapi import APIRouter
from typing import Optional
from datetime import date
from app.shared.http_input_validations.validate_demo_symbols import validate_demo_symbols
from app.services.market_regime_risk_detection.services import get_market_regime
from app.domain.market_ohlcv_data_classes.build_data_configs import build_market_config
from app.shared.helper.render_api_response import map_dataframe_and_metrics_json_api_response
from app.api.v1.market_regime_risk_detection.api_res_mapping import FIELD_NAME
from app.api.v1.market_regime_risk_detection.res_schema import MarketRegimeResponse

router = APIRouter(prefix="/market", tags=["Market"])


@router.get("/{symbol}/regime/analysis", response_model=MarketRegimeResponse)
async def market_regime_endpoint(symbol: str,
                                 start: Optional[date] = None,
                                 end: Optional[date] = None,
                                 period: Optional[str] = None,
                                 interval: str = "1d",
                                 rolling_window: int = 20,
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
    )

    result = await get_market_regime(config)

    data = result.data
    metrics = result.metrics

    raw_res = {
        "regime_data": data,
        "regime_analysis": metrics,
    }

    service_name = "regime"

    response = map_dataframe_and_metrics_json_api_response(raw_res, FIELD_NAME, service_name)

    return response
