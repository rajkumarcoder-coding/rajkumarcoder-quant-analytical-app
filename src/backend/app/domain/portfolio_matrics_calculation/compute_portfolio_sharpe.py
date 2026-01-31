import pandas as pd


# Short, correct answer

# This is a PORTFOLIO-LEVEL computation.
# It is NOT per-symbol.

def compute_portfolio_sharpe(
        portfolio_returns: pd.Series,
) -> float:
    if isinstance(portfolio_returns, pd.DataFrame):
        raise TypeError(
            "compute_portfolio_sharpe expects pd.Series, not DataFrame",
        )

    mean_return = portfolio_returns.mean()
    volatility = portfolio_returns.std()

    if float(volatility) == 0.0:
        return 0.0

    return float(mean_return / volatility)
