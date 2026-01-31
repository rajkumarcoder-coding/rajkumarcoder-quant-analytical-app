import pandas as pd
import numpy as np


def compute_trend_strength(
        close: pd.Series,
        lookback: int
) -> float:
    trend = (
        close.rolling(lookback)
        .apply(lambda x: np.polyfit(range(len(x)), x, 1)[0], raw=False)
    )

    return trend.iloc[-1]
