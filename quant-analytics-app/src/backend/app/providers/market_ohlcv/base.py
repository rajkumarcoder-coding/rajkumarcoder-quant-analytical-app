from abc import ABC, abstractmethod
from typing import Dict, Any
import pandas as pd
from app.domain.market_ohlcv_data_classes.input_data_models import MarketPriceConfig


class MarketDataProvider(ABC):
    """
    Base interface for all market data providers
    (yfinance, yahooquery, polygon, etc.)
    """

    # ---------- PRICE / TIME-SERIES DATA ----------

    @abstractmethod
    def fetch_prices(
            self,
            config: MarketPriceConfig,
    ) -> pd.DataFrame:
        """
        Fetch OHLCV / time-series price data.

        Returns:
            pd.DataFrame
        """
        raise NotImplementedError

    # ---------- FUNDAMENTAL / ENTITY DATA ----------

    @abstractmethod
    def fetch_fundamentals(
            self,
            symbol: str
    ) -> Dict[str, Any]:
        """
        Fetch company company_fundamentals / financial statements.

        Returns:
            dict with raw provider data
        """
        raise NotImplementedError
