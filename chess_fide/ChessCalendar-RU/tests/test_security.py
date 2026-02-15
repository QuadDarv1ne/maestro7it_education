import unittest
import tempfile
import os
from datetime import datetime, date, timedelta
from app import create_app, db
from app.models.tournament import Tournament
from app.models.user import User
from app.models.preference import UserInteraction
from app.utils.fide_parser import FIDEParses
from app.utils.cfr_parser import CFRParser
from app.utils.updater import updater


class TestSecurity(unittest.TestCase):

    def setUp(self):
        """Setup test database"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Create a sample user for testing
            sample_user = User(
                username="testuser",
                email="test@example.com",
                password="SecurePass123!"
            )
            db.session.add(sample_user)
            db.session.commit()
            
            # Store the user ID to use later
            self.sample_user_id = sample_user.id

    def tearDown(self):
        """Clean up after tests"""
        with self.app.app_context():
            db.drop_all()

    def test_password_strength_validation(self):
        """Test that passwords must meet security requirements"""
        with self.app.app_context():
            # Test weak password (too short)
            user = User(username="weakuser", email="weak@example.com", password="123")
            with self.assertRaises(ValueError):
                user.set_password("123")
            
            # Test weak password (no uppercase)
            with self.assertRaises(ValueError):
                user.set_password("password123!")
            
            # Test weak password (no lowercase)
            with self.assertRaises(ValueError):
                user.set_password("PASSWORD123!")
            
            # Test weak password (no digit)
            with self.assertRaises(ValueError):
                user.set_password("Password!")
            
            # Test weak password (no special char)
            with self.assertRaises(ValueError):
                user.set_password("Password123")
            
            # Test strong password (should pass)
            try:
                user.set_password("SecurePass123!")
                self.assertTrue(True)  # If we reach here, validation passed
            except ValueError:
                self.fail("Strong password was rejected")

    def test_account_lockout(self):
        """Test account lockout after failed login attempts"""
        with self.app.app_context():
            user = User.query.get(self.sample_user_id)
            
            # Simulate 5 failed login attempts
            for i in range(5):
                is_valid = user.check_password("wrongpassword")
                self.assertFalse(is_valid)
                self.assertEqual(user.failed_login_attempts, i + 1)
            
            # After 5 failed attempts, account should be locked
            self.assertTrue(user.is_locked())
            
            # Even with correct password, login should fail when locked
            is_valid = user.check_password("SecurePass123!")
            self.assertFalse(is_valid)

    def test_account_unlock_after_timeout(self):
        """Test that accounts unlock after the timeout period"""
        with self.app.app_context():
            # Create another user for this test
            user = User(username="tempuser", email="temp@example.com", password="SecurePass123!")
            db.session.add(user)
            db.session.commit()
            
            # Fail login 5 times to lock the account
            for i in range(5):
                user.check_password("wrongpassword")
            
            # Manually set locked_until to past time to simulate timeout
            user.locked_until = datetime.utcnow() - timedelta(minutes=1)
            db.session.commit()
            
            # Account should now be unlocked
            self.assertFalse(user.is_locked())

    def test_successful_login_resets_attempts(self):
        """Test that successful login resets failed attempts counter"""
        with self.app.app_context():
            user = User(username="resetuser", email="reset@example.com", password="SecurePass123!")
            db.session.add(user)
            db.session.commit()
            
            # Fail login twice
            user.check_password("wrongpassword")
            user.check_password("wrongpassword")
            
            # Should have 2 failed attempts
            self.assertEqual(user.failed_login_attempts, 2)
            
            # Successful login should reset counter
            is_valid = user.check_password("SecurePass123!")
            self.assertTrue(is_valid)
            self.assertEqual(user.failed_login_attempts, 0)


class TestAPIEndpointsSecurity(unittest.TestCase):

    def setUp(self):
        """Setup test database"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Create a sample user for testing
            sample_user = User(
                username="apiuser",
                email="api@example.com",
                password="SecurePass123!"
            )
            db.session.add(sample_user)
            db.session.commit()
            
            # Create a sample tournament
            sample_tournament = Tournament(
                name="Test Tournament",
                start_date=date(2026, 3, 15),
                end_date=date(2026, 3, 20),
                location="Moscow, Russia",
                category="FIDE",
                status="Scheduled",
                fide_id="TEST123",
                source_url="https://test.com"
            )
            db.session.add(sample_tournament)
            db.session.commit()
            
            # Store IDs
            self.sample_user_id = sample_user.id
            self.sample_tournament_id = sample_tournament.id

    def tearDown(self):
        """Clean up after tests"""
        with self.app.app_context():
            db.drop_all()

    def test_user_preferences_api(self):
        """Test user preferences API endpoints"""
        # Test getting user preferences
        response = self.client.get(f'/api/users/{self.sample_user_id}/preferences')
        self.assertEqual(response.status_code, 200)
        
        # Test updating user preferences
        response = self.client.post(
            f'/api/users/{self.sample_user_id}/preferences',
            json={
                'category_preference': '{"FIDE": 0.8, "National": 0.2}',
                'location_preference': '{"Moscow": 0.9, "SPB": 0.1}',
                'difficulty_preference': 'Advanced'
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_user_interactions_api(self):
        """Test user interactions API endpoints"""
        # Test recording a user interaction
        response = self.client.post(
            f'/api/users/{self.sample_user_id}/interactions',
            json={
                'tournament_id': self.sample_tournament_id,
                'interaction_type': 'view',
                'interaction_value': 1
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_trending_tournaments_api(self):
        """Test trending tournaments API endpoint"""
        response = self.client.get('/api/tournaments/trending')
        self.assertEqual(response.status_code, 200)
        
        # Check that response is valid JSON
        import json
        data = json.loads(response.data.decode())
        self.assertIn('tournaments', data)
        self.assertIn('count', data)

    def test_performance_metrics_api(self):
        """Test performance metrics API endpoint"""
        response = self.client.get('/api/metrics/performance')
        self.assertEqual(response.status_code, 200)
        
        # Check that response is valid JSON
        import json
        data = json.loads(response.data.decode())
        self.assertIn('summary', data)
        self.assertIn('slow_endpoints', data)
        self.assertIn('recent_requests_count', data)


if __name__ == '__main__':
    unittest.main()