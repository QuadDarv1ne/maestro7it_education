"""
Advanced Logging System for Production Environment
"""
import logging
import logging.handlers
import os
from datetime import datetime, timezone
import json
from flask import request, g
import traceback

class CustomFormatter(logging.Formatter):
    """Custom formatter for detailed logging"""
    
    def format(self, record):
        # Add timestamp
        record.timestamp = datetime.now(timezone.utc).isoformat()
        
        # Safely add request context if available
        try:
            from flask import g, request, has_request_context
            
            if has_request_context():
                if hasattr(g, 'user_id'):
                    record.user_id = g.user_id
                else:
                    record.user_id = 'anonymous'
                    
                if request:
                    record.request_id = getattr(request, 'id', 'unknown')
                    record.endpoint = request.endpoint or 'unknown'
                    record.method = request.method
                    record.url = request.url
                    record.remote_addr = request.remote_addr
                else:
                    record.request_id = 'unknown'
                    record.endpoint = 'unknown'
                    record.method = 'unknown'
                    record.url = 'unknown'
                    record.remote_addr = 'unknown'
            else:
                # No request context
                record.user_id = 'system'
                record.request_id = 'system'
                record.endpoint = 'system'
                record.method = 'SYSTEM'
                record.url = 'system'
                record.remote_addr = 'localhost'
        except Exception:
            # Fallback when context is not available
            record.user_id = 'system'
            record.request_id = 'system'
            record.endpoint = 'system'
            record.method = 'SYSTEM'
            record.url = 'system'
            record.remote_addr = 'localhost'
        
        # Format the message
        log_entry = {
            'timestamp': record.timestamp,
            'level': record.levelname,
            'logger': record.name,
            'user_id': record.user_id,
            'request_id': record.request_id,
            'endpoint': record.endpoint,
            'method': record.method,
            'url': record.url,
            'remote_addr': record.remote_addr,
            'message': record.getMessage()
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry, ensure_ascii=False)

def setup_logging(app):
    """Setup advanced logging for the application"""
    
    # Create logs directory
    log_dir = os.path.join(app.root_path, '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Close existing handlers before clearing
    for handler in root_logger.handlers[:]:
        handler.close()
    root_logger.handlers.clear()
    
    # Create formatters
    json_formatter = CustomFormatter()
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # File handler for all logs (JSON format)
    all_logs_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, 'application.log'),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    all_logs_handler.setFormatter(json_formatter)
    all_logs_handler.setLevel(logging.INFO)
    
    # Error file handler (JSON format)
    error_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, 'error.log'),
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3
    )
    error_handler.setFormatter(json_formatter)
    error_handler.setLevel(logging.ERROR)
    
    # Console handler for development (simple format)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(simple_formatter)
    console_handler.setLevel(logging.DEBUG if app.debug else logging.INFO)
    
    # Add handlers to root logger
    root_logger.addHandler(all_logs_handler)
    root_logger.addHandler(error_handler)
    root_logger.addHandler(console_handler)
    
    # Configure specific loggers
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy').setLevel(logging.WARNING)
    
    # Add request ID to each request
    @app.before_request
    def before_request():
        g.request_start_time = datetime.now(timezone.utc)
        request.id = os.urandom(8).hex()
    
    # Log request completion
    @app.after_request
    def after_request(response):
        if hasattr(g, 'request_start_time'):
            duration = (datetime.now(timezone.utc) - g.request_start_time).total_seconds()
            logging.info(f"Request completed - {request.endpoint} - {response.status_code} - {duration:.3f}s")
        return response
    
    # Log exceptions
    @app.errorhandler(Exception)
    def handle_exception(e):
        logging.error(f"Unhandled exception: {str(e)}", exc_info=True)
        return {"error": "Internal server error"}, 500
    
    # Log 404 errors
    @app.errorhandler(404)
    def handle_not_found(e):
        logging.warning(f"404 Not Found: {request.url}")
        return {"error": "Resource not found"}, 404
    
    logging.info("Logging system initialized successfully")
    return root_logger

def log_user_action(user_id, action, details=None):
    """Log user-specific actions"""
    extra = {
        'user_id': user_id,
        'action': action,
        'details': details or {}
    }
    logging.info(f"User action: {action}", extra=extra)

def log_security_event(event_type, user_id=None, details=None):
    """Log security-related events"""
    extra = {
        'event_type': event_type,
        'user_id': user_id or 'anonymous',
        'details': details or {}
    }
    logging.warning(f"Security event: {event_type}", extra=extra)

def log_performance_metric(metric_name, value, tags=None):
    """Log performance metrics"""
    extra = {
        'metric_name': metric_name,
        'value': value,
        'tags': tags or {}
    }
    logging.info(f"Performance metric: {metric_name} = {value}", extra=extra)

# Convenience functions for different log levels
def log_debug(message, **kwargs):
    logging.debug(message, extra=kwargs)

def log_info(message, **kwargs):
    logging.info(message, extra=kwargs)

def log_warning(message, **kwargs):
    logging.warning(message, extra=kwargs)

def log_error(message, **kwargs):
    logging.error(message, extra=kwargs)

def log_critical(message, **kwargs):
    logging.critical(message, extra=kwargs)