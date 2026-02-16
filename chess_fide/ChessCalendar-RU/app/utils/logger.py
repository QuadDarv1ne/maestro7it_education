"""
Enhanced logging system with structured logging and log aggregation
"""
import logging
import logging.handlers
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, 'extra'):
            log_data.update(record.extra)
        
        # Add request context if available
        try:
            from flask import request, g
            if request:
                log_data['request'] = {
                    'method': request.method,
                    'path': request.path,
                    'remote_addr': request.remote_addr,
                    'user_agent': request.headers.get('User-Agent', ''),
                }
                if hasattr(g, 'current_user'):
                    log_data['user_id'] = g.current_user.get('user_id')
        except (ImportError, RuntimeError):
            pass
        
        return json.dumps(log_data)


class ColoredFormatter(logging.Formatter):
    """Colored formatter for console output"""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors"""
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)


def setup_logging(
    app_name: str = 'chess_calendar',
    log_level: str = None,
    log_dir: str = 'logs',
    json_logs: bool = False,
    console_logs: bool = True
) -> logging.Logger:
    """
    Setup application logging
    
    Args:
        app_name: Application name
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files
        json_logs: Use JSON formatting for file logs
        console_logs: Enable console logging
    
    Returns:
        Configured logger
    """
    # Get log level from environment or parameter
    log_level = log_level or os.environ.get('LOG_LEVEL', 'INFO')
    log_level = getattr(logging, log_level.upper())
    
    # Create logger
    logger = logging.getLogger(app_name)
    logger.setLevel(log_level)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Create log directory
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    # File handler - All logs
    all_log_file = log_path / f'{app_name}.log'
    file_handler = logging.handlers.RotatingFileHandler(
        all_log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    
    if json_logs:
        file_handler.setFormatter(JSONFormatter())
    else:
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
    
    logger.addHandler(file_handler)
    
    # File handler - Error logs only
    error_log_file = log_path / f'{app_name}_error.log'
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    
    if json_logs:
        error_handler.setFormatter(JSONFormatter())
    else:
        error_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s\n%(pathname)s:%(lineno)d'
        ))
    
    logger.addHandler(error_handler)
    
    # Console handler
    if console_logs:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get logger for module"""
    return logging.getLogger(f'chess_calendar.{name}')


class RequestLogger:
    """Middleware for logging HTTP requests"""
    
    def __init__(self, app=None):
        self.app = app
        self.logger = get_logger('requests')
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with Flask app"""
        app.before_request(self.log_request)
        app.after_request(self.log_response)
    
    def log_request(self):
        """Log incoming request"""
        from flask import request
        
        self.logger.info(
            f"Request: {request.method} {request.path}",
            extra={
                'method': request.method,
                'path': request.path,
                'remote_addr': request.remote_addr,
                'user_agent': request.headers.get('User-Agent', ''),
            }
        )
    
    def log_response(self, response):
        """Log outgoing response"""
        from flask import request
        import time
        
        # Calculate request duration
        if hasattr(request, '_start_time'):
            duration = time.time() - request._start_time
        else:
            duration = 0
        
        self.logger.info(
            f"Response: {response.status_code} - {duration:.3f}s",
            extra={
                'status_code': response.status_code,
                'duration': duration,
                'path': request.path,
            }
        )
        
        return response


class CeleryLogger:
    """Logger for Celery tasks"""
    
    def __init__(self):
        self.logger = get_logger('celery')
    
    def log_task_start(self, task_name: str, task_id: str, args: tuple, kwargs: dict):
        """Log task start"""
        self.logger.info(
            f"Task started: {task_name}",
            extra={
                'task_name': task_name,
                'task_id': task_id,
                'args': str(args),
                'kwargs': str(kwargs),
            }
        )
    
    def log_task_success(self, task_name: str, task_id: str, result: Any, duration: float):
        """Log task success"""
        self.logger.info(
            f"Task completed: {task_name} - {duration:.3f}s",
            extra={
                'task_name': task_name,
                'task_id': task_id,
                'duration': duration,
                'result': str(result)[:200],  # Truncate long results
            }
        )
    
    def log_task_failure(self, task_name: str, task_id: str, exception: Exception, duration: float):
        """Log task failure"""
        self.logger.error(
            f"Task failed: {task_name} - {str(exception)}",
            extra={
                'task_name': task_name,
                'task_id': task_id,
                'duration': duration,
                'exception': str(exception),
            },
            exc_info=True
        )
    
    def log_task_retry(self, task_name: str, task_id: str, exception: Exception, retry_count: int):
        """Log task retry"""
        self.logger.warning(
            f"Task retry: {task_name} - Attempt {retry_count}",
            extra={
                'task_name': task_name,
                'task_id': task_id,
                'retry_count': retry_count,
                'exception': str(exception),
            }
        )


# Global logger instances
app_logger = setup_logging()
request_logger = RequestLogger()
celery_logger = CeleryLogger()
