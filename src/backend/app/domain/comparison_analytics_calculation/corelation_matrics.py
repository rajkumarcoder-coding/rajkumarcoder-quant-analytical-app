import pandas as pd


def compute_correlation_matrix(
        daily_returns: pd.DataFrame,
        round_digits: int = 4,
) -> dict:
    """
    Compute correlation matrix for multi-symbol daily returns.

    Parameters
    ----------
    daily_returns : pd.DataFrame
        Columns = symbols
        Rows = dates
        Values = daily returns

    round_digits : int
        Decimal precision for API output

    Returns
    -------
    dict
        Nested dict suitable for JSON response
    """
    # if daily_returns.empty or daily_returns.shape[1] < 2:
    #     return {}

    # if daily_returns.empty or len(daily_returns) < 2:
    #     # explicit, honest behavior
    #     return {col: 0.0 for col in daily_returns.columns}

    if len(daily_returns) < 2:
        symbols = [c.split("_")[-1] for c in daily_returns.columns]
        return {
            s1: {s2: None for s2 in symbols}
            for s1 in symbols
        }

    corr_df = daily_returns.corr()

    # return corr_df.round(round_digits).to_dict()
    return corr_df.round(round_digits).where(pd.notna(corr_df), None).to_dict()
