def parse_symbols(symbols_raw: str) -> list[str]:
    return [s.strip().upper() for s in symbols_raw.split(",") if s.strip()]
