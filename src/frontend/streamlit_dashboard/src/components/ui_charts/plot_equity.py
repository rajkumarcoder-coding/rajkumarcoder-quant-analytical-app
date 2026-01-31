# charts/equity.py
import plotly.graph_objects as go


def plot_equity(data: list[dict], symbol: str):
    dates = [d["date"] for d in data]
    equity = [d["equity"] for d in data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=equity, mode="lines", name="Equity"))

    fig.update_layout(
        title=f"{symbol} – Equity Curve",
        xaxis_title="Date",
        yaxis_title="Equity",
    )

    return fig
