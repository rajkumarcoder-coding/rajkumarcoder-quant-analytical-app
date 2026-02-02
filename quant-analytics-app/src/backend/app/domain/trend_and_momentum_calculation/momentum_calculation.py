import pandas as pd
from app.core_configs.exceptions import ValidationError


# Momentum = Close(t) − Close(t−n)

def compute_momentum(
        close: pd.Series,
        window: int,
) -> pd.Series:
    if window <= 0:
        raise ValidationError(
            message="Momentum window must be positive",
            reason=f"Momentum window must be positive: {window}",
        )

    return close - close.shift(window)
