import plotly.graph_objects as go
import pandas as pd


def plot_drawdown_curve(df: pd.DataFrame):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["portfolio_drawdown"],
            mode="lines",
            name="Portfolio Drawdown",
        ),
    )
    fig.update_layout(
        title="Portfolio Drawdown Curve",
        xaxis_title="Date",
        yaxis_title="Drawdown",
    )
    return fig
