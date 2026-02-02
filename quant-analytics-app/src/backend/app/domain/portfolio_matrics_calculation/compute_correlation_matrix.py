import pandas as pd


# use one when all symbols added return_df and store is a dict
def compute_correlation_matrix(
        returns_df: pd.DataFrame,
) -> dict:
    """
    Always expects multi-symbol returns.
    Returns JSON-safe correlation matrix.
    """

    numeric_df = returns_df.select_dtypes(include="number")

    if numeric_df.shape[1] < 2:
        raise ValueError("Correlation requires at least two symbols")

    corr_df = numeric_df.corr()

    # sanitize for API
    return (
        corr_df
        .round(4)
        .to_dict()
    )
