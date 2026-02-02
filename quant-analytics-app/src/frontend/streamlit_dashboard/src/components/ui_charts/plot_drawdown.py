# charts/drawdown.py
import plotly.graph_objects as go


def plot_drawdown(data: list[dict], symbol: str):
    dates = [d["date"] for d in data]
    drawdown = [d["drawdown"] for d in data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=drawdown, mode="lines", name="Drawdown"))

    fig.update_layout(
        title=f"{symbol} – Drawdown",
        xaxis_title="Date",
        yaxis_title="Drawdown",
    )

    return fig
