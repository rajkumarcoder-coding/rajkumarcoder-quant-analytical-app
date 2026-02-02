import pandas as pd


def compute_earnings_impact(
        returns: pd.Series,
        event_pos: int,
        window: int,
        symbol: str,
) -> dict:
    # 3️⃣ Compute metrics
    pre_returns = returns.iloc[event_pos - window:event_pos]
    post_returns = returns.iloc[event_pos + 1:event_pos + 1 + window]

    return {
        f"event_day_return_{symbol}": float(returns.iloc[event_pos]),
        f"pre_return_{symbol}": float(pre_returns.sum()),
        f"post_return_{symbol}": float(post_returns.sum()),
        f"volatility_pre_{symbol}": float(pre_returns.std()),
        f"volatility_post_{symbol}": float(post_returns.std()),
    }
