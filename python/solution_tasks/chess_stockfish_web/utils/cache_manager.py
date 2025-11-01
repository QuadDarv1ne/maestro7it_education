"""
Enhanced caching system with LRU eviction policy and size management.
Implements advanced caching strategies for the chess application.
"""

import time
import logging
from collections import OrderedDict
from threading import Lock
from typing import Any, Optional, Callable

logger = logging.getLogger(__name__)

class LRUCache:
    """
    Enhanced LRU Cache implementation with TTL and size limits.
    """
    
    def __init__(self, max_size: int = 1000, ttl: int = 300):
        """
        Initialize LRU cache.
        
        Args:
            max_size: Maximum number of items in cache
            ttl: Time to live in seconds
        """
        self.max_size = max_size
        self.ttl = ttl
        self.cache = OrderedDict()
        self.lock = Lock()
        self.hits = 0
        self.misses = 0
        self.evictions = 0
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        with self.lock:
            if key in self.cache:
                value, timestamp = self.cache[key]
                if time.time() - timestamp < self.ttl:
                    # Move to end (most recently used)
                    self.cache.move_to_end(key)
                    self.hits += 1
                    return value
                else:
                    # Expired entry
                    del self.cache[key]
                    self.misses += 1
                    return None
            else:
                self.misses += 1
                return None
    
    def put(self, key: str, value: Any) -> None:
        """
        Put value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        with self.lock:
            # Remove expired entries
            self._cleanup_expired()
            
            # Implement LRU eviction
            if len(self.cache) >= self.max_size:
                # Remove oldest entry
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
                self.evictions += 1
                logger.debug(f"Evicted oldest entry: {oldest_key}")
            
            # Add new entry
            self.cache[key] = (value, time.time())
            # Move to end (most recently used)
            self.cache.move_to_end(key)
    
    def _cleanup_expired(self) -> None:
        """Remove expired entries from cache."""
        current_time = time.time()
        expired_keys = [
            key for key, (_, timestamp) in self.cache.items()
            if current_time - timestamp >= self.ttl
        ]
        for key in expired_keys:
            del self.cache[key]
    
    def invalidate(self, key: str) -> bool:
        """
        Remove specific key from cache.
        
        Args:
            key: Key to remove
            
        Returns:
            True if key was removed, False if not found
        """
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                return True
            return False
    
    def clear(self) -> None:
        """Clear all entries from cache."""
        with self.lock:
            self.cache.clear()
            self.hits = 0
            self.misses = 0
            self.evictions = 0
    
    def get_stats(self) -> dict:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        total_requests = self.hits + self.misses
        hit_rate = self.hits / total_requests if total_requests > 0 else 0
        
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'evictions': self.evictions,
            'hit_rate': hit_rate,
            'ttl': self.ttl
        }

class CacheManager:
    """
    Central cache manager for the application.
    Manages multiple specialized caches.
    """
    
    def __init__(self):
        # Specialized caches for different operations with optimized sizes and TTLs
        # Increased cache sizes for better hit rates
        self.board_state_cache = LRUCache(max_size=1000, ttl=1)  # 1 second TTL
        self.valid_moves_cache = LRUCache(max_size=2000, ttl=2)  # 2 seconds TTL
        self.ai_move_cache = LRUCache(max_size=2000, ttl=15)  # 15 seconds TTL (increased for better reuse)
        self.evaluation_cache = LRUCache(max_size=1000, ttl=3)  # 3 seconds TTL
        self.game_status_cache = LRUCache(max_size=1000, ttl=1)  # 1 second TTL
        
        # Generic cache for other operations
        self.generic_cache = LRUCache(max_size=2000, ttl=600)  # 10 minutes TTL (increased)
        
        # Performance tracking
        self._last_cleanup_time = time.time()
        self._cleanup_interval = 10  # Cleanup every 10 seconds
    
    def get_cache_stats(self) -> dict:
        """
        Get statistics for all caches.
        
        Returns:
            Dictionary with cache statistics
        """
        # Perform periodic cleanup
        current_time = time.time()
        if current_time - self._last_cleanup_time > self._cleanup_interval:
            # This will be done automatically by the LRU cache, but we track the time
            self._last_cleanup_time = current_time
        
        return {
            'board_state_cache': self.board_state_cache.get_stats(),
            'valid_moves_cache': self.valid_moves_cache.get_stats(),
            'ai_move_cache': self.ai_move_cache.get_stats(),
            'evaluation_cache': self.evaluation_cache.get_stats(),
            'game_status_cache': self.game_status_cache.get_stats(),
            'generic_cache': self.generic_cache.get_stats()
        }
    
    def clear_all_caches(self) -> None:
        """Clear all caches."""
        self.board_state_cache.clear()
        self.valid_moves_cache.clear()
        self.ai_move_cache.clear()
        self.evaluation_cache.clear()
        self.game_status_cache.clear()
        self.generic_cache.clear()

# Global cache manager instance
cache_manager = CacheManager()

def cached(cache_type: str = 'generic'):
    """
    Decorator for caching function results.
    
    Args:
        cache_type: Type of cache to use ('board_state', 'valid_moves', 'ai_move', 
                   'evaluation', 'game_status', 'generic')
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            # Create cache key
            cache_key = f"{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Select appropriate cache
            cache_map = {
                'board_state': cache_manager.board_state_cache,
                'valid_moves': cache_manager.valid_moves_cache,
                'ai_move': cache_manager.ai_move_cache,
                'evaluation': cache_manager.evaluation_cache,
                'game_status': cache_manager.game_status_cache,
                'generic': cache_manager.generic_cache
            }
            
            selected_cache = cache_map.get(cache_type, cache_manager.generic_cache)
            
            # Try to get from cache
            cached_result = selected_cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Call function and cache result
            result = func(*args, **kwargs)
            selected_cache.put(cache_key, result)
            return result
        return wrapper
    return decorator