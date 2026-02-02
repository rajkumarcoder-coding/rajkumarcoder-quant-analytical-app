import pandas as pd


def add_total_return(df: pd.DataFrame, close_col: str, symbol: str) -> pd.DataFrame:
    total_return = (
        df[close_col].iloc[-1] / df[close_col].iloc[0] - 1
        if len(df) > 1
        else 0
    )
    df[f"Total_Return_{symbol}"] = total_return
    return df
