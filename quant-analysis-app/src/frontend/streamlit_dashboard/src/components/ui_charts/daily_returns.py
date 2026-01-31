import plotly.express as px
import pandas as pd


def daily_return_chart(df: pd.DataFrame, symbol: str):
    return px.line(
        df,
        x="date",
        y="daily_return",
        title=f"{symbol} Daily Returns",
    )
