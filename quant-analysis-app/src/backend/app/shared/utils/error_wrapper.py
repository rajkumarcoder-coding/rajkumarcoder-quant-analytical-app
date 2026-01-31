import logging
from functools import wraps
from typing import Callable, Type

from app.core_configs.exceptions import AppException

logger = logging.getLogger("app.errors")


def safe_execute(
        *,
        exception_cls: Type[AppException] = AppException,
        message: str = "Application error",
        reason: str | None = None,
):
    """
    Decorator to safely execute business logic and convert unexpected
    exceptions into controlled AppException errors.
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            # Already a controlled application error → rethrow
            except AppException:
                raise

            # Unexpected error → log + wrap
            except Exception as e:
                logger.exception(
                    "Unhandled exception in %s",
                    func.__name__,
                    exc_info=e,
                )

                raise exception_cls(
                    message=message,
                    reason=reason or exception_cls.error_type,
                    context={
                        "function": func.__name__,
                        "args": str(args),
                        "kwargs": str(kwargs),
                    },
                ) from e

        return wrapper

    return decorator
