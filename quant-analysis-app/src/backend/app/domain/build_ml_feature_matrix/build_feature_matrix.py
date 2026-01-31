import pandas as pd


def build_feature_matrix(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
    """
    Output: strictly numeric features for ML or signals.
    """
    features = pd.DataFrame()
    # use existing Date column
    features["date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")

    features[f"return_{symbol}"] = df[f"Close_{symbol}"].pct_change()
    features[f"volatility_{symbol}"] = features[f"return_{symbol}"].rolling(20).std()

    features[f"trend_strength_{symbol}"] = df[f"EMA_{symbol}"] - df[f"SMA_{symbol}"]
    features[f"momentum_{symbol}"] = df[f"Momentum_{symbol}"]
    features[f"roc_{symbol}"] = df[f"ROC_{symbol}"]

    features[f"volume_spike_{symbol}"] = df[f"Volume_Spike_{symbol}"]
    features[f"obv_slope_{symbol}"] = df[f"OBV_{symbol}"].diff(5)

    return features
