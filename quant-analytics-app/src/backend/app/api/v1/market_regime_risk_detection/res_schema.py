from typing import List, Dict, Literal
from pydantic import BaseModel


class RegimeDataRow(BaseModel):
    date: str

    returns: float  # `return` is a Python keyword
    volatility: float
    threshold: float
    trend_strength: float

    volatility_regime: Literal["low", "high"]
    trend_strength: float
    trend_regime: Literal["uptrend", "downtrend"]
    risk_state: Literal[
        "risk_on",
        "risk_off",
        "defensive",
        "volatile_bull",
    ]


class RegimeMetrics(BaseModel):
    dominant_regime: Literal[
        "risk_on",
        "risk_off",
        "defensive",
        "volatile_bull",
    ]
    high_vol_ratio: float
    uptrend_ratio: float


class PerSymbolRegimeData(BaseModel):
    data: List[RegimeDataRow]
    metrics: RegimeMetrics


class MarketRegimeResponse(BaseModel):
    symbols: List[str]
    data: Dict[str, PerSymbolRegimeData]
