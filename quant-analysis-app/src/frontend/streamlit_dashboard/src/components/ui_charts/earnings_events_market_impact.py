import pandas as pd
import streamlit as st
import plotly.express as px


def earnings_events_market_impact_chart(symbol_df: pd.DataFrame):
    # -----------------------------
    # CHARTS SECTION
    # -----------------------------
    st.subheader("📈 Earnings Impact Charts")

    # Event Day Return
    fig_event = px.bar(
        symbol_df,
        x="date",
        y="event_return",
        title="Event Day Return",
        labels={"event_return": "Return", "date": "Earnings Date"},
    )
    st.plotly_chart(fig_event, width="stretch")

    # Pre vs Post Return
    fig_pre_post = px.line(
        symbol_df.melt(
            id_vars="date",
            value_vars=["pre_return", "post_return"],
            var_name="period",
            value_name="return",
        ),
        x="date",
        y="return",
        color="period",
        title="Pre vs Post Earnings Return",
        labels={"return": "Return", "date": "Earnings Date"},
    )
    st.plotly_chart(fig_pre_post, width="stretch")

    # Gap chart
    fig_gap = px.bar(
        symbol_df,
        x="date",
        y="gap",
        title="Earnings Gap",
        labels={"gap": "Gap", "date": "Earnings Date"},
    )
    st.plotly_chart(fig_gap, width="stretch")
