from fastapi import APIRouter
from typing import Optional
from datetime import date
from app.shared.http_input_validations.validate_demo_symbols import validate_demo_symbols
from app.services.portfolio_return_analyzer.services import get_portfolio_returns
from app.domain.market_ohlcv_data_classes.portfolio_configs import portfolio_analyze_endpoint
from app.shared.helper.parse_weights import parse_weights
from app.shared.utils.str_to_list import str_to_list
from app.shared.helper.render_portfolio_api_response import reshape_portfolio_api_response_v2
from app.api.v1.portfolio_return_analyzer.res_schema import PortfolioAnalysisResponse

router = APIRouter(prefix="/market", tags=["Market"])


@router.get("/{symbol}/portfolio/analysis", response_model=PortfolioAnalysisResponse)
async def portfolio_return_endpoint(symbol: str,
                                    start: Optional[date] = None,
                                    end: Optional[date] = None,
                                    period: Optional[str] = None,
                                    interval: str = "1d",
                                    rolling_window: int = 20,
                                    trading_date: int = 252,
                                    weights: str = None,
                                    initial_capital: float = 100_000,
                                    ):
    demo_symbols = validate_demo_symbols(symbols=symbol)
    valid_weights = parse_weights(weights=weights)

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
        "weights": valid_weights,
        "initial_capital": initial_capital,
    }

    config = portfolio_analyze_endpoint(payload=payload)

    result = await get_portfolio_returns(config)

    data = result.data
    metrics = result.metrics

    symbol_list = str_to_list(demo_symbols)

    raw_response = reshape_portfolio_api_response_v2(
        data, symbol_list,
    )
    response = {
        "portfolio_data": raw_response,
        "portfolio_analysis": metrics,
    }

    return response
