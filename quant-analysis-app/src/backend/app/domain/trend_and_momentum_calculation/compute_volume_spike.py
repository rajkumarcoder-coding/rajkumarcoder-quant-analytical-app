import pandas as pd
from app.domain.trend_and_momentum_calculation.compute_volume_sma import compute_volume_sma
from app.core_configs.exceptions import ValidationError


def compute_volume_spike(
        volume: pd.Series,
        window: int,
) -> pd.Series:
    if window <= 0:
        raise ValidationError(
            message="Volume spike window must be positive",
            reason=f"Volume spike window must be positive: {window}",
        )

    vol_sma = compute_volume_sma(volume, window)
    return volume / vol_sma
