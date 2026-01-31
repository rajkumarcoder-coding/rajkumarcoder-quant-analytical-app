import pandas as pd
from app.core_configs.exceptions import ValidationError


def compute_ema(
        close: pd.Series,
        span: int,
) -> pd.Series:
    if span <= 0:
        raise ValidationError(
            message="EMA span must be positive",
            reason=f"EMA span must be positive: {span}",
        )

    return close.ewm(span=span, adjust=False).mean()
