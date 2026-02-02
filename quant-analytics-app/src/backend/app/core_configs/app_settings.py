from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
from app.core_configs.cache_ttl import RedisTTL

ttl = RedisTTL()


class AppSettings(BaseSettings):
    # ============================
    # APP
    # ============================
    APP_ENV: str = Field(default="development")
    DEBUG: bool = Field(default=False)
    API_KEY: str = Field(default="this is my api key")

    # ============================
    # SERVER
    # ============================
    HOST: str = Field(default="127.0.0.1")
    PORT: int = Field(default=8000)
    RELOAD: bool = Field(default=False)

    # ============================
    # REDIS
    # ============================
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_DB: int = Field(default=0)
    REDIS_PASSWORD: Optional[str] = Field(default=None)  # 5 minutes

    REDIS_DECODE_RESPONSES: bool = Field(default=False)
    REDIS_MAX_CONNECTIONS: int = Field(default=100)

    # ============================
    # REDIS TTLs (CACHING)
    # ============================
    # 🔒 Explicit cache TTL (time to live)
    REDIS_TTL_SECONDS: int = Field(default=300)
    REDIS_TTL_OHLCV_SECONDS: int = Field(default=ttl.OHLCV)
    REDIS_TTL_MARKET_RETURNS_SECONDS: int = Field(default=ttl.RETURNS)

    # ============================
    # RATE LIMITING
    # ============================
    RATE_LIMIT_WINDOW_SECONDS: int = Field(default=60)
    RATE_LIMIT_REQUESTS: int = Field(default=100)
    API_RATE_LIMIT_WINDOW_SECONDS: int = Field(default=60)
    API_RATE_LIMIT_REQUESTS: int = Field(default=10)

    # ============================
    # POSTGRESQL (DOCKER-BASED)
    # ============================
    # POSTGRES_HOST: str = Field(default="localhost")
    # POSTGRES_PORT: int = Field(default=5432)
    # POSTGRES_DB: str = Field(default="quant_analytics")
    # POSTGRES_USER: str = Field(default="postgres")
    # POSTGRES_PASSWORD: str = Field(default="postgres")
    #
    # POSTGRES_POOL_SIZE: int = Field(default=10)
    # POSTGRES_MAX_OVERFLOW: int = Field(default=20)
    # POSTGRES_ECHO: bool = Field(default=False)

    # ============================
    # DATA / EXTERNAL
    # ============================
    DATA_SOURCE: str = Field(default="yfinance")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = AppSettings()
