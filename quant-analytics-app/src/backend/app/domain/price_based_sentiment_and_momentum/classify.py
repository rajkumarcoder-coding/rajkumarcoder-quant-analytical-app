def classify(momentum: float, trend_strength: float, vol_z: float) -> str:
    if momentum > 0 and trend_strength > 0 and vol_z > 1:
        return "Bullish"
    elif momentum < 0 and trend_strength < 0 and vol_z > 1:
        return "Bearish"
    else:
        return "Neutral"
