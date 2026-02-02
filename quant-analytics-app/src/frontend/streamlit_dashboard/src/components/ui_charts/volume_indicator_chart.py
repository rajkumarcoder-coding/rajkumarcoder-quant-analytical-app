# streamlit_dashboard/src/components/charts/volume_overlay.py

import plotly.graph_objects as go
import pandas as pd


def volume_indicator_chart(
        df: pd.DataFrame,
        symbol: str,
) -> go.Figure:
    fig = go.Figure()

    # ---- Volume Bars ----
    fig.add_trace(
        go.Bar(
            x=df["date"],
            y=df["volume"],
            name="Volume",
            marker=dict(color="rgba(31, 119, 180, 0.6)"),
        ),
    )

    # ---- Volume SMA ----
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["volume_sma"],
            name="Volume SMA",
            line=dict(color="#ff7f0e", width=2),
        ),
    )

    # ---- Volume Spike (highlight) ----
    spike_df = df[df["volume_spike"] > 1]

    fig.add_trace(
        go.Scatter(
            x=spike_df["date"],
            y=spike_df["volume"],
            mode="markers",
            name="Volume Spike",
            marker=dict(color="red", size=8, symbol="triangle-up"),
        ),
    )

    fig.update_layout(
        title=f"{symbol} — Volume Analysis",
        xaxis_title="Date",
        yaxis_title="Volume",
        legend=dict(orientation="h", y=1.02),
        height=350,
        template="plotly_white",
    )

    return fig
