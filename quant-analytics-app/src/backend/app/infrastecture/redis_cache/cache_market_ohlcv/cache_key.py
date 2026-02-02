import hashlib


def market_ohlcv_cache_key(
        namespace: str,
        *parts: str | None
) -> str:
    raw = ":".join(str(p) for p in parts)
    digest = hashlib.md5(raw.encode()).hexdigest()
    return f"{namespace}:{digest}"
