from datetime import date


def resolve_time_params(
        *,
        period: str | None,
        start: date | None,
        end: date | None,
) -> dict:
    # Case 1: User gave nothing → assign default
    if period is None and start is None and end is None:
        return {"period": "1mo"}

    # Case 2: Period mode
    if period is not None:
        return {"period": period}

    # Case 3: Date range mode
    params = {}
    if start is not None:
        params["start"] = start.isoformat()
    if end is not None:
        params["end"] = end.isoformat()

    return params


    # if config.period:
    #         kwargs["period"] = config.period
    #     else:
    #         if config.start:
    #             kwargs["start"] = config.start.isoformat()
    #         if config.end:
    #             kwargs["end"] = config.end.isoformat()