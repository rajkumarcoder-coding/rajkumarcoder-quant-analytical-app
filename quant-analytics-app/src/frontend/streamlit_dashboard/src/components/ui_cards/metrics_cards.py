import streamlit as st


def render_per_symbol_metrics(metrics: dict):
    cols = st.columns(len(metrics))

    for col, (symbol, values) in zip(cols, metrics.items()):
        with col:
            st.subheader(symbol)
            st.metric("Avg Daily Return", f"{values['avg_daily_return']:.4f}")
            st.metric("Volatility", f"{values['volatility']:.4f}")
            st.metric("Total Return", f"{values['total_return'] * 100:.2f}%")
