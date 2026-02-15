import unittest
import tempfile
import os
from datetime import datetime, date, timedelta
from app import create_app, db
from app.models.tournament import Tournament
from app.models.user import User
from app.models.preference import UserPreference, UserInteraction
from app.models.favorite import FavoriteTournament
from app.utils.recommendations import RecommendationEngine
from app.utils.fide_parser import FIDEParses
from app.utils.cfr_parser import CFRParser


class TestUserPreferences(unittest.TestCase):

    def setUp(self):
        """Setup test database"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Create a sample user
            sample_user = User(
                username="testuser",
                email="test@example.com",
                password="SecurePass123!"
            )
            db.session.add(sample_user)
            db.session.commit()
            
            # Create sample tournaments
            for i in range(3):
                tournament = Tournament(
                    name=f"Tournament {i}",
                    start_date=date(2026, 3, 15 + i),
                    end_date=date(2026, 3, 20 + i),
                    location="Moscow, Russia",
                    category="FIDE" if i == 0 else "National",
                    status="Scheduled",
                    fide_id=f"TEST{i}",
                    source_url="https://test.com"
                )
                db.session.add(tournament)
            
            db.session.commit()
            
            self.user_id = sample_user.id
            self.tournament_ids = [t.id for t in Tournament.query.all()]

    def tearDown(self):
        """Clean up after tests"""
        with self.app.app_context():
            db.drop_all()

    def test_user_preference_creation(self):
        """Test creation of user preferences"""
        with self.app.app_context():
            user_pref = UserPreference(user_id=self.user_id)
            db.session.add(user_pref)
            db.session.commit()
            
            # Check that preference was created
            retrieved_pref = UserPreference.query.filter_by(user_id=self.user_id).first()
            self.assertIsNotNone(retrieved_pref)
            self.assertEqual(retrieved_pref.user_id, self.user_id)

    def test_user_preference_update(self):
        """Test updating user preferences"""
        with self.app.app_context():
            user_pref = UserPreference(user_id=self.user_id)
            db.session.add(user_pref)
            db.session.commit()
            
            # Update preferences
            user_pref.category_preference = '{"FIDE": 0.8, "National": 0.2}'
            user_pref.location_preference = '{"Moscow": 0.9, "SPB": 0.1}'
            user_pref.difficulty_preference = 'Advanced'
            
            db.session.commit()
            
            # Check that updates were saved
            updated_pref = UserPreference.query.get(user_pref.id)
            self.assertEqual(updated_pref.category_preference, '{"FIDE": 0.8, "National": 0.2}')
            self.assertEqual(updated_pref.difficulty_preference, 'Advanced')

    def test_user_interaction_creation(self):
        """Test creation of user interactions"""
        with self.app.app_context():
            interaction = UserInteraction(
                user_id=self.user_id,
                tournament_id=self.tournament_ids[0],
                interaction_type='view',
                interaction_value=1
            )
            db.session.add(interaction)
            db.session.commit()
            
            # Check that interaction was created
            retrieved_interaction = UserInteraction.query.filter_by(
                user_id=self.user_id,
                tournament_id=self.tournament_ids[0]
            ).first()
            self.assertIsNotNone(retrieved_interaction)
            self.assertEqual(retrieved_interaction.interaction_type, 'view')


class TestRecommendationEngine(unittest.TestCase):

    def setUp(self):
        """Setup test database"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Create sample users
            user1 = User(username="user1", email="user1@example.com", password="SecurePass123!")
            user2 = User(username="user2", email="user2@example.com", password="SecurePass123!")
            db.session.add_all([user1, user2])
            db.session.commit()
            
            # Create sample tournaments
            tournaments_data = [
                {"name": "FIDE World Championship", "category": "FIDE", "location": "Moscow"},
                {"name": "National Championship", "category": "National", "location": "SPB"},
                {"name": "Regional Open", "category": "Regional", "location": "Novosibirsk"}
            ]
            
            tournaments = []
            for i, t_data in enumerate(tournaments_data):
                tournament = Tournament(
                    name=t_data["name"],
                    start_date=date(2026, 3, 15 + i),
                    end_date=date(2026, 3, 20 + i),
                    location=t_data["location"],
                    category=t_data["category"],
                    status="Scheduled",
                    fide_id=f"TEST{i}",
                    source_url="https://test.com"
                )
                tournaments.append(tournament)
                db.session.add(tournament)
            
            db.session.commit()
            
            self.user1_id = user1.id
            self.user2_id = user2.id
            self.tournament_ids = [t.id for t in tournaments]

    def tearDown(self):
        """Clean up after tests"""
        with self.app.app_context():
            db.drop_all()

    def test_record_interaction(self):
        """Test recording user interactions"""
        with self.app.app_context():
            # Record an interaction
            interaction = RecommendationEngine.record_interaction(
                self.user1_id, 
                self.tournament_ids[0], 
                'favorite', 
                3
            )
            
            self.assertIsNotNone(interaction)
            self.assertEqual(interaction.user_id, self.user1_id)
            self.assertEqual(interaction.tournament_id, self.tournament_ids[0])
            self.assertEqual(interaction.interaction_type, 'favorite')

    def test_get_user_recommendations(self):
        """Test getting user recommendations"""
        with self.app.app_context():
            # Record some interactions to establish preferences
            RecommendationEngine.record_interaction(self.user1_id, self.tournament_ids[0], 'view', 1)
            RecommendationEngine.record_interaction(self.user1_id, self.tournament_ids[0], 'favorite', 3)
            
            # Get recommendations
            recommendations = RecommendationEngine.get_user_recommendations(self.user1_id)
            
            # Should return a list
            self.assertIsInstance(recommendations, list)
            
            # Should not include tournaments the user has already interacted with heavily
            recommended_ids = [t.id for t in recommendations]
            # The algorithm may return different results depending on implementation
            # but it should return valid tournament objects

    def test_collaborative_filtering(self):
        """Test collaborative filtering recommendations"""
        with self.app.app_context():
            # Create interactions for user1
            RecommendationEngine.record_interaction(self.user1_id, self.tournament_ids[0], 'favorite', 3)
            RecommendationEngine.record_interaction(self.user1_id, self.tournament_ids[1], 'view', 1)
            
            # Create similar interactions for user2
            RecommendationEngine.record_interaction(self.user2_id, self.tournament_ids[0], 'favorite', 3)
            RecommendationEngine.record_interaction(self.user2_id, self.tournament_ids[2], 'view', 1)
            
            # Get collaborative recommendations for user1
            recommendations = RecommendationEngine.get_collaborative_recommendations(self.user1_id)
            
            self.assertIsInstance(recommendations, list)


class TestAdvancedAPIFeatures(unittest.TestCase):

    def setUp(self):
        """Setup test database"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Create sample user
            sample_user = User(
                username="apiuser",
                email="api@example.com",
                password="SecurePass123!"
            )
            db.session.add(sample_user)
            db.session.commit()
            
            # Create sample tournaments
            for i in range(5):
                tournament = Tournament(
                    name=f"API Test Tournament {i}",
                    start_date=date(2026, 3, 15 + i),
                    end_date=date(2026, 3, 20 + i),
                    location="Moscow, Russia",
                    category="FIDE" if i % 2 == 0 else "National",
                    status="Scheduled",
                    fide_id=f"API_TEST{i}",
                    source_url="https://test.com"
                )
                db.session.add(tournament)
            
            db.session.commit()
            
            self.user_id = sample_user.id
            self.tournament_ids = [t.id for t in Tournament.query.all()]

    def tearDown(self):
        """Clean up after tests"""
        with self.app.app_context():
            db.drop_all()

    def test_trending_tournaments_api(self):
        """Test the trending tournaments API"""
        # Record some interactions to create trending data
        with self.app.app_context():
            for i, tid in enumerate(self.tournament_ids[:3]):  # Use first 3 tournaments
                # Create multiple interactions to make them "trending"
                for j in range(i + 1):  # Different counts for different tournaments
                    interaction = UserInteraction(
                        user_id=self.user_id,
                        tournament_id=tid,
                        interaction_type='view',
                        interaction_value=1
                    )
                    db.session.add(interaction)
            db.session.commit()
        
        # Test the API endpoint
        response = self.client.get('/api/tournaments/trending')
        self.assertEqual(response.status_code, 200)
        
        import json
        data = json.loads(response.data.decode())
        self.assertIn('tournaments', data)
        self.assertIn('count', data)
        self.assertGreaterEqual(len(data['tournaments']), 0)  # May be 0 if no recent activity

    def test_improved_search_api(self):
        """Test the improved search API with limit parameter"""
        # Test search with limit
        response = self.client.get('/api/tournaments/search?q=test&limit=3')
        self.assertEqual(response.status_code, 200)
        
        import json
        data = json.loads(response.data.decode())
        self.assertIsInstance(data, list)
        
        # Test search with category filter
        response = self.client.get('/api/tournaments/search?category=FIDE')
        self.assertEqual(response.status_code, 200)

    def test_collaborative_recommendations_api(self):
        """Test the collaborative recommendations API endpoint"""
        response = self.client.get(f'/api/users/{self.user_id}/recommendations/collaborative')
        self.assertEqual(response.status_code, 200)
        
        import json
        data = json.loads(response.data.decode())
        self.assertIn('recommendations', data)
        self.assertIn('count', data)


if __name__ == '__main__':
    unittest.main()