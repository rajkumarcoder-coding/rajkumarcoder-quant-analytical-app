import pandas as pd
import numpy as np


def compute_ma_strategy(
        close: pd.Series,
        sma_fast_window: int,
        sma_slow_window: int,
        ema_fast_window: int,
        ema_slow_window: int,
) -> dict[str, pd.Series]:
    """
    Compute MA indicators and strategy metrics.

    Input:
    - close: pd.Series (price series)

    Returns:
    - dict of pd.Series:
      SMA_fast, SMA_slow, EMA_fast, EMA_slow,
      signal, position, strategy_return, equity, drawdown
    """

    # -------- Moving Averages --------
    sma_fast = close.rolling(window=sma_fast_window).mean()
    sma_slow = close.rolling(window=sma_slow_window).mean()

    ema_fast = close.ewm(span=ema_fast_window, adjust=False).mean()
    ema_slow = close.ewm(span=ema_slow_window, adjust=False).mean()

    # -------- Signal --------
    signal = pd.Series(
        np.where(
            ema_fast > ema_slow, 1,
            np.where(ema_fast < ema_slow, -1, 0),
        ),
        index=close.index,
    )

    # -------- Position (lagged signal) --------
    position = signal.shift(1).fillna(0)

    # -------- Strategy Return --------
    returns = close.pct_change().fillna(0)
    strategy_return = position * returns

    # -------- Equity Curve --------
    equity = (1 + strategy_return).cumprod()

    # -------- Drawdown --------
    rolling_max = equity.cummax()
    drawdown = (equity / rolling_max) - 1

    return {
        "SMA_Fast": sma_fast,
        "SMA_Slow": sma_slow,
        "EMA_Fast": ema_fast,
        "EMA_Slow": ema_slow,
        "Signal": signal,
        "Position": position,
        "Strategy_Return": strategy_return,
        "Equity": equity,
        "Drawdown": drawdown,
    }
