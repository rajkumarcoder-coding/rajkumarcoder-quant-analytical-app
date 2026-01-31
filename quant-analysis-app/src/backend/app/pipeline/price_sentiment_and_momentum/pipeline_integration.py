import pandas as pd
from typing import Dict, Any
from app.domain.market_ohlcv_data_classes.price_sentiment import PriceSentimentEngineRequest
from app.infrastecture.redis_cache.cache_market_ohlcv.cache_data import \
    fetch_sanitize_market_ohlcv_prices
from app.shared.utils.str_to_list import str_to_list
from app.domain.price_based_sentiment_and_momentum.compute_sentiments import \
    compute_sentiment_multi_symbol


async def fetch_price_based_sentiment_data(
        config: PriceSentimentEngineRequest
) -> Dict[str, Any]:
    # copy from redis cached data or sanitized raw data
    market_prices = await fetch_sanitize_market_ohlcv_prices(config.market)

    market_price = market_prices.copy()
    market_price["Date"] = pd.to_datetime(market_price["Date"])
    market_price = market_price.set_index("Date").sort_index()

    symbol_list = str_to_list(config.market.symbols)

    sentiment = compute_sentiment_multi_symbol(
        market_price, symbol_list, config.price_sentiment.lookback,
    )

    return sentiment
