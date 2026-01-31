import pandas as pd
from app.domain.earnings_event_price_impact_analyzer.compute_earnings_impact import \
    compute_earnings_impact
from app.domain.earnings_event_price_impact_analyzer.compute_gap import compute_gap
from app.shared.logic_validators.dataframe_validations import require_dataframe


def build_earnings_event_dataframe(
        df: pd.DataFrame,
        symbol: str,
        earnings_dates: list[pd.Timestamp],
        window: int,
) -> pd.DataFrame:
    close_col = f"Close_{symbol}"
    if close_col not in df.columns:
        return pd.DataFrame()

    df = df.sort_index()
    results = []

    for event_date in earnings_dates:
        event_date = pd.to_datetime(event_date)

        if event_date < df.index.min() or event_date > df.index.max():
            continue

        if df.index.tz is not None:
            event_date = event_date.tz_localize(df.index.tz)

        event_pos = df.index.searchsorted(event_date, side="right") - 1

        if event_pos < 0 or event_pos >= len(df):
            continue

        if event_pos < window or event_pos + window >= len(df):
            continue

        window_df = df.iloc[event_pos - window: event_pos + window + 1]

        close = window_df[close_col]
        returns = close.pct_change().fillna(0.0)

        metrics = compute_earnings_impact(
            returns=returns,
            event_pos=window,
            window=window,
            symbol=symbol,
        )

        metrics[f"gap_{symbol}"] = compute_gap(close, window)
        metrics["Date"] = df.index[event_pos].strftime("%Y-%m-%d")

        results.append(metrics)

    return require_dataframe(
        pd.DataFrame(results),
        context="build_earnings_event_dataframe, period or start/end date must be above one year",
    )


def analyze_earnings_multi_symbol(
        df: pd.DataFrame,
        earnings_calendar: dict[str, list[pd.Timestamp]],
        window: int,
) -> pd.DataFrame:
    """
    Analyze earnings impact for multiple symbols using a single wide dataframe.
    Column-wise (suffix-based) multi-symbol output.
    """

    merged_df = None

    for symbol, earnings_dates in earnings_calendar.items():
        symbol_df = build_earnings_event_dataframe(
            df=df,
            symbol=symbol,
            earnings_dates=earnings_dates,
            window=window,
        )

        if symbol_df.empty:
            continue

        # symbol_df = symbol_df.set_index("date").astype(str)

        # ensure date is index for join
        symbol_df = symbol_df.set_index("Date")

        # suffix all metric columns with symbol
        # symbol_df = symbol_df.add_suffix(f"_{symbol}")

        merged_df = (
            symbol_df if merged_df is None
            else merged_df.join(symbol_df, how="outer")
        )

    if merged_df is None:
        return pd.DataFrame()

    return require_dataframe(
        merged_df,
        context="analyze_earnings_multi_symbol",
    )
