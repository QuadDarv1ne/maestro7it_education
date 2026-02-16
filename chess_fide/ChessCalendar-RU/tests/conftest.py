"""
Pytest configuration and fixtures
"""
import pytest
import os
import sys
from datetime import datetime, timedelta

# Add app to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.tournament import Tournament
from app.models.user import User
from app.models.notification import Notification


@pytest.fixture(scope='session')
def app():
    """Create application for testing"""
    os.environ['TESTING'] = 'True'
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    os.environ['SECRET_KEY'] = 'test-secret-key'
    os.environ['REDIS_URL'] = 'redis://localhost:6379/15'  # Test DB
    
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    return app


@pytest.fixture(scope='function')
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture(scope='function')
def db_session(app):
    """Create database session for testing"""
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


@pytest.fixture
def sample_tournament(db_session):
    """Create sample tournament"""
    tournament = Tournament(
        name='Test Tournament',
        start_date=datetime.now().date(),
        end_date=(datetime.now() + timedelta(days=3)).date(),
        location='Moscow',
        category='National',
        status='Scheduled',
        description='Test tournament description',
        organizer='Test Organizer'
    )
    db_session.session.add(tournament)
    db_session.session.commit()
    return tournament


@pytest.fixture
def sample_user(db_session):
    """Create sample user"""
    user = User(
        username='testuser',
        email='test@example.com',
        password='testpassword123',
        is_admin=False
    )
    db_session.session.add(user)
    db_session.session.commit()
    return user


@pytest.fixture
def admin_user(db_session):
    """Create admin user"""
    admin = User(
        username='admin',
        email='admin@example.com',
        password='adminpassword123',
        is_admin=True
    )
    db_session.session.add(admin)
    db_session.session.commit()
    return admin


@pytest.fixture
def auth_headers(client, admin_user):
    """Get JWT auth headers"""
    response = client.post('/auth/login', json={
        'username': 'admin',
        'password': 'adminpassword123'
    })
    
    if response.status_code == 200:
        token = response.json.get('token')
        return {'Authorization': f'Bearer {token}'}
    return {}


@pytest.fixture
def multiple_tournaments(db_session):
    """Create multiple tournaments"""
    tournaments = []
    for i in range(5):
        tournament = Tournament(
            name=f'Tournament {i+1}',
            start_date=(datetime.now() + timedelta(days=i)).date(),
            end_date=(datetime.now() + timedelta(days=i+2)).date(),
            location=f'City {i+1}',
            category='National' if i % 2 == 0 else 'Regional',
            status='Scheduled',
            organizer=f'Organizer {i+1}'
        )
        db_session.session.add(tournament)
        tournaments.append(tournament)
    
    db_session.session.commit()
    return tournaments


@pytest.fixture
def sample_notification(db_session, sample_user):
    """Create sample notification"""
    notification = Notification(
        user_id=sample_user.id,
        title='Test Notification',
        message='This is a test notification',
        type='info',
        is_read=False
    )
    db_session.session.add(notification)
    db_session.session.commit()
    return notification
