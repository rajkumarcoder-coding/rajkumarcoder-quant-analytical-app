from app.core_configs.exceptions import ValidationError
from app.shared.utils.allowed_symbols import load_allowed_symbols


def validate_two_symbols_for_comparison(symbols: str) -> str:
    """
    Ensure exactly two symbols are provided for comparison.
    Returns normalized symbol string if valid.
    """

    symbol_list = [
        s.strip().upper()
        for s in symbols.split(",")
        if s.strip()
    ]

    allowed_symbols = load_allowed_symbols()

    if len(symbol_list) != 2:
        raise ValidationError(
            message="Exactly two symbols are required for comparison",
            reason="invalid_symbol_count",
            context={
                "received_count": len(symbol_list),
                "symbols": symbol_list,
            },
            allowed_symbol=sorted(allowed_symbols),
        )

    # remove duplicates while preserving order
    symbol_list = list(dict.fromkeys(symbol_list))

    if len(symbol_list) != 2:
        raise ValidationError(
            message="Duplicate symbols are not allowed for comparison",
            reason="duplicate_symbols",
            context={
                "symbols": symbol_list,
            },
        )

    return ",".join(symbol_list)
