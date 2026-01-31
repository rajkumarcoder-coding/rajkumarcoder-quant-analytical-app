from typing import Set, Tuple, Any
import pandas as pd
from app.core_configs.exceptions import AnalysisError


def extract_symbol(col: Any) -> str | None:
    """
    Extract symbol from DataFrame column.

    Supports:
    - 'Close_AAPL'
    - ('Close', 'AAPL')  ← MultiIndex
    """
    if isinstance(col, tuple):
        return col[-1]
    if isinstance(col, str) and "_" in col:
        return col.split("_")[-1]
    return None


# applicable for multiindex dataframe
def validate_no_partial_symbol_failure(
        df: pd.DataFrame,
        expected_symbols: Set[str],
        *,
        context: str,
) -> None:
    """
    Ensure that all expected symbols are present in the DataFrame.
    Handles yfinance MultiIndex and flat columns.
    """

    available_symbols = {
        extract_symbol(col)
        for col in df.columns
        if extract_symbol(col) is not None
    }

    missing = expected_symbols - available_symbols

    if missing:
        raise AnalysisError(
            message="Some symbols returned no data",
            reason="partial_symbol_failure",
            context={
                "at": context,
                "missing_symbols": sorted(missing),
                "available_symbols": sorted(available_symbols),
            },
        )


# not applicable for multiindex dataframe
def detect_partial_symbol_failure(
        df: pd.DataFrame,
        expected_symbols: Set[str],
) -> Tuple[Set[str], Set[str]]:
    """
    Detect missing symbols in provider output.

    Returns:
        available_symbols, missing_symbols
    """

    available_symbols = {
        col.split("_")[-1]
        for col in df.columns
        if "_" in col
    }

    missing_symbols = expected_symbols - available_symbols

    return available_symbols, missing_symbols
