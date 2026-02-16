"""
API tests for ChessCalendar-RU application
"""
import unittest
import json
from datetime import date
from app import create_app
from app import db
from app.models.tournament import Tournament


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Create a sample tournament for testing
            tournament = Tournament(
                name="Test Tournament",
                start_date=date(2026, 5, 1),
                end_date=date(2026, 5, 10),
                location="Moscow",
                category="FIDE",
                status="Scheduled",
                description="A test tournament",
                organizer="Test Organizer"
            )
            db.session.add(tournament)
            db.session.commit()
    
    def test_get_tournaments(self):
        """Test getting tournaments via API"""
        response = self.client.get('/api/tournaments')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('tournaments', data)
        self.assertIn('pagination', data)
        self.assertGreaterEqual(len(data['tournaments']), 1)
    
    def test_get_tournaments_with_filters(self):
        """Test getting tournaments with filters"""
        response = self.client.get('/api/tournaments?category=FIDE')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('tournaments', data)
        # All returned tournaments should be FIDE category
        for tournament in data['tournaments']:
            if 'category' in tournament:
                self.assertEqual(tournament['category'], 'FIDE')
    
    def test_get_tournament_by_id(self):
        """Test getting a specific tournament by ID"""
        # First get a tournament ID
        response = self.client.get('/api/tournaments')
        data = json.loads(response.data)
        
        if data['tournaments']:
            tournament_id = data['tournaments'][0]['id']
            response = self.client.get(f'/api/tournaments/{tournament_id}')
            self.assertEqual(response.status_code, 200)
            
            tournament_data = json.loads(response.data)
            self.assertIn('id', tournament_data)
            self.assertEqual(tournament_data['id'], tournament_id)
    
    def test_search_tournaments(self):
        """Test searching tournaments"""
        response = self.client.get('/api/tournaments/search?q=Test')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    def test_invalid_tournament_id(self):
        """Test getting a tournament with invalid ID"""
        response = self.client.get('/api/tournaments/999999')
        self.assertEqual(response.status_code, 404)


class TestAppRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def test_homepage(self):
        """Test homepage loads correctly"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Tournament', response.data)  # Check for tournament-related content
    
    def test_calendar_page(self):
        """Test calendar page loads correctly"""
        response = self.client.get('/calendar')
        self.assertEqual(response.status_code, 200)
    
    def test_tournament_detail_page(self):
        """Test tournament detail page"""
        # Create a tournament first
        with self.app.app_context():
            tournament = Tournament(
                name="Detail Test Tournament",
                start_date=date(2026, 6, 1),
                end_date=date(2026, 6, 5),
                location="St. Petersburg",
                category="National",
                status="Scheduled"
            )
            db.session.add(tournament)
            db.session.commit()
            
            # Get the tournament ID
            tournament_id = tournament.id
        
        response = self.client.get(f'/tournament/{tournament_id}')
        self.assertEqual(response.status_code, 200)


class TestAPIPagination(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Create multiple tournaments for pagination testing
            for i in range(25):  # Create 25 tournaments
                tournament = Tournament(
                    name=f"Tournament {i}",
                    start_date=date(2026, 1, 1 + i),
                    end_date=date(2026, 1, 3 + i),
                    location=f"City {i}",
                    category="FIDE" if i % 2 == 0 else "National",
                    status="Scheduled"
                )
                db.session.add(tournament)
            db.session.commit()
    
    def test_pagination(self):
        """Test API pagination"""
        # Test first page
        response = self.client.get('/api/tournaments?page=1&per_page=10')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('tournaments', data)
        self.assertIn('pagination', data)
        self.assertEqual(len(data['tournaments']), 10)  # Should have 10 items per page
        self.assertEqual(data['pagination']['page'], 1)
        self.assertEqual(data['pagination']['pages'], 3)  # 25 items, 10 per page = 3 pages
    
    def test_second_page(self):
        """Test second page of results"""
        response = self.client.get('/api/tournaments?page=2&per_page=10')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['pagination']['page'], 2)
        self.assertEqual(len(data['tournaments']), 10)


if __name__ == '__main__':
    unittest.main()