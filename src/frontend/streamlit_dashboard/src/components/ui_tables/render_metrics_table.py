# tables/metrics.py
import streamlit as st
import pandas as pd


def format_metric(key: str, value):
    if value is None:
        return "—"

    if key in {"total_return", "max_drawdown", "win_rate"}:
        return f"{value * 100:.2f}%"

    if key == "sharpe_ratio":
        return f"{value:.2f}"

    if key == "num_trades":
        return f"{int(value)}"

    return value


#  number like 6.000, 0.15%, -0.23
def render_metrics_table(metrics: dict):
    df = pd.DataFrame(metrics, index=["Value"]).T
    st.table(df)


# charts with actual number like 6, 15%, -25%
def render_metrics_table_v2(metrics: dict):
    formatted = {
        k: format_metric(k, v)
        for k, v in metrics.items()
    }

    df = pd.DataFrame(
        list(formatted.items()),
        columns=["Metric", "Value"],
    )

    st.table(df)
