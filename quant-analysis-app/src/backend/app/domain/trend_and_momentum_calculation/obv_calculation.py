import pandas as pd


def compute_obv(
        close: pd.Series,
        volume: pd.Series,
) -> pd.Series:
    direction = close.diff().fillna(0).apply(
        lambda x: 1 if x > 0 else (-1 if x < 0 else 0),
    )
    return (direction * volume).cumsum()
