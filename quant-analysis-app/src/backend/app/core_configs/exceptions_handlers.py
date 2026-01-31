from fastapi import Request
from fastapi.responses import JSONResponse
from app.core_configs.exceptions import AppException
import logging

logger = logging.getLogger("app.errors")


async def app_exception_handler(request: Request, exc: AppException):
    """
    {
    "detail": {
        "message": "Invalid symbols provided",
        "reason": "unsupported_demo_symbol",
        "context": {
        "invalid_symbols": ["XYZ"]
        },
        "allowed_symbols": ["AAPL", "MSFT"]
        }
    }
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception", exc_info=exc)

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
