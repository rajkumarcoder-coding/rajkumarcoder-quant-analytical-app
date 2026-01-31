from typing import Dict


def parse_weights(weights: str) -> Dict[str, float]:
    """
    Parse weights string like:
    'AAPL=40,MSFT=30,GOOGL=30'
    into:
    {'AAPL': 0.4, 'MSFT': 0.3, 'GOOGL': 0.3}
    """

    if not weights:
        raise ValueError("Weights string is empty")

    weight_map: Dict[str, float] = {}

    for item in weights.split(","):
        try:
            symbol, value = item.split("=")
        except ValueError:
            raise ValueError(
                f"Invalid weight format: '{item}'. Expected SYMBOL=VALUE",
            )

        symbol = symbol.strip().upper()

        try:
            value = float(value.strip())
        except ValueError:
            raise ValueError(
                f"Invalid weight value for '{symbol}': '{value}'",
            )

        if value < 0:
            raise ValueError(f"Weight must be non-negative for '{symbol}'")

        weight_map[symbol] = value

    total = sum(weight_map.values())

    if total == 0:
        raise ValueError("Total weight cannot be zero")

    # Normalize to fractions (sum = 1.0)
    return {k: v / total for k, v in weight_map.items()}
