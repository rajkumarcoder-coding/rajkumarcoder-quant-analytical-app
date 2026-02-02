import pandas as pd
from typing import Optional, Dict, Any, List
from app.domain.market_ohlcv_data_classes.response_data_models import DataFrameJSONResponse


def df_to_records_str_keys(df: pd.DataFrame) -> List[Dict[str, Any]]:
    return [
        {str(k): v for k, v in row.items()}
        for row in df.to_dict(orient="records")
    ]


def df_json_convertor(
        df: pd.DataFrame,
        metrics: Optional[Dict[str, Any]] = None,
) -> DataFrameJSONResponse:
    return DataFrameJSONResponse(
        data=df_to_records_str_keys(df),
        metrics=metrics or {},
    )
