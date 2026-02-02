from dataclasses import dataclass
from app.core_configs.app_settings import settings


@dataclass(frozen=True)
class RateLimitConfig:
    GLOBAL_RATE_LIMIT = settings.RATE_LIMIT_WINDOW_SECONDS
    GLOBAL_WINDOW_SECONDS = settings.RATE_LIMIT_REQUESTS
    API_RATE_LIMIT = settings.API_RATE_LIMIT_REQUESTS
    API_WINDOW_SECONDS = settings.API_RATE_LIMIT_WINDOW_SECONDS
