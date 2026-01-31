import streamlit as st
from streamlit_dashboard.src.ui_models.market_inputs import MarketQueryInput
from streamlit_dashboard.src.services.risk_and_volatility_analyzer import fetch_risk_analyzer_data
from streamlit_dashboard.src.utils.records_to_dataframe import records_to_df_v2
from streamlit_dashboard.src.components.ui_cards.render_risk_metrics import render_risk_metrics
from streamlit_dashboard.src.components.ui_charts.risk_analysis_charts import plot_price, \
    plot_drawdown, plot_volatility
from streamlit_dashboard.src.config.http_fetcher_exceptions import FetchError


def render_risk_and_volatility_section(
        query: MarketQueryInput,
):
    try:
        with st.spinner(f"Fetching {query.symbols}..."):  # type: ignore[context-manager]
            payload = fetch_risk_analyzer_data(query=query)

        level_one_data = payload.get("data")[query.symbols]

        # 🔑 THIS is the only correct input
        records = level_one_data["data"]

        symbol = payload.get("symbol")
        df = records_to_df_v2(records)
        metrics = level_one_data.get("metrics", {})

        st.subheader(f"📈 {symbol}")

        # --- Metric cards ---
        render_risk_metrics(metrics)

        st.divider()

        st.plotly_chart(plot_price(df), width="stretch")
        st.plotly_chart(plot_drawdown(df), width="stretch")
        st.plotly_chart(plot_volatility(df), width="stretch", )


    except FetchError as e:
        st.error(e.message)

        if e.allowed_symbol:
            st.info(f"Allowed symbols: {', '.join(e.allowed_symbol)}")
