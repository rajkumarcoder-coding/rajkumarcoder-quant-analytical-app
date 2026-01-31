import pandas as pd


def compute_earnings_metrics(event_df: pd.DataFrame) -> dict:
    if event_df.empty:
        return {}

    return {
        "avg_event_return": float(event_df["event_return"].mean()),
        "avg_pre_return": float(event_df["pre_returns"].apply(sum).mean()),
        "avg_post_return": float(event_df["post_returns"].apply(sum).mean()),
        "post_earnings_win_rate": float(
            (event_df["post_returns"].apply(sum) > 0).mean(),
        ),
    }
