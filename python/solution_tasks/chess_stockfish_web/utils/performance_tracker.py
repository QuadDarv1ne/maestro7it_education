"""
Performance tracking utility for the chess application.
Implements timing measurements and performance metrics logging as specified in project requirements.
"""

import time
import logging
import json
from functools import wraps
from collections import defaultdict

# Set up logging
logger = logging.getLogger(__name__)
perf_logger = logging.getLogger('performance')

class PerformanceTracker:
    """
    Performance tracking class for monitoring game performance metrics.
    Based on project requirements for performance tracking system.
    """
    
    def __init__(self, log_file='performance.log'):
        self.metrics = defaultdict(list)
        self.log_file = log_file
        self.call_counts = defaultdict(int)
        self.error_counts = defaultdict(int)
        self.active_operations = {}
        
        # Performance optimization: Only log slow operations
        self.slow_operation_threshold = 0.5  # Reduced threshold to 0.5 seconds
        
        # Sampling rate to reduce logging overhead (0.0 = no sampling, 1.0 = log everything)
        self.sampling_rate = 0.1  # Only log 10% of operations to reduce overhead
        
        # Set up performance logger
        perf_handler = logging.FileHandler(log_file, encoding='utf-8')
        perf_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        perf_handler.setFormatter(perf_formatter)
        perf_logger.addHandler(perf_handler)
        perf_logger.setLevel(logging.INFO)
    
    def track_timing(self, operation_name):
        """
        Decorator to track timing of operations.
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Sampling to reduce overhead
                if self.sampling_rate < 1.0 and random.random() > self.sampling_rate:
                    # Skip tracking for most operations to reduce overhead
                    return func(*args, **kwargs)
                
                start_time = time.time()
                operation_id = f"{operation_name}_{int(start_time * 1000000)}"
                self.active_operations[operation_id] = {
                    'name': operation_name,
                    'start_time': start_time,
                    'args': args,
                    'kwargs': kwargs
                }
                
                try:
                    result = func(*args, **kwargs)
                    end_time = time.time()
                    duration = end_time - start_time
                    
                    # Only log operations that meet the threshold or are particularly important
                    if duration > self.slow_operation_threshold or operation_name in [
                        'engine_initialization', 'ai_move_calculation'
                    ]:
                        # Log timing
                        perf_logger.info(json.dumps({
                            'operation': operation_name,
                            'duration': duration,
                            'timestamp': time.time(),
                            'success': True
                        }))
                    
                    # Store metric
                    self.metrics[operation_name].append(duration)
                    self.call_counts[operation_name] += 1
                    
                    # Warn if operation takes too long
                    if duration > 1.0:  # 1 second threshold
                        logger.warning(f"Slow operation detected: {operation_name} took {duration:.2f} seconds")
                    
                    return result
                except Exception as e:
                    end_time = time.time()
                    duration = end_time - start_time
                    self.error_counts[operation_name] += 1
                    
                    # Always log errors
                    perf_logger.error(json.dumps({
                        'operation': operation_name,
                        'duration': duration,
                        'error': str(e),
                        'error_type': type(e).__name__,
                        'timestamp': time.time(),
                        'success': False
                    }))
                    raise
                finally:
                    # Clean up active operation tracking
                    if operation_id in self.active_operations:
                        del self.active_operations[operation_id]
            return wrapper
        return decorator
    
    def get_average_time(self, operation_name):
        """
        Get average execution time for an operation.
        """
        if operation_name in self.metrics and self.metrics[operation_name]:
            return sum(self.metrics[operation_name]) / len(self.metrics[operation_name])
        return 0
    
    def get_metrics_summary(self):
        """
        Get summary of all collected metrics.
        """
        summary = {}
        for operation, times in self.metrics.items():
            if times:
                summary[operation] = {
                    'count': len(times),
                    'call_count': self.call_counts.get(operation, 0),
                    'error_count': self.error_counts.get(operation, 0),
                    'average': sum(times) / len(times),
                    'min': min(times),
                    'max': max(times),
                    'total_time': sum(times)
                }
        return summary
    
    def get_active_operations(self):
        """
        Get currently active operations.
        """
        return dict(self.active_operations)
    
    def clear_metrics(self):
        """
        Clear collected metrics.
        """
        self.metrics.clear()
        self.call_counts.clear()
        self.error_counts.clear()
        self.active_operations.clear()

# Global performance tracker instance
performance_tracker = PerformanceTracker()

# Convenience decorators for common operations
track_engine_init = performance_tracker.track_timing('engine_initialization')
track_move_validation = performance_tracker.track_timing('move_validation')
track_move_execution = performance_tracker.track_timing('move_execution')
track_ai_calculation = performance_tracker.track_timing('ai_move_calculation')
track_game_status_check = performance_tracker.track_timing('game_status_check')
track_fen_retrieval = performance_tracker.track_timing('fen_retrieval')