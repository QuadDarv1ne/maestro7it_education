"""
Logging utilities and decorators.

Provides logging decorators and utilities for tracking function execution
and errors throughout the application.
"""

from __future__ import annotations

import functools
import logging
import time
from typing import Any, Callable, Optional, TypeVar

from flask import request

logger = logging.getLogger(__name__)

F = TypeVar('F', bound=Callable[..., Any])


def log_execution(
    log_args: bool = False,
    log_result: bool = False,
    log_errors: bool = True,
) -> Callable[[F], F]:
    """
    Decorator for logging function execution.

    Args:
        log_args: Whether to log function arguments.
        log_result: Whether to log function result.
        log_errors: Whether to log errors.

    Returns:
        Decorated function.
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            func_name = func.__name__
            start_time = time.time()

            try:
                if log_args:
                    logger.debug(
                        f"Calling {func_name} with args={args}, kwargs={kwargs}"
                    )
                else:
                    logger.debug(f"Calling {func_name}")

                result = func(*args, **kwargs)

                elapsed = time.time() - start_time

                if log_result:
                    logger.debug(
                        f"{func_name} completed in {elapsed:.3f}s with result={result}"
                    )
                else:
                    logger.debug(f"{func_name} completed in {elapsed:.3f}s")

                return result

            except Exception as e:
                elapsed = time.time() - start_time

                if log_errors:
                    logger.error(
                        f"{func_name} failed after {elapsed:.3f}s with error: {str(e)}",
                        exc_info=True,
                    )
                else:
                    logger.error(f"{func_name} failed: {str(e)}")

                raise

        return wrapper  # type: ignore

    return decorator


def log_database_operation(operation_type: str) -> Callable[[F], F]:
    """
    Decorator for logging database operations.

    Args:
        operation_type: Type of operation (e.g., 'SELECT', 'INSERT', 'UPDATE').

    Returns:
        Decorated function.
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            func_name = func.__name__
            start_time = time.time()

            try:
                logger.debug(f"Database {operation_type}: {func_name}")
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time
                logger.debug(
                    f"Database {operation_type} {func_name} completed in {elapsed:.3f}s"
                )
                return result

            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(
                    f"Database {operation_type} {func_name} failed after {elapsed:.3f}s: "
                    f"{str(e)}",
                    exc_info=True,
                )
                raise

        return wrapper  # type: ignore

    return decorator


def log_http_request() -> Callable[[F], F]:
    """
    Decorator for logging HTTP requests.

    Returns:
        Decorated function.
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            method = request.method
            path = request.path
            remote_addr = request.remote_addr

            logger.info(f"{method} {path} from {remote_addr}")

            start_time = time.time()

            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time

                logger.debug(
                    f"{method} {path} completed in {elapsed:.3f}s"
                )

                return result

            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(
                    f"{method} {path} failed after {elapsed:.3f}s: {str(e)}",
                    exc_info=True,
                )
                raise

        return wrapper  # type: ignore

    return decorator


class StructuredLogger:
    """Structured logging wrapper for consistent log format."""

    def __init__(self, name: str) -> None:
        """
        Initialize StructuredLogger.

        Args:
            name: Logger name (typically __name__).
        """
        self.logger = logging.getLogger(name)

    def info(
        self,
        message: str,
        **kwargs: Any,
    ) -> None:
        """
        Log info message with structured data.

        Args:
            message: Log message.
            **kwargs: Additional structured data.
        """
        if kwargs:
            self.logger.info(f"{message} | data={kwargs}")
        else:
            self.logger.info(message)

    def error(
        self,
        message: str,
        exception: Optional[Exception] = None,
        **kwargs: Any,
    ) -> None:
        """
        Log error message with optional exception.

        Args:
            message: Log message.
            exception: Optional exception object.
            **kwargs: Additional structured data.
        """
        if exception:
            self.logger.error(
                f"{message} | error={str(exception)} | data={kwargs}",
                exc_info=True,
            )
        else:
            self.logger.error(f"{message} | data={kwargs}")

    def warning(
        self,
        message: str,
        **kwargs: Any,
    ) -> None:
        """
        Log warning message with structured data.

        Args:
            message: Log message.
            **kwargs: Additional structured data.
        """
        if kwargs:
            self.logger.warning(f"{message} | data={kwargs}")
        else:
            self.logger.warning(message)

    def debug(
        self,
        message: str,
        **kwargs: Any,
    ) -> None:
        """
        Log debug message with structured data.

        Args:
            message: Log message.
            **kwargs: Additional structured data.
        """
        if kwargs:
            self.logger.debug(f"{message} | data={kwargs}")
        else:
            self.logger.debug(message)

    def critical(
        self,
        message: str,
        **kwargs: Any,
    ) -> None:
        """
        Log critical message with structured data.

        Args:
            message: Log message.
            **kwargs: Additional structured data.
        """
        if kwargs:
            self.logger.critical(f"{message} | data={kwargs}")
        else:
            self.logger.critical(message)
