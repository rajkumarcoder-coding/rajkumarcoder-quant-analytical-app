import pandas as pd


def trend_signal(
        df: pd.DataFrame,
        *,
        symbol: str,
) -> int:
    ema = df[f"EMA_{symbol}"].iloc[-1]
    sma = df[f"SMA_{symbol}"].iloc[-1]

    return 1 if ema > sma else -1
