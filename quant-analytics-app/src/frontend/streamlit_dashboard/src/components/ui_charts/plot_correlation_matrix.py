import pandas as pd
import plotly.express as px


def plot_correlation_matrix(corr_matrix: dict):
    corr_df = pd.DataFrame(corr_matrix)
    fig = px.imshow(
        corr_df,
        text_auto=True,
        aspect="auto",
        title="Asset Correlation Matrix",
    )
    return fig
