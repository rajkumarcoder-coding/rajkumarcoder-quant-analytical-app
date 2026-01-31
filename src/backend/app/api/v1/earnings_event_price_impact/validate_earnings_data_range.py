from datetime import date
from typing import Optional

from app.core_configs.exceptions import ValidationError


def validate_earnings_data_range(
        *,
        period: Optional[str],
        start: Optional[date],
        end: Optional[date],
        min_days: int = 365,
) -> None:
    """
    Validate that earnings analysis has sufficient data.
    Raises ValueError if requirements are not met.
    """

    # Period-based validation
    if period is not None:
        if period in {"1mo", "3mo", "6mo", "ytd"}:
            raise ValidationError(
                message="Date range must be at least 1 year for earnings impact analysis.",
            )

    # Date-range-based validation
    if start is not None and end is not None:
        if (end - start).days < min_days:
            raise ValidationError(
                message="Date range must be at least 1 year for earnings impact analysis.",
            )
