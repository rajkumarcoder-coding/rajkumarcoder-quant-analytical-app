import pandas as pd
import numpy as np


def compute_regime_strategy(
        close: pd.Series,
        window: int,
) -> dict[str, pd.Series]:
    # --- returns ---
    returns = close.pct_change().fillna(0.0)

    # --- volatility regime ---
    rolling_vol = returns.rolling(window).std()
    threshold = rolling_vol.median()

    vol_regime = pd.Series(
        np.where(rolling_vol > threshold, "high", "low"),
        index=close.index,
        name="volatility_regime",
    )

    # --- trend regime ---
    ema_20 = close.ewm(span=20, adjust=False).mean()
    ema_50 = close.ewm(span=50, adjust=False).mean()

    trend_strength = ema_20 - ema_50

    trend_regime = pd.Series(
        np.where(trend_strength > 0, "uptrend", "downtrend"),
        index=close.index,
        name="trend_regime",
    )

    # --- risk state (combine volatility + trend) ---
    risk_state = pd.Series(index=close.index, dtype="object")

    risk_state[(vol_regime == "low") & (trend_regime == "uptrend")] = "risk_on"
    risk_state[(vol_regime == "low") & (trend_regime == "downtrend")] = "defensive"
    risk_state[(vol_regime == "high") & (trend_regime == "uptrend")] = "volatile_bull"
    risk_state[(vol_regime == "high") & (trend_regime == "downtrend")] = "risk_off"

    risk_state.name = "risk_state"

    return {
        "Returns": returns,
        "Volatility": rolling_vol,
        "Threshold": pd.Series(threshold, index=close.index),
        "Volatility_Regime": vol_regime,
        "Trend_Strength": trend_strength,
        "Trend_Regime": trend_regime,
        "Risk_State": risk_state,
    }
