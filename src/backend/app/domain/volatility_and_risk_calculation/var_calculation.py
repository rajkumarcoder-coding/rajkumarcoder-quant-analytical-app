import pandas as pd


def compute_var(returns: pd.Series, confidence: float = 0.95) -> float:
    return returns.quantile(1 - confidence)

# var_95 = compute_var(returns, 0.95)