import pandas as pd
from typing import List


def print_duplicate_columns(df: pd.DataFrame) -> List[str]:
    """
    Prints duplicate column names in a DataFrame.
    Returns a list of duplicate column names.
    """

    duplicates = df.columns[df.columns.duplicated()]

    if len(duplicates) > 0:
        print("❌ Duplicate columns detected:")
        for col in duplicates:
            print(col)
        return duplicates.tolist()

    return []
