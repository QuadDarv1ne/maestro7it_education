"""
Advanced caching utilities for the chess application.
Implements multi-level caching strategies for better performance.
"""

import time
import threading
from typing import Any, Optional, Dict
from functools import wraps
from collections import OrderedDict
import hashlib
import pickle
import json


class LRUCache:
    """
    Least Recently Used Cache implementation with thread safety.
    """
    
    def __init__(self, max_size: int = 1000, ttl: int = 300):
        """
        Initialize LRU Cache.
        
        Args:
            max_size: Maximum number of items in cache
            ttl: Time to live in seconds
        """
        self.max_size = max_size
        self.ttl = ttl
        self.cache = OrderedDict()
        self.lock = threading.RLock()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get item from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        with self.lock:
            if key in self.cache:
                value, timestamp = self.cache[key]
                # Check if expired
                if time.time() - timestamp > self.ttl:
                    del self.cache[key]
                    return None
                
                # Move to end (most recently used)
                self.cache.move_to_end(key)
                return value
            return None
    
    def put(self, key: str, value: Any) -> None:
        """
        Put item in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        with self.lock:
            # Remove oldest items if at max size
            while len(self.cache) >= self.max_size:
                self.cache.popitem(last=False)
            
            self.cache[key] = (value, time.time())
            # Move to end (most recently used)
            self.cache.move_to_end(key)
    
    def invalidate(self, key: str) -> None:
        """
        Remove specific key from cache.
        
        Args:
            key: Key to remove
        """
        with self.lock:
            if key in self.cache:
                del self.cache[key]
    
    def clear(self) -> None:
        """Clear all cache."""
        with self.lock:
            self.cache.clear()


class AdvancedCacheManager:
    """
    Advanced cache manager with multiple cache layers and strategies.
    """
    
    def __init__(self):
        # Different cache instances for different purposes
        self.fen_cache = LRUCache(max_size=500, ttl=600)  # Longer TTL for FEN positions
        self.move_cache = LRUCache(max_size=1000, ttl=300)  # Medium TTL for moves
        self.evaluation_cache = LRUCache(max_size=200, ttl=180)  # Shorter TTL for evaluations
        self.game_state_cache = LRUCache(max_size=100, ttl=900)  # Longer TTL for game states
        
        self.lock = threading.RLock()
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0
        }
    
    def _generate_key(self, *args, **kwargs) -> str:
        """
        Generate cache key from arguments.
        
        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Generated cache key
        """
        # Create a hash from the arguments
        data = f"{args}{sorted(kwargs.items())}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def get_fen(self, fen: str) -> Optional[Any]:
        """Get cached FEN position."""
        result = self.fen_cache.get(f"fen_{fen}")
        if result is not None:
            self.stats['hits'] += 1
        else:
            self.stats['misses'] += 1
        return result
    
    def set_fen(self, fen: str, value: Any) -> None:
        """Set cached FEN position."""
        self.fen_cache.put(f"fen_{fen}", value)
    
    def get_move(self, position: str, move: str) -> Optional[Any]:
        """Get cached move."""
        key = f"move_{position}_{move}"
        result = self.move_cache.get(key)
        if result is not None:
            self.stats['hits'] += 1
        else:
            self.stats['misses'] += 1
        return result
    
    def set_move(self, position: str, move: str, value: Any) -> None:
        """Set cached move."""
        key = f"move_{position}_{move}"
        self.move_cache.put(key, value)
    
    def get_evaluation(self, fen: str, depth: int) -> Optional[Any]:
        """Get cached evaluation."""
        key = f"eval_{fen}_{depth}"
        result = self.evaluation_cache.get(key)
        if result is not None:
            self.stats['hits'] += 1
        else:
            self.stats['misses'] += 1
        return result
    
    def set_evaluation(self, fen: str, depth: int, value: Any) -> None:
        """Set cached evaluation."""
        key = f"eval_{fen}_{depth}"
        self.evaluation_cache.put(key, value)
    
    def invalidate_position(self, fen: str) -> None:
        """Invalidate all caches related to a position."""
        # This is a simplified version - in practice you'd have more sophisticated invalidation
        self.fen_cache.invalidate(f"fen_{fen}")
        # Remove all moves starting with this position
        # This would require a more complex implementation in real scenario
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self.lock:
            total_requests = self.stats['hits'] + self.stats['misses']
            hit_rate = self.stats['hits'] / total_requests if total_requests > 0 else 0
            
            return {
                'hits': self.stats['hits'],
                'misses': self.stats['misses'],
                'hit_rate': hit_rate,
                'fen_cache_size': len(self.fen_cache.cache),
                'move_cache_size': len(self.move_cache.cache),
                'eval_cache_size': len(self.evaluation_cache.cache),
                'game_state_cache_size': len(self.game_state_cache.cache)
            }
    
    def clear_all(self) -> None:
        """Clear all caches."""
        self.fen_cache.clear()
        self.move_cache.clear()
        self.evaluation_cache.clear()
        self.game_state_cache.clear()
        
        with self.lock:
            self.stats = {
                'hits': 0,
                'misses': 0,
                'evictions': 0
            }


# Global advanced cache instance
advanced_cache_manager = AdvancedCacheManager()


def cached_advanced(cache_type: str = 'generic', ttl: int = 300, max_size: int = 100):
    """
    Decorator for caching function results with advanced cache.
    
    Args:
        cache_type: Type of cache to use ('fen', 'move', 'evaluation', 'generic')
        ttl: Time to live in seconds
        max_size: Maximum cache size
    """
    def decorator(func):
        # Create cache instance for this function if needed
        func_cache = LRUCache(max_size=max_size, ttl=ttl)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from function arguments
            key = advanced_cache_manager._generate_key(func.__name__, *args, **kwargs)
            
            # Try to get from cache
            cached_result = func_cache.get(key)
            if cached_result is not None:
                advanced_cache_manager.stats['hits'] += 1
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            func_cache.put(key, result)
            advanced_cache_manager.stats['misses'] += 1
            
            return result
        
        # Add cache control methods to the wrapper
        wrapper.invalidate_cache = lambda: func_cache.clear()
        wrapper.cache_stats = lambda: {
            'size': len(func_cache.cache),
            'max_size': func_cache.max_size,
            'ttl': func_cache.ttl
        }
        
        return wrapper
    return decorator


# Performance monitoring decorators
def monitor_performance(func):
    """
    Decorator to monitor function performance.
    
    Args:
        func: Function to monitor
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Log performance metrics (in a real app, you'd send to monitoring system)
            print(f"Performance: {func.__name__} took {execution_time:.4f}s")
            
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"Performance: {func.__name__} failed after {execution_time:.4f}s - {str(e)}")
            raise
    
    return wrapper


def batch_process(items, processor_func, batch_size=10):
    """
    Process items in batches for better performance.
    
    Args:
        items: Items to process
        processor_func: Function to process each item
        batch_size: Size of each batch
        
    Returns:
        List of processed results
    """
    results = []
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        batch_results = [processor_func(item) for item in batch]
        results.extend(batch_results)
    return results


# Singleton pattern for cache manager
def get_advanced_cache():
    """Get singleton instance of advanced cache manager."""
    return advanced_cache_manager