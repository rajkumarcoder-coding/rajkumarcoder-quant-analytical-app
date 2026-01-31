from typing import List
import pandas as pd
from app.domain.returns_matrics_calculation.compute_daily_returns import compute_daily_returns
from app.domain.strategy_backtesting_engine.compute_backtesting_strategy import compute_ma_strategy
from app.domain.market_ohlcv_data_classes.backtesting_engine import BacktestingEngineRequest
from app.shared.logic_validators.dataframe_validations import require_dataframe


def add_backtesting_engine_pipeline(
        df: pd.DataFrame,
        close_cols: List[str],
        config: BacktestingEngineRequest
) -> pd.DataFrame:
    # copy from redis cached data or sanitized raw data
    df = df.copy()

    for close_col in close_cols:
        symbol = close_col.replace("Close_", "")

        df[f"Daily_Return_{symbol}"] = compute_daily_returns(df[f"Close_{symbol}"])

        results = compute_ma_strategy(
            close=df[f"Close_{symbol}"],
            sma_fast_window=config.backtesting.fast_window,
            sma_slow_window=config.backtesting.slow_window,
            ema_fast_window=config.backtesting.fast_window,
            ema_slow_window=config.backtesting.slow_window,
        )

        for key, series in results.items():
            if isinstance(series, pd.Series) and not series.isna().all():
                df[f"{key}_{symbol}"] = series

    return require_dataframe(df, context="add_return_metrics_pipeline", )
