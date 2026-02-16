"""
Утилиты для валидации данных
"""
from functools import wraps
from flask import request, jsonify
from pydantic import BaseModel, ValidationError
from typing import Type, Optional, Callable
import logging
import bleach
import re

logger = logging.getLogger(__name__)


def validate_request(schema: Type[BaseModel], location: str = 'json'):
    """
    Декоратор для валидации запроса с помощью Pydantic схемы
    
    Args:
        schema: Pydantic схема для валидации
        location: Откуда брать данные ('json', 'args', 'form')
    
    Example:
        @app.route('/api/tournaments', methods=['POST'])
        @validate_request(TournamentCreate)
        def create_tournament():
            data = request.validated_data
            # data уже провалидирован
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Получаем данные из запроса
                if location == 'json':
                    data = request.get_json()
                elif location == 'args':
                    data = request.args.to_dict()
                elif location == 'form':
                    data = request.form.to_dict()
                else:
                    return jsonify({'error': f'Invalid location: {location}'}), 500
                
                if data is None:
                    return jsonify({'error': 'No data provided'}), 400
                
                # Валидируем данные
                validated = schema(**data)
                
                # Сохраняем провалидированные данные в request
                request.validated_data = validated
                
                return f(*args, **kwargs)
            
            except ValidationError as e:
                # Форматируем ошибки валидации
                errors = []
                for error in e.errors():
                    field = '.'.join(str(loc) for loc in error['loc'])
                    errors.append({
                        'field': field,
                        'message': error['msg'],
                        'type': error['type']
                    })
                
                logger.warning(f"Validation error: {errors}")
                
                return jsonify({
                    'error': 'Validation error',
                    'details': errors
                }), 400
            
            except Exception as e:
                logger.error(f"Unexpected error in validation: {e}")
                return jsonify({'error': 'Internal server error'}), 500
        
        return decorated_function
    return decorator


def validate_response(schema: Type[BaseModel]):
    """
    Декоратор для валидации ответа
    
    Args:
        schema: Pydantic схема для валидации ответа
    
    Example:
        @app.route('/api/tournaments/<int:id>')
        @validate_response(TournamentResponse)
        def get_tournament(id):
            tournament = Tournament.query.get_or_404(id)
            return tournament  # Автоматически сериализуется
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                result = f(*args, **kwargs)
                
                # Если результат - tuple (response, status_code)
                if isinstance(result, tuple):
                    data, status_code = result[0], result[1]
                else:
                    data, status_code = result, 200
                
                # Валидируем и сериализуем
                if hasattr(data, '__dict__'):
                    # SQLAlchemy модель
                    validated = schema.from_orm(data)
                elif isinstance(data, dict):
                    validated = schema(**data)
                else:
                    validated = schema.parse_obj(data)
                
                return jsonify(validated.dict()), status_code
            
            except ValidationError as e:
                logger.error(f"Response validation error: {e}")
                return jsonify({'error': 'Internal server error'}), 500
            
            except Exception as e:
                logger.error(f"Unexpected error in response validation: {e}")
                return jsonify({'error': 'Internal server error'}), 500
        
        return decorated_function
    return decorator


def validate_email(email: str) -> bool:
    """
    Валидация email адреса
    
    Args:
        email: Email для проверки
    
    Returns:
        True если email валиден
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_username(username: str) -> bool:
    """
    Валидация username
    
    Args:
        username: Username для проверки
    
    Returns:
        True если username валиден
    """
    if len(username) < 3 or len(username) > 80:
        return False
    
    # Только буквы, цифры и подчеркивание
    pattern = r'^[a-zA-Z0-9_]+$'
    return bool(re.match(pattern, username))


def validate_url(url: str) -> bool:
    """
    Валидация URL
    
    Args:
        url: URL для проверки
    
    Returns:
        True если URL валиден
    """
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))


def sanitize_html(html: str, allowed_tags: Optional[list] = None) -> str:
    """
    Санитизация HTML
    
    Args:
        html: HTML для очистки
        allowed_tags: Разрешенные теги
    
    Returns:
        Очищенный HTML
    """
    if allowed_tags is None:
        allowed_tags = [
            'p', 'br', 'strong', 'em', 'u', 'a', 'ul', 'ol', 'li',
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'code', 'pre'
        ]
    
    allowed_attributes = {
        'a': ['href', 'title', 'target'],
        'img': ['src', 'alt', 'title']
    }
    
    return bleach.clean(
        html,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True
    )


def sanitize_input(text: str) -> str:
    """
    Базовая санитизация текстового ввода
    
    Args:
        text: Текст для очистки
    
    Returns:
        Очищенный текст
    """
    # Удаляем HTML теги
    text = bleach.clean(text, tags=[], strip=True)
    
    # Удаляем лишние пробелы
    text = ' '.join(text.split())
    
    return text.strip()


def validate_phone(phone: str) -> bool:
    """
    Валидация номера телефона
    
    Args:
        phone: Номер телефона
    
    Returns:
        True если номер валиден
    """
    # Простая валидация для международных номеров
    pattern = r'^\+?[1-9]\d{1,14}$'
    return bool(re.match(pattern, phone.replace(' ', '').replace('-', '')))


def validate_date_range(start_date, end_date) -> tuple[bool, Optional[str]]:
    """
    Валидация диапазона дат
    
    Args:
        start_date: Начальная дата
        end_date: Конечная дата
    
    Returns:
        (is_valid, error_message)
    """
    if not start_date or not end_date:
        return False, "Both dates are required"
    
    if end_date < start_date:
        return False, "End date must be greater than or equal to start date"
    
    return True, None


def validate_file_extension(filename: str, allowed_extensions: list) -> bool:
    """
    Валидация расширения файла
    
    Args:
        filename: Имя файла
        allowed_extensions: Разрешенные расширения
    
    Returns:
        True если расширение разрешено
    """
    if '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in allowed_extensions


def validate_file_size(file_size: int, max_size: int = 16777216) -> tuple[bool, Optional[str]]:
    """
    Валидация размера файла
    
    Args:
        file_size: Размер файла в байтах
        max_size: Максимальный размер (по умолчанию 16MB)
    
    Returns:
        (is_valid, error_message)
    """
    if file_size > max_size:
        max_mb = max_size / (1024 * 1024)
        return False, f"File size exceeds maximum allowed size of {max_mb}MB"
    
    return True, None


def validate_json_structure(data: dict, required_fields: list) -> tuple[bool, Optional[str]]:
    """
    Валидация структуры JSON
    
    Args:
        data: JSON данные
        required_fields: Обязательные поля
    
    Returns:
        (is_valid, error_message)
    """
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    return True, None


class ValidationError(Exception):
    """Кастомное исключение для ошибок валидации"""
    
    def __init__(self, message: str, field: Optional[str] = None, details: Optional[dict] = None):
        self.message = message
        self.field = field
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self):
        """Преобразование в словарь"""
        result = {'error': self.message}
        if self.field:
            result['field'] = self.field
        if self.details:
            result['details'] = self.details
        return result


def handle_validation_error(error: ValidationError):
    """
    Обработчик ошибок валидации
    
    Args:
        error: ValidationError
    
    Returns:
        JSON ответ с ошибкой
    """
    return jsonify(error.to_dict()), 400


# Регулярные выражения для валидации
REGEX_PATTERNS = {
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'username': r'^[a-zA-Z0-9_]{3,80}$',
    'url': r'^https?://[^\s/$.?#].[^\s]*$',
    'phone': r'^\+?[1-9]\d{1,14}$',
    'hex_color': r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
    'ipv4': r'^(\d{1,3}\.){3}\d{1,3}$',
    'ipv6': r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$',
}


def validate_pattern(value: str, pattern_name: str) -> bool:
    """
    Валидация по именованному паттерну
    
    Args:
        value: Значение для проверки
        pattern_name: Имя паттерна из REGEX_PATTERNS
    
    Returns:
        True если значение соответствует паттерну
    """
    if pattern_name not in REGEX_PATTERNS:
        raise ValueError(f"Unknown pattern: {pattern_name}")
    
    pattern = REGEX_PATTERNS[pattern_name]
    return bool(re.match(pattern, value))
