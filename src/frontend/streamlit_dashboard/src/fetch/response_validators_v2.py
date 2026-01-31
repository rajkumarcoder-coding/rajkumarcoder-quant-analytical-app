from typing import Any, Dict, Type
from streamlit_dashboard.src.config.http_fetcher_exceptions import FetchError


class ResponseValidatorV2:
    """
    Lightweight response validator for API payloads.

    Purpose:
    - Enforce basic structure
    - Fail early with clear errors
    - Avoid KeyError / AttributeError cascades
    """

    def __init__(self, payload: Any):
        self.payload = payload

    def require_dict(self) -> Dict[str, Any]:
        if not isinstance(self.payload, dict):
            raise FetchError(
                message="Invalid response format",
                reason="response_not_dict",
                context={"received_type": type(self.payload).__name__},
            )
        return self.payload

    def require_field(
            self,
            field: str,
            expected_type: Type,
    ) -> Any:
        payload = self.require_dict()

        if field not in payload:
            raise FetchError(
                message=f"Missing required field: {field}",
                reason="missing_field",
                context={"field": field},
            )

        value = payload[field]

        if not isinstance(value, expected_type):
            raise FetchError(
                message=f"Invalid type for field: {field}",
                reason="invalid_field_type",
                context={
                    "field": field,
                    "expected": expected_type.__name__,
                    "received": type(value).__name__,
                },
            )

        return value
