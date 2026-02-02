import streamlit as st
from streamlit_dashboard.src.components.ui_cards.signals_cards import render_signal_cards
from streamlit_dashboard.src.ui_models.market_inputs import MarketQueryInput
from streamlit_dashboard.src.services.indicators_and_returns import fetch_indicators_and_signals
from streamlit_dashboard.src.utils.records_to_dataframe import records_to_df
from streamlit_dashboard.src.components.ui_charts.indicator_overlay_chart import \
    indicator_overlay_chart
from streamlit_dashboard.src.components.ui_charts.volume_indicator_chart import \
    volume_indicator_chart
from streamlit_dashboard.src.config.http_fetcher_exceptions import FetchError


def render_indicator_and_signals_section(
        query: MarketQueryInput,
):
    try:
        with st.spinner(f"Fetching {query.symbols}..."):  # type: ignore[context-manager]
            payload = fetch_indicators_and_signals(query=query)

        # with st.spinner(f"Analyzing {symbol}..."):
        #     safe_render(
        #         lambda q=single_query: render_indicator_and_signals_section(query=q),
        #         f"Error loading data for {symbol}"
        #     )

        symbol = payload.get("symbol")
        df = records_to_df(payload.get("data"))
        signals = payload.get("metrics", {})
        signal = signals.get(symbol, {})

        st.subheader(f"📈 {symbol}")

        render_signal_cards(signal)

        st.divider()

        # ---- PRICE + INDICATORS ----
        st.plotly_chart(
            indicator_overlay_chart(df, symbol),
            width="stretch",
        )

        # ---- VOLUME INDICATORS ----
        st.plotly_chart(
            volume_indicator_chart(df, symbol),
            width="stretch",
        )

    except FetchError as e:
        st.error(e.message)

        if e.allowed_symbol:
            st.info(f"Allowed symbols: {', '.join(e.allowed_symbol)}")
