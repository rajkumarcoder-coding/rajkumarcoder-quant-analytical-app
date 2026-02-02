from typing import Any, Dict, List
from app.domain.market_ohlcv_data_classes.response_data_models import DataFrameJSONResponse


def refine_market_price_api_output(
        raw_output: DataFrameJSONResponse,
        symbols: str,
) -> Dict[str, Any]:
    """
    Refines raw multi-symbol DataFrameJSONResponse into clean API output.
    Pipeline remains untouched.
    """

    rows = raw_output.data
    if not rows:
        return {"data": []}

    # ---- normalize symbols input ----
    symbol_list: List[str] = [
        s.strip().upper() for s in symbols.split(",") if s.strip()
    ]

    refined: Dict[str, Any] = {}

    for symbol in symbol_list:
        symbol_data: List[Dict[str, Any]] = []
        total_return = None

        for row in rows:
            # capture total_return once
            if total_return is None:
                total_return = row.get(f"Total_Return_{symbol}")

            symbol_row = {
                "date": row.get("Date"),
                "open": round(row[f"Open_{symbol}"], 2) if f"Open_{symbol}" in row else None,
                "high": round(row[f"High_{symbol}"], 2) if f"High_{symbol}" in row else None,
                "low": round(row[f"Low_{symbol}"], 2) if f"Low_{symbol}" in row else None,
                "close": round(row[f"Close_{symbol}"], 2) if f"Close_{symbol}" in row else None,
                "volume": int(row[f"Volume_{symbol}"]) if f"Volume_{symbol}" in row else None,
                "daily_return": round(row[f"Daily_Return_{symbol}"], 6)
                if f"Daily_Return_{symbol}" in row
                else None,
                "cumulative_return": round(row[f"Cumulative_Return_{symbol}"], 6)
                if f"Cumulative_Return_{symbol}" in row
                else None,
            }

            symbol_data.append(symbol_row)

        refined[symbol] = {
            "symbol": symbol,
            "total_return": round(total_return, 6) if total_return is not None else None,
            "data": symbol_data,
        }

    # ---- final response shape ----
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
