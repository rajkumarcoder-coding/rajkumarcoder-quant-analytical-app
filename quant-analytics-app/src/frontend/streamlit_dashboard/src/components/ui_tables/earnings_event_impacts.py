import pandas as pd
import streamlit as st


def earnings_event_impacts_table(symbol_df: pd.DataFrame):
    # -----------------------------
    # TABLE SECTION
    # -----------------------------
    st.subheader("📋 Earnings Event Table")

    table_df = symbol_df[
        ["date", "event_return", "pre_return", "post_return", "gap"]
    ].sort_values("date")

    st.dataframe(
        table_df.style.format(
            {
                "event_return": "{:.2%}",
                "pre_return": "{:.2%}",
                "post_return": "{:.2%}",
                "gap": "{:.2%}",
            },
        ),
        width="stretch",
    )
