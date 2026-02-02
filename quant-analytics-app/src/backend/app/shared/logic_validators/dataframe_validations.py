import pandas as pd
from app.core_configs.exceptions import AnalysisError


def require_dataframe(
        value,
        *,
        allow_empty: bool = False,
        context: str = "",
) -> pd.DataFrame:
    if not isinstance(value, pd.DataFrame):
        raise AnalysisError(
            message="Invalid DataFrame",
            reason="invalid_type",
            context={"expected": "DataFrame", "received": str(type(value)), "at": context},
        )

    if not allow_empty and value.empty:
        raise AnalysisError(
            message="No data returned from Yahoo Finance",
            reason="symbol_not_found_or_delisted",
            context={"at": context},
        )

    return value
