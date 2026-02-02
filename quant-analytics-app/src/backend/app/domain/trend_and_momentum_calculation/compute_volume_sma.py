import pandas as pd
from app.core_configs.exceptions import ValidationError


def compute_volume_sma(
        volume: pd.Series,
        window: int,
) -> pd.Series:
    if window <= 0:
        raise ValidationError(
            message="Volume SMA window must be positive",
            reason=f"Volume SMA window must be positive: {window}",
        )

    return volume.rolling(window).mean()
