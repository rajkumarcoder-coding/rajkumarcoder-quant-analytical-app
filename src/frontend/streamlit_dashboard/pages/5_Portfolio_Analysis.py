import streamlit as st
from streamlit_dashboard.src.sidebar.sidebar import render_global_sidebar
from streamlit_dashboard.src.ui_inputs.portfolio_inputs_form import portfolio_inputs_form
from streamlit_dashboard.src.components.presenters.portfolio_analyzer_presenter import \
    render_portfolio_analyzer_section

sidebar_state = render_global_sidebar()

env = sidebar_state["environment"]

st.header("📊Portfolio Analyzer")

query = portfolio_inputs_form(
    default_symbols="AAPL,MSFT,GOOGL",
    enable_rolling=False,
)

if st.button("Compare"):
    response = render_portfolio_analyzer_section(query=query)
