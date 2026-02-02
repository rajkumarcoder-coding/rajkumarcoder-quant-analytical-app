# noinspection DuplicatedCode
def map_backtesting_response(api_response: dict) -> dict:
    backtesting_data = api_response.get("backtesting_data", [])
    backtesting_analysis = api_response.get("backtesting_analysis", {})

    # 1. Symbols are dynamic
    symbols = list(backtesting_analysis.keys())

    # Fields you want in final per-symbol data (NO suffix)
    # BASE_FIELDS = [
    #     "close",
    #     "signal",
    #     "position",
    #     "strategy_return",
    #     "equity",
    #     "drawdown",
    # ]

    # Mapping from API column prefix → output field
    field_map = {
        "Close": "close",
        "Signal": "signal",
        "Position": "position",
        "Strategy_Return": "strategy_return",
        "Equity": "equity",
        "Drawdown": "drawdown",
    }

    # Initialize output container
    data_by_symbol = {
        symbol: {"data": [], "metrics": backtesting_analysis.get(symbol, {})}
        for symbol in symbols
    }

    # 2. Build per-symbol time series
    for row in backtesting_data:
        date = row.get("Date")

        for symbol in symbols:
            record = {"date": date}

            for api_field, output_field in field_map.items():
                col = f"{api_field}_{symbol}"
                if col in row:
                    record[output_field] = row[col]

            data_by_symbol[symbol]["data"].append(record)

    return {
        "symbols": symbols,
        "data": data_by_symbol,
    }


# noinspection DuplicatedCode
def map_dataframe_and_metrics_json_api_response(
        api_response: dict,
        field_map: dict,
        service_name: str
) -> dict:
    data = api_response.get(f"{service_name}_data", [])
    analysis = api_response.get(f"{service_name}_analysis", {})

    # 1. Symbols are dynamic
    symbols = list(analysis.keys())

    # Initialize output container
    simble_by_date = {
        symbol: {"data": [], "metrics": analysis.get(symbol, {})}
        for symbol in symbols
    }

    # 2. Build per-symbol time series
    for row in data:
        date = row.get("Date")

        for symbol in symbols:
            record = {"date": date}

            for api_field, output_field in field_map.items():
                col = f"{api_field}_{symbol}"
                if col in row:
                    record[output_field] = row[col]

            simble_by_date[symbol]["data"].append(record)

    return {
        "symbols": symbols,
        "data": simble_by_date,
    }


def map_dataframe_json_api_response(
        api_response: dict,
        field_map: dict,
        service_name: str = "earnings_impact",
) -> dict:
    """
    Maps wide earnings impact API output into per-symbol time series.
    """

    data = api_response.get(f"{service_name}_data", [])

    if not data:
        return {"symbols": [], "data": {}}

    # 1. Dynamically detect symbols from column names
    symbols = set()
    for row in data:
        for key in row.keys():
            if "_" in key and key != "Date":
                symbols.add(key.split("_")[-1])

    symbols = sorted(symbols)

    # 2. Initialize output container
    # symbol_by_date = {
    #     symbol: {"data": [], "metrics": {}}
    #     for symbol in symbols
    # }
    symbol_by_date = {
        symbol: {"data": []}
        for symbol in symbols
    }

    # 3. Build per-symbol time series
    for row in data:
        date = row.get("Date")

        for symbol in symbols:
            record = {"date": date}

            for api_field, output_field in field_map.items():
                col = f"{api_field}_{symbol}"
                if col in row:
                    record[output_field] = row[col]

            # only append if something exists besides date
            if len(record) > 1:
                symbol_by_date[symbol]["data"].append(record)

    return {
        "symbols": symbols,
        "data": symbol_by_date,
    }
