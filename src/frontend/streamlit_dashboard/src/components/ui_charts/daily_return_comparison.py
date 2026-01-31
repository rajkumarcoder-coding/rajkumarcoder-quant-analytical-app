import plotly.express as px
import pandas as pd


def daily_return_comparison_chart(dfs: dict) -> px.line:
    combined = []

    for symbol, df in dfs.items():
        temp = df.copy()
        temp["symbol"] = symbol
        combined.append(temp)

    merged = pd.concat(combined)

    fig = px.line(
        merged,
        x="date",
        y="daily_return",
        color="symbol",
        title="Daily Return Comparison",
    )
    return fig
