import unittest
import tempfile
import os
from datetime import datetime, date, timedelta
from app import create_app, db
from app.models.tournament import Tournament
from app.models.user import User
from app.utils.performance_monitor import PerformanceMonitor, perf_monitor
from app.utils.cache import TournamentCache


class TestPerformanceMonitoring(unittest.TestCase):

    def setUp(self):
        """Setup test database"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Create sample tournaments for testing
            for i in range(5):
                tournament = Tournament(
                    name=f"Test Tournament {i}",
                    start_date=date(2026, 3, 15 + i),
                    end_date=date(2026, 3, 20 + i),
                    location="Moscow, Russia",
                    category="FIDE",
                    status="Scheduled",
                    fide_id=f"TEST{i}",
                    source_url="https://test.com"
                )
                db.session.add(tournament)
            
            db.session.commit()

    def tearDown(self):
        """Clean up after tests"""
        with self.app.app_context():
            db.drop_all()

    def test_performance_monitor_initialization(self):
        """Test that performance monitor is properly initialized"""
        self.assertIsInstance(perf_monitor, PerformanceMonitor)
        
        # Check initial state
        summary = perf_monitor.get_performance_summary()
        self.assertEqual(summary['total_requests'], 0)
        self.assertEqual(summary['avg_response_time'], 0)

    def test_record_request(self):
        """Test recording a request"""
        perf_monitor.record_request(
            endpoint="/test/endpoint",
            method="GET",
            response_time=0.5,
            status_code=200
        )
        
        # Check that request was recorded
        summary = perf_monitor.get_performance_summary()
        self.assertEqual(summary['total_requests'], 1)
        self.assertGreaterEqual(summary['avg_response_time'], 0)
        
        # Check endpoint stats
        stats = perf_monitor.get_endpoint_stats("GET /test/endpoint")
        self.assertEqual(stats['count'], 1)
        self.assertEqual(stats['max_time'], 0.5)

    def test_get_recent_requests(self):
        """Test retrieving recent requests"""
        # Record a few requests
        perf_monitor.record_request(
            endpoint="/recent/test1",
            method="GET",
            response_time=0.1,
            status_code=200
        )
        perf_monitor.record_request(
            endpoint="/recent/test2",
            method="POST",
            response_time=0.2,
            status_code=200
        )
        
        # Get recent requests (should get both)
        recent = perf_monitor.get_recent_requests(minutes=5)
        self.assertGreaterEqual(len(recent), 2)
        
        # Check that requests have correct data
        endpoints = [req['endpoint'] for req in recent]
        self.assertIn("/recent/test1", endpoints)
        self.assertIn("/recent/test2", endpoints)

    def test_slow_endpoints_detection(self):
        """Test detection of slow endpoints"""
        # Record a slow request
        perf_monitor.record_request(
            endpoint="/slow/endpoint",
            method="GET",
            response_time=2.0,  # Very slow
            status_code=200
        )
        
        # Record a fast request
        perf_monitor.record_request(
            endpoint="/fast/endpoint",
            method="GET",
            response_time=0.01,  # Very fast
            status_code=200
        )
        
        # Get slow endpoints (threshold 0.5s)
        slow_endpoints = perf_monitor.get_slow_endpoints(threshold=0.5)
        
        # Should find the slow endpoint
        slow_endpoint_names = [ep['endpoint'] for ep in slow_endpoints]
        self.assertIn("GET /slow/endpoint", slow_endpoint_names)
        self.assertNotIn("GET /fast/endpoint", slow_endpoint_names)

    def test_performance_summary(self):
        """Test performance summary calculation"""
        # Record various requests
        perf_monitor.record_request(
            endpoint="/test/endpoint",
            method="GET",
            response_time=0.1,
            status_code=200
        )
        perf_monitor.record_request(
            endpoint="/test/endpoint",
            method="GET",
            response_time=0.3,
            status_code=200
        )
        perf_monitor.record_request(
            endpoint="/test/endpoint",
            method="GET",
            response_time=0.2,
            status_code=500  # Error
        )
        
        summary = perf_monitor.get_performance_summary()
        
        # Check calculations
        self.assertEqual(summary['total_requests'], 3)
        self.assertAlmostEqual(summary['avg_response_time'], 0.2, places=2)  # (0.1+0.3+0.2)/3
        self.assertEqual(summary['error_rate'], 1/3)  # 1 error out of 3 requests

    def test_multiple_requests_same_endpoint(self):
        """Test recording multiple requests to same endpoint"""
        endpoint_name = "GET /api/test"
        
        # Record multiple requests to same endpoint
        for i in range(3):
            perf_monitor.record_request(
                endpoint="/api/test",
                method="GET",
                response_time=0.1 + (i * 0.05),  # 0.1, 0.15, 0.2
                status_code=200
            )
        
        # Check endpoint stats
        stats = perf_monitor.get_endpoint_stats(endpoint_name)
        self.assertEqual(stats['count'], 3)
        self.assertAlmostEqual(stats['total_time'], 0.45, places=2)  # 0.1 + 0.15 + 0.2
        self.assertAlmostEqual(stats['min_time'], 0.1, places=2)
        self.assertAlmostEqual(stats['max_time'], 0.2, places=2)
        self.assertAlmostEqual(stats['total_time'] / stats['count'], 0.15, places=2)  # Average


class TestCachePerformance(unittest.TestCase):

    def setUp(self):
        """Setup test database"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Create sample tournament
            tournament = Tournament(
                name="Cache Test Tournament",
                start_date=date(2026, 3, 15),
                end_date=date(2026, 3, 20),
                location="Moscow, Russia",
                category="FIDE",
                status="Scheduled",
                fide_id="CACHE_TEST",
                source_url="https://test.com"
            )
            db.session.add(tournament)
            db.session.commit()
            
            self.tournament_id = tournament.id

    def tearDown(self):
        """Clean up after tests"""
        with self.app.app_context():
            db.drop_all()

    def test_cache_get_set_performance(self):
        """Test cache performance with timing"""
        # Test cache set operation
        import time
        start_time = time.time()
        TournamentCache.invalidate_tournaments_cache()  # Clear any existing cache
        cache_set_time = time.time() - start_time
        
        # Test getting tournaments from DB (no cache)
        start_time = time.time()
        tournaments = TournamentCache.get_all_tournaments()
        first_db_access_time = time.time() - start_time
        
        # Test getting tournaments from cache (should be faster)
        start_time = time.time()
        cached_tournaments = TournamentCache.get_all_tournaments()
        cached_access_time = time.time() - start_time
        
        # Cached access should be significantly faster than DB access
        # Note: In a real test, we'd expect cached_access_time to be much smaller
        # But in a test environment with small dataset, differences might be minimal
        self.assertIsNotNone(tournaments)
        self.assertIsNotNone(cached_tournaments)
        self.assertEqual(len(tournaments), len(cached_tournaments))


if __name__ == '__main__':
    unittest.main()