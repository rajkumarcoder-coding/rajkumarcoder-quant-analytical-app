from typing import Any, Dict


def build_date_query_params(market_query) -> Dict[str, Any]:
    """
    Build date-related query params.

    Priority:
    - period
    - else start / end
    """
    params: Dict[str, Any] = {}

    if market_query.period:
        params["period"] = market_query.period
        return params

    if market_query.start:
        params["start"] = market_query.start.isoformat()

    if market_query.end:
        params["end"] = market_query.end.isoformat()

    return params
