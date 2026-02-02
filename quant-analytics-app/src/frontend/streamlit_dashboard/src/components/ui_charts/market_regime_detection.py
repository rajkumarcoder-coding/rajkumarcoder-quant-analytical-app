import plotly.graph_objs as go
import pandas as pd


def plot_risk_state_timeline(df: pd.DataFrame, symbol: str):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["trend_strength"],
            mode="lines+markers",
            name="Trend Strength",
        ),
    )

    fig.update_layout(
        title=f"{symbol} – Trend Strength Over Time",
        xaxis_title="Date",
        yaxis_title="Trend Strength",
        height=350,
    )

    return fig


def plot_volatility(df: pd.DataFrame, symbol: str):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["volatility"],
            mode="lines",
            name="Volatility",
        ),
    )

    fig.update_layout(
        title=f"{symbol} – Rolling Volatility",
        xaxis_title="Date",
        yaxis_title="Volatility",
        height=300,
    )

    return fig
