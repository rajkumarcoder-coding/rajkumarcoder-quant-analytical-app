import streamlit as st
from dataclasses import replace
from streamlit_dashboard.src.sidebar.sidebar import render_global_sidebar
from streamlit_dashboard.src.ui_inputs.market_querry_forms_v2 import market_query_form_v2
from streamlit_dashboard.src.utils.parse_symbol import parse_symbols
from streamlit_dashboard.src.components.presenters.risk_and_volatility_analyzer import \
    render_risk_and_volatility_section

sidebar_state = render_global_sidebar()

env = sidebar_state["environment"]

st.header("📈 Market Risk Analyzer")

query = market_query_form_v2(
    default_symbols="AAPL,MSFT",
    enable_rolling=False,
)

symbols = parse_symbols(query.symbols)

if st.button("📋 Raw Risk Data"):
    if not symbols:
        st.warning("Please enter at least one stock symbol.")
        st.stop()

    for symbol in symbols:
        st.divider()
        st.subheader(symbol)

        # 🔑 same backend route, single-symbol intent
        single_query = replace(query, symbols=symbol)

        render_risk_and_volatility_section(query=single_query)

        # safe_render(
        #     lambda q=single_query: render_risk_and_volatility_section(query=q),
        #     f"Failed to load indicators for {symbol}",
        # )
