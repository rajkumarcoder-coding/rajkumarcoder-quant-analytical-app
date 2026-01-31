import pandas as pd


def volume_confirmation(df: pd.DataFrame, symbol: str) -> int:
    return (
        1 if df[f"Volume_Spike_{symbol}"].iloc[-1] > 1.2
        else 0
    )
