from dataclasses import dataclass


@dataclass(frozen=True)
class RedisTTL:
    """
    Centralized Redis TTL definitions (in seconds)
    """

    # ---- Market Data ----
    OHLCV: int = 300  # 5 min
    RETURNS: int = 300  # 5 min
    INDICATORS: int = 600  # 10 min

    # ---- Risk & Analytics ----
    RISK_METRICS: int = 900  # 15 min
    PORTFOLIO: int = 900  # 15 min
    BACKTEST: int = 1800  # 30 min

    # ---- Advanced Analytics ----
    REGIME: int = 1800  # 30 min
    EARNINGS: int = 3600  # 1 hour
    SENTIMENT: int = 600  # 10 min

    # ---- System ----
    DEFAULT: int = 300  # fallback
