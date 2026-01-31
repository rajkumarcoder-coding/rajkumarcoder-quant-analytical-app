import streamlit as st
from datetime import date
from typing import Optional, Dict, Any


def render_market_time_inputs(
        default_symbols: str = "AAPL,MSFT,GOOGL",
) -> Dict[str, Any]:
    """
    Render market symbol & time range inputs.

    Returns:
        dict with keys:
        - symbols
        - interval
        - period OR start/end
    """

    st.subheader("Market Configuration")

    symbols = st.text_input(
        "Symbols (comma-separated)",
        value=default_symbols,
    )

    if not symbols.strip():
        st.warning("Please enter at least one symbol.")
        st.stop()

    st.subheader("Time Range")

    mode = st.radio(
        "Select time mode",
        options=["Period", "Custom Date Range"],
        horizontal=True,
    )

    interval = st.selectbox(
        "Interval",
        options=["1d", "1wk", "1mo"],
        index=0,
    )

    start: Optional[date] = None
    end: Optional[date] = None
    period: Optional[str] = None

    if mode == "Period":
        period = st.selectbox(
            "Period",
            options=["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"],
            index=3,
        )
    else:
        col1, col2 = st.columns(2)

        with col1:
            start = st.date_input(
                "Start date",
                value=date(2023, 1, 1),
            )

        with col2:
            end = st.date_input(
                "End date",
                value=date.today(),
            )

        today = date.today()

        if start >= end:
            st.error("Start date must be earlier than end date.")
            st.stop()

        if start > today or end > today:
            st.error("Future dates are not allowed.")
            st.stop()

    return {
        "symbols": symbols,
        "interval": interval,
        "period": period,
        "start": start,
        "end": end,
    }
