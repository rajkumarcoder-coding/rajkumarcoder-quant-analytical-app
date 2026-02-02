from typing import List
import pandas as pd
from app.domain.returns_matrics_calculation.daily_returns import \
    add_daily_return
from app.shared.logic_validators.dataframe_validations import require_dataframe


def add_comparison_metrics_pipeline(
        df: pd.DataFrame,
        close_cols: List[str],
) -> pd.DataFrame:
    # copy from redis cached data or sanitized raw data
    df = df.copy()

    for close_col in close_cols:
        symbol = close_col.replace("Close_", "")

        df = add_daily_return(df, close_col, symbol)

    return require_dataframe(df, context="add_return_metrics_pipeline", )
