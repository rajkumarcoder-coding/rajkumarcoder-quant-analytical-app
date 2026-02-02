import pandas as pd
import streamlit as st
import plotly.express as px


def price_based_sentiment_charts(df_table: pd.DataFrame):
    # -----------------------------
    # CHART SECTION
    # -----------------------------
    st.subheader("📈 Metric Visualizations")

    col1, col2 = st.columns(2)

    # Momentum Bar Chart
    with col1:
        fig_momentum = px.bar(
            df_table,
            x="Symbol",
            y="momentum",
            color="Sentiment",
            title="Momentum by Symbol",
        )
        st.plotly_chart(fig_momentum, width="stretch")

    # Volume Z-Score Bar Chart
    with col2:
        fig_volume = px.bar(
            df_table,
            x="Symbol",
            y="volume_zscore",
            color="Sentiment",
            title="Volume Z-Score by Symbol",
        )
        st.plotly_chart(fig_volume, width="stretch")


def price_based_sentiment_confidence_chart(df_table: pd.DataFrame):
    # -----------------------------
    # CONFIDENCE CHART
    # -----------------------------
    st.subheader("🎯 Sentiment Confidence")

    fig_confidence = px.bar(
        df_table,
        x="Symbol",
        y="Confidence",
        color="Sentiment",
        title="Confidence Score by Symbol",
        range_y=[0, 1],
    )
    st.plotly_chart(fig_confidence, width="stretch")
