import pandas as pd


def compute_momentum(
        close: pd.Series,
        lookback: int
) -> float:
    momentum = close.pct_change(lookback)

    return momentum.iloc[-1]
