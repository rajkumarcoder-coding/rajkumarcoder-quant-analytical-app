from typing import Dict, List
from pydantic import BaseModel


class EarningsEventRecord(BaseModel):
    date: str
    event_return: float
    pre_return: float
    post_return: float
    volatility_pre: float
    volatility_post: float
    gap: float


class EarningsSymbolData(BaseModel):
    data: List[EarningsEventRecord]


class EarningsImpactResponse(BaseModel):
    symbols: List[str]
    data: Dict[str, EarningsSymbolData]
