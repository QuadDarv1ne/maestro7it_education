"""
Memory optimization utilities for the profi_test application
"""
import gc
import weakref
import threading
from functools import wraps
import sys
import psutil
import os
from collections import defaultdict, deque
import logging
from typing import Any, Dict, List, Callable
from contextlib import contextmanager


logger = logging.getLogger(__name__)


class MemoryOptimizer:
    """Advanced memory optimization utilities for the application"""
    
    def __init__(self):
        self.object_registry = weakref.WeakValueDictionary()
        self.memory_stats = defaultdict(list)
        self.monitoring_thread = None
        self.is_monitoring = False
        self.monitoring_interval = 60  # seconds
        self.memory_threshold = 500 * 1024 * 1024  # 500 MB
        self.lock = threading.Lock()
        
    def track_object(self, obj: Any, name: str = None):
        """Track an object for memory optimization purposes"""
        if name is None:
            name = f"obj_{id(obj)}"
        
        # Use weak reference to avoid preventing garbage collection
        self.object_registry[name] = obj
        
    def get_memory_usage(self) -> Dict[str, Any]:
        """Get current memory usage statistics"""
        process = psutil.Process(os.getpid())
        
        memory_info = {
            'rss': process.memory_info().rss,  # Resident Set Size
            'vms': process.memory_info().vms,  # Virtual Memory Size
            'percent': process.memory_percent(),
            'shared': getattr(process.memory_info(), 'shared', 0),
            'text': getattr(process.memory_info(), 'text', 0),
            'lib': getattr(process.memory_info(), 'lib', 0),
            'data': getattr(process.memory_info(), 'data', 0),
            'dirty': getattr(process.memory_info(), 'dirty', 0),
        }
        
        # Python-specific memory info
        memory_info['python_heap'] = self._get_python_memory_usage()
        
        return memory_info
    
    def _get_python_memory_usage(self) -> Dict[str, int]:
        """Get Python-specific memory usage"""
        try:
            import tracemalloc
            if tracemalloc.is_tracing():
                current, peak = tracemalloc.get_traced_memory()
                return {
                    'current_bytes': current,
                    'peak_bytes': peak
                }
        except ImportError:
            pass
        
        # Fallback: approximate Python memory usage
        return {
            'approximate_bytes': len(gc.get_objects()) * 28  # Rough estimate
        }
    
    def start_monitoring(self):
        """Start background memory monitoring"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
            self.monitoring_thread.start()
            logger.info("Memory monitoring started")
    
    def stop_monitoring(self):
        """Stop memory monitoring"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("Memory monitoring stopped")
    
    def _monitoring_loop(self):
        """Background monitoring loop"""
        while self.is_monitoring:
            try:
                memory_usage = self.get_memory_usage()
                self._store_memory_stats(memory_usage)
                
                # Check if memory usage exceeds threshold
                if memory_usage['rss'] > self.memory_threshold:
                    self._handle_high_memory_usage(memory_usage)
                
                # Trigger garbage collection if needed
                if memory_usage['rss'] > self.memory_threshold * 0.8:  # 80% of threshold
                    self.force_garbage_collection()
                
                import time
                time.sleep(self.monitoring_interval)
            except Exception as e:
                logger.error(f"Memory monitoring error: {e}")
                import time
                time.sleep(5)  # Wait before retrying
    
    def _store_memory_stats(self, memory_usage: Dict[str, Any]):
        """Store memory statistics"""
        with self.lock:
            for key, value in memory_usage.items():
                self.memory_stats[key].append({
                    'value': value,
                    'timestamp': __import__('time').time()
                })
                
                # Keep only last 1000 measurements
                if len(self.memory_stats[key]) > 1000:
                    self.memory_stats[key] = self.memory_stats[key][-500:]
    
    def _handle_high_memory_usage(self, memory_usage: Dict[str, Any]):
        """Handle high memory usage situation"""
        logger.warning(f"High memory usage detected: {memory_usage['rss'] / (1024*1024):.2f} MB")
        
        # Force garbage collection
        collected = self.force_garbage_collection()
        logger.info(f"Garbage collection collected {collected} objects")
        
        # Clear caches if possible
        self.clear_unused_caches()
    
    def force_garbage_collection(self) -> int:
        """Force garbage collection and return number of collected objects"""
        collected = gc.collect()
        logger.debug(f"Garbage collection completed, collected {collected} objects")
        return collected
    
    def clear_unused_caches(self):
        """Clear unused cache entries"""
        # This is a placeholder - actual cache clearing depends on the cache implementation
        # In a real application, this would clear Flask cache, Redis cache, etc.
        logger.debug("Cleared unused caches")
    
    def optimize_list_operations(self, data: List[Any]) -> List[Any]:
        """Optimize list operations for memory efficiency"""
        # For large lists, consider using generators or iterators
        # This is a simplified version
        return data
    
    def get_memory_report(self) -> Dict[str, Any]:
        """Generate memory usage report"""
        memory_usage = self.get_memory_usage()
        
        with self.lock:
            stats_summary = {}
            for key, values in self.memory_stats.items():
                if values:
                    recent_values = [v['value'] for v in values[-10:]]  # Last 10 measurements
                    if recent_values:
                        stats_summary[key] = {
                            'current': recent_values[-1],
                            'average': sum(recent_values) / len(recent_values),
                            'min': min(recent_values),
                            'max': max(recent_values),
                            'count': len(recent_values)
                        }
        
        return {
            'current_usage': memory_usage,
            'historical_stats': stats_summary,
            'object_count': len(gc.get_objects()),
            'tracked_objects': len(self.object_registry),
            'garbage_objects': len(gc.garbage) if hasattr(gc, 'garbage') else 0
        }
    
    @contextmanager
    def memory_efficient_operation(self):
        """Context manager for memory-efficient operations"""
        initial_memory = self.get_memory_usage()['rss']
        try:
            yield
        finally:
            final_memory = self.get_memory_usage()['rss']
            memory_delta = final_memory - initial_memory
            if memory_delta > 10 * 1024 * 1024:  # More than 10MB increase
                logger.warning(f"Operation increased memory by {memory_delta / (1024*1024):.2f} MB")
                self.force_garbage_collection()


class MemoryOptimizedSession:
    """Memory-optimized session management"""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.sessions = {}
        self.access_order = deque()
        self.lock = threading.RLock()
    
    def get(self, session_id: str, default=None):
        """Get session data with LRU-like behavior"""
        with self.lock:
            if session_id in self.sessions:
                # Move to end to mark as recently used
                self.access_order.remove(session_id)
                self.access_order.append(session_id)
                return self.sessions[session_id]
            return default
    
    def set(self, session_id: str, data: Any):
        """Set session data with size management"""
        with self.lock:
            if session_id in self.sessions:
                # Update existing
                self.sessions[session_id] = data
                self.access_order.remove(session_id)
                self.access_order.append(session_id)
            else:
                # Add new
                self.sessions[session_id] = data
                self.access_order.append(session_id)
                
                # Evict oldest if exceeding max size
                if len(self.sessions) > self.max_size:
                    oldest = self.access_order.popleft()
                    del self.sessions[oldest]
    
    def cleanup_expired(self):
        """Clean up expired sessions"""
        # This is a simplified version - in practice, you'd check expiration times
        pass


def memory_efficient_cache(maxsize: int = 128):
    """Decorator for creating memory-efficient caches"""
    def decorator(func):
        cache = {}
        access_order = deque()
        lock = threading.RLock()
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create a cache key from arguments
            key = str((args, tuple(sorted(kwargs.items()))))
            
            with lock:
                if key in cache:
                    # Move to end to mark as recently used
                    access_order.remove(key)
                    access_order.append(key)
                    return cache[key]
                
                # Compute result
                result = func(*args, **kwargs)
                
                # Add to cache
                cache[key] = result
                access_order.append(key)
                
                # Manage cache size
                if len(cache) > maxsize:
                    oldest = access_order.popleft()
                    del cache[oldest]
                
                return result
        
        # Add cache management methods
        wrapper.cache_clear = lambda: cache.clear() or access_order.clear()
        wrapper.cache_info = lambda: {'hits': 0, 'misses': 0, 'size': len(cache), 'maxsize': maxsize}
        
        return wrapper
    return decorator


def batch_process_memory_efficient(items, batch_size: int = 100, processor: Callable = None):
    """Process items in batches to minimize memory usage"""
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        
        if processor:
            result = processor(batch)
            yield result
        else:
            yield batch
        
        # Explicitly delete batch to help with garbage collection
        del batch


# Global memory optimizer instance
memory_optimizer = MemoryOptimizer()


def init_memory_optimizations():
    """Initialize memory optimizations"""
    memory_optimizer.start_monitoring()
    logger.info("Memory optimizations initialized")


# Initialize when module is imported
init_memory_optimizations()


def get_memory_usage_report():
    """Get current memory usage report"""
    return memory_optimizer.get_memory_report()


def optimize_database_sessions():
    """Optimize database session memory usage"""
    from app import db
    
    # Clear SQLAlchemy session cache to free memory
    db.session.expunge_all()
    logger.debug("Database session cache cleared")


def memory_profile_function(func):
    """Decorator to profile memory usage of a function"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        initial_memory = memory_optimizer.get_memory_usage()['rss']
        result = func(*args, **kwargs)
        final_memory = memory_optimizer.get_memory_usage()['rss']
        
        memory_diff = final_memory - initial_memory
        logger.debug(f"Function {func.__name__} memory change: {memory_diff / (1024*1024):.2f} MB")
        
        return result
    return wrapper


def periodic_memory_cleanup():
    """Perform periodic memory cleanup operations"""
    # Force garbage collection
    gc.collect()
    
    # Only try to clear database sessions if we are in an app context
    try:
        from flask import has_app_context
        if has_app_context():
            from app import db
            db.session.expunge_all()
    except:
        # If anything goes wrong, just continue
        pass
    logger.debug("Periodic memory cleanup completed")