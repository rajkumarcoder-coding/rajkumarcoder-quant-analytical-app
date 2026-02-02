import pandas as pd
import numpy as np
from app.shared.logic_validators.dataframe_validations import require_dataframe


def sanitize_df(df: pd.DataFrame) -> pd.DataFrame:
    # df = df.copy()
    # pd.set_option('future.no_silent_downcasting', True) -> later, not now
    df = df.infer_objects(copy=False)
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.fillna(0)
    return require_dataframe(df, context="flatten_df")
