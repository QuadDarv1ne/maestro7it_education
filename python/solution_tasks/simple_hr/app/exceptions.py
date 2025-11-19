"""
Application-wide exception classes and handlers.

This module defines custom exceptions used throughout the application
and provides centralized error handling with proper logging.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Tuple

from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)


class ApplicationError(Exception):
    """Base exception class for all application errors."""

    def __init__(
        self,
        message: str,
        code: int = 500,
        payload: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize ApplicationError.

        Args:
            message: Error message for the user.
            code: HTTP status code.
            payload: Additional error details.
        """
        super().__init__()
        self.message = message
        self.code = code
        self.payload = payload or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary."""
        result = {'error': self.message, 'code': self.code}
        result.update(self.payload)
        return result


class ValidationError(ApplicationError):
    """Raised when data validation fails."""

    def __init__(
        self,
        message: str = "Validation failed",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize ValidationError.

        Args:
            message: Error message.
            details: Validation error details.
        """
        payload = {'details': details} if details else {}
        super().__init__(message, code=400, payload=payload)


class NotFoundError(ApplicationError):
    """Raised when a requested resource is not found."""

    def __init__(self, resource: str = "Resource") -> None:
        """
        Initialize NotFoundError.

        Args:
            resource: Name of the resource that was not found.
        """
        super().__init__(f"{resource} not found", code=404)


class UnauthorizedError(ApplicationError):
    """Raised when user is not authenticated."""

    def __init__(self, message: str = "Authentication required") -> None:
        """
        Initialize UnauthorizedError.

        Args:
            message: Error message.
        """
        super().__init__(message, code=401)


class ForbiddenError(ApplicationError):
    """Raised when user doesn't have required permissions."""

    def __init__(self, message: str = "Access denied") -> None:
        """
        Initialize ForbiddenError.

        Args:
            message: Error message.
        """
        super().__init__(message, code=403)


class ConflictError(ApplicationError):
    """Raised when there's a conflict with existing data."""

    def __init__(self, message: str = "Data conflict") -> None:
        """
        Initialize ConflictError.

        Args:
            message: Error message.
        """
        super().__init__(message, code=409)


class DatabaseError(ApplicationError):
    """Raised when database operation fails."""

    def __init__(self, message: str = "Database error occurred") -> None:
        """
        Initialize DatabaseError.

        Args:
            message: Error message.
        """
        super().__init__(message, code=500)


class OperationError(ApplicationError):
    """Raised when a business operation fails."""

    def __init__(self, message: str = "Operation failed") -> None:
        """
        Initialize OperationError.

        Args:
            message: Error message.
        """
        super().__init__(message, code=400)


def init_error_handlers(app: Flask) -> None:
    """
    Register error handlers with Flask application.

    Args:
        app: Flask application instance.
    """
    @app.errorhandler(ApplicationError)
    def handle_application_error(error: ApplicationError) -> Tuple[Dict[str, Any], int]:
        """Handle custom application errors."""
        logger.warning(f"Application error: {error.message}")
        if request.accept_mimetypes.get('application/json'):
            return error.to_dict(), error.code
        else:
            return (
                render_template(
                    'error.html',
                    error=error.message,
                    code=error.code,
                ),
                error.code,
            )

    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException) -> Tuple[Any, int]:
        """Handle HTTP exceptions."""
        logger.warning(f"HTTP error {error.code}: {error.description}")
        if request.accept_mimetypes.get('application/json'):
            return (
                jsonify(
                    {
                        'error': error.description or 'An error occurred',
                        'code': error.code,
                    }
                ),
                error.code,
            )
        else:
            return (
                render_template(
                    'error.html',
                    error=error.description or 'An error occurred',
                    code=error.code,
                ),
                error.code,
            )

    @app.errorhandler(Exception)
    def handle_generic_error(error: Exception) -> Tuple[Dict[str, Any], int]:
        """Handle all unhandled exceptions."""
        logger.error(f"Unhandled exception: {str(error)}", exc_info=True)
        if request.accept_mimetypes.get('application/json'):
            return (
                {
                    'error': 'An unexpected error occurred',
                    'code': 500,
                },
                500,
            )
        else:
            return (
                render_template(
                    'error.html',
                    error='An unexpected error occurred',
                    code=500,
                ),
                500,
            )


def register_api_error_handlers(app: Flask) -> None:
    """
    Register API-specific error handlers.

    Args:
        app: Flask application instance.
    """
    @app.errorhandler(404)
    def not_found(error: HTTPException) -> Tuple[Dict[str, Any], int]:
        """Handle 404 errors."""
        if request.path.startswith('/api/'):
            logger.debug(f"API endpoint not found: {request.path}")
            return {'error': 'Not found', 'code': 404}, 404
        return (
            render_template('404.html'),
            404,
        )

    @app.errorhandler(403)
    def forbidden(error: HTTPException) -> Tuple[Dict[str, Any], int]:
        """Handle 403 errors."""
        if request.path.startswith('/api/'):
            logger.warning(f"Forbidden access to: {request.path}")
            return {'error': 'Forbidden', 'code': 403}, 403
        return (
            render_template('403.html'),
            403,
        )

    @app.errorhandler(500)
    def internal_error(error: HTTPException) -> Tuple[Dict[str, Any], int]:
        """Handle 500 errors."""
        if request.path.startswith('/api/'):
            logger.error("Internal server error in API")
            return {'error': 'Internal server error', 'code': 500}, 500
        return (
            render_template('500.html'),
            500,
        )
