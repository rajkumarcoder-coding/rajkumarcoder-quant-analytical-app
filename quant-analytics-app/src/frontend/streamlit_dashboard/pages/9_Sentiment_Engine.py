import streamlit as st
from streamlit_dashboard.src.sidebar.sidebar import render_global_sidebar
from streamlit_dashboard.src.ui_inputs.price_sentiment_inputs_form import \
    price_based_sentiment_input_form
from streamlit_dashboard.src.components.presenters.price_based_sentiment_presenter import \
    render_price_based_sentiment_section

sidebar_state = render_global_sidebar()

env = sidebar_state["environment"]

st.header("📊 Price Based Sentiment Engine")

query = price_based_sentiment_input_form(
    default_symbols="AAPL,MSFT,GOOGL",
    enable_rolling=False,
)

run = st.button("Fetch Price Based Sentiment")

if not run:
    st.info("Configure parameters and run the backtest")
    st.stop()

render_price_based_sentiment_section(query=query)
