import streamlit as st
from streamlit_dashboard.src.sidebar.sidebar import render_global_sidebar
from streamlit_dashboard.src.ui_inputs.market_input_forms_v3_and_v4 import market_input_forms_v3
from streamlit_dashboard.src.components.presenters.earnings_events_market_impact_presenter import \
    render_earnings_events_impacts_section

sidebar_state = render_global_sidebar()

env = sidebar_state["environment"]

st.header("📊 Earnings Event Market Impact Engine")

query = market_input_forms_v3(
    default_symbols="AAPL,MSFT,GOOGL",
    enable_rolling=True,
)

run = st.button("Fetch Earnings Event Market Impact")

if not run:
    st.info("Configure parameters and run the backtest")
    st.stop()

render_earnings_events_impacts_section(query=query)
