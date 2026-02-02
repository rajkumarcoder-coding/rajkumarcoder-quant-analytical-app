from typing import List
import pandas as pd
from app.domain.returns_matrics_calculation.daily_returns import \
    add_daily_return
from app.domain.volatility_and_risk_calculation.compute_daily_volatility import \
    add_daily_volatility
from app.domain.volatility_and_risk_calculation.compute_drawdown_series import \
    compute_drawdown_series
from app.shared.logic_validators.dataframe_validations import require_dataframe


def add_risk_metrics_pipeline(
        df: pd.DataFrame,
        close_cols: List[str],
) -> pd.DataFrame:
    # copy from redis cached data or sanitized raw data
    df = df.copy()

    for close_col in close_cols:
        symbol = close_col.replace("Close_", "")

        df = add_daily_return(df, close_col, symbol)
        df[f"Daily_Volatility_{symbol}"] = add_daily_volatility(
            df[f"Daily_Return_{symbol}"],
        )
        df[f"Drawdown_{symbol}"] = compute_drawdown_series(
            df[f"Close_{symbol}"],
        )

    return require_dataframe(df, context="add_risk_metrics_pipeline", )
