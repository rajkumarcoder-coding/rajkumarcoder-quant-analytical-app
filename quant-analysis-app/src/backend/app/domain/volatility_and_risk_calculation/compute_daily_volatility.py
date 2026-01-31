import pandas as pd


def add_daily_volatility(daily_returns: pd.Series) -> pd.Series:
    return daily_returns.pct_change()
