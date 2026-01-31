from typing import Dict, Optional, Any, List
from app.domain.market_ohlcv_data_classes.response_data_models import DataFrameJSONResponse


class SymbolFieldMapping:
    """
    Defines how symbol-specific columns should be extracted.
    key   -> output field name
    value -> column prefix in raw dataframe
    """

    def __init__(
            self,
            *,
            fields: Dict[str, str],
            total_field: Optional[str] = None,
            round_map: Optional[Dict[str, int]] = None,
    ):
        self.fields = fields
        self.total_field = total_field
        self.round_map = round_map or {}


def refine_symbol_based_api_output(
        *,
        raw_output: DataFrameJSONResponse,
        symbols: str,
        mapping: SymbolFieldMapping,
) -> Dict[str, Any]:
    rows = raw_output.data
    if not rows:
        return {"data": []}

    symbol_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
    refined: Dict[str, Any] = {}

    for symbol in symbol_list:
        symbol_rows: List[Dict[str, Any]] = []
        total_value = None

        for row in rows:
            if total_value is None and mapping.total_field:
                total_value = row.get(f"{mapping.total_field}_{symbol}")

            output_row: Dict[str, Any] = {"date": row.get("Date")}

            for out_key, prefix in mapping.fields.items():
                col_name = f"{prefix}_{symbol}"
                value = row.get(col_name)

                if value is not None and out_key in mapping.round_map:
                    value = round(value, mapping.round_map[out_key])

                output_row[out_key] = value

            symbol_rows.append(output_row)

        refined[symbol] = {
            "symbol": symbol,
            "data": symbol_rows,
        }

        if mapping.total_field:
            refined[symbol]["total_return"] = (
                round(total_value, 6) if total_value is not None else None
            )

    response: Dict[str, Any]
    if len(refined) == 1:
        response = next(iter(refined.values()))
    else:
        response = {
            "symbols": symbol_list,
            "data": refined,
        }

    if raw_output.metrics:
        response["metrics"] = raw_output.metrics

    return response
