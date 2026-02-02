from pydantic import BaseModel
from typing import Dict, Literal


class SentimentMetrics(BaseModel):
    momentum: float
    trend_strength: float
    volume_zscore: float
    price_volume_divergence: float


class SymbolSentiment(BaseModel):
    sentiment: Literal["Bullish", "Bearish", "Neutral"]
    metrics: SentimentMetrics
    confidence: float


class MultiSymbolSentimentData(BaseModel):
    data: Dict[str, SymbolSentiment]


class MultiSymbolSentimentResponse(BaseModel):
    price_sentiment_data: MultiSymbolSentimentData
