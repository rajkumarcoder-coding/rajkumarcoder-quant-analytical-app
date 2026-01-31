from typing import List
import pandas as pd
from app.domain.returns_matrics_calculation.daily_returns import \
    add_daily_return
from app.domain.trend_and_momentum_calculation.sma_calculation import compute_sma
from app.domain.trend_and_momentum_calculation.ema_calculation import compute_ema
from app.domain.trend_and_momentum_calculation.momentum_calculation import compute_momentum
from app.domain.trend_and_momentum_calculation.roc_calculation import compute_roc
from app.domain.volatility_and_risk_calculation.atr_calculation import compute_atr
from app.domain.trend_and_momentum_calculation.compute_volume_sma import compute_volume_sma
from app.domain.trend_and_momentum_calculation.compute_volume_spike import compute_volume_spike
from app.domain.trend_and_momentum_calculation.obv_calculation import compute_obv
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.shared.logic_validators.dataframe_validations import require_dataframe


def add_technical_indicators_pipeline(
        df: pd.DataFrame,
        close_cols: List[str],
        config: MarketPriceConfig,
) -> pd.DataFrame:
    # copy from redis cached data or sanitized raw data
    df = df.copy()

    for close_col in close_cols:
        symbol = close_col.replace("Close_", "")

        # price indicators
        df = add_daily_return(df, close_col, symbol)
        df[f"SMA_{symbol}"] = compute_sma(df[close_col], config.rolling_window)
        df[f"EMA_{symbol}"] = compute_ema(df[close_col], config.rolling_window)
        df[f"Momentum_{symbol}"] = compute_momentum(df[close_col], config.rolling_window)
        df[f"ROC_{symbol}"] = compute_roc(df[close_col], config.rolling_window)
        df[f"ATR_{symbol}"] = compute_atr(
            df[f"High_{symbol}"], df[f"Low_{symbol}"], df[close_col], config.rolling_window,
        )

        # volume indicators
        df[f"Volume_SMA_{symbol}"] = compute_volume_sma(
            df[f"Volume_{symbol}"], config.rolling_window,
        )
        df[f"Volume_Spike_{symbol}"] = compute_volume_spike(
            df[f"Volume_{symbol}"], config.rolling_window,
        )
        df[f"OBV_{symbol}"] = compute_obv(df[close_col], df[f"Volume_{symbol}"])

    return require_dataframe(df, context="add_technical_indicators_pipeline", )
