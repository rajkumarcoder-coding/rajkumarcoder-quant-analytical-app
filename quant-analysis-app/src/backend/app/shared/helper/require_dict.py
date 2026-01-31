def require_dict(value, default: dict | None = None) -> dict:
    """
    Ensure value is a dictionary, otherwise return default or empty dict.
    """
    if isinstance(value, dict):
        return value
    return default or {}
