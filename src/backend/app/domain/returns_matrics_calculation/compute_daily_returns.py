import pandas as pd


def compute_daily_returns(prices: pd.Series) -> pd.Series:
    return prices.pct_change().fillna(0.0)
