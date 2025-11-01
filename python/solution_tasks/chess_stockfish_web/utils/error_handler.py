"""
Enhanced error handling and recovery mechanisms for the chess application.
Implements comprehensive error handling strategies with automatic recovery where possible.
"""

import logging
import time
import traceback
from typing import Any, Callable, Optional
from functools import wraps

logger = logging.getLogger(__name__)

class ChessAppError(Exception):
    """Base exception class for chess application errors."""
    def __init__(self, message: str, error_code: Optional[str] = None, recoverable: bool = True):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.recoverable = recoverable

class EngineInitializationError(ChessAppError):
    """Exception raised when Stockfish engine fails to initialize."""
    def __init__(self, message: str):
        super().__init__(message, error_code="ENGINE_INIT_ERROR", recoverable=True)

class MoveValidationError(ChessAppError):
    """Exception raised when move validation fails."""
    def __init__(self, message: str):
        super().__init__(message, error_code="MOVE_VALIDATION_ERROR", recoverable=True)

class GameLogicError(ChessAppError):
    """Exception raised when game logic encounters an error."""
    def __init__(self, message: str):
        super().__init__(message, error_code="GAME_LOGIC_ERROR", recoverable=True)

class SessionError(ChessAppError):
    """Exception raised when session management fails."""
    def __init__(self, message: str):
        super().__init__(message, error_code="SESSION_ERROR", recoverable=True)

class CacheError(ChessAppError):
    """Exception raised when cache operations fail."""
    def __init__(self, message: str):
        super().__init__(message, error_code="CACHE_ERROR", recoverable=True)

class ErrorHandler:
    """
    Central error handling system for the chess application.
    Provides comprehensive error handling with automatic recovery mechanisms.
    """
    
    def __init__(self):
        self.error_counts = {}
        self.last_error_time = {}
        self.recovery_attempts = {}
        self.max_recovery_attempts = 3
        self.error_cooldown_periods = {
            'EngineInitializationError': 5.0,  # 5 seconds cooldown
            'MoveValidationError': 0.1,        # 100ms cooldown
            'GameLogicError': 1.0,             # 1 second cooldown
            'SessionError': 1.0,               # 1 second cooldown
            'CacheError': 0.5                  # 500ms cooldown
        }
        
    def handle_error(self, error: Exception, context: str = "", recoverable: bool = True) -> dict:
        """
        Handle an error with comprehensive logging and potential recovery.
        
        Args:
            error: The exception that occurred
            context: Context where the error occurred
            recoverable: Whether the error is recoverable
            
        Returns:
            Dictionary with error information and recovery status
        """
        error_type = type(error).__name__
        error_message = str(error)
        
        # Update error counts
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        self.last_error_time[error_type] = time.time()
        
        # Log error with full context
        logger.error(f"Error in {context}: {error_type}: {error_message}")
        logger.debug(f"Full traceback:\n{traceback.format_exc()}")
        
        # Determine if recovery is possible
        can_recover = recoverable and self._can_attempt_recovery(error_type)
        
        # Add cooldown period check
        cooldown_period = self.error_cooldown_periods.get(error_type, 1.0)
        last_error_time = self.last_error_time.get(error_type, 0)
        in_cooldown = (time.time() - last_error_time) < cooldown_period
        
        error_info = {
            'type': error_type,
            'message': error_message,
            'context': context,
            'recoverable': recoverable,
            'can_recover': can_recover,
            'in_cooldown': in_cooldown,
            'attempts': self.recovery_attempts.get(error_type, 0),
            'timestamp': time.time()
        }
        
        return error_info
    
    def _can_attempt_recovery(self, error_type: str) -> bool:
        """
        Determine if recovery can be attempted for this error type.
        
        Args:
            error_type: Type of error
            
        Returns:
            Boolean indicating if recovery can be attempted
        """
        attempts = self.recovery_attempts.get(error_type, 0)
        
        # Check cooldown period
        cooldown_period = self.error_cooldown_periods.get(error_type, 1.0)
        last_error_time = self.last_error_time.get(error_type, 0)
        in_cooldown = (time.time() - last_error_time) < cooldown_period
        
        # Don't attempt recovery if in cooldown or max attempts reached
        return not in_cooldown and attempts < self.max_recovery_attempts
    
    def attempt_recovery(self, error_type: str, recovery_func: Callable) -> bool:
        """
        Attempt to recover from an error.
        
        Args:
            error_type: Type of error
            recovery_func: Function to attempt recovery
            
        Returns:
            Boolean indicating if recovery was successful
        """
        # Update recovery attempts
        self.recovery_attempts[error_type] = self.recovery_attempts.get(error_type, 0) + 1
        
        try:
            recovery_result = recovery_func()
            if recovery_result:
                logger.info(f"Recovery successful for {error_type}")
                # Reset error count on successful recovery
                self.error_counts[error_type] = 0
                return True
            else:
                logger.warning(f"Recovery failed for {error_type}")
                return False
        except Exception as e:
            logger.error(f"Recovery attempt failed for {error_type}: {e}")
            return False
    
    def get_error_stats(self) -> dict:
        """
        Get error statistics.
        
        Returns:
            Dictionary with error statistics
        """
        return {
            'error_counts': self.error_counts,
            'last_error_time': self.last_error_time,
            'recovery_attempts': self.recovery_attempts,
            'max_recovery_attempts': self.max_recovery_attempts
        }
    
    def clear_error_stats(self) -> None:
        """Clear error statistics."""
        self.error_counts.clear()
        self.last_error_time.clear()
        self.recovery_attempts.clear()

# Global error handler instance
error_handler = ErrorHandler()

def handle_chess_errors(context: str = ""):
    """
    Decorator for handling chess application errors.
    
    Args:
        context: Context where the function is used
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ChessAppError as e:
                error_info = error_handler.handle_error(e, context, e.recoverable)
                # Re-raise chess app errors
                raise
            except Exception as e:
                # Handle unexpected errors
                error_info = error_handler.handle_error(e, context, recoverable=True)
                # Convert to ChessAppError
                raise ChessAppError(f"Unexpected error in {context}: {str(e)}") from e
        return wrapper
    return decorator

def retry_on_failure(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Decorator to retry a function on failure with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each retry
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}")
                    
                    # Don't delay on the last attempt
                    if attempt < max_attempts - 1:
                        logger.info(f"Retrying in {current_delay} seconds...")
                        time.sleep(current_delay)
                        current_delay *= backoff
            
            # If all attempts failed, raise the last exception
            logger.error(f"All {max_attempts} attempts failed for {func.__name__}")
            raise Exception(f"All {max_attempts} attempts failed for {func.__name__}") from last_exception
        return wrapper
    return decorator