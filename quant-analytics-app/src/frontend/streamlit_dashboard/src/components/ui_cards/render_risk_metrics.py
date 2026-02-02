import streamlit as st


def render_risk_metrics(metrics: dict):
    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Volatility", f"{metrics.get('volatility', 0):.4f}")
    c2.metric("Ann. Volatility", f"{metrics.get('annualized_volatility', 0):.4f}")
    c3.metric("Max Drawdown", f"{metrics.get('max_drawdown', 0):.2%}")
    c4.metric("VaR (95%)", f"{metrics.get('var_95', 0):.2%}")
    c5.metric("Sharpe", f"{metrics.get('sharpe_ratio', 0):.2f}")
