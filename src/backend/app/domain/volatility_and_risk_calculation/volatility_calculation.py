import pandas as pd
from typing import Dict


def compute_volatility(
        daily_returns: pd.DataFrame,
) -> Dict[str, float]:
    # if daily_returns.empty or daily_returns.shape[1] < 2:
    #     return {}

    if daily_returns.empty or len(daily_returns) < 2:
        # explicit, honest behavior
        return {col: 0.0 for col in daily_returns.columns}
    return daily_returns.std().to_dict()


def compute_normal_daily_volatility(returns: pd.Series) -> float:
    return returns.std()
