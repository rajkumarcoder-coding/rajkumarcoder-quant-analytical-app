from app.core_configs.exceptions import ValidationError
from app.shared.http_input_validations.validate_symbol_syntax import validate_symbol_syntax
from app.shared.logic_validators.duplicate_value_validator import CommaSeparatedDeduplicator
from app.shared.utils.allowed_symbols import load_allowed_symbols


def validate_demo_symbols(symbols: str) -> str:
    # Missing input
    # if not symbols:
    #     raise ValidationError(
    #         message="No symbols provided",
    #         reason="missing_symbols",
    #     )

    valid_symbols = validate_symbol_syntax(symbols)

    cleaned_symbols = CommaSeparatedDeduplicator.dedupe(valid_symbols)

    # Normalize input
    symbol_list = [s.strip().upper() for s in cleaned_symbols.split(",") if s.strip()]

    # Empty after normalization
    if not symbol_list:
        raise ValidationError(
            message="No valid symbols found",
            reason="empty_symbol_list",
        )

    allowed_symbols = load_allowed_symbols()

    # Invalid symbols (demo restriction)
    invalid_symbols = [s for s in symbol_list if s not in allowed_symbols]

    if invalid_symbols:
        pass # Use pass when you want an empty block
        # raise ValidationError(
        #     message="Invalid symbols provided",
        #     reason="unsupported_demo_symbol",
        #     context={
        #         "invalid_symbols": invalid_symbols,
        #     },
        #     allowed_symbol=sorted(allowed_symbols),
        # )

    #  Return normalized STRING (important)
    symbol_str = ",".join(symbol_list)

    return symbol_str
