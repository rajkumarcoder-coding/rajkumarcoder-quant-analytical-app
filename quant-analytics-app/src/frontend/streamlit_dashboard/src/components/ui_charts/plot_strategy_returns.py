# charts/returns.py
import plotly.graph_objects as go


def plot_strategy_returns(data: list[dict], symbol: str):
    dates = [d["date"] for d in data]
    returns = [d["strategy_return"] for d in data]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=dates, y=returns, name="Strategy Return"))

    fig.update_layout(
        title=f"{symbol} – Strategy Returns",
        xaxis_title="Date",
        yaxis_title="Return",
    )

    return fig
