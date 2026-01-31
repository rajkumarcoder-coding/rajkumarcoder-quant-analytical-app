from typing import Dict, Any
from app.core_configs.exceptions import ValidationError


def embed_metrics_per_symbol(response: Dict[str, Any], context: str) -> Dict[str, Any]:
    """
    Normalize single-symbol and multi-symbol risk responses into
    a unified multi-symbol response with per-symbol embedded metrics.
    """

    # -------------------------
    # Case 1: Multi-symbol input
    # -------------------------
    if "symbols" in response and "data" in response:
        symbols = response.get("symbols", [])
        data = response.get("data", {})
        metrics = response.get("metrics", {})

        new_data = {}

        for symbol in symbols:
            symbol_block = data.get(symbol, {})
            new_data[symbol] = {
                "data": symbol_block.get("data", []),
                "metrics": metrics.get(symbol),
            }

        return {
            "symbols": symbols,
            "data": new_data,
        }

    # -------------------------
    # Case 2: Single-symbol input
    # -------------------------
    if "symbol" in response and "data" in response:
        symbol = response["symbol"]
        metrics = response.get("metrics", {}).get(symbol)

        return {
            "symbols": [symbol],
            "data": {
                symbol: {
                    "data": response.get("data", []),
                    "metrics": metrics,
                }
            },
        }

    # -------------------------
    # Unknown shape → fail fast
    # -------------------------
    raise ValidationError(message=f"Unable to normalize {context} response")


# this is for multi stock only
# def embed_metrics_per_symbol_v2(response: Dict[str, Any]) -> Dict[str, Any]:
#     """
#     Move top-level per-symbol metrics into each symbol's data block.
#     Removes redundant 'symbol' fields and top-level 'metrics'.
#     """
#
#     symbols = response.get("symbols", [])
#     data = response.get("data", {})
#     metrics = response.get("metrics", {})
#
#     new_data = {}
#
#     for symbol in symbols:
#         symbol_block = data.get(symbol, {})
#
#         new_data[symbol] = {
#             "data": symbol_block.get("data", []),
#             "metrics": metrics.get(symbol),
#         }
#
#     return {
#         "symbols": symbols,
#         "data": new_data,
#     }
