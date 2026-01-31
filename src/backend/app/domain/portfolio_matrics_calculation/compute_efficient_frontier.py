import numpy as np
import pandas as pd


def simulate_portfolios(
        returns_df: pd.DataFrame,
        n_portfolios: int = 5000,
) -> pd.DataFrame:
    """
    Monte Carlo simulation of random portfolios.
    """

    symbols = returns_df.columns
    mean_returns = returns_df.mean()
    cov_matrix = returns_df.cov()

    results = []

    for _ in range(n_portfolios):
        weights = np.random.random(len(symbols))
        weights /= np.sum(weights)

        portfolio_return = np.dot(weights, mean_returns)
        portfolio_volatility = np.sqrt(
            np.dot(weights.T, np.dot(cov_matrix, weights)),
        )

        sharpe = (
            portfolio_return / portfolio_volatility
            if portfolio_volatility != 0
            else 0.0
        )

        results.append(
            {
                "return": portfolio_return,
                "volatility": portfolio_volatility,
                "sharpe_ratio": sharpe,
                "weights": dict(zip(symbols, weights)),
            },
        )

    return pd.DataFrame(results)
