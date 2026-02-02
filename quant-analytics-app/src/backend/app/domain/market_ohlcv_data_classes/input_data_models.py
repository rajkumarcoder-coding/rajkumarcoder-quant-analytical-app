from pydantic import BaseModel, Field, model_validator, field_validator
from datetime import date
from typing import Optional


class MarketPriceConfig(BaseModel):
    symbols: str = Field(..., min_length=1)
    interval: str = "1d"
    period: Optional[str] = None

    start: Optional[date] = None
    end: Optional[date] = None

    auto_adjust: bool = False
    progress: bool = False

    rolling_window: int = 20
    trading_days: int = 252

    @model_validator(mode="after")
    def validate_time_range(self):
        if (self.start or self.end) and self.period is not None:
            raise ValueError(
                "Use either (start/end) or period, not both",
            )
        return self

    @field_validator("symbols")
    @classmethod
    def normalize_symbols(cls, v: str) -> str:
        parsed = [
            s.strip().upper()
            for s in v.split(",")
            if s.strip()
        ]

        if not parsed:
            raise ValueError(
                "symbols must contain at least one valid symbol",
            )

        # 🔹 remove duplicates while preserving order
        unique_symbols = list(dict.fromkeys(parsed))

        return ",".join(unique_symbols)
