import pandas as pd
from app.shared.utils.df_get_symbol_column_names import get_symbol_column_names
from app.shared.logic_validators.dataframe_validations import require_dataframe


def df_select_cols_with_index(
        df: pd.DataFrame,
        cols_names: str,
        symbols: str,
) -> pd.DataFrame:
    selected_cols = get_symbol_column_names(df, cols_names, symbols)

    # ---- Handle Date ----
    if df.index.name == "Date":
        return df[selected_cols].copy()

    if "Date" in df.columns:
        return df[["Date"] + selected_cols].copy()

    df = df[selected_cols].copy()

    return require_dataframe(df, context="df_select_cols_with_index")
