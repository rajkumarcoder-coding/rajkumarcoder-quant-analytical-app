import requests
from typing import Any, Dict

from streamlit_dashboard.src.fetch.handle_request_exceptions import (
    handle_request_exceptions,
)
from streamlit_dashboard.src.fetch.handle_market_fetch_errors import (
    handle_market_fetch_errors,
)


def execute_get_request(
        *,
        url: str,
        params: Dict[str, Any],
        timeout: int = 20,
) -> Dict[str, Any]:
    """
    Execute HTTP GET request with centralized error handling.
    """

    try:
        response = requests.get(
            url,
            params=params,
            timeout=timeout,
        )
    except Exception as exc:
        handle_request_exceptions(exc)
        return {}

    if response.status_code != 200:
        handle_market_fetch_errors(response)
        return {}

    return response.json()
