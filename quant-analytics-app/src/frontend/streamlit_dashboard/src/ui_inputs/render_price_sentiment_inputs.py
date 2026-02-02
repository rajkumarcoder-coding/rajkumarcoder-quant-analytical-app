import streamlit as st
from streamlit_dashboard.src.ui_models.price_based_sentiment import PriceSentimentInputs


def render_price_sentiment_form() -> PriceSentimentInputs:
    """
    Render backtesting input form.
    Returns:
        dict | None
    """

    st.subheader("Price Sentiment Configuration")

    lookback = st.number_input(
        "lookback",
        min_value=1,
        value=20,
        step=1,
    )

    price_sentiment_inputs = PriceSentimentInputs(
        lookback=lookback,
    )

    if not price_sentiment_inputs.is_valid():
        st.warning("Invalid portfolio inputs")
        st.stop()

    return price_sentiment_inputs
