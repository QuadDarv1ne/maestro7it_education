"""
Enhanced structured logging system with rotation and advanced features
"""
import logging
import logging.handlers
import json
import os
import sys
from datetime import datetime
from functools import wraps
from collections import defaultdict
from threading import Lock
import traceback
from flask import request, g, has_request_context
import uuid

class StructuredLogger:
    """Advanced structured logging system"""
    
    def __init__(self, app=None):
        self.app = app
        self.loggers = {}
        self.metrics = defaultdict(list)
        self.lock = Lock()
        self.request_stats = defaultdict(int)
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize logging with Flask app"""
        self.app = app
        
        # Create logs directory
        log_dir = os.path.join(app.root_path, '..', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        # Configure root logger
        self._setup_root_logger(log_dir)
        
        # Configure specific loggers
        self._setup_application_loggers()
        
        # Add request tracking
        self._setup_request_tracking(app)
        
        # Add exception handling
        self._setup_exception_handling(app)
        
        logging.info("Enhanced logging system initialized")
    
    def _setup_root_logger(self, log_dir):
        """Setup root logger with handlers"""
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        root_logger.handlers.clear()
        
        # JSON formatter for structured logging
        json_formatter = StructuredFormatter()
        
        # Simple formatter for console
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # File handler for all logs (JSON format)
        all_logs_handler = logging.handlers.RotatingFileHandler(
            os.path.join(log_dir, 'application.json.log'),
            maxBytes=50*1024*1024,  # 50MB
            backupCount=10
        )
        all_logs_handler.setFormatter(json_formatter)
        all_logs_handler.setLevel(logging.INFO)
        
        # Error file handler (JSON format)
        error_handler = logging.handlers.RotatingFileHandler(
            os.path.join(log_dir, 'error.json.log'),
            maxBytes=20*1024*1024,  # 20MB
            backupCount=5
        )
        error_handler.setFormatter(json_formatter)
        error_handler.setLevel(logging.ERROR)
        
        # Console handler for development
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(simple_formatter)
        console_handler.setLevel(logging.DEBUG if self.app.debug else logging.INFO)
        
        # Add handlers
        root_logger.addHandler(all_logs_handler)
        root_logger.addHandler(error_handler)
        root_logger.addHandler(console_handler)
    
    def _setup_application_loggers(self):
        """Setup specific application loggers"""
        # Suppress noisy loggers
        logging.getLogger('werkzeug').setLevel(logging.WARNING)
        logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
        logging.getLogger('sqlalchemy.dialects').setLevel(logging.WARNING)
        
        # Create specialized loggers
        self.loggers['security'] = logging.getLogger('app.security')
        self.loggers['performance'] = logging.getLogger('app.performance')
        self.loggers['database'] = logging.getLogger('app.database')
        self.loggers['audit'] = logging.getLogger('app.audit')
        
        # Set levels for specialized loggers
        for logger in self.loggers.values():
            logger.setLevel(logging.INFO)
    
    def _setup_request_tracking(self, app):
        """Setup request tracking and timing"""
        @app.before_request
        def before_request():
            g.request_start_time = datetime.utcnow()
            g.request_id = str(uuid.uuid4())
            if has_request_context():
                self.request_stats['total_requests'] += 1
        
        @app.after_request
        def after_request(response):
            if hasattr(g, 'request_start_time'):
                duration = (datetime.utcnow() - g.request_start_time).total_seconds()
                
                # Log request completion
                self.log_request_completion(
                    request.endpoint or 'unknown',
                    response.status_code,
                    duration
                )
                
                # Track slow requests
                if duration > 1.0:  # 1 second threshold
                    self.request_stats['slow_requests'] += 1
                    logging.warning(f"Slow request: {request.endpoint} took {duration:.3f}s")
                
                # Add timing header
                response.headers['X-Response-Time'] = f"{duration:.3f}s"
                response.headers['X-Request-ID'] = g.request_id
            
            return response
    
    def _setup_exception_handling(self, app):
        """Setup global exception handling"""
        @app.errorhandler(Exception)
        def handle_exception(e):
            # Log the exception with full context
            self.log_exception(e)
            
            # Increment error counter
            self.request_stats['errors'] += 1
            
            # Return generic error response
            return {"error": "Internal server error"}, 500
        
        @app.errorhandler(404)
        def handle_not_found(e):
            self.log_security_event('not_found', details={'url': request.url})
            return {"error": "Resource not found"}, 404
        
        @app.errorhandler(403)
        def handle_forbidden(e):
            self.log_security_event('forbidden_access', details={'url': request.url})
            return {"error": "Access forbidden"}, 403
    
    def log_request_completion(self, endpoint, status_code, duration):
        """Log request completion with performance metrics"""
        self.loggers['performance'].info(
            "Request completed",
            extra={
                'event_type': 'request_completion',
                'endpoint': endpoint,
                'status_code': status_code,
                'duration': duration,
                'method': request.method if has_request_context() else 'unknown',
                'user_agent': request.headers.get('User-Agent', 'unknown') if has_request_context() else 'unknown'
            }
        )
    
    def log_exception(self, exception):
        """Log exception with full context"""
        # Get exception details
        exc_type, exc_value, exc_traceback = sys.exc_info()
        
        # Format traceback
        tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        traceback_str = ''.join(tb_lines)
        
        # Log with structured data
        logging.error(
            f"Unhandled exception: {str(exception)}",
            extra={
                'event_type': 'exception',
                'exception_type': exc_type.__name__ if exc_type else 'unknown',
                'exception_message': str(exc_value),
                'traceback': traceback_str,
                'request_id': getattr(g, 'request_id', 'unknown'),
                'endpoint': request.endpoint if has_request_context() else 'unknown'
            },
            exc_info=True
        )
    
    def log_security_event(self, event_type, user_id=None, details=None):
        """Log security-related events"""
        self.loggers['security'].warning(
            f"Security event: {event_type}",
            extra={
                'event_type': 'security',
                'security_event': event_type,
                'user_id': user_id or 'anonymous',
                'details': details or {},
                'ip_address': request.remote_addr if has_request_context() else 'unknown',
                'user_agent': request.headers.get('User-Agent', 'unknown') if has_request_context() else 'unknown'
            }
        )
    
    def log_user_action(self, user_id, action, details=None):
        """Log user-specific actions for audit trail"""
        self.loggers['audit'].info(
            f"User action: {action}",
            extra={
                'event_type': 'user_action',
                'user_id': user_id,
                'action': action,
                'details': details or {},
                'request_id': getattr(g, 'request_id', 'unknown')
            }
        )
    
    def log_performance_metric(self, metric_name, value, tags=None):
        """Log performance metrics"""
        with self.lock:
            self.metrics[metric_name].append({
                'value': value,
                'timestamp': datetime.utcnow().isoformat(),
                'tags': tags or {}
            })
            
            # Keep only last 1000 measurements per metric
            if len(self.metrics[metric_name]) > 1000:
                self.metrics[metric_name] = self.metrics[metric_name][-500:]
        
        self.loggers['performance'].info(
            f"Performance metric: {metric_name}",
            extra={
                'event_type': 'performance_metric',
                'metric_name': metric_name,
                'value': value,
                'tags': tags or {}
            }
        )
    
    def log_database_query(self, query_name, duration, rows_affected=None):
        """Log database query performance"""
        self.loggers['database'].info(
            f"Database query: {query_name}",
            extra={
                'event_type': 'database_query',
                'query_name': query_name,
                'duration': duration,
                'rows_affected': rows_affected,
                'is_slow': duration > 0.5  # 500ms threshold
            }
        )
        
        # Track slow queries
        if duration > 0.5:
            self.request_stats['slow_queries'] += 1
    
    def get_log_statistics(self):
        """Get logging and request statistics"""
        with self.lock:
            stats = dict(self.request_stats)
            
            # Add metric summaries
            metric_summaries = {}
            for metric_name, values in self.metrics.items():
                if values:
                    recent_values = [v['value'] for v in values[-100:]]
                    metric_summaries[metric_name] = {
                        'count': len(recent_values),
                        'avg': sum(recent_values) / len(recent_values),
                        'min': min(recent_values),
                        'max': max(recent_values),
                        'latest': recent_values[-1] if recent_values else None
                    }
            
            stats['metrics'] = metric_summaries
            return stats
    
    def reset_statistics(self):
        """Reset all statistics"""
        with self.lock:
            self.request_stats.clear()
            self.metrics.clear()

class StructuredFormatter(logging.Formatter):
    """Formatter for structured JSON logging"""
    
    def format(self, record):
        # Create base log entry
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage()
        }
        
        # Add request context if available
        if has_request_context():
            try:
                log_entry.update({
                    'request_id': getattr(g, 'request_id', 'unknown'),
                    'endpoint': request.endpoint or 'unknown',
                    'method': request.method,
                    'url': request.url,
                    'remote_addr': request.remote_addr,
                    'user_agent': request.headers.get('User-Agent', 'unknown')
                })
            except:
                # Fallback if any attributes are missing
                log_entry.update({
                    'request_id': 'unknown',
                    'endpoint': 'unknown',
                    'method': 'unknown',
                    'url': 'unknown',
                    'remote_addr': 'unknown',
                    'user_agent': 'unknown'
                })
        else:
            log_entry.update({
                'request_id': 'unknown',
                'endpoint': 'unknown',
                'method': 'unknown',
                'url': 'unknown',
                'remote_addr': 'unknown',
                'user_agent': 'unknown'
            })
        
        # Add structured data from extra
        if hasattr(record, 'extra') and isinstance(record.extra, dict):
            log_entry.update(record.extra)
        
        # Add exception info if present
        if record.exc_info:
            exc_type, exc_value, exc_traceback = record.exc_info
            log_entry['exception'] = {
                'type': exc_type.__name__ if exc_type else 'unknown',
                'message': str(exc_value),
                'traceback': ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            }
        
        return json.dumps(log_entry, ensure_ascii=False)

# Global structured logger instance
structured_logger = StructuredLogger()

# Convenience decorator for logging function execution
def log_execution_time(logger_name='performance'):
    """Decorator to log function execution time"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                structured_logger.log_performance_metric(
                    f'function.{func.__name__}.duration',
                    duration,
                    {'function': func.__name__}
                )
                
                return result
            except Exception as e:
                duration = time.time() - start_time
                structured_logger.log_exception(e)
                raise
        return wrapper
    return decorator

# Flask CLI commands for log management
def register_logging_commands(app):
    """Register logging management CLI commands"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('log-stats')
    @with_appcontext
    def log_statistics():
        """Show logging and request statistics"""
        stats = structured_logger.get_log_statistics()
        click.echo("Logging Statistics:")
        click.echo(f"  Total requests: {stats.get('total_requests', 0)}")
        click.echo(f"  Slow requests: {stats.get('slow_requests', 0)}")
        click.echo(f"  Errors: {stats.get('errors', 0)}")
        click.echo(f"  Slow queries: {stats.get('slow_queries', 0)}")
        
        if 'metrics' in stats:
            click.echo("\nPerformance Metrics:")
            for metric_name, summary in stats['metrics'].items():
                click.echo(f"  {metric_name}: avg={summary['avg']:.3f}, "
                          f"min={summary['min']:.3f}, max={summary['max']:.3f}")
    
    @app.cli.command('log-reset')
    @with_appcontext
    def reset_log_stats():
        """Reset logging statistics"""
        structured_logger.reset_statistics()
        click.echo("Logging statistics reset successfully")

# Import time here to avoid circular imports
import time