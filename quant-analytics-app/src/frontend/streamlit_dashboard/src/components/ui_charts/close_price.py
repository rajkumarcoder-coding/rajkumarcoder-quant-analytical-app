import plotly.express as px
import pandas as pd


def close_price_chart(df: pd.DataFrame, symbol: str):
    return px.line(
        df,
        x="date",
        y="close",
        title=f"{symbol} Close Price",
    )
