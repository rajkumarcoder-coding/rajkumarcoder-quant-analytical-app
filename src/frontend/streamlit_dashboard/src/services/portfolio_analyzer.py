import streamlit as st
from typing import Dict, Any
from streamlit_dashboard.src.config.base_url import API_BASE_URL
from streamlit_dashboard.src.ui_models.portfolio_query_inputs import PortfolioQueryInput
from streamlit_dashboard.src.fetch.execute_get_request import execute_get_request


@st.cache_data(ttl=300, show_spinner=False)
def fetch_portfolio_analyzer_data(
        *,
        query: PortfolioQueryInput,
        timeout: int = 20,
) -> Dict[str, Any]:
    """
    Fetch comparison data for exactly two symbols.
    """
    url = f"{API_BASE_URL}/market/{query.market_query.symbols}/portfolio/analysis"

    params = query.to_query_params()

    return execute_get_request(
        url=url,
        params=params,
        timeout=timeout,
    )
