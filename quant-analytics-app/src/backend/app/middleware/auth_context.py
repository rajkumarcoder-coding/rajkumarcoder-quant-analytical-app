from fastapi import Request
from jose import JWTError
from app.api_dependencies.jwt_auth.jwt_refresh_token import decode_token


async def auth_context_middleware(request: Request, call_next):
    request.state.user = None

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = decode_token(token)
            if payload.get("type") == "access":
                request.state.user = payload.get("sub")
        except JWTError:
            pass  # invalid token → treated as anonymous

    return await call_next(request)
