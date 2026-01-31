from app.shared.utils.api_json_refining import SymbolFieldMapping

INDICATORS_MAPPING = SymbolFieldMapping(
    fields={
        "close": "Close",
        "volume": "Volume",
        "sma": "SMA",
        "ema": "EMA",
        "momentum": "Momentum",
        "roc": "ROC",
        "atr": "ATR",
        "volume_sma": "Volume_SMA",
        "volume_spike": "Volume_Spike",
        "obv": "OBV",
    },
    round_map={
        "close": 2,
        "volume": 2,
        "sma": 2,
        "ema": 2,
        "momentum": 2,
        "roc": 2,
        "atr": 6,
        "volume_sma": 6,
        "volume_spike": 6,
        "obv": 6,
    },
)
