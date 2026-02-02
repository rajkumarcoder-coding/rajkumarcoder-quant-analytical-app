import requests
from streamlit_dashboard.src.config.http_fetcher_exceptions import FetchError


def handle_request_exceptions(exc: Exception) -> None:
    if isinstance(exc, requests.exceptions.ConnectionError):
        raise FetchError("Service currently unavailable. Try again later.")
    if isinstance(exc, requests.exceptions.Timeout):
        raise FetchError("Request timed out. Try again later.")
    if isinstance(exc, requests.exceptions.RequestException):
        raise FetchError("Network error while contacting server. Try again later.")

    raise exc  # unexpected
