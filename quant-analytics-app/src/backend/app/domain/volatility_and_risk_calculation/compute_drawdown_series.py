import pandas as pd


def compute_drawdown_series(prices: pd.Series) -> pd.Series:
    rolling_max = prices.cummax()
    drawdown = (prices / rolling_max) - 1
    return drawdown


def compute_max_drawdown(drawdown: pd.Series) -> float:
    return drawdown.min()
