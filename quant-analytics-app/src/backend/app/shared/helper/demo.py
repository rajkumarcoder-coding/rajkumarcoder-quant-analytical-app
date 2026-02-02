# src/app/analytics/signal_engine.py
import pandas as pd
from typing import Dict


def compute_signals(
        df: pd.DataFrame,
) -> Dict[str, str | int]:
    """
    Computes rule-based trading signals from indicators.
    """

    signals = {
        "trend": (
            "bullish"
            if df["EMA"].iloc[-1] > df["SMA"].iloc[-1]
            else "bearish"
        ),
        "momentum": (
            "positive"
            if df["Momentum"].iloc[-1] > 0
            else "negative"
        ),
        "volatility_regime": (
            "high"
            if df["ATR"].iloc[-1]
               > df["ATR"].rolling(20).mean().iloc[-1]
            else "low"
        ),
        "volume_confirmation": (
            "strong"
            if df["Volume_Spike"].iloc[-1] > 1.2
            else "weak"
        ),
    }

    # ---- Composite signal ----
    score = (
        (1 if signals["trend"] == "bullish" else -1)
        + (1 if signals["momentum"] == "positive" else -1)
        + (1 if signals["volume_confirmation"] == "strong" else 0)
    )

    signals["composite"] = (
        "bullish" if score >= 2
        else "bearish" if score <= -2
        else "neutral"
    )

    return signals
