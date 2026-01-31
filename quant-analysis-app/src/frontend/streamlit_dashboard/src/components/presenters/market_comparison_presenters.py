import streamlit as st
from streamlit_dashboard.src.ui_models.market_inputs import MarketQueryInput
from streamlit_dashboard.src.services.market_compare_api import fetch_market_comparison
from streamlit_dashboard.src.utils.records_to_dataframe import records_to_df
from streamlit_dashboard.src.components.ui_cards.metrics_cards import render_per_symbol_metrics
from streamlit_dashboard.src.components.ui_charts.close_price_comparison import \
    close_price_comparison_chart
from streamlit_dashboard.src.components.ui_charts.daily_return_comparison import \
    daily_return_comparison_chart
from streamlit_dashboard.src.components.ui_tables.correlation_table import \
    render_correlation_matrix
from streamlit_dashboard.src.config.http_fetcher_exceptions import FetchError


def render_market_comparison_section(
        query: MarketQueryInput,
):
    try:
        with st.spinner(f"Fetching {query.symbols}..."):  # type: ignore[context-manager]
            payload = fetch_market_comparison(query=query)

        # ---- Validate payload early ----
        symbols = payload.get("symbols")
        data = payload.get("data")
        metrics = payload.get("metrics")

        if not symbols or not data or not metrics:
            st.error("Invalid response received from backend")
            return

        # ---- Build DataFrames per symbol ----
        dfs = {
            symbol: records_to_df(data[symbol]["data"])
            for symbol in symbols
        }

        # ---- Metrics (TOP) ----
        st.subheader("Key Metrics")
        render_per_symbol_metrics(metrics["per_symbol"])

        st.divider()

        # ---- Close Price Comparison ----
        st.plotly_chart(
            close_price_comparison_chart(dfs),
            width="stretch",
        )

        # ---- Daily Return Comparison ----
        st.plotly_chart(
            daily_return_comparison_chart(dfs),
            width="stretch",
        )

        st.divider()

        # ---- Correlation Matrix ----
        render_correlation_matrix(metrics["correlation_matrix"])

    except FetchError as e:
        st.error(e.message)

        if e.allowed_symbol:
            st.info(f"Allowed symbols: {', '.join(e.allowed_symbol)}")

        # if e.context:
        #     with st.expander("Details"):
        #         st.json(e.context)
