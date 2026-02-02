from pydantic import BaseModel
from typing import List, Dict


class StrategyDataPoint(BaseModel):
    date: str
    close: float
    signal: int
    position: int
    strategy_return: float
    equity: float
    drawdown: float


class StrategyMetrics(BaseModel):
    total_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    num_trades: int


class SymbolStrategyResult(BaseModel):
    data: List[StrategyDataPoint]
    metrics: StrategyMetrics


class BacktestingStrategyResponse(BaseModel):
    symbols: List[str]
    data: Dict[str, SymbolStrategyResult]
