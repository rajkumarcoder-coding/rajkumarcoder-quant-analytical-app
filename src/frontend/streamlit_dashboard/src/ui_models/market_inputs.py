from dataclasses import dataclass
from datetime import date
from typing import Optional, Dict, Any


@dataclass
class MarketQueryInput:
    symbols: str
    interval: str = "1d"
    period: Optional[str] = None
    start: Optional[date] = None
    end: Optional[date] = None

    rolling_window: int = 20
    trading_days: int = 252

    def to_query_params(self) -> Dict[str, Any]:
        """
        Convert query input into HTTP query parameters.
        """
        params: Dict[str, Any] = {
            "interval": self.interval,
            "rolling_window": self.rolling_window,
            "trading_days": self.trading_days,
        }

        if self.period:
            params["period"] = self.period
        else:
            if self.start:
                params["start"] = self.start.isoformat()
            if self.end:
                params["end"] = self.end.isoformat()

        return params
