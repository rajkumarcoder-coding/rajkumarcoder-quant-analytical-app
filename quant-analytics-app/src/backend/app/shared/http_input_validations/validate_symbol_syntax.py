import re
from typing import List

from app.core_configs.exceptions import ValidationError

SYMBOL_PATTERN = re.compile(r"^[A-Z0-9.\-^=]{1,20}$")


def validate_symbol_syntax(symbols: str) -> str:
    """
    Validate symbol syntax (not existence).
    Lowercase is normalized to uppercase.
    Supports stocks, indices, forex, crypto.
    """

    if not symbols:
        raise ValidationError(
            message="No symbols provided",
            reason="missing_symbols",
        )

    parsed: List[str] = []
    invalid: List[str] = []

    for raw in symbols.split(","):
        sym = raw.strip().upper()  # 🔑 normalize first

        if not sym:
            continue

        # character + length validation
        if not SYMBOL_PATTERN.fullmatch(sym):
            invalid.append(sym)
            continue

        # reject repeated nonsense
        if any(bad in sym for bad in ("..", "^^", "--", "==")):
            invalid.append(sym)
            continue

        parsed.append(sym)

    if not parsed:
        raise ValidationError(
            message="No valid symbols after validation",
            reason="empty_symbol_list",
        )

    if invalid:
        raise ValidationError(
            message="Invalid symbol syntax",
            reason="invalid_symbol_format",
            context={
                "invalid_symbols": invalid,
            },
        )

    # remove duplicates, preserve order
    unique = list(dict.fromkeys(parsed))

    return ",".join(unique)
