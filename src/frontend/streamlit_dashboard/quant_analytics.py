import streamlit as st
import logging
from streamlit_dashboard.src.sidebar.sidebar import render_global_sidebar
from streamlit_dashboard.src.config.app_settings import settings

# -----------------------------
# Logging
# -----------------------------
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# -----------------------------
# Debug info (run once per session)
# -----------------------------
if settings.DEBUG and not st.session_state.get("_debug_info_shown"):
    st.sidebar.caption(
        f"Environment: {settings.APP_ENV}\n"
        f"Streamlit: {settings.STREAMLIT_SERVER_ADDRESS}:{settings.STREAMLIT_SERVER_PORT}",
    )
    st.session_state["_debug_info_shown"] = True

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Quant Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Sidebar
# -----------------------------
sidebar_state = render_global_sidebar()
env = sidebar_state["environment"]

# -----------------------------
# Main content
# -----------------------------
st.title("📊 Quant Analytics Platform")

st.markdown(
    """
    Welcome to the **Quant Analytics Dashboard**.

    Use the sidebar to navigate between:
    - Market Overview
    - Market Comparison
    - Indicators
    - Risk & Volatility
    - Portfolio Analysis
    - Backtesting
    - Market Regime
    - Earnings Impact
    - Sentiment Engine
    """,
)

st.info("Allowed Demo symbols are: AAPL,MSFT,AMZN,GOOGL,TSLA")

st.info("This dashboard is powered by FastAPI backend services.")
