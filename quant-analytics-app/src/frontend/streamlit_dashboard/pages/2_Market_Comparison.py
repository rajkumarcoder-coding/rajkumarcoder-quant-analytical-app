import streamlit as st
from streamlit_dashboard.src.sidebar.sidebar import render_global_sidebar
from streamlit_dashboard.src.ui_inputs.market_query_form import market_query_form
from streamlit_dashboard.src.components.presenters.market_comparison_presenters import \
    render_market_comparison_section

sidebar_state = render_global_sidebar()

env = sidebar_state["environment"]

st.header("📊 Stock Comparison")

query = market_query_form(
    default_symbols="AAPL,MSFT",
    enable_date_range=True,
    enable_rolling=False,
)

if st.button("Compare"):
    response = render_market_comparison_section(query=query)

# if st.button("Compare"):
#     def _render():
#         render_market_comparison_section(query=query)
#
#     safe_render(_render, "Failed to load market comparison")

