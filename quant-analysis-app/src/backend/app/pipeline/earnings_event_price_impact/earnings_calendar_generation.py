import pandas as pd
from app.infrastecture.redis_cache.cache_fundamentals.cache_data import \
    fetch_sanitize_market_fundamentals
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.shared.utils.str_to_list import str_to_list


def extract_earnings_dates(earnings_dates) -> list[pd.Timestamp]:
    """
    Normalize yfinance earnings dates into clean, timezone-naive trading dates.
    """

    if earnings_dates is None or earnings_dates.empty:
        return []

    dates: list[pd.Timestamp] = []

    for ts in earnings_dates.index:
        if pd.isna(ts):
            continue

        ts = pd.to_datetime(ts)

        # Remove timezone if present
        if ts.tzinfo is not None:
            ts = ts.tz_convert(None)

        # Normalize to date
        dates.append(ts.normalize())

    return sorted(set(dates))


async def fetch_earnings_calendar(
        config: MarketPriceConfig,
) -> dict[str, list[pd.Timestamp]]:
    symbols = str_to_list(config.symbols)
    calendar = {}

    for symbol in symbols:
        data = await fetch_sanitize_market_fundamentals(config)
        dates = extract_earnings_dates(data.get("earnings_dates"))
        calendar[symbol] = dates

    return calendar
