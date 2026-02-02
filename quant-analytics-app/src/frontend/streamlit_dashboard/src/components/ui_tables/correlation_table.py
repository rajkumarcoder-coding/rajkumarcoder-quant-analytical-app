import pandas as pd
import streamlit as st


# old one where corr has only int value
# def render_correlation_matrix(corr: dict) -> None:
#     st.subheader("Correlation Matrix")
#     df = pd.DataFrame(corr)
#     st.dataframe(df.style.format("{:.4f}"))

# new one where corr may have value of None
def correlation_dict_to_df(
        corr: dict[str, dict[str, float | None]],
) -> pd.DataFrame:
    df = pd.DataFrame(corr)
    return df.astype(float)  # None → NaN (safe in pandas)


def render_correlation_matrix(corr: dict):
    df = correlation_dict_to_df(corr)

    st.subheader("Correlation Matrix")

    st.dataframe(
        df.style.format("{:.4f}", na_rep="—"),
    )
