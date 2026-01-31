import streamlit as st
from streamlit_dashboard.src.ui_models.market_inputs import MarketQueryInput
from datetime import date

MIN_DAYS_REQUIRED = 2


def market_query_form(
        *,
        default_symbols: str = "AAPL,MSFT",
        enable_date_range: bool = True,
        enable_rolling: bool = False,
) -> MarketQueryInput:
    symbols = st.text_input(
        "Symbols (comma-separated)",
        value=default_symbols,
    )

    st.subheader("Time Range")

    interval = st.selectbox(
        "Interval",
        options=["1d", "1wk", "1mo"],
        index=0,
    )

    period = None
    start = end = None

    if enable_date_range:
        use_date_range = st.checkbox(
            "Use custom date range",
            value=False,
        )
    else:
        use_date_range = False

    if use_date_range:
        c1, c2 = st.columns(2)
        with c1:
            start = st.date_input("Start date", value=date(2023, 1, 1))
        with c2:
            end = st.date_input("End date", value=date.today())
    else:
        period = st.selectbox(
            "Period",
            options=["1mo", "3mo", "6mo", "1y", "2y"],
            index=0,
        )

    # ---- Date validation (UI-level) ----
    today = date.today()

    if start and end:
        if start >= end:
            st.error("Start date must be earlier than end date.")
            st.stop()

        if start > today or end > today:
            st.error("Future dates are not allowed.")
            st.stop()

        delta_days = (end - start).days

        if delta_days < MIN_DAYS_REQUIRED:
            st.error(
                f"Please select a date range of at least {MIN_DAYS_REQUIRED} days "
                "to compute comparison metrics.",
            )
            st.stop()

    rolling_window = 20
    trading_days = 252

    if enable_rolling:
        rolling_window = st.number_input(
            "Rolling window",
            min_value=1,
            value=20,
        )
        trading_days = st.number_input(
            "Trading days per year",
            min_value=1,
            value=252,
        )

    return MarketQueryInput(
        symbols=symbols,
        interval=interval,
        period=period,
        start=start,
        end=end,
        rolling_window=rolling_window,
        trading_days=trading_days,
    )
