import pandas as pd


def volatility_regime(df: pd.DataFrame, symbol: str) -> str:
    atr = df[f"ATR_{symbol}"].iloc[-1]
    atr_avg = df[f"ATR_{symbol}"].rolling(20).mean().iloc[-1]
    return "high" if atr > atr_avg else "low"
