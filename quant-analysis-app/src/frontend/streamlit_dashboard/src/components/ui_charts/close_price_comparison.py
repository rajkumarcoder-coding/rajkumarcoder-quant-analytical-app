import plotly.express as px
import pandas as pd


def close_price_comparison_chart(dfs: dict) -> px.line:
    combined = []

    for symbol, df in dfs.items():
        temp = df.copy()
        temp["symbol"] = symbol
        combined.append(temp)

    merged = pd.concat(combined)

    fig = px.line(
        merged,
        x="date",
        y="close",
        color="symbol",
        title="Close Price Comparison",
    )
    return fig
