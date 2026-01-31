import streamlit as st


def render_signal_cards(signal: dict):
    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Trend", "Bullish" if signal.get("trend", "N/A") == 1 else "Bearish")
    c2.metric("Momentum", "Positive" if signal.get("momentum", "N/A") == 1 else "Negative")
    c3.metric("Volatility", signal.get("volatility", "N/A").capitalize())
    c4.metric("Volume", "Strong" if signal.get("volume_confirmation", "N/A") else "Weak")
    c5.metric("Composite", signal.get("composite", "N/A").capitalize())
