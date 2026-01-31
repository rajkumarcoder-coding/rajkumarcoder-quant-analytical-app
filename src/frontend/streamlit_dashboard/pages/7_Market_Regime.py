import streamlit as st
from streamlit_dashboard.src.sidebar.sidebar import render_global_sidebar
from streamlit_dashboard.src.ui_inputs.market_input_forms_v3_and_v4 import market_input_forms_v3
from streamlit_dashboard.src.components.presenters.market_regime_detection_presenter import \
    render_market_regime_detection_section

sidebar_state = render_global_sidebar()

env = sidebar_state["environment"]

st.header("📊 Market Regime Detection Engine")

query = market_input_forms_v3(
    default_symbols="AAPL,MSFT,GOOGL",
    enable_rolling=True,
)

run = st.button("Fetch Price-based Sentiment")

if not run:
    st.info("Configure parameters and run the backtest")
    st.stop()

render_market_regime_detection_section(query=query)
