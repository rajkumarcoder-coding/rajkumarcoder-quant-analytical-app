import pandas as pd


def compute_portfolio_volatility(portfolio_returns: pd.Series) -> float:
    return float(portfolio_returns.std())
