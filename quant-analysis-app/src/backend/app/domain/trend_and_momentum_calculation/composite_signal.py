import pandas as pd
from app.domain.trend_and_momentum_calculation.trend_signal import trend_signal
from app.domain.trend_and_momentum_calculation.momentum_signal import momentum_signal
from app.domain.trend_and_momentum_calculation.volume_confirmation import volume_confirmation


def composite_signal(df: pd.DataFrame) -> str:
    score = (
            trend_signal(df)
            + momentum_signal(df)
            + volume_confirmation(df)
    )

    if score >= 2:
        return "bullish"
    if score <= -2:
        return "bearish"
    return "neutral"
