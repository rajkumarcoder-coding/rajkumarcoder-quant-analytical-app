import pandas as pd


def compute_regime_metrics(df: pd.DataFrame, symbol: str) -> dict:
    """
    Compute summary regime metrics from regime time series.

    Expected columns in df:
    - Risk_State
    - Volatility_Regime
    - Trend_Regime
    """

    if df.empty:
        return {
            "dominant_regime": None,
            "high_vol_ratio": 0.0,
            "uptrend_ratio": 0.0,
        }

    # --- dominant regime ---
    dominant_regime = (
        df[f"Risk_State_{symbol}"]
        .value_counts()
        .idxmax()
    )

    # --- ratios ---
    high_vol_ratio = (
        (df[f"Volatility_Regime_{symbol}"] == "high")
        .mean()
    )

    uptrend_ratio = (
        (df[f"Trend_Regime_{symbol}"] == "uptrend")
        .mean()
    )

    return {
        "dominant_regime": dominant_regime,
        "high_vol_ratio": round(float(high_vol_ratio), 4),
        "uptrend_ratio": round(float(uptrend_ratio), 4),
    }


def compute_market_regime_metrics_for_all_symbols(
        df: pd.DataFrame,
        symbols: list[str],
) -> dict[str, dict]:
    metrics_by_symbol = {}

    for symbol in symbols:
        metrics_by_symbol[symbol] = compute_regime_metrics(
            df=df,
            symbol=symbol,
        )

    return metrics_by_symbol
