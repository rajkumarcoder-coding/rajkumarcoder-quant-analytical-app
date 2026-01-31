import pandas as pd
from typing import Dict


def compute_avg_daily_returns(
        daily_returns: pd.DataFrame,
) -> Dict[str, float]:
    return daily_returns.mean().to_dict()
