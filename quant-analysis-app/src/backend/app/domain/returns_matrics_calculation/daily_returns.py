import pandas as pd


def add_daily_return(df: pd.DataFrame, close_col: str, symbol: str) -> pd.DataFrame:
    df[f"Daily_Return_{symbol}"] = df[close_col].pct_change()
    return df
