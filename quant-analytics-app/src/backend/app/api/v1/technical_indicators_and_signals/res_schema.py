from typing import Dict, List, Literal, Union, Optional
from pydantic import BaseModel


class IndicatorRow(BaseModel):
    date: str

    close: float
    volume: int

    sma: float
    ema: float
    momentum: float
    roc: float
    atr: float

    volume_sma: float
    volume_spike: float
    obv: float


class SignalMetrics(BaseModel):
    trend: int  # -1 / +1
    momentum: int  # -1 / +1
    volatility: Literal["high", "low"]
    volume_confirmation: int  # 0 / 1
    composite: Literal["bullish", "bearish", "neutral"]


class SingleStockIndicatorsResponse(BaseModel):
    symbol: str
    data: List[IndicatorRow]
    metrics: Optional[Dict[str, SignalMetrics]] = None



class MultiStockIndicatorsResponse(BaseModel):
    symbols: List[str]
    data: Dict[str, SingleStockIndicatorsResponse]
    metrics: Optional[Dict[str, SignalMetrics]] = None



IndicatorsAPIResponse = Union[
    SingleStockIndicatorsResponse,
    MultiStockIndicatorsResponse,
]
