import pandas as pd


def compute_gap(close: pd.Series, event_pos: int) -> float:
    gap = (
        (close.iloc[event_pos + 1] - close.iloc[event_pos])
        / close.iloc[event_pos]
        if event_pos + 1 < len(close)
        else 0.0
    )
    return float(gap)
