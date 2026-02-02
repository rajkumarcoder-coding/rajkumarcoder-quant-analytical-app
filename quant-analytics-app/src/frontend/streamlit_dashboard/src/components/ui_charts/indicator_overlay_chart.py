# streamlit_dashboard/src/components/charts/indicator_overlay.py

import plotly.graph_objects as go
import pandas as pd


def indicator_overlay_chart(
        df: pd.DataFrame,
        symbol: str,
) -> go.Figure:
    fig = go.Figure()

    # ---- Close Price ----
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["close"],
            name="Close",
            line=dict(color="#1f77b4", width=2),
        ),
    )

    # ---- SMA ----
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["sma"],
            name="SMA",
            line=dict(color="#ff7f0e", width=1.5, dash="dot"),
        ),
    )

    # ---- EMA ----
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["ema"],
            name="EMA",
            line=dict(color="#2ca02c", width=1.5),
        ),
    )

    # ---- ATR (optional, secondary axis) ----
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["atr"],
            name="ATR",
            yaxis="y2",
            line=dict(color="#d62728", width=1),
        ),
    )

    fig.update_layout(
        title=f"{symbol} — Price & Trend Indicators",
        xaxis_title="Date",
        yaxis_title="Price",
        yaxis2=dict(
            title="ATR",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        legend=dict(orientation="h", y=1.02),
        height=450,
        template="plotly_white",
    )

    return fig
