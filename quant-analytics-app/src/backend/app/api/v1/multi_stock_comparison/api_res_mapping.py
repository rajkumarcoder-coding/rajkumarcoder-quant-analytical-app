from app.shared.utils.api_json_refining import SymbolFieldMapping

MARKET_PRICE_MAPPING = SymbolFieldMapping(
    fields={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
        "daily_return": "Daily_Return",
    },
    round_map={
        "open": 2,
        "high": 2,
        "low": 2,
        "close": 2,
        "daily_return": 6,
    },
)
