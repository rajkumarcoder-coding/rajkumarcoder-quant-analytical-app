import pandas as pd
from app.shared.utils.sanitize_df import sanitize_df
from app.shared.utils.flatten_df import flatten_df
from app.shared.logic_validators.dataframe_validations import require_dataframe


def normalize_df(raw_df: pd.DataFrame) -> pd.DataFrame:
    df = sanitize_df(raw_df)
    df = flatten_df(df)
    df = df.reset_index()
    df["Date"] = df["Date"].astype(str)

    return require_dataframe(df, context="normalize_df", )


def normalize_pipeline_output_df(raw_df: pd.DataFrame) -> pd.DataFrame:
    df = sanitize_df(raw_df)
    df = df.reset_index()
    df["Date"] = df["Date"].astype(str)

    return require_dataframe(df, context="normalize_pipeline_df", )
