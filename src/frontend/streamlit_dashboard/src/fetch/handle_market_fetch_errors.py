import requests
from streamlit_dashboard.src.fetch.response_validators import ResponseValidator
from streamlit_dashboard.src.config.http_fetcher_exceptions import FetchError


def handle_market_fetch_errors(response: requests.Response) -> None:
    """
    Handle non-200 HTTP responses and raise FetchError with clean context.
    """
    try:
        err_res = response.json().get("detail", {})
    except Exception:
        # Non-JSON error response
        raise FetchError(
            message="Invalid response from server",
            reason="invalid_response",
        )

    validator = ResponseValidator(payload=err_res)
    payload = validator.require_dict()

    raise FetchError(
        message=payload.get("message", "Failed to fetch stock data"),
        reason=payload.get("reason"),
        context=payload.get("context"),
        current_symbol=payload.get("current_symbol"),
        allowed_symbol=payload.get("allowed_symbol"),
    )
