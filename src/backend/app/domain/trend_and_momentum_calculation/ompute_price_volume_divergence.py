import pandas as pd
from app.core_configs.exceptions import ValidationError


def compute_price_volume_divergence(
        close: pd.Series,
        volume: pd.Series,
        window: int,
) -> pd.Series:
    if span <= 0:
        raise ValidationError(
            message="price volume divergence window must be positive",
            reason=f"price volume divergence window must be positive: {window}",
        )

    price_trend = close.diff(window)
    volume_trend = volume.diff(window)
    return price_trend * volume_trend
