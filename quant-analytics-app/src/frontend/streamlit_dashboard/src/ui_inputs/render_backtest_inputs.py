import streamlit as st
from streamlit_dashboard.src.ui_models.backtesting_engine import BacktestingInputs


def render_backtesting_form() -> BacktestingInputs:
    """
    Render backtesting input form.
    Returns:
        dict | None
    """

    st.subheader("Backtesting Configuration")

    capital = st.number_input(
        "Capital",
        min_value=1_000.0,
        value=100_000.0,
        step=1_000.0,
    )

    fast_window = st.number_input(
        "Fast Window",
        min_value=1,
        value=12,
        step=1,
    )

    slow_window = st.number_input(
        "Slow Window",
        min_value=2,
        value=26,
        step=1,
    )

    backtesting_inputs = BacktestingInputs(
        capital=capital,
        fast_window=fast_window,
        slow_window=slow_window,
    )

    if not backtesting_inputs.is_valid():
        st.warning("Invalid portfolio inputs")
        st.stop()

    return backtesting_inputs
