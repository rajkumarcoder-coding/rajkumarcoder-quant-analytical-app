import pandas as pd


def compute_volume_zscore(
        volume: pd.Series,
        lookback: int
) -> float:
    rolling_mean = volume.rolling(lookback).mean()
    rolling_std = volume.rolling(lookback).std()

    vol_z = (volume - rolling_mean) / rolling_std

    return vol_z.iloc[-1]
