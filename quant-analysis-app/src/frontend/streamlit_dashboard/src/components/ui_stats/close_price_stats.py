import pandas as pd


def close_price_stats(df: pd.DataFrame) -> dict:
    return {
        "mean": df["close"].mean(),
        "min": df["close"].min(),
        "max": df["close"].max(),
    }
