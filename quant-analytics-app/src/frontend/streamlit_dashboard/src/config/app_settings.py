from pydantic_settings import BaseSettings
from pydantic import Field


class AppSettings(BaseSettings):
    # ============================
    # APP
    # ============================
    APP_ENV: str = Field(default="development")
    DEBUG: bool = Field(default=False)

    # ============================
    # STREAMLIT
    # ============================
    STREAMLIT_SERVER_ADDRESS: str = Field(default="localhost")
    STREAMLIT_SERVER_PORT: int = Field(default=8501)
    STREAMLIT_BACKEND_URL: str = Field(default="http://localhost:8000")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = AppSettings()
