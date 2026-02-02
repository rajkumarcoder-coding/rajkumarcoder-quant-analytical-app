from typing import Dict, Any


class AppException(Exception):
    """
    Base application exception.

    All custom exceptions should inherit from this.
    """
    status_code: int = 400
    error_type: str = "application_error"

    def __init__(
            self,
            message: str,
            *,
            reason: str | None = None,
            context: Dict[str, Any] | None = None,
            allowed_symbol: list[str] | None = None,
    ):
        self.detail = {
            "message": message,
            "reason": reason or self.error_type,
            "context": context,
            "allowed_symbol": allowed_symbol,
        }
        super().__init__(message)


class ValidationError(AppException):
    """
    Raised when user input is invalid.
    Example:
    - Invalid stock symbol
    - Unsupported timeframe
    """
    status_code = 422
    error_type = "validation_error"


class DataFetchError(AppException):
    """
    Raised when data cannot be fetched from external sources.
    Example:
    - API down
    - Timeout
    - Provider error
    """
    status_code = 502
    error_type = "data_fetch_error"


class AnalysisError(AppException):
    """
    Raised when analysis or computation fails.
    Example:
    - Indicator calculation error
    - Empty dataset
    """
    status_code = 500
    error_type = "analysis_error"


class InfrastructureError(AppException):
    """
    Raised when internal infrastructure fails.
    Example:
    - Database down
    - Redis unavailable
    """
    status_code = 503
    error_type = "infrastructure_error"


class NotFoundError(AppException):
    """
    Raised when internal infrastructure fails.
    Example:
    - Database down
    - Redis unavailable
    """
    status_code = 400
    error_type = "not_found_error"
