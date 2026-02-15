import unittest
from datetime import date, datetime
from app import create_app, db
from app.models.tournament import Tournament
from app.models.user import User
from app.models.rating import TournamentRating
from app.models.favorite import FavoriteTournament
from app.models.notification import Notification, Subscription, NotificationType

class TestModels(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Tear down test fixtures after each test method."""
        with self.app.app_context():
            db.drop_all()
    
    def test_tournament_model(self):
        """Test Tournament model creation and validation."""
        tournament = Tournament(
            name="Test Tournament",
            start_date=date(2026, 12, 1),
            end_date=date(2026, 12, 3),
            location="Moscow",
            category="FIDE",
            status="Scheduled"
        )
        
        self.assertEqual(tournament.name, "Test Tournament")
        self.assertEqual(tournament.location, "Moscow")
        self.assertEqual(tournament.category, "FIDE")
        self.assertEqual(tournament.status, "Scheduled")
        self.assertEqual(tournament.start_date, date(2026, 12, 1))
        self.assertEqual(tournament.end_date, date(2026, 12, 3))
        
        # Test validation
        errors = tournament.validate()
        self.assertEqual(errors, [])
    
    def test_tournament_validation(self):
        """Test tournament validation with invalid data."""
        tournament = Tournament(
            name="",  # Invalid: empty name
            start_date=None,  # Invalid: no start date
            end_date=date(2026, 12, 3),
            location="",  # Invalid: empty location
            category="FIDE",
            status="Scheduled"
        )
        
        errors = tournament.validate()
        self.assertIn("Название турнира не может быть пустым", errors)
        self.assertIn("Дата начала обязательна", errors)
        self.assertIn("Место проведения не может быть пустым", errors)
    
    def test_user_model(self):
        """Test User model creation and validation."""
        user = User(
            username="testuser",
            email="test@example.com",
            password="securepassword123"
        )
        
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("securepassword123"))
        self.assertFalse(user.check_password("wrongpassword"))
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_regular_user)
        self.assertIsNotNone(user.api_key)
        
        # Test validation
        errors = user.validate()
        self.assertEqual(errors, [])
    
    def test_user_validation(self):
        """Test user validation with invalid data."""
        user = User(
            username="",  # Invalid: empty username
            email="invalid-email",  # Invalid: invalid email format
            password="password123"
        )
        
        # We need to set the password manually since the constructor validates it
        user.username = ""
        user.email = "invalid-email"
        
        errors = user.validate()
        self.assertIn("Имя пользователя не может быть пустым", errors)
        self.assertIn("Недопустимый формат email", errors)
    
    def test_tournament_rating_model(self):
        """Test TournamentRating model."""
        # First create a tournament and user
        tournament = Tournament(
            name="Test Tournament",
            start_date=date(2026, 12, 1),
            end_date=date(2026, 12, 3),
            location="Moscow",
            category="FIDE",
            status="Scheduled"
        )
        
        user = User(
            username="testuser",
            email="test@example.com",
            password="securepassword123"
        )
        
        with self.app.app_context():
            db.session.add(tournament)
            db.session.add(user)
            db.session.commit()
            
            rating = TournamentRating(
                user_id=user.id,
                tournament_id=tournament.id,
                rating=5,
                review="Excellent tournament!"
            )
            
            db.session.add(rating)
            db.session.commit()
            
            # Retrieve the rating to verify it was saved
            saved_rating = TournamentRating.query.first()
            self.assertEqual(saved_rating.rating, 5)
            self.assertEqual(saved_rating.review, "Excellent tournament!")
            self.assertEqual(saved_rating.user_id, user.id)
            self.assertEqual(saved_rating.tournament_id, tournament.id)
    
    def test_tournament_rating_validation(self):
        """Test TournamentRating validation."""
        rating = TournamentRating(
            user_id=1,
            tournament_id=1,
            rating=6,  # Invalid: rating too high
            review="Test review"
        )
        
        errors = rating.validate()
        self.assertIn("Рейтинг должен быть от 1 до 5", errors)
    
    def test_favorite_tournament_model(self):
        """Test FavoriteTournament model."""
        # Create tournament and user
        tournament = Tournament(
            name="Test Tournament",
            start_date=date(2026, 12, 1),
            end_date=date(2026, 12, 3),
            location="Moscow",
            category="FIDE",
            status="Scheduled"
        )
        
        user = User(
            username="testuser",
            email="test@example.com",
            password="securepassword123"
        )
        
        with self.app.app_context():
            db.session.add(tournament)
            db.session.add(user)
            db.session.commit()
            
            favorite = FavoriteTournament(
                user_id=user.id,
                tournament_id=tournament.id
            )
            
            db.session.add(favorite)
            db.session.commit()
            
            # Verify the favorite was saved
            saved_favorite = FavoriteTournament.query.first()
            self.assertEqual(saved_favorite.user_id, user.id)
            self.assertEqual(saved_favorite.tournament_id, tournament.id)
    
    def test_notification_model(self):
        """Test Notification model."""
        # Create a tournament first
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
            
            notification = Notification(
                title="Test Notification",
                message="Test message",
                type=NotificationType.NEW_TOURNAMENT,
                recipient_email="test@example.com",
                tournament_id=tournament.id
            )
            
            db.session.add(notification)
            db.session.commit()
            
            # Verify the notification was saved
            saved_notification = Notification.query.first()
            self.assertEqual(saved_notification.title, "Test Notification")
            self.assertEqual(saved_notification.message, "Test message")
            self.assertEqual(saved_notification.type, NotificationType.NEW_TOURNAMENT)
            self.assertEqual(saved_notification.recipient_email, "test@example.com")
            self.assertEqual(saved_notification.tournament_id, tournament.id)
    
    def test_subscription_model(self):
        """Test Subscription model."""
        subscription = Subscription(
            email="test@example.com",
            preferences={
                'new_tournaments': True,
                'tournament_updates': True,
                'reminders': True
            }
        )
        
        self.assertEqual(subscription.email, "test@example.com")
        self.assertTrue(subscription.preferences['new_tournaments'])
        self.assertTrue(subscription.active)


if __name__ == '__main__':
    unittest.main()