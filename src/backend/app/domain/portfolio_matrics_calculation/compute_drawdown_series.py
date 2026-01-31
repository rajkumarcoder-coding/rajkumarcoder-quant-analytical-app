import pandas as pd


def compute_drawdown_series(returns: pd.Series) -> pd.Series:
    """
    returns: daily portfolio returns
    """
    equity_curve = (1 + returns).cumprod()
    rolling_max = equity_curve.cummax()
    drawdown = (equity_curve / rolling_max) - 1
    return drawdown


def compute_max_drawdown(drawdown: pd.Series) -> float:
    return float(drawdown.min())
