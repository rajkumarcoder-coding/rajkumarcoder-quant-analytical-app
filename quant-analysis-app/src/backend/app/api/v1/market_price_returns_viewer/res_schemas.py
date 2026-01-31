from typing import List, Dict
from pydantic import BaseModel


class MarketPriceRow(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    daily_return: float
    cumulative_return: float
    total_return: float


class MarketPriceData(BaseModel):
    data: List[MarketPriceRow]


class MultiSymbolMarketPriceResponse(BaseModel):
    symbols: List[str]
    data: Dict[str, MarketPriceData]
