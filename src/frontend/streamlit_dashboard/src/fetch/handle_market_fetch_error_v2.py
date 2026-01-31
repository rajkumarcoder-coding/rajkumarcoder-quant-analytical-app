import requests
from typing import Any
from streamlit_dashboard.src.fetch.response_validators import ResponseValidator
from streamlit_dashboard.src.config.http_fetcher_exceptions import FetchError


def handle_market_fetch_errors_v2(response: requests.Response) -> None:
    """
    Handle non-200 HTTP responses.
    ALWAYS raises FetchError.
    """

    try:
        raw_json = response.json()
    except Exception:
        # Covers ValueError, JSONDecodeError, etc.
        raise FetchError(
            message="Invalid response from server",
            reason="invalid_response_format",
            context={
                "status_code": response.status_code,
                "text": response.text[:300],  # limit noise
            },
        )

    # Safely extract `detail`
    detail: Any = raw_json.get("detail", {})

    if not isinstance(detail, dict):
        raise FetchError(
            message="Invalid error payload received",
            reason="invalid_error_payload",
            context={
                "status_code": response.status_code,
                "detail_type": type(detail).__name__,
            },
        )

    # Validate error payload shape
    validator = ResponseValidator(payload=detail)

    try:
        payload = validator.require_dict()
    except FetchError:
        # Re-raise cleanly (already your domain error)
        raise
    except Exception:
        # Catch ANY unexpected validator error
        raise FetchError(
            message="Malformed error response from server",
            reason="error_validation_failed",
            context={
                "status_code": response.status_code,
                "detail": detail,
            },
        )

    # Final, canonical FetchError
    raise FetchError(
        message=payload.get("message", "Failed to fetch stock data"),
        reason=payload.get("reason", "unknown_error"),
        context=payload.get("context"),
        current_symbol=payload.get("current_symbol"),
        allowed_symbol=payload.get("allowed_symbol"),
    )
