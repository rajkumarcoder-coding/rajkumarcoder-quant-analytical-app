from fastapi import FastAPI, Request
# from app.core_configs.security import verify_api_key
import logging
from app.core_configs.looging import setup_logging
from app.core_configs.response_validation_exception_handler import register_exception_handlers
from app.providers.redis_database.redis_lifespan import redis_lifespan
from app.core_configs.exceptions import AppException
from app.core_configs.exceptions_handlers import (
    app_exception_handler,
    generic_exception_handler
)
from app.middleware.global_rate_limiting import global_rate_limit_middleware
from app.middleware.request_logging import request_logging_middleware
from app.api.v1.routers import router as v1_router

setup_logging(level="INFO")
logger = logging.getLogger(__name__)
app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    title="Fastapi stockquant backend platform",
    description="Fastapi stockquant backend platform",
    version="0.0.1",
    lifespan=redis_lifespan,
    # dependencies=[Depends(verify_api_key)],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("REQUEST %s %s", request.method, request.url.path)
    response = await call_next(request)
    return response


# register once
register_exception_handlers(app)

logger.info("Service started")

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.middleware("http")(request_logging_middleware)
app.middleware("http")(global_rate_limit_middleware)


@app.get("/")
def root():
    return {"message": "Quant API Platform Running"}


@app.get("/health")
def root():
    return {"message": "health check"}


app.include_router(v1_router, prefix="/api/v1")
