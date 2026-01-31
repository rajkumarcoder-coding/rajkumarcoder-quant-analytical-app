import streamlit as st
from streamlit_dashboard.src.sidebar.sidebar import render_global_sidebar
from streamlit_dashboard.src.ui_inputs.backtesting_inputs_form import backtesting_input_form
from streamlit_dashboard.src.components.presenters.backtesting_engine_presenter import \
    render_backtesting_engine_section

sidebar_state = render_global_sidebar()

env = sidebar_state["environment"]

st.header("📊 Backtesting Engine")

query = backtesting_input_form(
    default_symbols="AAPL,MSFT,GOOGL",
    enable_rolling=False,
)

run = st.button("Run Backtest")

if not run:
    st.info("Configure parameters and run the backtest")
    st.stop()

if query.backtesting.fast_window >= query.backtesting.slow_window:
    st.error("Fast window must be smaller than slow window")
    st.stop()

render_backtesting_engine_section(query=query)
