"""
Performance optimization utilities for the profi_test application
"""
from functools import wraps
from flask import request, current_app
from flask_caching import Cache
import hashlib
import json
import time
from collections import defaultdict, deque
from threading import Lock
from datetime import datetime
import logging

# Initialize cache - will be configured in app factory
cache = Cache()

# Performance monitoring
class PerformanceMonitor:
    """Monitor application performance and collect metrics"""
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.query_stats = defaultdict(int)
        self.lock = Lock()
        self.slow_queries = deque(maxlen=100)
        
    def record_query(self, query_name, duration):
        """Record database query performance"""
        with self.lock:
            self.query_stats[query_name] += 1
            if duration > 0.1:  # Slow query threshold (100ms)
                self.slow_queries.append({
                    'query': query_name,
                    'duration': duration,
                    'timestamp': datetime.utcnow().isoformat()
                })
    
    def record_metric(self, metric_name, value):
        """Record general performance metric"""
        with self.lock:
            self.metrics[metric_name].append({
                'value': value,
                'timestamp': time.time()
            })
            # Keep only last 1000 measurements
            if len(self.metrics[metric_name]) > 1000:
                self.metrics[metric_name] = self.metrics[metric_name][-500:]
    
    def get_stats(self):
        """Get performance statistics"""
        with self.lock:
            stats = {
                'query_counts': dict(self.query_stats),
                'slow_queries': list(self.slow_queries),
                'metrics_summary': {}
            }
            
            # Calculate summary statistics for each metric
            for metric_name, values in self.metrics.items():
                if values:
                    recent_values = [v['value'] for v in values[-100:]]  # Last 100 measurements
                    stats['metrics_summary'][metric_name] = {
                        'count': len(recent_values),
                        'avg': sum(recent_values) / len(recent_values),
                        'min': min(recent_values),
                        'max': max(recent_values),
                        'latest': recent_values[-1] if recent_values else None
                    }
            
            return stats

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

def cached_query(timeout=300, key_prefix=''):
    """
    Decorator for caching database query results
    
    Args:
        timeout: Cache timeout in seconds
        key_prefix: Prefix for cache key to avoid collisions
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Generate cache key
            cache_key = f"{key_prefix}_{f.__name__}"
            
            # Add function arguments to cache key
            if args:
                cache_key += f"_args_{hashlib.md5(str(args).encode()).hexdigest()}"
            if kwargs:
                cache_key += f"_kwargs_{hashlib.md5(str(sorted(kwargs.items())).encode()).hexdigest()}"
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                performance_monitor.record_metric('cache_hits', 1)
                return cached_result
            
            # Execute function and cache result
            start_time = time.time()
            result = f(*args, **kwargs)
            duration = time.time() - start_time
            
            # Record performance
            performance_monitor.record_metric(f'query_{f.__name__}_duration', duration)
            performance_monitor.record_query(f.__name__, duration)
            
            # Cache the result
            cache.set(cache_key, result, timeout=timeout)
            performance_monitor.record_metric('cache_misses', 1)
            
            return result
        return decorated_function
    return decorator

def batch_process(items, batch_size=50):
    """
    Process items in batches to reduce memory usage and improve performance
    
    Args:
        items: Iterable of items to process
        batch_size: Number of items per batch
    """
    items = list(items)  # Convert to list if needed
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        yield batch

def optimize_db_query(query, relationships=None, page=None, per_page=None):
    """
    Optimize database queries with eager loading and pagination
    
    Args:
        query: SQLAlchemy query object
        relationships: List of relationships to eager load
        page: Page number for pagination
        per_page: Items per page
    """
    from sqlalchemy.orm import joinedload
    
    # Apply eager loading
    if relationships:
        for rel in relationships:
            query = query.options(joinedload(rel))
    
    # Apply pagination
    if page and per_page:
        offset = (page - 1) * per_page
        query = query.offset(offset).limit(per_page)
    
    return query

def get_cache_stats():
    """Get cache statistics"""
    try:
        return {
            'cache_type': cache.config.get('CACHE_TYPE', 'unknown'),
            'default_timeout': cache.config.get('CACHE_DEFAULT_TIMEOUT', 0),
            'performance_stats': performance_monitor.get_stats()
        }
    except Exception as e:
        logging.error(f"Error getting cache stats: {e}")
        return {'error': str(e)}

# Database query optimization utilities
class QueryOptimizer:
    """Utility class for optimizing database queries"""
    
    @staticmethod
    def select_columns(query, *columns):
        """Select only specific columns to reduce data transfer"""
        return query.with_entities(*columns)
    
    @staticmethod
    def add_index_hint(query, index_name):
        """Add index hint for query optimization (database specific)"""
        # This is a simplified version - actual implementation depends on database
        return query
    
    @staticmethod
    def use_subquery(query, subquery_condition):
        """Convert to subquery for better performance in some cases"""
        return query.filter(subquery_condition)

# Memory optimization utilities
class MemoryOptimizer:
    """Utilities for memory optimization"""
    
    @staticmethod
    def chunk_large_dataset(dataset, chunk_size=1000):
        """Process large datasets in chunks"""
        for i in range(0, len(dataset), chunk_size):
            yield dataset[i:i + chunk_size]
    
    @staticmethod
    def clear_session_cache():
        """Clear SQLAlchemy session cache to free memory"""
        from app import db
        db.session.expunge_all()

# API response optimization
def optimize_api_response(data, fields=None, exclude=None):
    """
    Optimize API response by filtering fields
    
    Args:
        data: Data to optimize (dict or list of dicts)
        fields: List of fields to include
        exclude: List of fields to exclude
    """
    if isinstance(data, list):
        return [optimize_api_response(item, fields, exclude) for item in data]
    elif isinstance(data, dict):
        result = data.copy()
        
        # Filter fields
        if fields:
            result = {k: v for k, v in result.items() if k in fields}
        
        # Exclude fields
        if exclude:
            for field in exclude:
                result.pop(field, None)
        
        return result
    
    return data

# Rate limiting decorator
def rate_limit(max_requests=100, window=60):
    """
    Simple rate limiting decorator
    
    Args:
        max_requests: Maximum requests per window
        window: Time window in seconds
    """
    def decorator(f):
        requests = defaultdict(list)
        
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr or 'unknown'
            current_time = time.time()
            
            # Clean old requests
            requests[client_ip] = [
                req_time for req_time in requests[client_ip] 
                if current_time - req_time < window
            ]
            
            # Check rate limit
            if len(requests[client_ip]) >= max_requests:
                return {'error': 'Rate limit exceeded'}, 429
            
            # Record request
            requests[client_ip].append(current_time)
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator