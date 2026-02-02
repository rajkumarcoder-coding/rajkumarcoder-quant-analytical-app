import pandas as pd
from app.core_configs.exceptions import ValidationError


def compute_atr(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        window: int,
) -> pd.Series:
    if window <= 0:
        raise ValidationError(
            message="ATR span must be positive",
            reason=f"ATR span must be positive: {span}",
        )

    prev_close = close.shift(1)

    tr = pd.concat(
        [
            high - low,
            (high - prev_close).abs(),
            (low - prev_close).abs(),
        ], axis=1,
    ).max(axis=1)

    return tr.rolling(window=window).mean()
