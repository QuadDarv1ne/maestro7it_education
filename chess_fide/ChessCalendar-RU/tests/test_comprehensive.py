import unittest
import tempfile
import os
from datetime import datetime, date
from app import create_app, db
from app.models.tournament import Tournament
from app.models.user import User
from app.utils.fide_parser import FIDEParses
from app.utils.cfr_parser import CFRParser
from app.utils.updater import updater


class TestComprehensive(unittest.TestCase):
    
    def setUp(self):
        """Setup test database"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Create a sample tournament for testing
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
            
            # Store the ID to use later
            self.sample_tournament_id = sample_tournament.id
    
    def tearDown(self):
        """Clean up after tests"""
        with self.app.app_context():
            db.drop_all()
    
    def test_app_creation(self):
        """Test that app is created successfully"""
        self.assertIsNotNone(self.app)
    
    def test_database_operations(self):
        """Test basic database operations"""
        with self.app.app_context():
            # Test reading from database
            tournament = Tournament.query.first()
            self.assertEqual(tournament.name, "Test Tournament")
            self.assertEqual(tournament.location, "Moscow, Russia")
            
            # Test creating new tournament
            new_tournament = Tournament(
                name="New Test Tournament",
                start_date=date(2026, 4, 1),
                end_date=date(2026, 4, 5),
                location="St. Petersburg, Russia",
                category="National",
                status="Scheduled"
            )
            db.session.add(new_tournament)
            db.session.commit()
            
            # Verify it was added
            tournaments = Tournament.query.all()
            self.assertEqual(len(tournaments), 2)
    
    def test_tournament_model_validation(self):
        """Test tournament model validation"""
        with self.app.app_context():
            # Test valid tournament
            valid_tournament = Tournament(
                name="Valid Tournament",
                start_date=date(2026, 5, 1),
                end_date=date(2026, 5, 5),
                location="Test Location",
                category="National",
                status="Scheduled"
            )
            
            validation_errors = valid_tournament.validate()
            self.assertEqual(len(validation_errors), 0)
            
            # Test invalid tournament (end date before start date)
            invalid_tournament = Tournament(
                name="Invalid Tournament",
                start_date=date(2026, 5, 10),
                end_date=date(2026, 5, 5),  # End date before start date
                location="Test Location",
                category="National",
                status="Scheduled"
            )
            
            validation_errors = invalid_tournament.validate()
            self.assertIn("Дата начала не может быть позже даты окончания", validation_errors)
    
    def test_user_model(self):
        """Test user model functionality"""
        with self.app.app_context():
            # Create a test user
            user = User(username="testuser", email="test@example.com", password="SecurePass123!")
            db.session.add(user)
            db.session.commit()
            
            # Verify user was created
            retrieved_user = User.query.filter_by(username="testuser").first()
            self.assertIsNotNone(retrieved_user)
            self.assertTrue(retrieved_user.check_password("SecurePass123!"))
            self.assertFalse(retrieved_user.check_password("wrongpassword"))
            self.assertIsNotNone(retrieved_user.api_key)
    
    def test_main_routes(self):
        """Test main application routes"""
        # Test home page
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Test tournament detail page (should return 404 for non-existent tournament)
        response = self.client.get('/tournament/999')
        self.assertEqual(response.status_code, 404)
        
        # Test existing tournament detail page
        with self.app.app_context():
            response = self.client.get(f'/tournament/{self.sample_tournament_id}')
            self.assertEqual(response.status_code, 200)
    
    def test_api_routes(self):
        """Test API routes"""
        # Test tournaments API
        response = self.client.get('/api/tournaments')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'application/json', response.content_type.encode())
        
        # Test specific tournament API
        with self.app.app_context():
            response = self.client.get(f'/api/tournaments/{self.sample_tournament_id}')
            self.assertEqual(response.status_code, 200)
    
    def test_parser_initialization(self):
        """Test parser initialization"""
        fide_parser = FIDEParses()
        cfr_parser = CFRParser()
        
        self.assertIsNotNone(fide_parser)
        self.assertIsNotNone(cfr_parser)
        self.assertEqual(fide_parser.base_url, "https://calendar.fide.com")
        self.assertEqual(cfr_parser.base_url, "https://ruchess.ru")
    
    def test_updater_functionality(self):
        """Test updater functionality"""
        # Just test that updater object exists and has required methods
        self.assertIsNotNone(updater)
        self.assertTrue(hasattr(updater, 'update_all_sources'))
        self.assertTrue(hasattr(updater, '_update_from_fide'))
        self.assertTrue(hasattr(updater, '_update_from_cfr'))
        self.assertTrue(hasattr(updater, 'start_scheduler'))


class TestModelMethods(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.drop_all()
    
    def test_tournament_to_dict(self):
        """Test tournament to_dict method"""
        with self.app.app_context():
            tournament = Tournament(
                name="Test Tournament",
                start_date=date(2026, 3, 15),
                end_date=date(2026, 3, 20),
                location="Moscow, Russia",
                category="FIDE",
                status="Scheduled",
                fide_id="TEST123",
                source_url="https://test.com"
            )
            
            tournament_dict = tournament.to_dict()
            
            self.assertEqual(tournament_dict['name'], "Test Tournament")
            self.assertEqual(tournament_dict['location'], "Moscow, Russia")
            self.assertEqual(tournament_dict['category'], "FIDE")
            self.assertEqual(tournament_dict['status'], "Scheduled")


if __name__ == '__main__':
    unittest.main()