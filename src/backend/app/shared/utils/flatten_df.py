from typing import Optional
import pandas as pd
from app.shared.logic_validators.dataframe_validations import require_dataframe


def flatten_df(df, symbol: Optional[str] = None) -> pd.DataFrame:
    # Case 1: MultiIndex (multiple tickers)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ["_".join([str(c) for c in col if c]) for col in df.columns]
        return df

    # Case 2: Single stock but want renamed columns with ticker prefix
    if symbol:
        df.columns = [
            f"{symbol}_{col}" if col not in ["Date"] else "Date"
            for col in df.columns
        ]
    return require_dataframe(df, context="flatten_df")
