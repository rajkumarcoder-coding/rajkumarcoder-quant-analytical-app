import pandas as pd


def slice_event_window(
        df: pd.DataFrame,
        event_date: pd.Timestamp,
        window: int,
) -> pd.DataFrame:
    buffer_days = window * 4

    return df.loc[
        (df.index >= event_date - pd.Timedelta(days=buffer_days)) &
        (df.index <= event_date + pd.Timedelta(days=buffer_days))
        ]
