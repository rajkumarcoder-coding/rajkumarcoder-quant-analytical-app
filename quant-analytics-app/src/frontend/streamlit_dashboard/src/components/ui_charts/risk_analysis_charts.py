import plotly.graph_objects as go


def plot_price(df):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["close"],
            mode="lines",
            name="Close Price",
        ),
    )
    fig.update_layout(
        title="Price",
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig


def plot_drawdown(df):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["drawdown"],
            fill="tozeroy",
            name="Drawdown",
        ),
    )
    fig.update_layout(
        title="Drawdown",
        height=250,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig


def plot_volatility(df):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["daily_volatility"],
            mode="lines",
            name="Daily Volatility",
        ),
    )
    fig.update_layout(
        title="Daily Volatility",
        height=250,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig
