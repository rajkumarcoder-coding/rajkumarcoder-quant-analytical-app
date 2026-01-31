import streamlit as st
import pandas as pd
from streamlit_dashboard.src.ui_models.price_based_sentiment import PriceSentimentQueryInput
from streamlit_dashboard.src.services.price_based_sentiment import fetch_price_based_sentiment_data
from streamlit_dashboard.src.components.ui_tables.price_based_sentiment import \
    price_based_sentiment_table
from streamlit_dashboard.src.components.ui_charts.price_sentiment import \
    price_based_sentiment_charts, price_based_sentiment_confidence_chart
from streamlit_dashboard.src.config.http_fetcher_exceptions import FetchError


def render_price_based_sentiment_section(
        query: PriceSentimentQueryInput,
):
    try:
        with st.spinner("Fetching data"):  # type: ignore[context-manager]
            payload = fetch_price_based_sentiment_data(query=query)

        price_sentiment_data = payload.get("price_sentiment_data")
        data = price_sentiment_data.get("data", {})

        if not data:
            st.warning("No sentiment data returned.")
            return

        symbols = list(data.keys())

        # -----------------------------
        # SYMBOL TABS
        # -----------------------------
        tabs = st.tabs([f"📈 {symbol}" for symbol in symbols])

        for tab, symbol in zip(tabs, symbols):
            with tab:
                symbol_data = data.get(symbol)

                if not symbol_data:
                    st.warning(f"No data available for {symbol}")
                    continue

                symbol_table_rows = [{
                    "Symbol": symbol,
                    "Sentiment": symbol_data["sentiment"],
                    "Confidence": symbol_data["confidence"],
                    **symbol_data["metrics"],
                }]

                df_symbol = pd.DataFrame(symbol_table_rows)

                # ---- TABLE ----
                price_based_sentiment_table(df_symbol)

                # ---- CHARTS ----
                price_based_sentiment_charts(df_symbol)
                price_based_sentiment_confidence_chart(df_symbol)

    except FetchError as e:
        st.error(e.message)

        if e.allowed_symbol:
            st.info(f"Allowed symbols: {', '.join(e.allowed_symbol)}")
