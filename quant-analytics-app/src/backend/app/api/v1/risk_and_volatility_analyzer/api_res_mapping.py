from app.shared.utils.api_json_refining import SymbolFieldMapping

RISK_ANALYZER_MAPPING = SymbolFieldMapping(
    fields={
        "close": "Close",
        "daily_return": "Daily_Return",
        "daily_volatility": "Daily_Volatility",
        "drawdown": "Drawdown",
    },
    total_field="Total_Return",
    round_map={
        "close": 2,
        "daily_return": 6,
        "daily_volatility": 6,
        "drawdown": 6,
    },
)
