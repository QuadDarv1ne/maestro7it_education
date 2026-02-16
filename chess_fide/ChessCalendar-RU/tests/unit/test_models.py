"""
Unit tests for models
"""
import pytest
from datetime import datetime, timedelta
from app.models.tournament import Tournament
from app.models.user import User


class TestTournamentModel:
    """Tests for Tournament model"""
    
    def test_create_tournament(self, db_session):
        """Test creating a tournament"""
        tournament = Tournament(
            name='Test Tournament',
            start_date=datetime.now().date(),
            end_date=(datetime.now() + timedelta(days=3)).date(),
            location='Moscow',
            category='National',
            status='Scheduled'
        )
        db_session.session.add(tournament)
        db_session.session.commit()
        
        assert tournament.id is not None
        assert tournament.name == 'Test Tournament'
        assert tournament.location == 'Moscow'
        assert tournament.category == 'National'
        assert tournament.status == 'Scheduled'
    
    def test_tournament_validation(self, db_session):
        """Test tournament validation"""
        tournament = Tournament(
            name='Test',
            start_date=datetime.now().date(),
            end_date=(datetime.now() - timedelta(days=1)).date(),  # Invalid: end before start
            location='Moscow',
            category='National',
            status='Scheduled'
        )
        
        errors = tournament.validate()
        assert len(errors) > 0
        assert any('end_date' in error.lower() for error in errors)
    
    def test_tournament_to_dict(self, sample_tournament):
        """Test tournament serialization"""
        data = sample_tournament.to_dict()
        
        assert isinstance(data, dict)
        assert data['name'] == 'Test Tournament'
        assert data['location'] == 'Moscow'
        assert 'id' in data
        assert 'start_date' in data
        assert 'end_date' in data
    
    def test_tournament_status_update(self, sample_tournament, db_session):
        """Test updating tournament status"""
        sample_tournament.status = 'Ongoing'
        db_session.session.commit()
        
        assert sample_tournament.status == 'Ongoing'


class TestUserModel:
    """Tests for User model"""
    
    def test_create_user(self, db_session):
        """Test creating a user"""
        user = User(
            username='testuser',
            email='test@example.com',
            password='password123',
            is_admin=False
        )
        db_session.session.add(user)
        db_session.session.commit()
        
        assert user.id is not None
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.is_admin is False
    
    def test_password_hashing(self, db_session):
        """Test password hashing"""
        user = User(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        
        # Password should be hashed
        assert user.password_hash != 'password123'
        
        # Check password should work
        assert user.check_password('password123')
        assert not user.check_password('wrongpassword')
    
    def test_user_unique_constraints(self, db_session, sample_user):
        """Test unique constraints on username and email"""
        # Try to create user with same username
        duplicate_user = User(
            username='testuser',  # Same as sample_user
            email='different@example.com',
            password='password123'
        )
        db_session.session.add(duplicate_user)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.session.commit()
    
    def test_user_to_dict(self, sample_user):
        """Test user serialization"""
        data = sample_user.to_dict()
        
        assert isinstance(data, dict)
        assert data['username'] == 'testuser'
        assert data['email'] == 'test@example.com'
        assert 'password_hash' not in data  # Should not expose password
        assert 'id' in data
    
    def test_admin_user(self, admin_user):
        """Test admin user"""
        assert admin_user.is_admin is True
        assert admin_user.username == 'admin'
