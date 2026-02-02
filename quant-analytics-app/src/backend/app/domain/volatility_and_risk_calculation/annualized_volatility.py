import numpy as np


def compute_annualized_volatility(daily_volatility: float) -> float:
    return daily_volatility * np.sqrt(252)
