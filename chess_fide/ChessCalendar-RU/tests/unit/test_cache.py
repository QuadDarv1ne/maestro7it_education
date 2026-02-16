"""
Unit tests for cache manager
"""
import pytest
import time
from app.utils.cache_manager import MultiLevelCache, cached, invalidate_cache


class TestMultiLevelCache:
    """Tests for MultiLevelCache"""
    
    @pytest.fixture
    def cache(self):
        """Create cache instance"""
        return MultiLevelCache(l1_max_size=10)
    
    def test_set_and_get(self, cache):
        """Test basic set and get"""
        cache.set('test_key', 'test_value', timeout=60)
        value = cache.get('test_key')
        
        assert value == 'test_value'
    
    def test_get_nonexistent(self, cache):
        """Test getting non-existent key"""
        value = cache.get('nonexistent_key')
        assert value is None
    
    def test_delete(self, cache):
        """Test deleting key"""
        cache.set('test_key', 'test_value')
        cache.delete('test_key')
        
        value = cache.get('test_key')
        assert value is None
    
    def test_l1_eviction(self, cache):
        """Test L1 cache eviction (LFU)"""
        # Fill L1 cache beyond max size
        for i in range(15):
            cache.set(f'key_{i}', f'value_{i}')
        
        # L1 should have only 10 items
        assert len(cache.l1_cache) <= cache.l1_max_size
    
    def test_cache_promotion(self, cache):
        """Test cache promotion from L2 to L1"""
        # Set in cache
        cache.set('test_key', 'test_value')
        
        # Clear L1
        cache.l1_cache.clear()
        
        # Get should promote from L2 to L1
        value = cache.get('test_key')
        assert value == 'test_value'
        assert 'test_key' in cache.l1_cache
    
    def test_invalidate_by_tag(self, cache):
        """Test invalidation by tag"""
        cache.set('key1', 'value1', tags=['tag1'])
        cache.set('key2', 'value2', tags=['tag1'])
        cache.set('key3', 'value3', tags=['tag2'])
        
        cache.invalidate_by_tag('tag1')
        
        assert cache.get('key1') is None
        assert cache.get('key2') is None
        assert cache.get('key3') == 'value3'
    
    def test_invalidate_by_pattern(self, cache):
        """Test invalidation by pattern"""
        cache.set('user:1', 'data1')
        cache.set('user:2', 'data2')
        cache.set('tournament:1', 'data3')
        
        cache.invalidate_by_pattern('user:*')
        
        assert cache.get('user:1') is None
        assert cache.get('user:2') is None
        assert cache.get('tournament:1') == 'data3'
    
    def test_clear(self, cache):
        """Test clearing all cache"""
        cache.set('key1', 'value1')
        cache.set('key2', 'value2')
        
        cache.clear()
        
        assert cache.get('key1') is None
        assert cache.get('key2') is None
    
    def test_stats(self, cache):
        """Test cache statistics"""
        cache.set('key1', 'value1')
        cache.set('key2', 'value2')
        
        stats = cache.get_stats()
        
        assert 'l1' in stats
        assert stats['l1']['size'] >= 0
        assert stats['l1']['max_size'] == 10


class TestCacheDecorators:
    """Tests for cache decorators"""
    
    def test_cached_decorator(self):
        """Test @cached decorator"""
        call_count = 0
        
        @cached(timeout=60, key_prefix='test')
        def expensive_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        # First call
        result1 = expensive_function(5)
        assert result1 == 10
        assert call_count == 1
        
        # Second call (should use cache)
        result2 = expensive_function(5)
        assert result2 == 10
        assert call_count == 1  # Not incremented
        
        # Different argument
        result3 = expensive_function(10)
        assert result3 == 20
        assert call_count == 2
    
    def test_invalidate_cache_decorator(self):
        """Test @invalidate_cache decorator"""
        from app.utils.cache_manager import cache_manager
        
        # Set some cached data
        cache_manager.set('test:data', 'value', tags=['test'])
        
        @invalidate_cache(tags=['test'])
        def update_function():
            return 'updated'
        
        # Call function
        result = update_function()
        assert result == 'updated'
        
        # Cache should be invalidated
        assert cache_manager.get('test:data') is None
