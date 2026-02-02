from typing import List
import pandas as pd
from app.shared.utils.str_to_list import str_to_list
from app.shared.logic_validators.column_validation import require_columns


def get_symbol_column_names(
        df: pd.DataFrame,
        cols_names: str,
        symbols: str,
) -> List[str]:
    col_prefixes = str_to_list(cols_names)
    symbol_list = str_to_list(symbols)

    # Build dynamic column list
    selected_cols: List[str] = []

    for prefix in col_prefixes:
        for symbol in symbol_list:
            col_name = f"{prefix}_{symbol}"
            if col_name in df.columns:
                selected_cols.append(col_name)

    selected_cols = require_columns(
        df=df,
        columns=selected_cols,
        context="df_select_cols_with_index",
        reason="missing_select_columns",
        expected={
            "prefixes": col_prefixes,
            "symbols": symbol_list,
            "pattern": "col_prefixes_<SYMBOL>",
        },
    )

    return selected_cols
