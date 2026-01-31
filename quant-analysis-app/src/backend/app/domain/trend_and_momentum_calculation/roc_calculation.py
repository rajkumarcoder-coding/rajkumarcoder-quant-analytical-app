import pandas as pd
from app.core_configs.exceptions import ValidationError


# ROC = (Close / Close.shift(n)) − 1

def compute_roc(
        close: pd.Series,
        window: int,
) -> pd.Series:
    if window <= 0:
        raise ValidationError(
            message="ROC window must be positive",
            reason=f"ROC window must be positive: {window}",
        )

    return close.pct_change(periods=window)
