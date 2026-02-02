"""
Comprehensive test suite for profi_test application
"""
import pytest
import json
import time
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

# Import app components
from app import create_app, db
from app.models import User, TestResult, TestQuestion
from app.performance import cached_query, performance_monitor
from app.validators import InputValidator, FormValidator, APIValidator
from app.security import rate_limiter, api_protector, RateLimiter
from app.tasks import task_manager, TaskStatus

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test-secret-key',
        'CACHE_TYPE': 'simple',
        'WTF_CSRF_ENABLED': False
    })
    
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
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture
def auth_client(client):
    """A test client with authenticated user."""
    # Create test user
    with client.application.app_context():
        user = User(username='testuser', email='test@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()
    
    # Login
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword'
    })
    
    return client

class TestModels:
    """Test database models"""
    
    def test_user_model(self, app):
        """Test User model creation and methods"""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('testpass')
            
            assert user.username == 'testuser'
            assert user.email == 'test@example.com'
            assert user.check_password('testpass') is True
            assert user.check_password('wrongpass') is False
            assert str(user) == '<User testuser>'
    
    def test_test_result_model(self, app):
        """Test TestResult model"""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            db.session.add(user)
            db.session.commit()
            
            result = TestResult(
                user_id=user.id,
                methodology='klimov',
                answers='{"1": 3, "2": 2}',
                results='{"scores": {"tech": 85}}',
                recommendation='Test recommendation'
            )
            
            db.session.add(result)
            db.session.commit()
            
            assert result.user_id == user.id
            assert result.methodology == 'klimov'
            assert str(result) == f'<TestResult {result.id} for User {user.id}>'
    
    def test_relationships(self, app):
        """Test model relationships"""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            db.session.add(user)
            db.session.commit()
            
            result = TestResult(user_id=user.id, methodology='klimov')
            db.session.add(result)
            db.session.commit()
            
            # Test relationship loading
            user_from_db = User.query.get(user.id)
            assert len(user_from_db.test_results) == 1
            assert user_from_db.test_results[0].id == result.id

class TestPerformance:
    """Test performance optimization utilities"""
    
    def test_cached_query_decorator(self, app):
        """Test cached query decorator"""
        call_count = 0
        
        @cached_query(timeout=10)
        def expensive_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        with app.app_context():
            # First call should execute function
            result1 = expensive_function(5)
            assert result1 == 10
            assert call_count == 1
            
            # Second call should use cache
            result2 = expensive_function(5)
            assert result2 == 10
            assert call_count == 1  # Function not called again
            
            # Different argument should call function again
            result3 = expensive_function(6)
            assert result3 == 12
            assert call_count == 2
    
    def test_performance_monitor(self, app):
        """Test performance monitoring"""
        with app.app_context():
            # Record some metrics
            performance_monitor.record_query('test_query', 0.05)
            performance_monitor.record_query('test_query', 0.15)  # Slow query
            performance_monitor.record_metric('test_metric', 100)
            performance_monitor.record_metric('test_metric', 200)
            
            stats = performance_monitor.get_stats()
            
            assert 'test_query' in stats['query_counts']
            assert len(stats['slow_queries']) == 1  # Only the slow query
            assert 'test_metric' in stats['metrics_summary']
            assert stats['metrics_summary']['test_metric']['count'] == 2

class TestValidators:
    """Test input validation utilities"""
    
    def test_email_validation(self):
        """Test email validation"""
        assert InputValidator.validate_email('test@example.com') is True
        assert InputValidator.validate_email('invalid-email') is False
        assert InputValidator.validate_email('') is False
        assert InputValidator.validate_email(None) is False
    
    def test_username_validation(self):
        """Test username validation"""
        assert InputValidator.validate_username('testuser') is True
        assert InputValidator.validate_username('test_user_123') is True
        assert InputValidator.validate_username('ab') is False  # Too short
        assert InputValidator.validate_username('a' * 31) is False  # Too long
        assert InputValidator.validate_username('test-user') is False  # Invalid chars
    
    def test_password_validation(self):
        """Test password validation"""
        result = InputValidator.validate_password('StrongPass123!')
        assert result['valid'] is True
        assert len(result['errors']) == 0
        
        result = InputValidator.validate_password('weak')
        assert result['valid'] is False
        assert len(result['errors']) > 0
    
    def test_integer_validation(self):
        """Test integer validation"""
        assert InputValidator.validate_integer('123') == 123
        assert InputValidator.validate_integer('123', min_value=100) == 123
        assert InputValidator.validate_integer('123', max_value=200) == 123
        
        with pytest.raises(Exception):
            InputValidator.validate_integer('abc')
        
        with pytest.raises(Exception):
            InputValidator.validate_integer('50', min_value=100)
    
    def test_string_sanitization(self):
        """Test string sanitization"""
        assert InputValidator.sanitize_string('<script>alert("xss")</script>') == 'alert(xss)'
        assert InputValidator.sanitize_string('  test  ') == 'test'
        assert len(InputValidator.sanitize_string('a' * 2000)) <= 1000

class TestSecurity:
    """Test security utilities"""
    
    def test_rate_limiter(self):
        """Test rate limiting functionality"""
        limiter = RateLimiter()
        key = 'test_client:test_endpoint'
        
        # Should allow first requests
        for i in range(5):
            assert limiter.check_rate_limit(key, 'default') is True
        
        # Should block when limit exceeded
        assert limiter.check_rate_limit(key, 'default') is False
        
        # Should allow after time passes
        time.sleep(1)
        # Clean old requests manually for test
        limiter.requests[key] = [t for t in limiter.requests[key] if time.time() - t < 60]
        assert len(limiter.requests[key]) < 5
    
    def test_api_protector(self):
        """Test API protection"""
        # Test suspicious pattern detection
        assert api_protector._check_suspicious_data('DROP TABLE users') is True
        assert api_protector._check_suspicious_data('normal text') is False
        assert api_protector._check_suspicious_data('<script>alert(1)</script>') is True
        
        # Test IP blocking
        test_ip = '192.168.1.100'
        assert api_protector.is_ip_blocked(test_ip) is False
        api_protector.block_ip(test_ip)
        assert api_protector.is_ip_blocked(test_ip) is True
        api_protector.unblock_ip(test_ip)
        assert api_protector.is_ip_blocked(test_ip) is False

class TestTasks:
    """Test background task system"""
    
    def test_task_creation(self):
        """Test task creation and management"""
        def test_function():
            return "test result"
        
        task_id = task_manager.create_task(
            name="Test Task",
            func=test_function,
            priority=1
        )
        
        assert task_id is not None
        assert isinstance(task_id, str)
        
        # Check task status
        status = task_manager.get_task_status(task_id)
        assert status is not None
        assert status['name'] == "Test Task"
        assert status['status'] in [TaskStatus.PENDING.value, TaskStatus.RUNNING.value]
    
    def test_task_cancellation(self):
        """Test task cancellation"""
        def long_running_task():
            time.sleep(10)
            return "result"
        
        task_id = task_manager.create_task(
            name="Long Task",
            func=long_running_task
        )
        
        # Task should be pending initially
        status = task_manager.get_task_status(task_id)
        assert status['status'] == TaskStatus.PENDING.value
        
        # Cancel task
        result = task_manager.cancel_task(task_id)
        assert result is True
        
        # Check status after cancellation
        status = task_manager.get_task_status(task_id)
        assert status['status'] == TaskStatus.CANCELLED.value
    
    def test_task_stats(self):
        """Test task statistics"""
        stats = task_manager.get_stats()
        assert isinstance(stats, dict)
        assert 'total_tasks' in stats
        assert 'pending' in stats
        assert 'running' in stats
        assert 'completed' in stats
        assert 'failed' in stats

class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/api/monitoring/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data
        assert 'database' in data
        assert 'cache' in data
    
    def test_cache_stats(self, client):
        """Test cache statistics endpoint"""
        # Test without authentication (should fail)
        response = client.get('/api/monitoring/cache/stats')
        assert response.status_code == 401 or response.status_code == 302
        
        # Test with admin user would require more setup
    
    def test_task_endpoints(self, client):
        """Test task management endpoints"""
        # Test without authentication
        response = client.get('/api/tasks')
        assert response.status_code == 401 or response.status_code == 302

class TestIntegration:
    """Integration tests"""
    
    def test_user_registration_and_login(self, client):
        """Test complete user flow"""
        # Register new user
        response = client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'StrongPass123!',
            'password_confirm': 'StrongPass123!'
        })
        
        # Should redirect after successful registration
        assert response.status_code in [200, 302]
        
        # Login with new user
        response = client.post('/login', data={
            'username': 'newuser',
            'password': 'StrongPass123!'
        })
        
        # Should be logged in
        assert response.status_code in [200, 302]
    
    def test_test_submission_flow(self, auth_client):
        """Test complete test submission flow"""
        # Submit test answers
        test_data = {
            '1': 3,
            '2': 2,
            '3': 1,
            '4': 3,
            '5': 2
        }
        
        response = auth_client.post('/api/test/submit_test/klimov',
                                  json=test_data,
                                  content_type='application/json')
        
        if response.status_code == 200:
            data = json.loads(response.data)
            assert 'success' in data
            assert 'result_id' in data

# Performance tests
class TestPerformanceIntegration:
    """Performance integration tests"""
    
    def test_concurrent_requests(self, client):
        """Test handling of concurrent requests"""
        import threading
        
        def make_request():
            response = client.get('/api/monitoring/health')
            return response.status_code == 200
        
        # Make multiple concurrent requests
        threads = []
        results = []
        
        for i in range(10):
            thread = threading.Thread(target=lambda: results.append(make_request()))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # All requests should succeed
        assert all(results)
    
    def test_cache_performance(self, app):
        """Test cache performance improvement"""
        with app.app_context():
            @cached_query(timeout=10)
            def slow_function():
                time.sleep(0.1)  # Simulate slow operation
                return "result"
            
            # First call - slow
            start_time = time.time()
            result1 = slow_function()
            first_duration = time.time() - start_time
            
            # Second call - fast (cached)
            start_time = time.time()
            result2 = slow_function()
            second_duration = time.time() - start_time
            
            # Second call should be much faster
            assert second_duration < first_duration * 0.1
            assert result1 == result2

# Run tests with: pytest tests/ -v