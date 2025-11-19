"""
API Gateway with advanced rate limiting and request management.

Provides centralized handling of API requests with rate limiting,
request validation, and metrics collection.
"""

from __future__ import annotations

import logging
import time
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, Optional, TypeVar

from flask import Flask, Request, Response, jsonify, request
from functools import wraps

logger = logging.getLogger(__name__)

F = TypeVar('F', bound=Callable[..., Any])


class RateLimiter:
    """Advanced rate limiting with multiple strategies."""

    def __init__(self) -> None:
        """Initialize rate limiter."""
        self.ip_limits: Dict[str, list] = {}
        self.user_limits: Dict[int, list] = {}
        self.endpoint_limits: Dict[str, list] = {}

    def _cleanup_old_entries(self, entries: list, window_seconds: int) -> None:
        """Remove old entries outside time window."""
        cutoff = time.time() - window_seconds
        while entries and entries[0] < cutoff:
            entries.pop(0)

    def check_ip_limit(
        self,
        ip: str,
        limit: int = 100,
        window_seconds: int = 60,
    ) -> tuple[bool, Dict[str, Any]]:
        """
        Check IP-based rate limit.

        Args:
            ip: IP address to check.
            limit: Maximum requests per window.
            window_seconds: Time window in seconds.

        Returns:
            Tuple of (is_allowed, info_dict).
        """
        if ip not in self.ip_limits:
            self.ip_limits[ip] = []

        self._cleanup_old_entries(self.ip_limits[ip], window_seconds)

        remaining = limit - len(self.ip_limits[ip])
        reset_time = int(time.time()) + window_seconds

        if remaining > 0:
            self.ip_limits[ip].append(time.time())
            return True, {
                'remaining': remaining,
                'limit': limit,
                'reset': reset_time,
            }
        else:
            return False, {
                'remaining': 0,
                'limit': limit,
                'reset': reset_time,
            }

    def check_user_limit(
        self,
        user_id: int,
        limit: int = 500,
        window_seconds: int = 3600,
    ) -> tuple[bool, Dict[str, Any]]:
        """
        Check user-based rate limit.

        Args:
            user_id: User ID to check.
            limit: Maximum requests per window.
            window_seconds: Time window in seconds.

        Returns:
            Tuple of (is_allowed, info_dict).
        """
        if user_id not in self.user_limits:
            self.user_limits[user_id] = []

        self._cleanup_old_entries(self.user_limits[user_id], window_seconds)

        remaining = limit - len(self.user_limits[user_id])
        reset_time = int(time.time()) + window_seconds

        if remaining > 0:
            self.user_limits[user_id].append(time.time())
            return True, {
                'remaining': remaining,
                'limit': limit,
                'reset': reset_time,
            }
        else:
            return False, {
                'remaining': 0,
                'limit': limit,
                'reset': reset_time,
            }

    def check_endpoint_limit(
        self,
        endpoint: str,
        limit: int = 1000,
        window_seconds: int = 3600,
    ) -> tuple[bool, Dict[str, Any]]:
        """
        Check endpoint-based rate limit.

        Args:
            endpoint: Endpoint name to check.
            limit: Maximum requests per window.
            window_seconds: Time window in seconds.

        Returns:
            Tuple of (is_allowed, info_dict).
        """
        if endpoint not in self.endpoint_limits:
            self.endpoint_limits[endpoint] = []

        self._cleanup_old_entries(self.endpoint_limits[endpoint], window_seconds)

        remaining = limit - len(self.endpoint_limits[endpoint])
        reset_time = int(time.time()) + window_seconds

        if remaining > 0:
            self.endpoint_limits[endpoint].append(time.time())
            return True, {
                'remaining': remaining,
                'limit': limit,
                'reset': reset_time,
            }
        else:
            return False, {
                'remaining': 0,
                'limit': limit,
                'reset': reset_time,
            }

    def get_stats(self) -> Dict[str, Any]:
        """Get rate limiter statistics."""
        return {
            'ips_tracked': len(self.ip_limits),
            'users_tracked': len(self.user_limits),
            'endpoints_tracked': len(self.endpoint_limits),
            'total_ips': sum(len(v) for v in self.ip_limits.values()),
            'total_users': sum(len(v) for v in self.user_limits.values()),
            'total_endpoints': sum(len(v) for v in self.endpoint_limits.values()),
        }


class APIGateway:
    """Central API Gateway for request handling and metrics."""

    def __init__(self, app: Optional[Flask] = None) -> None:
        """
        Initialize API Gateway.

        Args:
            app: Flask application instance.
        """
        self.rate_limiter = RateLimiter()
        self.request_metrics: Dict[str, Any] = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_time': 0,
        }
        self.endpoint_metrics: Dict[str, Dict[str, Any]] = {}

        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """
        Initialize with Flask app.

        Args:
            app: Flask application instance.
        """
        @app.before_request
        def before_request_handler() -> Optional[Response]:
            return self._handle_before_request()

        @app.after_request
        def after_request_handler(response: Response) -> Response:
            return self._handle_after_request(response)

    def _handle_before_request(self) -> Optional[Response]:
        """Handle pre-request checks."""
        request.start_time = time.time()

        # IP-based rate limiting
        client_ip = request.remote_addr
        if request.path.startswith('/api/'):
            is_allowed, info = self.rate_limiter.check_ip_limit(
                client_ip,
                limit=100,
                window_seconds=60,
            )

            if not is_allowed:
                logger.warning(f"Rate limit exceeded for IP: {client_ip}")
                return jsonify({'error': 'Rate limit exceeded'}), 429

            # Add rate limit headers
            response = jsonify({'message': 'ok'})
            response.headers['X-RateLimit-Limit'] = str(info['limit'])
            response.headers['X-RateLimit-Remaining'] = str(info['remaining'])
            response.headers['X-RateLimit-Reset'] = str(info['reset'])

        return None

    def _handle_after_request(self, response: Response) -> Response:
        """Handle post-request metrics."""
        if not hasattr(request, 'start_time'):
            return response

        elapsed_time = time.time() - request.start_time

        # Update global metrics
        self.request_metrics['total_requests'] += 1
        self.request_metrics['total_time'] += elapsed_time

        if response.status_code < 400:
            self.request_metrics['successful_requests'] += 1
        else:
            self.request_metrics['failed_requests'] += 1

        # Update endpoint metrics
        endpoint = request.endpoint or 'unknown'
        if endpoint not in self.endpoint_metrics:
            self.endpoint_metrics[endpoint] = {
                'count': 0,
                'total_time': 0,
                'min_time': float('inf'),
                'max_time': 0,
                'errors': 0,
            }

        metrics = self.endpoint_metrics[endpoint]
        metrics['count'] += 1
        metrics['total_time'] += elapsed_time
        metrics['min_time'] = min(metrics['min_time'], elapsed_time)
        metrics['max_time'] = max(metrics['max_time'], elapsed_time)

        if response.status_code >= 400:
            metrics['errors'] += 1

        # Add timing header
        response.headers['X-Response-Time'] = f"{elapsed_time:.4f}s"

        return response

    def get_metrics(self) -> Dict[str, Any]:
        """Get aggregated metrics."""
        total = self.request_metrics['total_requests']
        avg_time = (
            self.request_metrics['total_time'] / total
            if total > 0
            else 0
        )

        return {
            'total_requests': total,
            'successful_requests': self.request_metrics['successful_requests'],
            'failed_requests': self.request_metrics['failed_requests'],
            'average_response_time': avg_time,
            'rate_limiter': self.rate_limiter.get_stats(),
            'endpoints': self.endpoint_metrics,
        }

    def reset_metrics(self) -> None:
        """Reset all metrics."""
        self.request_metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_time': 0,
        }
        self.endpoint_metrics = {}


def rate_limit(
    limit: int = 100,
    window: int = 60,
    by: str = 'ip',
) -> Callable[[F], F]:
    """
    Decorator for endpoint-level rate limiting.

    Args:
        limit: Maximum requests per window.
        window: Time window in seconds.
        by: Rate limit by 'ip', 'user', or 'endpoint'.

    Returns:
        Decorated function.
    """
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Implementation would use the gateway instance
            # This is a placeholder for actual implementation
            return func(*args, **kwargs)

        return wrapper  # type: ignore

    return decorator


def track_metrics(func: F) -> F:
    """
    Decorator for automatic metrics tracking.

    Args:
        func: Function to track.

    Returns:
        Decorated function.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()

        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            logger.debug(
                f"{func.__name__} completed in {elapsed:.4f}s"
            )
            return result
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(
                f"{func.__name__} failed after {elapsed:.4f}s: {str(e)}",
                exc_info=True,
            )
            raise

    return wrapper  # type: ignore
