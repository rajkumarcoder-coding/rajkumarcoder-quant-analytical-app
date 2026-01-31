import pandas as pd
from streamlit_dashboard.src.config.http_fetcher_exceptions import FetchError


# ===============================
# Helpers: Data Preparation
# ===============================

def build_portfolio_df(api_response: dict) -> pd.DataFrame:
    portfolio_data = api_response.get("portfolio_data")
    portfolio_level_two_data = portfolio_data.get("portfolio")

    if not portfolio_level_two_data.get("data"):
        raise FetchError("Empty data received")

    data = portfolio_level_two_data.get("data")
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    return df


def extract_metrics(api_response: dict) -> dict:
    return api_response["portfolio_analysis"]
