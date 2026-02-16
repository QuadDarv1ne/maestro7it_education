"""
Тесты валидаторов
"""
import pytest
from app.utils.validators import (
    validate_email,
    validate_username,
    validate_url,
    sanitize_html,
    sanitize_input,
    validate_phone,
    validate_date_range,
    validate_file_extension,
    validate_file_size,
    validate_json_structure,
    validate_pattern
)
from datetime import datetime, timedelta


class TestEmailValidation:
    """Тесты валидации email"""
    
    def test_valid_emails(self):
        """Тест валидных email"""
        valid_emails = [
            'test@example.com',
            'user.name@example.com',
            'user+tag@example.co.uk',
            'test123@test-domain.com'
        ]
        
        for email in valid_emails:
            assert validate_email(email), f"Email should be valid: {email}"
    
    def test_invalid_emails(self):
        """Тест невалидных email"""
        invalid_emails = [
            'invalid',
            '@example.com',
            'test@',
            'test @example.com',
            'test@example',
        ]
        
        for email in invalid_emails:
            assert not validate_email(email), f"Email should be invalid: {email}"


class TestUsernameValidation:
    """Тесты валидации username"""
    
    def test_valid_usernames(self):
        """Тест валидных username"""
        valid_usernames = [
            'user',
            'user123',
            'user_name',
            'User_123'
        ]
        
        for username in valid_usernames:
            assert validate_username(username), f"Username should be valid: {username}"
    
    def test_invalid_usernames(self):
        """Тест невалидных username"""
        invalid_usernames = [
            'ab',  # Слишком короткий
            'a' * 81,  # Слишком длинный
            'user name',  # Пробел
            'user@name',  # Недопустимый символ
            'user-name',  # Дефис
        ]
        
        for username in invalid_usernames:
            assert not validate_username(username), f"Username should be invalid: {username}"


class TestURLValidation:
    """Тесты валидации URL"""
    
    def test_valid_urls(self):
        """Тест валидных URL"""
        valid_urls = [
            'http://example.com',
            'https://example.com',
            'https://example.com/path',
            'https://example.com/path?query=value',
            'https://subdomain.example.com'
        ]
        
        for url in valid_urls:
            assert validate_url(url), f"URL should be valid: {url}"
    
    def test_invalid_urls(self):
        """Тест невалидных URL"""
        invalid_urls = [
            'not a url',
            'ftp://example.com',  # Не http/https
            'example.com',  # Без протокола
            'http://',
        ]
        
        for url in invalid_urls:
            assert not validate_url(url), f"URL should be invalid: {url}"


class TestHTMLSanitization:
    """Тесты санитизации HTML"""
    
    def test_sanitize_dangerous_html(self):
        """Тест удаления опасного HTML"""
        dangerous_html = '<script>alert("XSS")</script><p>Safe content</p>'
        clean_html = sanitize_html(dangerous_html)
        
        assert '<script>' not in clean_html
        assert 'alert' not in clean_html
        assert '<p>Safe content</p>' in clean_html
    
    def test_sanitize_allowed_tags(self):
        """Тест сохранения разрешенных тегов"""
        html = '<p>Text with <strong>bold</strong> and <em>italic</em></p>'
        clean_html = sanitize_html(html)
        
        assert '<p>' in clean_html
        assert '<strong>' in clean_html
        assert '<em>' in clean_html
    
    def test_sanitize_input(self):
        """Тест базовой санитизации"""
        dirty_input = '  <script>alert("XSS")</script>  Text   with   spaces  '
        clean_input = sanitize_input(dirty_input)
        
        assert '<script>' not in clean_input
        assert clean_input == 'alert("XSS") Text with spaces'


class TestPhoneValidation:
    """Тесты валидации телефона"""
    
    def test_valid_phones(self):
        """Тест валидных номеров"""
        valid_phones = [
            '+79991234567',
            '+1234567890',
            '79991234567',
        ]
        
        for phone in valid_phones:
            assert validate_phone(phone), f"Phone should be valid: {phone}"
    
    def test_invalid_phones(self):
        """Тест невалидных номеров"""
        invalid_phones = [
            '123',  # Слишком короткий
            'not a phone',
            '+0123456789',  # Начинается с 0
        ]
        
        for phone in invalid_phones:
            assert not validate_phone(phone), f"Phone should be invalid: {phone}"


class TestDateRangeValidation:
    """Тесты валидации диапазона дат"""
    
    def test_valid_date_range(self):
        """Тест валидного диапазона"""
        start = datetime.now()
        end = start + timedelta(days=7)
        
        is_valid, error = validate_date_range(start, end)
        assert is_valid
        assert error is None
    
    def test_invalid_date_range(self):
        """Тест невалидного диапазона"""
        start = datetime.now()
        end = start - timedelta(days=7)
        
        is_valid, error = validate_date_range(start, end)
        assert not is_valid
        assert error is not None
    
    def test_missing_dates(self):
        """Тест отсутствующих дат"""
        is_valid, error = validate_date_range(None, datetime.now())
        assert not is_valid
        assert error is not None


class TestFileValidation:
    """Тесты валидации файлов"""
    
    def test_valid_file_extension(self):
        """Тест валидного расширения"""
        allowed = ['jpg', 'png', 'gif']
        
        assert validate_file_extension('image.jpg', allowed)
        assert validate_file_extension('photo.PNG', allowed)
        assert not validate_file_extension('document.pdf', allowed)
    
    def test_file_without_extension(self):
        """Тест файла без расширения"""
        allowed = ['jpg', 'png']
        assert not validate_file_extension('filename', allowed)
    
    def test_valid_file_size(self):
        """Тест валидного размера файла"""
        is_valid, error = validate_file_size(1024 * 1024)  # 1MB
        assert is_valid
        assert error is None
    
    def test_invalid_file_size(self):
        """Тест превышения размера"""
        is_valid, error = validate_file_size(20 * 1024 * 1024)  # 20MB
        assert not is_valid
        assert error is not None


class TestJSONValidation:
    """Тесты валидации JSON"""
    
    def test_valid_json_structure(self):
        """Тест валидной структуры"""
        data = {'name': 'Test', 'email': 'test@example.com'}
        required = ['name', 'email']
        
        is_valid, error = validate_json_structure(data, required)
        assert is_valid
        assert error is None
    
    def test_missing_fields(self):
        """Тест отсутствующих полей"""
        data = {'name': 'Test'}
        required = ['name', 'email']
        
        is_valid, error = validate_json_structure(data, required)
        assert not is_valid
        assert 'email' in error


class TestPatternValidation:
    """Тесты валидации по паттернам"""
    
    def test_email_pattern(self):
        """Тест паттерна email"""
        assert validate_pattern('test@example.com', 'email')
        assert not validate_pattern('invalid', 'email')
    
    def test_username_pattern(self):
        """Тест паттерна username"""
        assert validate_pattern('user123', 'username')
        assert not validate_pattern('ab', 'username')
    
    def test_url_pattern(self):
        """Тест паттерна URL"""
        assert validate_pattern('https://example.com', 'url')
        assert not validate_pattern('not a url', 'url')
    
    def test_hex_color_pattern(self):
        """Тест паттерна цвета"""
        assert validate_pattern('#FF0000', 'hex_color')
        assert validate_pattern('#F00', 'hex_color')
        assert not validate_pattern('FF0000', 'hex_color')
    
    def test_ipv4_pattern(self):
        """Тест паттерна IPv4"""
        assert validate_pattern('192.168.1.1', 'ipv4')
        assert not validate_pattern('256.256.256.256', 'ipv4')
    
    def test_unknown_pattern(self):
        """Тест неизвестного паттерна"""
        with pytest.raises(ValueError):
            validate_pattern('test', 'unknown_pattern')
