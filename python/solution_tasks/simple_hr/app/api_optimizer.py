"""
API route optimization with query optimization and caching.

Optimizes endpoints for performance with lazy loading and caching.
"""

from __future__ import annotations

from functools import wraps
from typing import Any, Callable, Optional

from app.cache_utils import cached
from app.query_optimization import OptimizedQuery


def optimized_endpoint(
    cache_time: int = 300,
    use_query_optimization: bool = True,
) -> Callable:
    """
    Decorator for optimized API endpoints.

    Applies caching and query optimization automatically.

    Args:
        cache_time: Cache duration in seconds.
        use_query_optimization: Enable query optimization.

    Returns:
        Decorator function.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Generate cache key from function and parameters
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"

            # Try cache first
            result = None
            if cache_time > 0:
                from app import cache

                if cache is not None:
                    try:
                        result = cache.get(cache_key)
                        if result is not None:
                            return result
                    except Exception:
                        pass

            # Execute function
            result = func(*args, **kwargs)

            # Cache result
            if cache_time > 0:
                from app import cache

                if cache is not None:
                    try:
                        cache.set(cache_key, result, timeout=cache_time)
                    except Exception:
                        pass

            return result

        wrapper.__wrapped__ = func
        return wrapper

    return decorator


class APIOptimizer:
    """Centralizes API optimization strategies."""

    def __init__(self) -> None:
        """Initialize API optimizer."""
        self.query_cache: dict = {}
        self.endpoint_stats: dict = {}

    def optimize_list_endpoint(
        self,
        query,
        page: int = 1,
        limit: int = 20,
        sort_by: Optional[str] = None,
        eager_load: Optional[list] = None,
    ) -> dict:
        """
        Optimize list endpoint query.

        Args:
            query: Base SQLAlchemy query.
            page: Page number.
            limit: Items per page.
            sort_by: Sort column.
            eager_load: Relations to eager load.

        Returns:
            Paginated results with metadata.
        """
        # Apply eager loading
        if eager_load:
            for relation in eager_load:
                query = query.options(
                    __import__('sqlalchemy.orm', fromlist=['joinedload']).joinedload(
                        relation
                    )
                )

        # Apply sorting
        if sort_by:
            direction = 'asc'
            if sort_by.startswith('-'):
                sort_by = sort_by[1:]
                direction = 'desc'

            if hasattr(query.column_descriptions[0]['entity'], sort_by):
                order_column = getattr(query.column_descriptions[0]['entity'], sort_by)
                if direction == 'desc':
                    query = query.order_by(order_column.desc())
                else:
                    query = query.order_by(order_column)

        # Count total before pagination
        total = query.count()

        # Apply pagination
        offset = (page - 1) * limit
        items = query.offset(offset).limit(limit).all()

        return {
            'items': items,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total,
                'pages': (total + limit - 1) // limit,
            },
        }

    def optimize_filter_endpoint(
        self,
        query,
        filters: dict,
        model,
        eager_load: Optional[list] = None,
    ) -> list:
        """
        Apply optimized filtering to query.

        Args:
            query: Base SQLAlchemy query.
            filters: Filter conditions.
            model: SQLAlchemy model class.
            eager_load: Relations to eager load.

        Returns:
            Filtered results.
        """
        # Apply eager loading first
        if eager_load:
            for relation in eager_load:
                try:
                    query = query.options(
                        __import__('sqlalchemy.orm', fromlist=['joinedload']).joinedload(
                            relation
                        )
                    )
                except Exception:
                    pass

        # Apply filters
        for field, value in filters.items():
            if hasattr(model, field):
                column = getattr(model, field)

                # Handle different value types
                if isinstance(value, list):
                    query = query.filter(column.in_(value))
                elif isinstance(value, dict):
                    if 'gte' in value:
                        query = query.filter(column >= value['gte'])
                    if 'lte' in value:
                        query = query.filter(column <= value['lte'])
                    if 'gt' in value:
                        query = query.filter(column > value['gt'])
                    if 'lt' in value:
                        query = query.filter(column < value['lt'])
                    if 'like' in value:
                        query = query.filter(column.like(f"%{value['like']}%"))
                else:
                    query = query.filter(column == value)

        return query.all()

    def record_endpoint_stat(
        self,
        endpoint: str,
        response_time: float,
        query_count: int,
        status_code: int,
    ) -> None:
        """
        Record endpoint statistics for analysis.

        Args:
            endpoint: Endpoint path.
            response_time: Response time in seconds.
            query_count: Number of database queries.
            status_code: HTTP status code.
        """
        if endpoint not in self.endpoint_stats:
            self.endpoint_stats[endpoint] = {
                'calls': 0,
                'total_time': 0,
                'avg_time': 0,
                'total_queries': 0,
                'avg_queries': 0,
                'status_codes': {},
            }

        stats = self.endpoint_stats[endpoint]
        stats['calls'] += 1
        stats['total_time'] += response_time
        stats['avg_time'] = stats['total_time'] / stats['calls']
        stats['total_queries'] += query_count
        stats['avg_queries'] = stats['total_queries'] / stats['calls']
        stats['status_codes'][status_code] = stats['status_codes'].get(status_code, 0) + 1

    def get_endpoint_stats(self, endpoint: Optional[str] = None) -> dict:
        """
        Get endpoint statistics.

        Args:
            endpoint: Specific endpoint or None for all.

        Returns:
            Statistics dictionary.
        """
        if endpoint:
            return self.endpoint_stats.get(endpoint, {})
        return self.endpoint_stats

    def get_slow_endpoints(self, threshold: float = 1.0) -> list:
        """
        Get endpoints slower than threshold.

        Args:
            threshold: Time threshold in seconds.

        Returns:
            List of slow endpoints.
        """
        slow = []
        for endpoint, stats in self.endpoint_stats.items():
            if stats.get('avg_time', 0) > threshold:
                slow.append(
                    {
                        'endpoint': endpoint,
                        'avg_time': stats['avg_time'],
                        'avg_queries': stats['avg_queries'],
                    }
                )
        return sorted(slow, key=lambda x: x['avg_time'], reverse=True)

    def get_high_query_endpoints(self, threshold: int = 10) -> list:
        """
        Get endpoints with high query counts.

        Args:
            threshold: Query count threshold.

        Returns:
            List of endpoints with high query counts.
        """
        high_query = []
        for endpoint, stats in self.endpoint_stats.items():
            if stats.get('avg_queries', 0) > threshold:
                high_query.append(
                    {
                        'endpoint': endpoint,
                        'avg_queries': stats['avg_queries'],
                        'avg_time': stats['avg_time'],
                    }
                )
        return sorted(high_query, key=lambda x: x['avg_queries'], reverse=True)


# Global optimizer instance
_optimizer: Optional[APIOptimizer] = None


def get_api_optimizer() -> APIOptimizer:
    """Get global API optimizer instance."""
    global _optimizer
    if _optimizer is None:
        _optimizer = APIOptimizer()
    return _optimizer


def init_api_optimizer() -> APIOptimizer:
    """Initialize API optimizer."""
    global _optimizer
    _optimizer = APIOptimizer()
    return _optimizer
