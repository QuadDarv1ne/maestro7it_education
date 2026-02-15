import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path


class LoggingConfig:
    """Configuration class for application logging"""
    
    def __init__(self, app_name='ChessCalendar-RU', log_dir='logs'):
        self.app_name = app_name
        self.log_dir = Path(log_dir)
        self.setup_log_directory()
        
    def setup_log_directory(self):
        """Create log directory if it doesn't exist"""
        self.log_dir.mkdir(exist_ok=True)
        
    def setup_logging(self, level=logging.INFO, max_bytes=10*1024*1024, backup_count=5):
        """Setup comprehensive logging configuration"""
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Root logger configuration
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        
        # Clear existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        root_logger.addHandler(console_handler)
        
        # File handler for general logs
        general_log_file = self.log_dir / f"{self.app_name.lower()}_general.log"
        file_handler = logging.handlers.RotatingFileHandler(
            general_log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(file_handler)
        
        # Error log file for errors only
        error_log_file = self.log_dir / f"{self.app_name.lower()}_errors.log"
        error_handler = logging.handlers.RotatingFileHandler(
            error_log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(error_handler)
        
        # Specific loggers for different components
        self._setup_component_loggers(detailed_formatter)
        
        logging.info(f"Logging configured for {self.app_name}")
        
    def _setup_component_loggers(self, formatter):
        """Setup specific loggers for different application components"""
        
        # Parser logger
        parser_logger = logging.getLogger('app.parsers')
        parser_logger.setLevel(logging.DEBUG)
        
        parser_file_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / f"{self.app_name.lower()}_parsers.log",
            maxBytes=5*1024*1024,
            backupCount=3
        )
        parser_file_handler.setFormatter(formatter)
        parser_logger.addHandler(parser_file_handler)
        
        # Database logger
        db_logger = logging.getLogger('app.database')
        db_logger.setLevel(logging.INFO)
        
        db_file_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / f"{self.app_name.lower()}_database.log",
            maxBytes=5*1024*1024,
            backupCount=3
        )
        db_file_handler.setFormatter(formatter)
        db_logger.addHandler(db_file_handler)
        
        # Scheduler logger
        scheduler_logger = logging.getLogger('app.scheduler')
        scheduler_logger.setLevel(logging.INFO)
        
        scheduler_file_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / f"{self.app_name.lower()}_scheduler.log",
            maxBytes=5*1024*1024,
            backupCount=3
        )
        scheduler_file_handler.setFormatter(formatter)
        scheduler_logger.addHandler(scheduler_file_handler)
        
        # API logger
        api_logger = logging.getLogger('app.api')
        api_logger.setLevel(logging.INFO)
        
        api_file_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / f"{self.app_name.lower()}_api.log",
            maxBytes=5*1024*1024,
            backupCount=3
        )
        api_file_handler.setFormatter(formatter)
        api_logger.addHandler(api_file_handler)


# Global logging configuration instance
log_config = LoggingConfig()


def get_logger(name):
    """Convenience function to get a logger with the specified name"""
    return logging.getLogger(name)


def log_function_call(func):
    """Decorator to log function calls"""
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        logger.debug(f"Calling function: {func.__name__} with args: {args}, kwargs: {kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Function {func.__name__} completed successfully")
            return result
        except Exception as e:
            logger.error(f"Function {func.__name__} raised exception: {e}", exc_info=True)
            raise
    return wrapper


def log_event(event_type, message, level=logging.INFO, extra_data=None):
    """Log a specific event with additional metadata"""
    logger = get_logger('app.events')
    
    log_msg = f"[{event_type}] {message}"
    if extra_data:
        log_msg += f" | Extra data: {extra_data}"
    
    if level == logging.DEBUG:
        logger.debug(log_msg)
    elif level == logging.INFO:
        logger.info(log_msg)
    elif level == logging.WARNING:
        logger.warning(log_msg)
    elif level == logging.ERROR:
        logger.error(log_msg)
    elif level == logging.CRITICAL:
        logger.critical(log_msg)


# Initialize the logging system
def init_logging():
    """Initialize the logging system"""
    log_config.setup_logging()