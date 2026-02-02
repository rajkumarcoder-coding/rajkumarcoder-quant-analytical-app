from typing import Dict, Any
from dataclasses import dataclass
from streamlit_dashboard.src.ui_models.market_inputs import MarketQueryInput
from streamlit_dashboard.src.ui_models.build_date_params import build_date_query_params


@dataclass
class PortfolioInputs:
    """
    Frontend-only container.
    Sends raw inputs to backend.
    """

    capital: float
    weights: str  # e.g. "AAPL=40,MSFT=30,GOOGL=30"

    def is_valid(self) -> bool:
        if self.capital <= 0:
            return False

        if not self.weights:
            return False

        return True


@dataclass
class PortfolioQueryInput:
    market_query: MarketQueryInput
    portfolio: PortfolioInputs

    def to_query_params(self) -> Dict[str, Any]:
        """
        Convert query input into HTTP query parameters.
        """
        params: Dict[str, Any] = {
            "interval": self.market_query.interval,
            "rolling_window": self.market_query.rolling_window,
            "trading_days": self.market_query.trading_days,
            "initial_capital": self.portfolio.capital,
            "weights": self.portfolio.weights,
        }

        # Date params injected here
        params.update(build_date_query_params(self.market_query))

        return params
