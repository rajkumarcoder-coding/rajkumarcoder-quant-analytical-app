from typing import List, Dict
from pydantic import BaseModel, Field


# -------------------------
# Time-series models
# -------------------------

class PortfolioReturnRow(BaseModel):
    date: str
    portfolio_return: float
    capital_curve: float
    portfolio_drawdown: float


class AssetReturnRow(BaseModel):
    date: str
    close: float
    daily_return: float
    drawdown: float


# -------------------------
# Containers for time-series
# -------------------------

class PortfolioTimeSeries(BaseModel):
    data: List[PortfolioReturnRow]


class AssetTimeSeries(BaseModel):
    data: List[AssetReturnRow]


class PortfolioData(BaseModel):
    symbols: List[str]
    portfolio: PortfolioTimeSeries
    assets: Dict[str, AssetTimeSeries]


# -------------------------
# Risk / analysis metrics
# -------------------------

class AssetRiskMetrics(BaseModel):
    max_drawdown: float


class PortfolioAnalysis(BaseModel):
    # per-asset metrics
    asset_metrics: Dict[str, AssetRiskMetrics] = Field(
        description="Per-asset risk metrics",
    )

    # portfolio-level metrics
    portfolio_volatility: float
    portfolio_sharpe: float
    cumulative_return: float
    portfolio_max_drawdown: float

    # cross-asset metrics
    correlation_matrix: Dict[str, Dict[str, float]]


# -------------------------
# Final API response
# -------------------------

class PortfolioAnalysisResponse(BaseModel):
    portfolio_data: PortfolioData
    portfolio_analysis: PortfolioAnalysis
