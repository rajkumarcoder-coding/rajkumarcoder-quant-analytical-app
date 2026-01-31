import streamlit as st
from datetime import date
from streamlit_dashboard.src.ui_models.market_inputs import MarketQueryInput
from streamlit_dashboard.src.ui_inputs.rolling_params_inputs import rolling_params_input


def market_query_form_v2(
        *,
        default_symbols: str = "AAPL,MSFT",
        enable_rolling: bool = False,
) -> MarketQueryInput:
    symbols = st.text_input(
        "Symbols (comma-separated)",
        value=default_symbols,
    )

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

    start = end = period = None

    if mode == "Period":
        period = st.selectbox(
            "Period",
            options=["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"],
            index=3,
        )
    else:
        col1, col2 = st.columns(2)
        with col1:
            start = st.date_input("Start date", value=date(2023, 1, 1))
        with col2:
            end = st.date_input("End date", value=date.today())

        today = date.today()

        if start >= end:
            st.error("Start date must be earlier than end date.")
            st.stop()

        if start > today or end > today:
            st.error("Future dates are not allowed.")
            st.stop()

    rolling_window, trading_days = rolling_params_input(
        enable=enable_rolling,
    )

    return MarketQueryInput(
        symbols=symbols,  # 🔑 keep as string
        interval=interval,
        period=period,
        start=start,
        end=end,
        rolling_window=rolling_window,
        trading_days=trading_days,
    )
