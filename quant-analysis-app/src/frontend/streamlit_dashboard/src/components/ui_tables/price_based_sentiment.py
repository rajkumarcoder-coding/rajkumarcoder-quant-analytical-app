import streamlit as st
import pandas as pd


def price_based_sentiment_table(df_table: pd.DataFrame) -> st.dataframe:
    # -----------------------------
    # TABLE SECTION
    # -----------------------------
    st.subheader("📋 Sentiment Metrics Table")

    st.dataframe(
        df_table.set_index("Symbol"),
        width="stretch",
    )
