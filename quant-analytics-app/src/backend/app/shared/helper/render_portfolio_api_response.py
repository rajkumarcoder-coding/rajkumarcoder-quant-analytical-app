from typing import Any, Dict, List


def reshape_portfolio_api_response(
        raw_response: dict,
        symbols: list[str],
) -> dict:
    asset_data = {symbol: [] for symbol in symbols}
    portfolio_data = []

    for row in raw_response["data"]:
        date = row["Date"]

        portfolio_data.append(
            {
                "date": date,
                "portfolio_return": row.get("Portfolio_Return"),
            },
        )

        for symbol in symbols:
            asset_data[symbol].append(
                {
                    "date": date,
                    "close": row.get(f"Close_{symbol}"),
                    "daily_return": row.get(f"Daily_Return_{symbol}"),
                    "drawdown": row.get(f"Drawdown_{symbol}"),
                },
            )

    return {
        "symbols": symbols,
        "portfolio": {
            "data": portfolio_data
        },
        "assets": {
            symbol: {"data": asset_data[symbol]}
            for symbol in symbols
        }
    }


def reshape_portfolio_api_response_v2(
        raw_response: List[Dict[str, Any]],
        symbols: List[str],
) -> Dict[str, Any]:
    asset_data = {symbol: [] for symbol in symbols}
    portfolio_data = []

    for row in raw_response:
        date = row.get("Date")

        portfolio_data.append(
            {
                "date": date,
                "portfolio_return": row.get("Portfolio_Return"),
                "capital_curve": row.get("Capital_Curve"),
                "portfolio_drawdown": row.get("Portfolio_Drawdown"),
            },
        )

        for symbol in symbols:
            asset_data[symbol].append(
                {
                    "date": date,
                    "close": row.get(f"Close_{symbol}"),
                    "daily_return": row.get(f"Daily_Return_{symbol}"),
                    "drawdown": row.get(f"Drawdown_{symbol}"),
                },
            )

    return {
        "symbols": symbols,
        "portfolio": {
            "data": portfolio_data
        },
        "assets": {
            symbol: {"data": asset_data[symbol]}
            for symbol in symbols
        }
    }
