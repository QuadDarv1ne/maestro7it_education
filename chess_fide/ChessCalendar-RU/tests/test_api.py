import unittest
import json
from datetime import date
from app import create_app, db
from app.models.tournament import Tournament
from app.models.user import User

class TestAPI(unittest.TestCase):
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
    
    def test_get_tournaments(self):
        """Test GET /api/tournaments endpoint."""
        # Create test tournaments
        tournament1 = Tournament(
            name="Test Tournament 1",
            start_date=date(2026, 12, 1),
            end_date=date(2026, 12, 3),
            location="Moscow",
            category="FIDE",
            status="Scheduled"
        )
        
        tournament2 = Tournament(
            name="Test Tournament 2",
            start_date=date(2026, 12, 5),
            end_date=date(2026, 12, 7),
            location="St. Petersburg",
            category="National",
            status="Scheduled"
        )
        
        with self.app.app_context():
            db.session.add(tournament1)
            db.session.add(tournament2)
            db.session.commit()
        
        # Make request
        response = self.client.get('/api/tournaments')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(len(data['tournaments']), 2)
        self.assertEqual(data['pagination']['total'], 2)
    
    def test_get_tournaments_with_filters(self):
        """Test GET /api/tournaments with filters."""
        # Create test tournaments
        tournament1 = Tournament(
            name="FIDE Tournament",
            start_date=date(2026, 12, 1),
            end_date=date(2026, 12, 3),
            location="Moscow",
            category="FIDE",
            status="Scheduled"
        )
        
        tournament2 = Tournament(
            name="National Tournament",
            start_date=date(2026, 12, 5),
            end_date=date(2026, 12, 7),
            location="St. Petersburg",
            category="National",
            status="Scheduled"
        )
        
        with self.app.app_context():
            db.session.add(tournament1)
            db.session.add(tournament2)
            db.session.commit()
        
        # Test category filter
        response = self.client.get('/api/tournaments?category=FIDE')
        data = json.loads(response.data)
        self.assertEqual(len(data['tournaments']), 1)
        self.assertEqual(data['tournaments'][0]['category'], 'FIDE')
    
    def test_get_tournament_by_id(self):
        """Test GET /api/tournaments/<id> endpoint."""
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
            tournament_id = tournament.id
        
        # Make request
        response = self.client.get(f'/api/tournaments/{tournament_id}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Test Tournament')
        self.assertEqual(data['location'], 'Moscow')
        self.assertEqual(data['category'], 'FIDE')
    
    def test_get_nonexistent_tournament(self):
        """Test GET /api/tournaments/<id> for nonexistent tournament."""
        response = self.client.get('/api/tournaments/999')
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_get_upcoming_tournaments(self):
        """Test GET /api/tournaments/upcoming endpoint."""
        # Create tournaments
        past_tournament = Tournament(
            name="Past Tournament",
            start_date=date(2020, 1, 1),
            end_date=date(2020, 1, 3),
            location="Past City",
            category="FIDE",
            status="Completed"
        )
        
        future_tournament = Tournament(
            name="Future Tournament",
            start_date=date(2026, 12, 1),
            end_date=date(2026, 12, 3),
            location="Future City",
            category="FIDE",
            status="Scheduled"
        )
        
        with self.app.app_context():
            db.session.add(past_tournament)
            db.session.add(future_tournament)
            db.session.commit()
        
        # Request upcoming tournaments
        response = self.client.get('/api/tournaments/upcoming')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(len(data['tournaments']), 1)
        self.assertEqual(data['tournaments'][0]['name'], 'Future Tournament')
    
    def test_register_user(self):
        """Test POST /api/users/register endpoint."""
        # Register a new user
        response = self.client.post('/api/users/register', 
                                  data=json.dumps({
                                      'username': 'testuser',
                                      'email': 'test@example.com',
                                      'password': 'SecurePass123!'
                                  }),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'User registered successfully')
        self.assertEqual(data['user']['username'], 'testuser')
        self.assertEqual(data['user']['email'], 'test@example.com')
    
    def test_register_user_duplicate(self):
        """Test POST /api/users/register with duplicate username/email."""
        # Create a user first
        user = User(
            username='testuser',
            email='test@example.com',
            password='SecurePass123!'
        )
        
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()
        
        # Try to register the same user again
        response = self.client.post('/api/users/register',
                                  data=json.dumps({
                                      'username': 'testuser',
                                      'email': 'different@example.com',
                                      'password': 'SecurePass123!'
                                  }),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 409)  # Conflict
        
        response = self.client.post('/api/users/register',
                                  data=json.dumps({
                                      'username': 'differentuser',
                                      'email': 'test@example.com',
                                      'password': 'SecurePass123!'
                                  }),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 409)  # Conflict
    
    def test_login_user(self):
        """Test POST /api/users/login endpoint."""
        # Create a user first
        user = User(
            username='testuser',
            email='test@example.com',
            password='SecurePass123!'
        )
        
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()
        
        # Try to login
        response = self.client.post('/api/users/login',
                                  data=json.dumps({
                                      'username': 'testuser',
                                      'password': 'SecurePass123!'
                                  }),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Login successful')
        self.assertEqual(data['user']['username'], 'testuser')
    
    def test_login_user_invalid_credentials(self):
        """Test POST /api/users/login with invalid credentials."""
        response = self.client.post('/api/users/login',
                                  data=json.dumps({
                                      'username': 'nonexistent',
                                      'password': 'wrongpassword'
                                  }),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 401)  # Unauthorized
    
    def test_health_check(self):
        """Test GET /api/health endpoint."""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)
        self.assertIn('service', data)


if __name__ == '__main__':
    unittest.main()