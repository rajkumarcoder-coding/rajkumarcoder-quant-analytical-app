# import math
#
#
# def sanitize_metrics(obj):
#     if isinstance(obj, dict):
#         return {k: sanitize_metrics(v) for k, v in obj.items()}
#     if isinstance(obj, list):
#         return [sanitize_metrics(v) for v in obj]
#     if isinstance(obj, float):
#         if math.isnan(obj) or math.isinf(obj):
#             return None
#     return obj


# for solving the issue of fetching by <2 days gap in comparison date, use this
# 1. pydantic model of backend - corelation_maatrix=Dict[str, Dict[str, float | None]]
"""
2.
def compute_correlation_matrix_safe(
    daily_returns: pd.DataFrame,
    symbols: List[str],
) -> Dict[str, Dict[str, float | None]]:

    # Not enough data → return empty matrix
    if len(daily_returns) < 2:
        return empty_correlation_matrix(symbols)

    corr = daily_returns.corr()

    return corr.round(6).where(pd.notna(corr), None).to_dict()

note - it will include correlation_matrix as seperate part from "per_symbol" in metrics obj
and it will produce "None" value which is json compertabe
"""
