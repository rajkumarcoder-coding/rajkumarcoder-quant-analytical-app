import pandas as pd


def momentum_signal(df: pd.DataFrame, symbol: str) -> int:
    return (
        1 if df[f"Momentum_{symbol}"].iloc[-1] > 0
        else -1
    )
