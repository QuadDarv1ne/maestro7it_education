"""
Caching utilities and decorators.

Provides caching decorators and utilities for improving application performance
by reducing redundant database queries and computations.
"""

from __future__ import annotations

import functools
import hashlib
import json
from typing import Any, Callable, Optional, TypeVar

from flask import current_app, request
from flask_caching import Cache

logger = None

F = TypeVar('F', bound=Callable[..., Any])

# Global cache instance
_cache: Optional[Cache] = None


def init_cache(cache: Cache) -> None:
    """
    Initialize global cache instance.

    Args:
        cache: Flask-Caching instance.
    """
    global _cache
    _cache = cache


def get_cache() -> Optional[Cache]:
    """
    Get global cache instance.

    Returns:
        Flask-Caching instance or None.
    """
    return _cache


def cache_key(*args: Any, **kwargs: Any) -> str:
    """
    Generate cache key from arguments.

    Args:
        *args: Positional arguments.
        **kwargs: Keyword arguments.

    Returns:
        Generated cache key.
    """
    # Create a string representation of the arguments
    key_data = {
        'args': str(args),
        'kwargs': str(sorted(kwargs.items())),
    }
    key_str = json.dumps(key_data, sort_keys=True)
    return hashlib.md5(key_str.encode()).hexdigest()


def cached(
    timeout: int = 300,
    key_prefix: Optional[str] = None,
) -> Callable[[F], F]:
    """
    Decorator for caching function results.

    Args:
        timeout: Cache timeout in seconds.
        key_prefix: Prefix for cache key.

    Returns:
        Decorated function.
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            cache = get_cache()
            if not cache:
                return func(*args, **kwargs)

            # Generate cache key
            func_key = key_prefix or func.__name__
            args_key = cache_key(*args, **kwargs)
            full_key = f"{func_key}:{args_key}"

            # Try to get from cache
            result = cache.get(full_key)
            if result is not None:
                return result

            # Call function and cache result
            result = func(*args, **kwargs)
            cache.set(full_key, result, timeout=timeout)

            return result

        # Add method to clear cache for this function
        def clear_cache(*args: Any, **kwargs: Any) -> None:
            """Clear cache for this function."""
            cache = get_cache()
            if cache:
                func_key = key_prefix or func.__name__
                args_key = cache_key(*args, **kwargs)
                full_key = f"{func_key}:{args_key}"
                cache.delete(full_key)

        wrapper.clear_cache = clear_cache  # type: ignore

        return wrapper  # type: ignore

    return decorator


def cache_per_user(
    timeout: int = 300,
) -> Callable[[F], F]:
    """
    Cache function result per user.

    Args:
        timeout: Cache timeout in seconds.

    Returns:
        Decorated function.
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            cache = get_cache()
            if not cache:
                return func(*args, **kwargs)

            from flask_login import current_user

            user_id = current_user.id if current_user.is_authenticated else 'anonymous'
            func_key = f"{func.__name__}:user:{user_id}"
            args_key = cache_key(*args, **kwargs)
            full_key = f"{func_key}:{args_key}"

            result = cache.get(full_key)
            if result is not None:
                return result

            result = func(*args, **kwargs)
            cache.set(full_key, result, timeout=timeout)

            return result

        return wrapper  # type: ignore

    return decorator


def cache_per_request(
    timeout: int = 300,
) -> Callable[[F], F]:
    """
    Cache function result per HTTP request.

    Args:
        timeout: Cache timeout in seconds.

    Returns:
        Decorated function.
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            cache = get_cache()
            if not cache:
                return func(*args, **kwargs)

            request_id = request.environ.get('werkzeug.request').id if hasattr(request, 'environ') else 'unknown'
            func_key = f"{func.__name__}:request:{request_id}"
            args_key = cache_key(*args, **kwargs)
            full_key = f"{func_key}:{args_key}"

            result = cache.get(full_key)
            if result is not None:
                return result

            result = func(*args, **kwargs)
            cache.set(full_key, result, timeout=timeout)

            return result

        return wrapper  # type: ignore

    return decorator


def invalidate_cache(pattern: str) -> None:
    """
    Invalidate cache entries matching pattern.

    Args:
        pattern: Cache key pattern to match.
    """
    cache = get_cache()
    if cache and hasattr(cache, '_cache'):
        # Simple pattern matching for in-memory cache
        cache_dict = cache._cache
        keys_to_delete = [k for k in cache_dict.keys() if pattern in k]
        for key in keys_to_delete:
            cache.delete(key)


class CacheContext:
    """Context manager for cache operations."""

    def __init__(self, key: str, timeout: int = 300) -> None:
        """
        Initialize CacheContext.

        Args:
            key: Cache key.
            timeout: Cache timeout in seconds.
        """
        self.key = key
        self.timeout = timeout
        self.cache = get_cache()

    def __enter__(self) -> Any:
        """Enter context and return cached value if exists."""
        if self.cache:
            value = self.cache.get(self.key)
            if value is not None:
                return value
        return None

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context and cache the value."""
        if self.cache and exc_type is None:
            # Cache the value if no exception occurred
            pass

    def set_value(self, value: Any) -> None:
        """Set value in cache."""
        if self.cache:
            self.cache.set(self.key, value, timeout=self.timeout)

    def delete(self) -> None:
        """Delete value from cache."""
        if self.cache:
            self.cache.delete(self.key)
