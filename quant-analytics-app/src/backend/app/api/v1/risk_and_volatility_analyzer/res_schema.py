from pydantic import BaseModel
from typing import List, Dict, Generic, TypeVar, Optional

TData = TypeVar("TData")
TMetrics = TypeVar("TMetrics")


class PerSymbolPayload(BaseModel, Generic[TData, TMetrics]):
    data: List[TData]
    metrics: Optional[TMetrics] = None


class MultiSymbolResponse(BaseModel, Generic[TData, TMetrics]):
    symbols: List[str]
    data: Dict[str, PerSymbolPayload[TData, TMetrics]]


class RiskRow(BaseModel):
    date: str
    close: float
    daily_return: float
    daily_volatility: float
    drawdown: float


class RiskMetrics(BaseModel):
    volatility: float
    annualized_volatility: float
    max_drawdown: float
    var_95: float
    sharpe_ratio: float


RiskResponse = MultiSymbolResponse[RiskRow, RiskMetrics]
