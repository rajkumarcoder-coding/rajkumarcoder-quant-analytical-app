import pandas as pd
import plotly.graph_objects as go


def plot_capital_growth(df: pd.DataFrame):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["capital_curve"],
            mode="lines",
            name="Portfolio Value",
        ),
    )
    fig.update_layout(
        title="Portfolio Capital Growth",
        yaxis_title="Capital",
        xaxis_title="Date",
    )
    return fig
