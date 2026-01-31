from fastapi import Header, HTTPException, status
from app.core_configs.app_settings import settings

JWT_SECRET_KEY = "CHANGE_ME_IN_PROD"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5
REFRESH_TOKEN_EXPIRE_DAYS = 7

API_KEY = settings.API_KEY


def verify_api_key(x_api_key: str = Header(None)):
    if not API_KEY or x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )
