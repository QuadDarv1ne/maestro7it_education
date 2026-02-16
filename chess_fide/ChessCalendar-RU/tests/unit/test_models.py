"""
Тесты моделей данных
"""
import pytest
from datetime import datetime, timedelta
from app.models.user import User
from app.models.tournament import Tournament
from app.models.favorite import Favorite
from app.models.rating import Rating


class TestUserModel:
    """Тесты модели User"""
    
    def test_create_user(self, db_session):
        """Тест создания пользователя"""
        user = User(
            username='testuser',
            email='test@example.com'
        )
        user.set_password('password123')
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.check_password('password123')
        assert not user.check_password('wrongpassword')
    
    def test_user_password_hashing(self, db_session):
        """Тест хеширования пароля"""
        user = User(username='test', email='test@test.com')
        user.set_password('secret')
        
        assert user.password_hash != 'secret'
        assert user.check_password('secret')
        assert not user.check_password('wrong')
    
    def test_user_unique_username(self, db_session, regular_user):
        """Тест уникальности username"""
        duplicate_user = User(
            username='user',  # Уже существует
            email='another@test.com'
        )
        db_session.add(duplicate_user)
        
        with pytest.raises(Exception):
            db_session.commit()
    
    def test_user_unique_email(self, db_session, regular_user):
        """Тест уникальности email"""
        duplicate_user = User(
            username='another',
            email='user@test.com'  # Уже существует
        )
        db_session.add(duplicate_user)
        
        with pytest.raises(Exception):
            db_session.commit()


class TestTournamentModel:
    """Тесты модели Tournament"""
    
    def test_create_tournament(self, db_session):
        """Тест создания турнира"""
        tournament = Tournament(
            name='Чемпионат России',
            start_date=datetime.now() + timedelta(days=30),
            end_date=datetime.now() + timedelta(days=37),
            location='Москва',
            category='National',
            status='Scheduled'
        )
        db_session.add(tournament)
        db_session.commit()
        
        assert tournament.id is not None
        assert tournament.name == 'Чемпионат России'
        assert tournament.category == 'National'
        assert tournament.status == 'Scheduled'
    
    def test_tournament_dates_validation(self, db_session):
        """Тест валидации дат турнира"""
        # end_date должна быть после start_date
        tournament = Tournament(
            name='Тест',
            start_date=datetime.now() + timedelta(days=10),
            end_date=datetime.now() + timedelta(days=5),  # Раньше start_date
            location='Москва',
            category='Regional'
        )
        db_session.add(tournament)
        
        # Должна быть ошибка валидации
        with pytest.raises(Exception):
            db_session.commit()
    
    def test_tournament_status_values(self, db_session):
        """Тест допустимых значений статуса"""
        valid_statuses = ['Scheduled', 'Ongoing', 'Completed', 'Cancelled']
        
        for status in valid_statuses:
            tournament = Tournament(
                name=f'Турнир {status}',
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=1),
                location='Тест',
                category='Regional',
                status=status
            )
            db_session.add(tournament)
            db_session.commit()
            assert tournament.status == status
            db_session.delete(tournament)
            db_session.commit()
    
    def test_tournament_search(self, db_session, multiple_tournaments):
        """Тест поиска турниров"""
        # Поиск по названию
        results = Tournament.query.filter(
            Tournament.name.ilike('%Турнир 1%')
        ).all()
        assert len(results) >= 1
        
        # Поиск по категории
        fide_tournaments = Tournament.query.filter_by(category='FIDE').all()
        assert len(fide_tournaments) > 0


class TestFavoriteModel:
    """Тесты модели Favorite"""
    
    def test_add_favorite(self, db_session, regular_user, sample_tournament):
        """Тест добавления в избранное"""
        favorite = Favorite(
            user_id=regular_user.id,
            tournament_id=sample_tournament.id
        )
        db_session.add(favorite)
        db_session.commit()
        
        assert favorite.id is not None
        assert favorite.user_id == regular_user.id
        assert favorite.tournament_id == sample_tournament.id
    
    def test_unique_favorite(self, db_session, regular_user, sample_tournament):
        """Тест уникальности избранного"""
        favorite1 = Favorite(
            user_id=regular_user.id,
            tournament_id=sample_tournament.id
        )
        db_session.add(favorite1)
        db_session.commit()
        
        # Попытка добавить дубликат
        favorite2 = Favorite(
            user_id=regular_user.id,
            tournament_id=sample_tournament.id
        )
        db_session.add(favorite2)
        
        with pytest.raises(Exception):
            db_session.commit()


class TestRatingModel:
    """Тесты модели Rating"""
    
    def test_add_rating(self, db_session, regular_user, sample_tournament):
        """Тест добавления рейтинга"""
        rating = Rating(
            user_id=regular_user.id,
            tournament_id=sample_tournament.id,
            rating=5
        )
        db_session.add(rating)
        db_session.commit()
        
        assert rating.id is not None
        assert rating.rating == 5
    
    def test_rating_range(self, db_session, regular_user, sample_tournament):
        """Тест диапазона рейтинга (1-5)"""
        # Валидный рейтинг
        for value in [1, 2, 3, 4, 5]:
            rating = Rating(
                user_id=regular_user.id,
                tournament_id=sample_tournament.id,
                rating=value
            )
            db_session.add(rating)
            db_session.commit()
            assert rating.rating == value
            db_session.delete(rating)
            db_session.commit()
        
        # Невалидный рейтинг
        invalid_rating = Rating(
            user_id=regular_user.id,
            tournament_id=sample_tournament.id,
            rating=6  # Больше 5
        )
        db_session.add(invalid_rating)
        
        with pytest.raises(Exception):
            db_session.commit()
