from typing import Set
import pandas as pd


def extract_symbol_from_column(col) -> str | None:
    """
    Extract symbol from DataFrame column.
    Supports:
    - 'Close_AAPL'
    - ('Close', 'AAPL')
    """
    if isinstance(col, tuple):
        return col[-1]  # MultiIndex → symbol is last
    if isinstance(col, str) and "_" in col:
        return col.split("_")[-1]
    return None


def detect_all_nan_symbols(
        df: pd.DataFrame,
        expected_symbols: Set[str],
) -> Set[str]:
    """
    Detect symbols whose columns exist but contain only NaN values.
    """

    nan_only_symbols: Set[str] = set()

    for symbol in expected_symbols:
        symbol_cols = [
            col for col in df.columns
            if extract_symbol_from_column(col) == symbol
        ]

        if not symbol_cols:
            continue

        symbol_df = df[symbol_cols]

        if symbol_df.isna().all().all():
            nan_only_symbols.add(symbol)

    return nan_only_symbols
