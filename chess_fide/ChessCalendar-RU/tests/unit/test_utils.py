"""
Тесты утилит
"""
import pytest
from datetime import datetime, timedelta
from app.utils.cache import cache_get, cache_set, cache_delete
from app.utils.ratings import calculate_average_rating
from app.utils.recommendations import get_recommendations


class TestCacheUtils:
    """Тесты кэширования"""
    
    def test_cache_set_and_get(self):
        """Тест установки и получения из кэша"""
        key = 'test_key'
        value = {'data': 'test_value'}
        
        cache_set(key, value, timeout=60)
        result = cache_get(key)
        
        assert result == value
    
    def test_cache_expiration(self):
        """Тест истечения кэша"""
        import time
        
        key = 'expiring_key'
        value = 'test'
        
        cache_set(key, value, timeout=1)
        time.sleep(2)
        result = cache_get(key)
        
        assert result is None
    
    def test_cache_delete(self):
        """Тест удаления из кэша"""
        key = 'delete_key'
        value = 'test'
        
        cache_set(key, value)
        cache_delete(key)
        result = cache_get(key)
        
        assert result is None


class TestRatingUtils:
    """Тесты рейтинговых утилит"""
    
    def test_calculate_average_rating(self, db_session, sample_tournament, regular_user):
        """Тест расчета среднего рейтинга"""
        from app.models.rating import Rating
        
        # Добавляем несколько рейтингов
        ratings = [5, 4, 3, 5, 4]
        for rating_value in ratings:
            rating = Rating(
                user_id=regular_user.id,
                tournament_id=sample_tournament.id,
                rating=rating_value
            )
            db_session.add(rating)
        db_session.commit()
        
        avg = calculate_average_rating(sample_tournament.id)
        expected = sum(ratings) / len(ratings)
        
        assert avg == expected
    
    def test_calculate_average_rating_no_ratings(self, sample_tournament):
        """Тест расчета среднего без рейтингов"""
        avg = calculate_average_rating(sample_tournament.id)
        
        assert avg == 0.0


class TestRecommendationUtils:
    """Тесты рекомендаций"""
    
    def test_get_recommendations_for_user(self, db_session, regular_user, multiple_tournaments):
        """Тест получения рекомендаций"""
        recommendations = get_recommendations(regular_user.id, limit=5)
        
        assert len(recommendations) <= 5
        assert all(isinstance(t, dict) for t in recommendations)
    
    def test_get_recommendations_empty_user(self, db_session):
        """Тест рекомендаций для пользователя без истории"""
        recommendations = get_recommendations(99999, limit=5)
        
        # Должны вернуться популярные турниры
        assert isinstance(recommendations, list)


class TestDateUtils:
    """Тесты работы с датами"""
    
    def test_format_date(self):
        """Тест форматирования даты"""
        from app.utils.helpers import format_date
        
        date = datetime(2024, 12, 25, 15, 30)
        formatted = format_date(date, format='%d.%m.%Y')
        
        assert formatted == '25.12.2024'
    
    def test_is_upcoming_tournament(self):
        """Тест проверки предстоящего турнира"""
        from app.utils.helpers import is_upcoming
        
        future_date = datetime.now() + timedelta(days=7)
        past_date = datetime.now() - timedelta(days=7)
        
        assert is_upcoming(future_date) is True
        assert is_upcoming(past_date) is False


class TestValidationUtils:
    """Тесты валидации"""
    
    def test_validate_email(self):
        """Тест валидации email"""
        from app.utils.validators import validate_email
        
        assert validate_email('test@example.com') is True
        assert validate_email('invalid-email') is False
        assert validate_email('test@') is False
        assert validate_email('@example.com') is False
    
    def test_validate_username(self):
        """Тест валидации username"""
        from app.utils.validators import validate_username
        
        assert validate_username('validuser') is True
        assert validate_username('user123') is True
        assert validate_username('ab') is False  # Слишком короткий
        assert validate_username('a' * 51) is False  # Слишком длинный
        assert validate_username('user@name') is False  # Недопустимые символы
    
    def test_sanitize_html(self):
        """Тест санитизации HTML"""
        from app.utils.validators import sanitize_html
        
        dirty_html = '<script>alert("XSS")</script><p>Safe content</p>'
        clean_html = sanitize_html(dirty_html)
        
        assert '<script>' not in clean_html
        assert '<p>Safe content</p>' in clean_html
