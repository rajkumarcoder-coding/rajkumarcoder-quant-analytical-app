import streamlit as st
from typing import Dict, Any
from streamlit_dashboard.src.config.base_url import API_BASE_URL
from streamlit_dashboard.src.ui_models.backtesting_engine import BacktestingQueryInput
from streamlit_dashboard.src.fetch.execute_get_request import execute_get_request


@st.cache_data(ttl=300, show_spinner=False)
def fetch_backtesting_engine_data(
        *,
        query: BacktestingQueryInput,
        timeout: int = 20,
) -> Dict[str, Any]:
    """
    Fetch comparison data for exactly two symbols.
    """
    url = f"{API_BASE_URL}/market/{query.market_query.symbols}/backtesting"

    params = query.to_query_params()

    return execute_get_request(
        url=url,
        params=params,
        timeout=timeout,
    )
