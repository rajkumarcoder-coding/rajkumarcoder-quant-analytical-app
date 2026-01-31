import streamlit as st
from dataclasses import replace
from streamlit_dashboard.src.sidebar.sidebar import render_global_sidebar
from streamlit_dashboard.src.ui_inputs.market_input_forms_v3_and_v4 import market_input_forms_v4
from streamlit_dashboard.src.utils.parse_symbol import parse_symbols
from streamlit_dashboard.src.components.presenters.market_price_and_return_presenter import \
    render_market_price_and_return_section

sidebar_state = render_global_sidebar()

env = sidebar_state["environment"]

st.header("📈 Market Prices & Returns")

query = market_input_forms_v4(
    default_symbols="AAPL,MSFT,GOOGL",
    enable_rolling=False,
)

symbols = parse_symbols(query.symbols)

if st.button("Get Data"):
    if not symbols:
        st.warning("Please enter at least one stock symbol.")
        st.stop()

    for symbol in symbols:
        st.divider()
        st.subheader(symbol)

        # 🔑 same backend route, single-symbol intent
        single_query = replace(query, symbols=symbol)

        render_market_price_and_return_section(query=single_query)
