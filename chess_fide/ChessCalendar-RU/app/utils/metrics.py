"""
Prometheus metrics for application monitoring
"""
from prometheus_client import Counter, Histogram, Gauge, Info, generate_latest, CONTENT_TYPE_LATEST
from functools import wraps
import time
from flask import request, g


# HTTP Metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    buckets=(0.01, 0.05, 0.1, 0.5, 1.0, 2.5, 5.0, 10.0)
)

http_requests_in_progress = Gauge(
    'http_requests_in_progress',
    'HTTP requests currently in progress',
    ['method', 'endpoint']
)

# Cache Metrics
cache_requests_total = Counter(
    'cache_requests_total',
    'Total cache requests',
    ['cache_level', 'operation']
)

cache_hits_total = Counter(
    'cache_hits_total',
    'Total cache hits',
    ['cache_level']
)

cache_misses_total = Counter(
    'cache_misses_total',
    'Total cache misses',
    ['cache_level']
)

cache_size_bytes = Gauge(
    'cache_size_bytes',
    'Current cache size in bytes',
    ['cache_level']
)

# Database Metrics
db_queries_total = Counter(
    'db_queries_total',
    'Total database queries',
    ['operation', 'table']
)

db_query_duration_seconds = Histogram(
    'db_query_duration_seconds',
    'Database query duration in seconds',
    ['operation', 'table'],
    buckets=(0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0)
)

db_connections_active = Gauge(
    'db_connections_active',
    'Active database connections'
)

# Celery Metrics
celery_tasks_total = Counter(
    'celery_tasks_total',
    'Total Celery tasks',
    ['task_name', 'status']
)

celery_task_duration_seconds = Histogram(
    'celery_task_duration_seconds',
    'Celery task duration in seconds',
    ['task_name'],
    buckets=(1.0, 5.0, 10.0, 30.0, 60.0, 300.0, 600.0)
)

celery_active_tasks = Gauge(
    'celery_active_tasks',
    'Currently active Celery tasks',
    ['task_name']
)

celery_queue_length = Gauge(
    'celery_queue_length',
    'Length of Celery queue',
    ['queue_name']
)

# Application Metrics
app_info = Info(
    'app_info',
    'Application information'
)

active_users = Gauge(
    'active_users',
    'Number of active users'
)

tournaments_total = Gauge(
    'tournaments_total',
    'Total number of tournaments',
    ['status']
)

# Business Metrics
tournament_views_total = Counter(
    'tournament_views_total',
    'Total tournament views',
    ['tournament_id']
)

user_registrations_total = Counter(
    'user_registrations_total',
    'Total user registrations'
)

api_errors_total = Counter(
    'api_errors_total',
    'Total API errors',
    ['endpoint', 'error_type']
)


class MetricsMiddleware:
    """Middleware for collecting HTTP metrics"""
    
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with Flask app"""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
    
    def before_request(self):
        """Record request start time"""
        g._start_time = time.time()
        
        # Increment in-progress counter
        endpoint = request.endpoint or 'unknown'
        http_requests_in_progress.labels(
            method=request.method,
            endpoint=endpoint
        ).inc()
    
    def after_request(self, response):
        """Record request metrics"""
        if not hasattr(g, '_start_time'):
            return response
        
        # Calculate duration
        duration = time.time() - g._start_time
        
        # Get endpoint
        endpoint = request.endpoint or 'unknown'
        
        # Record metrics
        http_requests_total.labels(
            method=request.method,
            endpoint=endpoint,
            status=response.status_code
        ).inc()
        
        http_request_duration_seconds.labels(
            method=request.method,
            endpoint=endpoint
        ).observe(duration)
        
        http_requests_in_progress.labels(
            method=request.method,
            endpoint=endpoint
        ).dec()
        
        return response


def track_cache_operation(cache_level: str, operation: str):
    """Decorator to track cache operations"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_requests_total.labels(
                cache_level=cache_level,
                operation=operation
            ).inc()
            
            result = func(*args, **kwargs)
            
            # Track hits/misses for get operations
            if operation == 'get':
                if result is not None:
                    cache_hits_total.labels(cache_level=cache_level).inc()
                else:
                    cache_misses_total.labels(cache_level=cache_level).inc()
            
            return result
        return wrapper
    return decorator


def track_db_query(operation: str, table: str):
    """Decorator to track database queries"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                db_queries_total.labels(
                    operation=operation,
                    table=table
                ).inc()
                
                db_query_duration_seconds.labels(
                    operation=operation,
                    table=table
                ).observe(duration)
                
                return result
            except Exception as e:
                duration = time.time() - start_time
                db_query_duration_seconds.labels(
                    operation=operation,
                    table=table
                ).observe(duration)
                raise
        return wrapper
    return decorator


def track_celery_task(task_name: str):
    """Decorator to track Celery tasks"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Increment active tasks
            celery_active_tasks.labels(task_name=task_name).inc()
            
            start_time = time.time()
            status = 'success'
            
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                status = 'failure'
                raise
            finally:
                duration = time.time() - start_time
                
                # Record metrics
                celery_tasks_total.labels(
                    task_name=task_name,
                    status=status
                ).inc()
                
                celery_task_duration_seconds.labels(
                    task_name=task_name
                ).observe(duration)
                
                # Decrement active tasks
                celery_active_tasks.labels(task_name=task_name).dec()
        
        return wrapper
    return decorator


def update_business_metrics():
    """Update business metrics (call periodically)"""
    try:
        from app.models.tournament import Tournament
        from app.models.user import User
        from app import db
        
        # Update tournament counts by status
        for status in ['Scheduled', 'Ongoing', 'Completed', 'Cancelled']:
            count = Tournament.query.filter_by(status=status).count()
            tournaments_total.labels(status=status).set(count)
        
        # Update active users (logged in last 24 hours)
        # This is a placeholder - implement based on your user tracking
        active_count = User.query.filter_by(is_active=True).count()
        active_users.set(active_count)
        
    except Exception as e:
        from app.utils.logger import get_logger
        logger = get_logger('metrics')
        logger.error(f"Error updating business metrics: {e}")


def metrics_endpoint():
    """Endpoint to expose Prometheus metrics"""
    # Update business metrics before exposing
    update_business_metrics()
    
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


# Initialize app info
app_info.info({
    'version': '2.1',
    'name': 'Chess Calendar RU',
    'environment': 'production'
})
