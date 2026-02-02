from typing import Dict, List
import pandas as pd
from app.shared.logic_validators.dataframe_validations import require_dataframe


def reshape_features_per_symbol(
        df: pd.DataFrame,
        symbols: List[str],
) -> Dict[str, List[dict]]:
    """
    Convert wide multi-symbol feature DF into per-symbol records.
    """
    df = require_dataframe(df, context="reshape_features_per_symbol")

    result: Dict[str, List[dict]] = {}

    for symbol in symbols:
        symbol_cols = {
            col.replace(f"_{symbol}", ""): col
            for col in df.columns
            if col.endswith(f"_{symbol}")
        }

        symbol_df = df[["date"] + list(symbol_cols.values())].rename(
            columns=symbol_cols,
        )

        result[symbol] = symbol_df.to_dict(orient="records")

    return result


# per_symbol_data = reshape_features_per_symbol(
#     df=multi_symbol_features,
#     symbols=["AAPL", "MSFT", "GOOGL"],
# )
