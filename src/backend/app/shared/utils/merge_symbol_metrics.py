from typing import Dict, Any


def merge_symbol_metrics(
        metrics_by_name: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Merge metrics into:
    - per_symbol metrics
    - global (cross-symbol) metrics like correlation matrix
    """

    per_symbol: Dict[str, Dict[str, float]] = {}
    global_metrics: Dict[str, Any] = {}

    for metric_name, metric_value in metrics_by_name.items():

        # ---- CASE 1: Per-symbol metric (symbol -> value) ----
        if all(isinstance(v, (int, float)) for v in metric_value.values()):
            for symbol, value in metric_value.items():
                per_symbol.setdefault(symbol, {})[metric_name] = value

        # ---- CASE 2: Global / matrix metric ----
        else:
            global_metrics[metric_name] = metric_value

    return {
        "per_symbol": per_symbol,
        **global_metrics,
    }


def merge_symbol_metrics_v2(
        metrics_by_name: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Merge metrics into:
    - per_symbol metrics (symbol -> scalar)
    - global metrics (symbol -> symbol -> value)
    """

    per_symbol: Dict[str, Dict[str, float]] = {}
    global_metrics: Dict[str, Any] = {}

    for metric_name, metric_value in metrics_by_name.items():

        # ---- CASE 1: Global / matrix metric (nested dict) ----
        if any(isinstance(v, dict) for v in metric_value.values()):
            global_metrics[metric_name] = metric_value
            continue

        # ---- CASE 2: Per-symbol scalar metric ----
        for symbol, value in metric_value.items():
            per_symbol.setdefault(symbol, {})[metric_name] = value

    return {
        "per_symbol": per_symbol,
        **global_metrics,
    }
