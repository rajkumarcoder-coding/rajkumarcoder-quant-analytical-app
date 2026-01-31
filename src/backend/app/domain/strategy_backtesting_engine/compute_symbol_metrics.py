import numpy as np
import pandas as pd
from app.core_configs.exceptions import ValidationError


def compute_symbol_metrics_from_wide_df(
        df: pd.DataFrame,
        symbol: str,
        risk_free_rate: float = 0.0,
) -> dict:
    """
    Compute metrics for ONE symbol from a wide multi-symbol DataFrame.
    """

    ret_col = f"Strategy_Return_{symbol}"
    eq_col = f"Equity_{symbol}"
    dd_col = f"Drawdown_{symbol}"
    pos_col = f"Position_{symbol}"

    # ---- Safety checks ----
    required_cols = [ret_col, eq_col, dd_col, pos_col]
    for col in required_cols:
        if col not in df.columns:
            raise ValidationError(
                message=f"Missing column: {col}",
                reason=f"Column: {col}",
            )

    returns = df[ret_col].dropna()

    # ---- Total Return ----
    total_return = df[eq_col].iloc[-1] - 1

    # ---- Max Drawdown ----
    max_drawdown = df[dd_col].min()

    # ---- Sharpe Ratio ----
    if returns.std() != 0:
        sharpe_ratio = (
                               (returns.mean() - risk_free_rate) / returns.std()
                       ) * np.sqrt(252)
    else:
        sharpe_ratio = 0.0

    # ---- Trade metrics ----
    position_change = df[pos_col].diff().fillna(0)
    trade_entries = position_change != 0

    num_trades = int(trade_entries.sum())

    trade_panels = returns[trade_entries]

    win_rate = (
        (trade_panels > 0).sum() / num_trades
        if num_trades > 0
        else 0.0
    )

    return {
        "total_return": float(total_return),
        "max_drawdown": float(max_drawdown),
        "sharpe_ratio": float(sharpe_ratio),
        "win_rate": float(win_rate),
        "num_trades": int(num_trades),
    }


def compute_metrics_for_all_symbols(
        df: pd.DataFrame,
        symbols: list[str],
) -> dict[str, dict]:
    metrics_by_symbol = {}

    for symbol in symbols:
        metrics_by_symbol[symbol] = compute_symbol_metrics_from_wide_df(
            df=df,
            symbol=symbol,
        )

    return metrics_by_symbol
