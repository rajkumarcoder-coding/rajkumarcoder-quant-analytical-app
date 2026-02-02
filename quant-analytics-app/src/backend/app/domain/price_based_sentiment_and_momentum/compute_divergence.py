import pandas as pd
import pandas as pd


def compute_divergence(
        close: pd.Series,
        volume: pd.Series
) -> float:
    price_change = close.pct_change()
    volume_change = volume.pct_change()

    divergence = price_change - volume_change

    return divergence.iloc[-1]
