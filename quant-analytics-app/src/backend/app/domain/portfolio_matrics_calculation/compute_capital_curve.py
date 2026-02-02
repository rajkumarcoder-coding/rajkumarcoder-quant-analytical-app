import pandas as pd


def compute_capital_curve(
        returns: pd.Series,
        initial_capital: float = 100_000,
) -> pd.Series:
    return initial_capital * (1 + returns).cumprod()
