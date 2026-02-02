import pandas as pd
from app.core_configs.exceptions import ValidationError


def compute_sma(
        close: pd.Series,
        window: int,
) -> pd.Series:
    if window <= 0:
        raise ValidationError(
            message="SMA window must be positive",
            reason=f"SMA window must be positive: {window}",
        )

    return close.rolling(window=window).mean()
