from typing import Dict, Any
from dataclasses import dataclass
from streamlit_dashboard.src.ui_models.market_inputs import MarketQueryInput
from streamlit_dashboard.src.ui_models.build_date_params import build_date_query_params


@dataclass
class PriceSentimentInputs:
    """
    Frontend-only container.
    Sends raw inputs to backend.
    """
    lookback: int

    def is_valid(self) -> bool:
        if self.lookback <= 0:
            return False

        return True


@dataclass
class PriceSentimentQueryInput:
    market_query: MarketQueryInput
    price_sentiment: PriceSentimentInputs

    def to_query_params(self) -> Dict[str, Any]:
        """
        Convert query input into HTTP query parameters.
        """
        params: Dict[str, Any] = {
            "interval": self.market_query.interval,
            "lookback": self.price_sentiment.lookback,
        }

        # Date params injected here
        params.update(build_date_query_params(self.market_query))

        return params
