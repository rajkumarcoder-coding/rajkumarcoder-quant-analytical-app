from fastapi import APIRouter
from typing import Optional
from datetime import date
from app.shared.http_input_validations.validate_demo_symbols import validate_demo_symbols
from app.services.price_based_sentiment.services import get_price_sentiment
from app.domain.market_ohlcv_data_classes.price_sentiment import build_price_sentiment_endpoint
from app.api.v1.price_based_sentiment.res_schema import MultiSymbolSentimentResponse

router = APIRouter(prefix="/market", tags=["Market"])


@router.get("/{symbol}/sentiment", response_model=MultiSymbolSentimentResponse)
async def price_sentiment_endpoint(symbol: str,
                                   start: Optional[date] = None,
                                   end: Optional[date] = None,
                                   period: Optional[str] = None,
                                   interval: str = "1d",
                                   lookback: int = 20,
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
        "lookback": lookback,
    }

    config = build_price_sentiment_endpoint(payload=payload)

    result = await get_price_sentiment(config)

    raw_res = {
        "price_sentiment_data": result,
    }

    return raw_res
