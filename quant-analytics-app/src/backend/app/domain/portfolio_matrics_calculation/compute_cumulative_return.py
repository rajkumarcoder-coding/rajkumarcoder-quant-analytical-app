import pandas as pd


def compute_cumulative_return(portfolio_returns: pd.Series) -> float:
    return float((1 + portfolio_returns).prod() - 1)

# 3️⃣ Average portfolio return (NOT final performance)
# portfolio_returns.mean()