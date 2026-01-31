import pandas as pd
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.infrastecture.redis_cache.cache_market_ohlcv.cache_data import \
    fetch_sanitize_market_ohlcv_prices
from app.domain.earnings_event_price_impact_analyzer.build_earnings_event_dataframe import \
    analyze_earnings_multi_symbol
from app.pipeline.earnings_event_price_impact.earnings_calendar_generation import \
    fetch_earnings_calendar
from app.shared.utils.normalize_df import normalize_pipeline_output_df
from app.shared.logic_validators.dataframe_validations import require_dataframe


async def fetch_earnings_events_price_impact_data(
        config: MarketPriceConfig
) -> pd.DataFrame:
    # copy from redis cached data or sanitized raw data
    market_prices = await fetch_sanitize_market_ohlcv_prices(config)

    market_price = market_prices.copy()
    market_price["Date"] = pd.to_datetime(market_price["Date"])
    market_price = market_price.set_index("Date").sort_index()

    earnings_calendar = await fetch_earnings_calendar(config)

    # this function has problem
    earnings_df = analyze_earnings_multi_symbol(
        market_price, earnings_calendar, config.rolling_window,
    )

    earnings_df = normalize_pipeline_output_df(earnings_df)

    return require_dataframe(earnings_df, context="fetch_earnings_events_price_impact_data", )
