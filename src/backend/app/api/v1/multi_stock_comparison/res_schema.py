from typing import Dict, List
from pydantic import BaseModel
from datetime import date


class MarketPriceRow(BaseModel):
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int
    daily_return: float


class SingleSymbolMarketData(BaseModel):
    symbol: str
    data: List[MarketPriceRow]


class PerSymbolMetrics(BaseModel):
    avg_daily_return: float
    volatility: float
    total_return: float


class MarketComparisonMetrics(BaseModel):
    per_symbol: Dict[str, PerSymbolMetrics]
    # correlation_matrix: Dict[str, Dict[str, float]]
    correlation_matrix: Dict[str, Dict[str, float | None]]


class MultiSymbolMarketComparisonResponse(BaseModel):
    symbols: List[str]
    data: Dict[str, SingleSymbolMarketData]
    metrics: MarketComparisonMetrics
