from typing import List
import pandas as pd
from app.domain.returns_matrics_calculation.compute_daily_returns import compute_daily_returns
from app.domain.portfolio_matrics_calculation.compute_drawdown_series import \
    compute_drawdown_series

from app.shared.logic_validators.dataframe_validations import require_dataframe


def add_portfolio_analyzer_pipeline(
        df: pd.DataFrame,
        close_cols: List[str],
) -> pd.DataFrame:
    # copy from redis cached data or sanitized raw data
    df = df.copy()

    for close_col in close_cols:
        symbol = close_col.replace("Close_", "")

        df[f"Daily_Return_{symbol}"] = compute_daily_returns(df[f"Close_{symbol}"])
        df[f"Drawdown_{symbol}"] = compute_drawdown_series(df[f"Daily_Return_{symbol}"])

    return require_dataframe(df, context="add_return_metrics_pipeline", )
