import pandas as pd


def add_cumulative_return(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
    df[f"Cumulative_Return_{symbol}"] = (
                                                1 + df[f"Daily_Return_{symbol}"]
                                        ).cumprod() - 1
    return df
