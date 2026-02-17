import unittest
from unittest.mock import patch, MagicMock
from app import create_app, db
from app.models.tournament import Tournament
from app.utils.unified_cache import UnifiedCache, TournamentCache, cached
from datetime import date

class TestCache(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Tear down test fixtures after each test method."""
        with self.app.app_context():
            db.drop_all()
    
    def test_cache_service_initialization(self):
        """Test CacheService initialization."""
        with patch('redis.Redis.ping', return_value=None):
            cache_service = CacheService(host='localhost', port=6379, db=0)
            self.assertTrue(cache_service.use_redis)
    
    def test_cache_service_fallback(self):
        """Test CacheService fallback to in-memory when Redis is unavailable."""
        with patch('redis.Redis.ping', side_effect=Exception()):
            cache_service = CacheService(host='localhost', port=6379, db=0)
            self.assertFalse(cache_service.use_redis)
            self.assertEqual(cache_service.cache, {})
    
    def test_cache_set_get(self):
        """Test setting and getting values from cache."""
        with patch('redis.Redis.ping', side_effect=Exception()):  # Force in-memory cache
            cache_service = CacheService()
            
            # Test set and get
            cache_service.set('test_key', 'test_value', timeout=300)
            result = cache_service.get('test_key')
            self.assertEqual(result, 'test_value')
            
            # Test getting non-existent key
            result = cache_service.get('non_existent_key')
            self.assertIsNone(result)
    
    def test_cache_decorator(self):
        """Test the cached decorator functionality."""
        call_count = 0
        
        @cached(timeout=300, key_prefix='test_cache')
        def test_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        # Call function twice with same argument - should only execute once due to caching
        result1 = test_function(5)
        result2 = test_function(5)
        
        self.assertEqual(result1, 10)
        self.assertEqual(result2, 10)
        self.assertEqual(call_count, 1)  # Function should only be called once due to caching
        
        # Call with different argument - should execute again
        result3 = test_function(10)
        self.assertEqual(result3, 20)
        self.assertEqual(call_count, 2)  # Should now be 2 calls total
    
    def test_tournament_cache_functions(self):
        """Test TournamentCache functions."""
        # Create a tournament in the database
        tournament = Tournament(
            name="Test Tournament",
            start_date=date(2026, 12, 1),
            end_date=date(2026, 12, 3),
            location="Moscow",
            category="FIDE",
            status="Scheduled"
        )
        
        with self.app.app_context():
            db.session.add(tournament)
            db.session.commit()
            
            # Test get_tournament_by_id
            cached_tournament = TournamentCache.get_tournament_by_id(tournament.id)
            self.assertIsNotNone(cached_tournament)
            self.assertEqual(cached_tournament.name, "Test Tournament")
            
            # Test get_all_tournaments
            all_tournaments = TournamentCache.get_all_tournaments()
            self.assertEqual(len(all_tournaments), 1)
            self.assertEqual(all_tournaments[0].name, "Test Tournament")
    
    def test_tournament_cache_invalidation(self):
        """Test TournamentCache invalidation functions."""
        with patch('redis.Redis.ping', side_effect=Exception()):  # Force in-memory cache
            # Add a tournament
            tournament = Tournament(
                name="Test Tournament",
                start_date=date(2026, 12, 1),
                end_date=date(2026, 12, 3),
                location="Moscow",
                category="FIDE",
                status="Scheduled"
            )
            
            with self.app.app_context():
                db.session.add(tournament)
                db.session.commit()
                
                # Get tournament to populate cache
                cached_tournament = TournamentCache.get_tournament_by_id(tournament.id)
                self.assertIsNotNone(cached_tournament)
                
                # Invalidate the cache
                TournamentCache.invalidate_tournaments_cache()
                
                # The cache should be cleared for tournament-related entries


class TestCacheWithRedis(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Tear down test fixtures after each test method."""
        with self.app.app_context():
            db.drop_all()
    
    @patch('redis.Redis')
    def test_redis_cache_operations(self, mock_redis_class):
        """Test Redis cache operations."""
        mock_redis_instance = MagicMock()
        mock_redis_class.return_value = mock_redis_instance
        mock_redis_instance.ping.return_value = True
        
        cache_service = CacheService()
        self.assertTrue(cache_service.use_redis)
        
        # Mock the serialization/deserialization
        import pickle
        mock_redis_instance.get.return_value = pickle.dumps('test_value')
        
        # Test get
        result = cache_service.get('test_key')
        self.assertEqual(result, 'test_value')
        
        # Test set
        cache_service.set('test_key', 'test_value')
        mock_redis_instance.setex.assert_called_once()


if __name__ == '__main__':
    unittest.main()