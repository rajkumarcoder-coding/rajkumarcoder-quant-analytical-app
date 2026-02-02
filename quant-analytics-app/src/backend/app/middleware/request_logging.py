import time
import logging
from fastapi import Request

logger = logging.getLogger("app.requests")


async def request_logging_middleware(request: Request, call_next):
    start_time = time.time()
    client_ip = request.client.host if request.client else "unknown"

    status_code: int | None = None

    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception:
        status_code = 500
        raise
    finally:
        duration = round((time.time() - start_time) * 1000, 2)

        logger.info(
            "request",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": status_code,
                "duration_ms": duration,
                "client_ip": client_ip,
            },
        )

    return response
