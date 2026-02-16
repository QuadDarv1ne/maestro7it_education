"""
Тесты Pydantic схем
"""
import pytest
from pydantic import ValidationError
from datetime import datetime, timedelta
from app.schemas.tournament import (
    TournamentCreate,
    TournamentUpdate,
    TournamentFilter,
    TournamentCategory,
    TournamentStatus
)
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserLogin,
    UserPasswordChange
)
from app.schemas.common import (
    PaginationParams,
    DateRangeFilter,
    SearchParams
)


class TestTournamentSchemas:
    """Тесты схем турниров"""
    
    def test_tournament_create_valid(self):
        """Тест создания валидного турнира"""
        data = {
            'name': 'Test Tournament',
            'start_date': datetime.now() + timedelta(days=7),
            'end_date': datetime.now() + timedelta(days=9),
            'location': 'Moscow',
            'category': 'National',
            'status': 'Scheduled'
        }
        
        tournament = TournamentCreate(**data)
        
        assert tournament.name == 'Test Tournament'
        assert tournament.category == TournamentCategory.NATIONAL
        assert tournament.status == TournamentStatus.SCHEDULED
    
    def test_tournament_create_invalid_dates(self):
        """Тест создания с невалидными датами"""
        data = {
            'name': 'Test Tournament',
            'start_date': datetime.now() + timedelta(days=9),
            'end_date': datetime.now() + timedelta(days=7),  # Раньше start_date
            'location': 'Moscow',
            'category': 'National'
        }
        
        with pytest.raises(ValidationError) as exc_info:
            TournamentCreate(**data)
        
        assert 'end_date' in str(exc_info.value)
    
    def test_tournament_create_short_name(self):
        """Тест создания с коротким названием"""
        data = {
            'name': 'AB',  # Слишком короткое
            'start_date': datetime.now(),
            'end_date': datetime.now() + timedelta(days=1),
            'location': 'Moscow',
            'category': 'National'
        }
        
        with pytest.raises(ValidationError):
            TournamentCreate(**data)
    
    def test_tournament_create_whitespace_name(self):
        """Тест создания с пробелами в названии"""
        data = {
            'name': '   Test Tournament   ',
            'start_date': datetime.now(),
            'end_date': datetime.now() + timedelta(days=1),
            'location': 'Moscow',
            'category': 'National'
        }
        
        tournament = TournamentCreate(**data)
        assert tournament.name == 'Test Tournament'  # Пробелы должны быть удалены
    
    def test_tournament_update_partial(self):
        """Тест частичного обновления"""
        data = {
            'status': 'Ongoing',
            'description': 'Updated description'
        }
        
        update = TournamentUpdate(**data)
        
        assert update.status == TournamentStatus.ONGOING
        assert update.description == 'Updated description'
        assert update.name is None  # Не обновляется
    
    def test_tournament_filter(self):
        """Тест фильтров турниров"""
        data = {
            'category': 'National',
            'status': 'Scheduled',
            'location': 'Moscow',
            'start_date_from': datetime.now(),
            'start_date_to': datetime.now() + timedelta(days=30)
        }
        
        filters = TournamentFilter(**data)
        
        assert filters.category == TournamentCategory.NATIONAL
        assert filters.status == TournamentStatus.SCHEDULED
    
    def test_tournament_filter_invalid_date_range(self):
        """Тест фильтров с невалидным диапазоном дат"""
        data = {
            'start_date_from': datetime.now() + timedelta(days=30),
            'start_date_to': datetime.now()  # Раньше start_date_from
        }
        
        with pytest.raises(ValidationError):
            TournamentFilter(**data)


class TestUserSchemas:
    """Тесты схем пользователей"""
    
    def test_user_create_valid(self):
        """Тест создания валидного пользователя"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePass123'
        }
        
        user = UserCreate(**data)
        
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
    
    def test_user_create_weak_password(self):
        """Тест создания со слабым паролем"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'weak'  # Нет заглавных букв и цифр
        }
        
        with pytest.raises(ValidationError):
            UserCreate(**data)
    
    def test_user_create_invalid_email(self):
        """Тест создания с невалидным email"""
        data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password': 'SecurePass123'
        }
        
        with pytest.raises(ValidationError):
            UserCreate(**data)
    
    def test_user_create_invalid_username(self):
        """Тест создания с невалидным username"""
        data = {
            'username': 'test user',  # Пробел
            'email': 'test@example.com',
            'password': 'SecurePass123'
        }
        
        with pytest.raises(ValidationError):
            UserCreate(**data)
    
    def test_user_create_username_lowercase(self):
        """Тест преобразования username в lowercase"""
        data = {
            'username': 'TestUser',
            'email': 'test@example.com',
            'password': 'SecurePass123'
        }
        
        user = UserCreate(**data)
        assert user.username == 'testuser'
    
    def test_user_update_partial(self):
        """Тест частичного обновления пользователя"""
        data = {
            'email': 'newemail@example.com'
        }
        
        update = UserUpdate(**data)
        
        assert update.email == 'newemail@example.com'
        assert update.username is None
    
    def test_user_login(self):
        """Тест схемы входа"""
        data = {
            'username': 'testuser',
            'password': 'password123'
        }
        
        login = UserLogin(**data)
        
        assert login.username == 'testuser'
        assert login.password == 'password123'
    
    def test_user_login_with_2fa(self):
        """Тест схемы входа с 2FA"""
        data = {
            'username': 'testuser',
            'password': 'password123',
            'totp_code': '123456'
        }
        
        login = UserLogin(**data)
        
        assert login.totp_code == '123456'
    
    def test_user_password_change(self):
        """Тест схемы смены пароля"""
        data = {
            'old_password': 'OldPass123',
            'new_password': 'NewSecurePass456'
        }
        
        change = UserPasswordChange(**data)
        
        assert change.old_password == 'OldPass123'
        assert change.new_password == 'NewSecurePass456'
    
    def test_user_password_change_weak_new(self):
        """Тест смены на слабый пароль"""
        data = {
            'old_password': 'OldPass123',
            'new_password': 'weak'
        }
        
        with pytest.raises(ValidationError):
            UserPasswordChange(**data)


class TestCommonSchemas:
    """Тесты общих схем"""
    
    def test_pagination_params_default(self):
        """Тест параметров пагинации по умолчанию"""
        params = PaginationParams()
        
        assert params.page == 1
        assert params.per_page == 20
    
    def test_pagination_params_custom(self):
        """Тест кастомных параметров пагинации"""
        params = PaginationParams(page=2, per_page=50)
        
        assert params.page == 2
        assert params.per_page == 50
    
    def test_pagination_params_invalid_page(self):
        """Тест невалидной страницы"""
        with pytest.raises(ValidationError):
            PaginationParams(page=0)  # Должна быть >= 1
    
    def test_pagination_params_invalid_per_page(self):
        """Тест невалидного количества на странице"""
        with pytest.raises(ValidationError):
            PaginationParams(per_page=101)  # Должно быть <= 100
    
    def test_date_range_filter_valid(self):
        """Тест валидного диапазона дат"""
        data = {
            'start_date': datetime.now(),
            'end_date': datetime.now() + timedelta(days=7)
        }
        
        filter_obj = DateRangeFilter(**data)
        
        assert filter_obj.start_date is not None
        assert filter_obj.end_date is not None
    
    def test_date_range_filter_invalid(self):
        """Тест невалидного диапазона дат"""
        data = {
            'start_date': datetime.now() + timedelta(days=7),
            'end_date': datetime.now()  # Раньше start_date
        }
        
        with pytest.raises(ValidationError):
            DateRangeFilter(**data)
    
    def test_search_params(self):
        """Тест параметров поиска"""
        data = {
            'q': 'chess tournament',
            'limit': 50
        }
        
        params = SearchParams(**data)
        
        assert params.q == 'chess tournament'
        assert params.limit == 50
    
    def test_search_params_empty_query(self):
        """Тест пустого поискового запроса"""
        with pytest.raises(ValidationError):
            SearchParams(q='')  # Должен быть минимум 1 символ
    
    def test_search_params_too_long_query(self):
        """Тест слишком длинного запроса"""
        with pytest.raises(ValidationError):
            SearchParams(q='a' * 201)  # Максимум 200 символов


class TestSchemaValidation:
    """Тесты валидации схем"""
    
    def test_enum_validation(self):
        """Тест валидации enum"""
        # Валидное значение
        data = {
            'name': 'Test',
            'start_date': datetime.now(),
            'end_date': datetime.now() + timedelta(days=1),
            'location': 'Moscow',
            'category': 'National'
        }
        
        tournament = TournamentCreate(**data)
        assert tournament.category == TournamentCategory.NATIONAL
        
        # Невалидное значение
        data['category'] = 'InvalidCategory'
        with pytest.raises(ValidationError):
            TournamentCreate(**data)
    
    def test_url_validation(self):
        """Тест валидации URL"""
        # Валидный URL
        data = {
            'name': 'Test',
            'start_date': datetime.now(),
            'end_date': datetime.now() + timedelta(days=1),
            'location': 'Moscow',
            'category': 'National',
            'source_url': 'https://example.com/tournament'
        }
        
        tournament = TournamentCreate(**data)
        assert str(tournament.source_url) == 'https://example.com/tournament'
        
        # Невалидный URL
        data['source_url'] = 'not a url'
        with pytest.raises(ValidationError):
            TournamentCreate(**data)
    
    def test_string_length_validation(self):
        """Тест валидации длины строки"""
        # Слишком короткое название
        with pytest.raises(ValidationError):
            TournamentCreate(
                name='AB',
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=1),
                location='Moscow',
                category='National'
            )
        
        # Слишком длинное название
        with pytest.raises(ValidationError):
            TournamentCreate(
                name='A' * 201,
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=1),
                location='Moscow',
                category='National'
            )
