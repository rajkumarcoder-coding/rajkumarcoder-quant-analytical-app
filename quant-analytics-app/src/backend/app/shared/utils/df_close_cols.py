import pandas as pd
from typing import List
from app.shared.logic_validators.column_validation import require_columns
from app.shared.utils.str_to_list import str_to_list


def get_close_columns_list(df: pd.DataFrame, symbols: str) -> List[str]:
    close_cols = [c for c in df.columns if c.startswith("Close_")]
    symbol_list = str_to_list(symbols)

    close_cols = require_columns(
        df=df,
        columns=close_cols,
        context="get_close_columns_list",
        reason="missing_close_columns",
        expected={
            "symbols": symbol_list,
            "pattern": "Close_<SYMBOL>",
        },
    )

    return close_cols
