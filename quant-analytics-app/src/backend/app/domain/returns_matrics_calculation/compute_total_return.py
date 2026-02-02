import pandas as pd
from typing import Dict


def compute_total_return(
        close_cols: pd.DataFrame,
) -> Dict[str, float]:
    """
    Compute total return per symbol from close price DataFrame.

    Assumes:
    - rows are ordered by time
    - columns are symbols
    """
    if close_cols.empty or len(close_cols) < 2:
        # explicit, honest behavior
        return {col: 0.0 for col in close_cols.columns}

    total_return = (close_cols.iloc[-1] / close_cols.iloc[0] - 1)

    return total_return.to_dict()
