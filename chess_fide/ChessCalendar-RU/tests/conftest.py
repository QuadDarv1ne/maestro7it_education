"""
Pytest конфигурация и фикстуры
"""
import pytest
import os
import tempfile
from app import create_app, db
from app.models.user import User
from app.models.tournament import Tournament
from datetime import datetime, timedelta


# In-memory SQLite для изоляции тестов: переопределяем конфигурацию пула соединений
# до инициализации приложения, чтобы StaticPool применялся с самого начала.
def _test_engine_options(app, pool_size=10, max_overflow=20):
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'poolclass': 'sqlalchemy.pool.StaticPool',
        'connect_args': {'check_same_thread': False}
    }


from app.utils.db_optimization import QueryOptimizer
QueryOptimizer.enable_connection_pooling = staticmethod(_test_engine_options)


@pytest.fixture(scope='session')
def app():
    """Создание тестового приложения"""
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    os.environ['TESTING'] = 'True'
    os.environ['SECRET_KEY'] = 'test-secret-key'
    os.environ['WTF_CSRF_ENABLED'] = 'False'
    
    app = create_app('testing')
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SERVER_NAME': 'localhost.localdomain'
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Тестовый клиент Flask"""
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """CLI runner для тестирования команд"""
    return app.test_cli_runner()


@pytest.fixture(scope='function')
def db_session(app):
    """Сессия БД с полной изоляцией между тестами"""
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()


@pytest.fixture
def admin_user(db_session):
    """Создание тестового администратора"""
    user = User(
        username='admin',
        email='admin@test.com',
        password='Admin123!test',
        is_admin=True
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def regular_user(db_session):
    """Создание обычного пользователя"""
    user = User(
        username='user',
        email='user@test.com',
        password='User123!test'
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def sample_tournament(db_session):
    """Создание тестового турнира"""
    tournament = Tournament(
        name='Тестовый турнир',
        start_date=datetime.now() + timedelta(days=7),
        end_date=datetime.now() + timedelta(days=9),
        location='Москва',
        category='National',
        status='Scheduled',
        description='Описание тестового турнира',
        source_url='https://example.com/tournament'
    )
    db_session.add(tournament)
    db_session.commit()
    return tournament


@pytest.fixture
def multiple_tournaments(db_session):
    """Создание нескольких турниров для тестирования"""
    tournaments = []
    categories = ['FIDE', 'National', 'Regional']
    
    for i in range(10):
        tournament = Tournament(
            name=f'Турнир {i+1}',
            start_date=datetime.now() + timedelta(days=i*7),
            end_date=datetime.now() + timedelta(days=i*7+2),
            location=f'Город {i+1}',
            category=categories[i % 3],
            status='Scheduled',
            description=f'Описание турнира {i+1}'
        )
        db_session.add(tournament)
        tournaments.append(tournament)
    
    db_session.commit()
    return tournaments


@pytest.fixture
def auth_headers(client, admin_user):
    """JWT токен для аутентифицированных запросов"""
    response = client.post('/auth/login', json={
        'username': 'admin',
        'password': 'Admin123!test'
    })
    token = response.json.get('access_token')
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture(autouse=True)
def reset_db(db_session):
    """Автоматическая очистка БД после каждого теста"""
    yield
    db_session.rollback()
