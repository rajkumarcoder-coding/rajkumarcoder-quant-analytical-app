from typing import List
import pandas as pd
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig
from app.domain.market_regime_and_risk_detection.compute_regime_and_risk_state import \
    compute_regime_strategy
from app.shared.logic_validators.dataframe_validations import require_dataframe


def add_market_regime_risk_detection_pipeline(
        df: pd.DataFrame,
        close_cols: List[str],
        config: MarketPriceConfig
) -> pd.DataFrame:
    # copy from redis cached data or sanitized raw data
    df = df.copy()

    for close_col in close_cols:
        symbol = close_col.replace("Close_", "")

        results = compute_regime_strategy(
            close=df[f"Close_{symbol}"],
            window=config.rolling_window,
        )

        for key, series in results.items():
            if isinstance(series, pd.Series) and not series.isna().all():
                df[f"{key}_{symbol}"] = series

    return require_dataframe(df, context="add_return_metrics_pipeline", )
