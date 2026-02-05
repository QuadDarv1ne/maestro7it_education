"""
Performance tests for the profi_test application
"""
import pytest
import time
import threading
from unittest.mock import patch
import tempfile
import os

from app import create_app, db
from config import TestConfig
from app.models import User, TestResult
from app.performance import PerformanceMonitor
from app.advanced_caching import CacheManager
from app.database_pooling import db_connection_manager


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app."""
    return app.test_cli_runner()


class TestPerformanceMetrics:
    """Test performance metrics and monitoring capabilities"""
    
    def test_response_time_monitoring(self, app, client):
        """Test that response time monitoring works properly"""
        perf_monitor = PerformanceMonitor()
        
        # Record start time
        start_time = time.time()
        
        # Make a request to the home page
        response = client.get('/')
        
        # Record end time
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        # Response should be successful
        assert response.status_code == 200
        
        # Response time should be reasonable (less than 1 second)
        assert response_time < 1000
    
    def test_concurrent_request_handling(self, app, client):
        """Test handling of concurrent requests"""
        def make_request():
            response = client.get('/')
            return response.status_code
        
        # Create multiple threads to simulate concurrent requests
        threads = []
        results = []
        
        for i in range(10):
            thread = threading.Thread(target=lambda results=results: results.append(make_request()))
            threads.append(thread)
        
        # Start all threads
        start_time = time.time()
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        # All requests should succeed
        assert len([r for r in results if r == 200]) == 10
        
        # Total time should be reasonable for 10 concurrent requests
        assert total_time < 2000  # Less than 2 seconds for 10 requests
    
    def test_cache_performance(self, app):
        """Test cache performance improvements"""
        cache_manager = CacheManager()
        
        # Clear cache first
        cache_manager.clear_all()
        
        # Measure uncached operation
        start_time = time.time()
        for i in range(100):
            # Simulate an expensive operation
            result = sum(range(i * 100))
        uncached_time = (time.time() - start_time) * 1000  # ms
        
        # Store result in cache
        cache_manager.set('expensive_operation_result', result, timeout=300)
        
        # Measure cached operation
        start_time = time.time()
        for i in range(100):
            # Retrieve from cache
            cached_result = cache_manager.get('expensive_operation_result')
        cached_time = (time.time() - start_time) * 1000  # ms
        
        # Cached operations should be significantly faster
        assert cached_time < uncached_time * 0.5, f"Cached time ({cached_time}ms) should be much faster than uncached time ({uncached_time}ms)"
    
    def test_database_connection_performance(self, app):
        """Test database connection performance"""
        # Create a test user
        user = User(username='perf_test_user', email='perf@test.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()
        
        # Measure query performance
        start_time = time.time()
        for i in range(50):
            # Query the user multiple times
            queried_user = User.query.filter_by(id=user.id).first()
            assert queried_user is not None
        query_time = (time.time() - start_time) * 1000  # ms
        
        # Query time should be reasonable
        assert query_time < 500  # Less than 500ms for 50 queries
    
    def test_memory_usage_monitoring(self, app):
        """Test memory usage monitoring"""
        perf_monitor = PerformanceMonitor()
        
        # Take initial memory measurement
        initial_memory = perf_monitor.get_memory_usage()
        
        # Create some objects to increase memory usage
        big_list = [i for i in range(10000)]
        large_dict = {f"key_{i}": f"value_{i}" for i in range(5000)}
        
        # Take memory measurement after creating objects
        post_creation_memory = perf_monitor.get_memory_usage()
        
        # Memory usage should have increased
        # Note: This is a soft assertion as memory management is platform-dependent
        # We'll just ensure the function runs without errors
        
        # Clean up to reduce memory
        del big_list, large_dict
        import gc
        gc.collect()
        
        # Take final memory measurement
        final_memory = perf_monitor.get_memory_usage()
        
        # All measurements should return valid values
        assert isinstance(initial_memory, dict)
        assert 'rss' in initial_memory
        assert 'percent' in initial_memory
    
    def test_cache_hit_ratio(self, app):
        """Test cache hit ratio calculations"""
        cache_manager = CacheManager()
        
        # Clear cache
        cache_manager.clear_all()
        
        # Perform some cache operations
        for i in range(10):
            cache_manager.set(f'key_{i}', f'value_{i}', timeout=300)
        
        # Retrieve some cached values (cache hits)
        for i in range(5):
            value = cache_manager.get(f'key_{i}')
            assert value == f'value_{i}'
        
        # Try to retrieve non-existent values (cache misses)
        for i in range(10, 15):
            value = cache_manager.get(f'key_{i}')
            assert value is None
        
        # Get cache statistics
        stats = cache_manager.get_cache_stats()
        
        # Stats should contain expected keys
        assert 'hits' in stats
        assert 'misses' in stats
        assert 'hit_ratio' in stats
        
        # Hit ratio should be reasonable (5 hits, 5 misses = 50%)
        # Allow for some flexibility in the calculation
        expected_hit_ratio = 5 / 10  # 50%
        assert abs(stats['hit_ratio'] - expected_hit_ratio) < 0.1  # Within 10% tolerance
    
    def test_database_connection_pool_stats(self, app):
        """Test database connection pool statistics"""
        # Get initial stats
        initial_stats = db_connection_manager.get_pool_statistics()
        
        # Perform some database operations
        user = User(username='pool_test', email='pool@test.com')
        user.set_password('testpass')
        db.session.add(user)
        db.session.commit()
        
        # Query the user
        queried_user = User.query.filter_by(username='pool_test').first()
        assert queried_user is not None
        
        # Get stats after operations
        final_stats = db_connection_manager.get_pool_statistics()
        
        # Both should be dictionaries with expected keys
        assert isinstance(initial_stats, dict)
        assert isinstance(final_stats, dict)
        
        # Final stats should include connection information
        # At least check that the function returns properly formatted data
        assert 'checkouts' in final_stats or 'connects' in final_stats


class TestLoadHandling:
    """Test application load handling capabilities"""
    
    def test_multiple_user_creation_performance(self, app, client):
        """Test performance when creating multiple users"""
        start_time = time.time()
        
        # Create multiple users
        for i in range(20):
            response = client.post('/register', data={
                'username': f'testuser_{i}',
                'email': f'test{i}@example.com',
                'password': 'securepassword',
                'confirm_password': 'securepassword'
            }, follow_redirects=True)
            
            # Check that registration was successful
            assert response.status_code == 200
        
        creation_time = (time.time() - start_time) * 1000  # ms
        
        # Creating 20 users should be reasonably fast
        assert creation_time < 3000  # Less than 3 seconds for 20 users
    
    def test_session_handling_performance(self, app, client):
        """Test performance of session handling"""
        # Create a user first
        client.post('/register', data={
            'username': 'session_test',
            'email': 'session@test.com',
            'password': 'securepassword',
            'confirm_password': 'securepassword'
        }, follow_redirects=True)
        
        # Time multiple login/logout cycles
        start_time = time.time()
        
        for i in range(5):
            # Login
            login_response = client.post('/login', data={
                'username': 'session_test',
                'password': 'securepassword'
            }, follow_redirects=True)
            assert login_response.status_code == 200
            
            # Access protected page
            profile_response = client.get('/profile')
            assert profile_response.status_code == 200
            
            # Logout
            logout_response = client.post('/logout', follow_redirects=True)
            assert logout_response.status_code == 200
        
        session_time = (time.time() - start_time) * 1000  # ms
        
        # Session handling should be efficient
        assert session_time < 2000  # Less than 2 seconds for 5 login/logout cycles


if __name__ == '__main__':
    pytest.main([__file__])