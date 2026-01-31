import pandas as pd
from app.shared.logic_validators.dataframe_validations import require_dataframe


def normalize_return_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [
        col.replace("Daily_Return_", "")
        for col in df.columns
    ]
    return require_dataframe(df, context="normalize return columns")
