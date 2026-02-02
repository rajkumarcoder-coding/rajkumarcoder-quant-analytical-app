from typing import List
import pandas as pd
from app.core_configs.exceptions import AnalysisError


def require_columns(
        *,
        df: pd.DataFrame,
        columns: List[str],
        context: str,
        reason: str,
        expected: dict | None = None,
) -> List[str]:
    """
    Ensure required columns are present in a DataFrame.

    Returns:
        The validated columns (unchanged) if present.
    """
    if not columns:
        raise AnalysisError(
            message="Required columns not found in DataFrame",
            reason=reason,
            context={
                "at": context,
                "expected": expected,
                "available_columns": list(df.columns),
            },
        )

    return columns
