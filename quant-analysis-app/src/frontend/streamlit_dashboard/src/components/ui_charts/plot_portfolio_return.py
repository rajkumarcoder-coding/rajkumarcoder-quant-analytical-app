import plotly.graph_objects as go
import pandas as pd


def plot_portfolio_return(df: pd.DataFrame):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["portfolio_return"],
            mode="lines",
            name="Portfolio Return",
        ),
    )
    fig.update_layout(
        title="Portfolio Daily Returns",
        xaxis_title="Date",
        yaxis_title="Return",
    )
    return fig
