import pandas as pd


def compute_sharpe_ratio(
        returns: pd.Series,
        volatility: float,
) -> float:
    mean_return = returns.mean()
    return mean_return / volatility if volatility != 0 else 0.0
