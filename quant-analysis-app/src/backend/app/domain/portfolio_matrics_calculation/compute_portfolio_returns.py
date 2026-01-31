import pandas as pd
from typing import Dict


def compute_portfolio_returns(
        returns_df: pd.DataFrame,
        weights: Dict[str, float],
) -> pd.Series:
    """
    returns_df: columns = symbols, rows = daily returns
    """
    weight_series = pd.Series(weights)
    return returns_df.mul(weight_series, axis=1).sum(axis=1)
