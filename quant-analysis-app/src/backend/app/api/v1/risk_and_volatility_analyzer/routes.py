from fastapi import APIRouter
from typing import Optional
from datetime import date
from app.shared.http_input_validations.validate_demo_symbols import validate_demo_symbols
from app.services.risk_and_volatility_analyzer.services import get_risk_analyzer
from app.api.v1.risk_and_volatility_analyzer.api_res_mapping import RISK_ANALYZER_MAPPING
from app.shared.utils.api_json_refining import refine_symbol_based_api_output
from app.domain.market_ohlcv_data_classes.build_data_configs import build_market_config
from app.shared.helper.embed_metrics_per_symbol import embed_metrics_per_symbol
from app.api.v1.risk_and_volatility_analyzer.res_schema import RiskResponse

router = APIRouter(prefix="/market", tags=["Market"])


@router.get("/{symbol}/risk/analysis", response_model=RiskResponse)
async def risk_analyzer_endpoint(symbol: str,
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

    result = await get_risk_analyzer(config)

    raw_response = refine_symbol_based_api_output(
        raw_output=result, symbols=demo_symbols, mapping=RISK_ANALYZER_MAPPING,
    )

    clean_response = embed_metrics_per_symbol(raw_response, context="Risk Analyzer")

    return clean_response
