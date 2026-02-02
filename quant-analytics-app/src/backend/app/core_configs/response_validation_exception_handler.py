from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import ResponseValidationError
import logging

logger = logging.getLogger(__name__)


def register_exception_handlers(app):
    @app.exception_handler(ResponseValidationError)
    async def response_validation_exception_handler(
            request: Request,
            exc: ResponseValidationError,
    ):
        logger.warning(
            "Response validation failed",
            extra={
                "path": request.url.path,
                "method": request.method,
                "errors": exc.errors(),
            },
        )

        return JSONResponse(
            status_code=500,
            content={"detail": "Internal response validation error"},
        )
