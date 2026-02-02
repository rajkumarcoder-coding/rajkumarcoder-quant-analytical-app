import streamlit as st
from typing import Any


class ResponseValidator:
    """
    Validates backend response structure for Streamlit presenters.
    Handles user-facing errors and stops execution safely.
    """

    def __init__(self, payload: Any):
        self.payload = payload

    def require_dict(self) -> dict:
        if not isinstance(self.payload, dict):
            self._fail("Service currently unavailable. Try again later")
        return self.payload

    def require_field(self, name: str, expected_type: type):
        value = self.payload.get(name)

        if not isinstance(value, expected_type):
            self._fail(f"Invalid '{name}' format")

        return value

    # noinspection PyMethodMayBeStatic
    def _fail(self, message: str):
        """Instance method by design (override-friendly)."""
        st.error(message)
        st.stop()
