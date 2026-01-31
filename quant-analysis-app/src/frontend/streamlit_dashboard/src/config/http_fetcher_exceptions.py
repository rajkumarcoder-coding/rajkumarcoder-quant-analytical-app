class FetchError(Exception):
    def __init__(
            self,
            message: str,
            *,
            reason: str | None = None,
            context: dict | None = None,
            current_symbol: str | None = None,
            allowed_symbol: list[str] | None = None,
            status_code: int | None = None,
    ):
        self.message = message
        self.reason = reason
        self.context = context or {}
        self.current_symbol = current_symbol
        self.allowed_symbol = allowed_symbol
        self.status_code = status_code
        super().__init__(message)
