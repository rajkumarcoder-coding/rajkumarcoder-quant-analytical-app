import pandas as pd
from app.domain.price_based_sentiment_and_momentum.compute_momentum import compute_momentum
from app.domain.price_based_sentiment_and_momentum.compute_trend_strength import \
    compute_trend_strength
from app.domain.price_based_sentiment_and_momentum.compute_volume_zscore import \
    compute_volume_zscore
from app.domain.price_based_sentiment_and_momentum.compute_divergence import compute_divergence
from app.domain.price_based_sentiment_and_momentum.classify import classify


def compute_sentiment_for_symbol(df: pd.DataFrame, symbol: str, lookback: int) -> dict:
    momentum = compute_momentum(df[f"Close_{symbol}"], lookback)
    trend = compute_trend_strength(df[f"Close_{symbol}"], lookback)
    vol_z = compute_volume_zscore(df[f"Volume_{symbol}"], lookback)
    divergence = compute_divergence(df[f"Close_{symbol}"], df[f"Volume_{symbol}"])

    sentiment = classify(momentum, trend, vol_z)

    confidence = min(
        1.0,
        (abs(momentum) + abs(trend) + abs(vol_z)) / 3,
    )

    return {
        "sentiment": sentiment,
        "metrics": {
            "momentum": round(momentum, 4),
            "trend_strength": round(trend, 4),
            "volume_zscore": round(vol_z, 2),
            "price_volume_divergence": round(divergence, 4),
        },
        "confidence": round(confidence, 2),
    }


def compute_sentiment_multi_symbol(
        df: pd.DataFrame,
        symbols: list[str],
        lookback: int = 20
) -> dict:
    results = {}

    for symbol in symbols:
        results[symbol] = compute_sentiment_for_symbol(df, symbol, lookback)

    return {
        "data": results
    }
