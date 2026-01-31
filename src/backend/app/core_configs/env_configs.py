import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

"""
  this is for learning purposes
  it was didn't use anywhere
  only app.settings.py - AppSettings were used instead of this
"""


@dataclass(frozen=True)
class AppConfig:
    app_env: str = os.getenv("APP_ENV", "development")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"


@dataclass(frozen=True)
class ServerConfig:
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", 8000))
    reload: bool = os.getenv("RELOAD", "false").lower() == "true"


@dataclass(frozen=True)
class RedisConfig:
    host: str = os.getenv("REDIS_HOST", "localhost")
    port: int = int(os.getenv("REDIS_PORT", 6379))
    db: int = int(os.getenv("REDIS_DB", 0))
    password: str | None = os.getenv("REDIS_PASSWORD") or None


@dataclass(frozen=True)
class RateLimitConfig:
    window_seconds: int = int(
        os.getenv("RATE_LIMIT_WINDOW_SECONDS", 60),
    )
    max_requests: int = int(
        os.getenv("RATE_LIMIT_REQUESTS", 100),
    )


# ---- single exported config objects ----
app_config = AppConfig()
server_config = ServerConfig()
redis_config = RedisConfig()
rate_limit_config = RateLimitConfig()


"""
use case example
import uvicorn
from app.core.core_configs import server_config


def start() -> None:
    uvicorn.run(
        "app.main:app",
        host=server_config.host,
        port=server_config.port,
        reload=server_config.reload,
    )
"""