import streamlit as st
from typing import Tuple


def rolling_params_input(
        *,
        enable: bool,
        default_window: int = 20,
        default_trading_days: int = 252,
) -> Tuple[int, int]:
    """
    Collect rolling window parameters if enabled.
    Returns (rolling_window, trading_days).
    """

    if not enable:
        return default_window, default_trading_days

    rolling_window = st.number_input(
        "Rolling window",
        min_value=1,
        value=default_window,
    )

    trading_days = st.number_input(
        "Trading days per year",
        min_value=1,
        value=default_trading_days,
    )

    return rolling_window, trading_days


def rolling_window_input(
        *,
        enable: bool,
        default_window: int = 20,
) -> int:
    """
    Collect rolling window parameters if enabled.
    Returns (rolling_window, trading_days).
    """

    if not enable:
        return default_window

    rolling_window = st.number_input(
        "Rolling window",
        min_value=1,
        value=default_window,
    )

    return rolling_window
