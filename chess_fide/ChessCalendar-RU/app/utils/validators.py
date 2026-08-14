"""
Расширенная система валидации данных
"""
import re
from datetime import datetime, date
from typing import Any, Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Ошибка валидации"""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")


class Validator:
    """Базовый класс валидатора"""
    
    def __init__(self, required: bool = True, nullable: bool = False):
        self.required = required
        self.nullable = nullable
    
    def validate(self, value: Any, field_name: str) -> Tuple[bool, Optional[str]]:
        """Валидация значения"""
        # Проверка обязательности
        if value is None:
            if self.required and not self.nullable:
                return False, f"{field_name} is required"
            return True, None
        
        return self._validate_value(value, field_name)
    
    def _validate_value(self, value: Any, field_name: str) -> Tuple[bool, Optional[str]]:
        """Валидация конкретного значения (переопределяется в подклассах)"""
        return True, None


class StringValidator(Validator):
    """Валидатор строк"""
    
    def __init__(self, min_length: int = 0, max_length: int = None, 
                 pattern: str = None, **kwargs):
        super().__init__(**kwargs)
        self.min_length = min_length
        self.max_length = max_length
        self.pattern = re.compile(pattern) if pattern else None
    
    def _validate_value(self, value: Any, field_name: str) -> Tuple[bool, Optional[str]]:
        if not isinstance(value, str):
            return False, f"{field_name} must be a string"
        
        if len(value) < self.min_length:
            return False, f"{field_name} must be at least {self.min_length} characters"
        
        if self.max_length and len(value) > self.max_length:
            return False, f"{field_name} must be at most {self.max_length} characters"
        
        if self.pattern and not self.pattern.match(value):
            return False, f"{field_name} has invalid format"
        
        return True, None


class EmailValidator(StringValidator):
    """Валидатор email"""
    
    def __init__(self, **kwargs):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        super().__init__(pattern=email_pattern, max_length=120, **kwargs)
    
    def _validate_value(self, value: Any, field_name: str) -> Tuple[bool, Optional[str]]:
        is_valid, error = super()._validate_value(value, field_name)
        if not is_valid:
            return False, f"{field_name} must be a valid email address"
        return True, None


class URLValidator(Validator):
    """Валидатор URL"""
    
    def _validate_value(self, value: Any, field_name: str) -> Tuple[bool, Optional[str]]:
        if not isinstance(value, str):
            return False, f"{field_name} must be a string"
        
        from urllib.parse import urlparse
        parsed = urlparse(value)
        if parsed.scheme not in ('http', 'https') or not parsed.netloc:
            return False, f"{field_name} must be a valid http/https URL"
        
        return True, None


class PasswordValidator(StringValidator):
    """Валидатор пароля"""
    
    def __init__(self, min_length: int = 8, max_length: int = 128, **kwargs):
        super().__init__(min_length=min_length, max_length=max_length, **kwargs)
    
    def _validate_value(self, value: Any, field_name: str) -> Tuple[bool, Optional[str]]:
        is_valid, error = super()._validate_value(value, field_name)
        if not is_valid:
            return False, error
        
        has_upper = any(c.isupper() for c in value)
        has_lower = any(c.islower() for c in value)
        has_digit = any(c.isdigit() for c in value)
        
        if not (has_upper and has_lower and has_digit):
            return False, f"{field_name} must contain uppercase and lowercase letters and digits"
        
        return True, None


class IntegerValidator(Validator):
    """Валидатор целых чисел"""
    
    def __init__(self, min_value: int = None, max_value: int = None, **kwargs):
        super().__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value
    
    def _validate_value(self, value: Any, field_name: str) -> Tuple[bool, Optional[str]]:
        if not isinstance(value, int) or isinstance(value, bool):
            return False, f"{field_name} must be an integer"
        
        if self.min_value is not None and value < self.min_value:
            return False, f"{field_name} must be at least {self.min_value}"
        
        if self.max_value is not None and value > self.max_value:
            return False, f"{field_name} must be at most {self.max_value}"
        
        return True, None


class BooleanValidator(Validator):
    """Валидатор булевых значений"""
    
    def _validate_value(self, value: Any, field_name: str) -> Tuple[bool, Optional[str]]:
        if not isinstance(value, bool):
            return False, f"{field_name} must be a boolean"
        return True, None


class DateValidator(Validator):
    """Валидатор дат"""
    
    def __init__(self, min_date: date = None, max_date: date = None, **kwargs):
        super().__init__(**kwargs)
        self.min_date = min_date
        self.max_date = max_date
    
    def _validate_value(self, value: Any, field_name: str) -> Tuple[bool, Optional[str]]:
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value).date()
            except ValueError:
                return False, f"{field_name} must be a valid date (ISO format)"
        
        if not isinstance(value, date):
            return False, f"{field_name} must be a date"
        
        if self.min_date and value < self.min_date:
            return False, f"{field_name} must be after {self.min_date}"
        
        if self.max_date and value > self.max_date:
            return False, f"{field_name} must be before {self.max_date}"
        
        return True, None


class ListValidator(Validator):
    """Валидатор списков"""
    
    def __init__(self, item_validator: Validator = None, 
                 min_items: int = 0, max_items: int = None, **kwargs):
        super().__init__(**kwargs)
        self.item_validator = item_validator
        self.min_items = min_items
        self.max_items = max_items
    
    def _validate_value(self, value: Any, field_name: str) -> Tuple[bool, Optional[str]]:
        if not isinstance(value, list):
            return False, f"{field_name} must be a list"
        
        if len(value) < self.min_items:
            return False, f"{field_name} must have at least {self.min_items} items"
        
        if self.max_items and len(value) > self.max_items:
            return False, f"{field_name} must have at most {self.max_items} items"
        
        if self.item_validator:
            for i, item in enumerate(value):
                is_valid, error = self.item_validator.validate(item, f"{field_name}[{i}]")
                if not is_valid:
                    return False, error
        
        return True, None


class DictValidator(Validator):
    """Валидатор словарей"""
    
    def __init__(self, schema: Dict[str, Validator] = None, **kwargs):
        super().__init__(**kwargs)
        self.schema = schema or {}
    
    def _validate_value(self, value: Any, field_name: str) -> Tuple[bool, Optional[str]]:
        if not isinstance(value, dict):
            return False, f"{field_name} must be a dictionary"
        
        for key, validator in self.schema.items():
            field_value = value.get(key)
            is_valid, error = validator.validate(field_value, f"{field_name}.{key}")
            if not is_valid:
                return False, error
        
        return True, None


class Schema:
    """Схема валидации"""
    
    def __init__(self, fields: Dict[str, Validator]):
        self.fields = fields
    
    def validate(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Валидация данных по схеме"""
        errors = []
        
        for field_name, validator in self.fields.items():
            value = data.get(field_name)
            is_valid, error = validator.validate(value, field_name)
            
            if not is_valid:
                errors.append(error)
        
        return len(errors) == 0, errors
    
    def validate_or_raise(self, data: Dict[str, Any]):
        """Валидация с выбросом исключения"""
        is_valid, errors = self.validate(data)
        
        if not is_valid:
            raise ValidationError('validation', '; '.join(errors))


# Предопределенные схемы

USER_REGISTRATION_SCHEMA = Schema({
    'username': StringValidator(min_length=3, max_length=80, 
                                pattern=r'^[A-Za-z0-9_-]+$'),
    'email': EmailValidator(),
    'password': StringValidator(min_length=8, max_length=128)
})

USER_UPDATE_SCHEMA = Schema({
    'email': EmailValidator(required=False),
    'is_active': BooleanValidator(required=False),
    'is_admin': BooleanValidator(required=False)
})

PASSWORD_CHANGE_SCHEMA = Schema({
    'current_password': StringValidator(min_length=1),
    'new_password': StringValidator(min_length=8, max_length=128)
})

TOURNAMENT_SCHEMA = Schema({
    'name': StringValidator(min_length=3, max_length=200),
    'start_date': DateValidator(),
    'end_date': DateValidator(),
    'location': StringValidator(min_length=2, max_length=200),
    'category': StringValidator(min_length=2, max_length=100),
    'description': StringValidator(max_length=2000, required=False),
    'prize_fund': StringValidator(max_length=100, required=False),
    'organizer': StringValidator(max_length=200, required=False)
})


def validate_data(schema: Schema, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Вспомогательная функция для валидации данных"""
    return schema.validate(data)


def validate_or_raise(schema: Schema, data: Dict[str, Any]):
    """Вспомогательная функция для валидации с выбросом исключения"""
    schema.validate_or_raise(data)


def slugify(text: str) -> str:
    """
    Создать URL-friendly slug из текста
    
    Args:
        text: Исходный текст
        
    Returns:
        URL-friendly slug (например: 'Мой турнир' -> 'moy-turir')
    """
    import re
    import unicodedata
    
    if not text:
        return ''
    
    # Приводим к нижнему регистру
    text = text.lower()
    
    # Транслитерация кириллицы
    cyrillic_to_latin = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya',
        ' ': '-',
    }
    
    # Транслитерация
    result = []
    for char in text:
        result.append(cyrillic_to_latin.get(char, char))
    text = ''.join(result)
    
    # Удаляем все кроме букв, цифр и дефиса
    text = re.sub(r'[^a-z0-9\-]', '', text)
    
    # Заменяем несколько дефисов на один
    text = re.sub(r'-+', '-', text)
    
    # Удаляем дефисы в начале и конце
    text = text.strip('-')
    
    return text


# ─── Функциональные валидаторы (обратная совместимость) ───────────────────────

EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
USERNAME_PATTERN = re.compile(r'^[A-Za-z0-9_]{3,50}$')
PHONE_PATTERN = re.compile(r'^\+?[1-9]\d{9,14}$')
HEX_COLOR_PATTERN = re.compile(r'^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$')
IPV4_PATTERN = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')

ALLOWED_TAGS = [
    'a', 'abbr', 'acronym', 'b', 'blockquote', 'br', 'code', 'em',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'i', 'img', 'li', 'ol', 'p',
    'pre', 'strong', 'ul'
]
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'img': ['src', 'alt', 'title']
}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 МБ


def validate_email(email: Any) -> bool:
    """Проверка корректности email"""
    if not isinstance(email, str):
        return False
    return EMAIL_PATTERN.match(email.strip()) is not None


def validate_username(username: Any) -> bool:
    """Проверка корректности username (3-50 символов, буквы/цифры/подчеркивание)"""
    if not isinstance(username, str):
        return False
    return USERNAME_PATTERN.match(username) is not None


def validate_url(url: Any) -> bool:
    """Проверка корректности URL (только http/https)"""
    if not isinstance(url, str):
        return False
    
    from urllib.parse import urlparse
    parsed = urlparse(url)
    return parsed.scheme in ('http', 'https') and bool(parsed.netloc)


def sanitize_html(html: Any, allowed_tags: Optional[List[str]] = None,
                  allowed_attributes: Optional[Dict[str, List[str]]] = None) -> str:
    """Очистка HTML от опасных тегов и скриптов"""
    if html is None:
        return ''
    
    import bleach
    
    text = str(html)
    # Удаляем блоки script/style вместе с содержимым
    text = re.sub(r'<\s*script\b[^>]*>.*?<\s*/\s*script\s*>', '', text,
                  flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<\s*style\b[^>]*>.*?<\s*/\s*style\s*>', '', text,
                  flags=re.IGNORECASE | re.DOTALL)
    
    tags = allowed_tags if allowed_tags is not None else ALLOWED_TAGS
    attrs = allowed_attributes if allowed_attributes is not None else ALLOWED_ATTRIBUTES
    
    return bleach.clean(text, tags=tags, attributes=attrs, strip=True)


def sanitize_input(text: Any, max_length: Optional[int] = None) -> str:
    """Базовая санитизация строки: удаление HTML и схлопывание пробелов"""
    if text is None:
        return ''
    
    text = str(text)
    text = re.sub(r'<[^>]*>', '', text)
    text = ' '.join(text.split())
    
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text


def validate_phone(phone: Any) -> bool:
    """Проверка корректности телефона (E.164: 10-15 цифр, не начинается с 0)"""
    if not isinstance(phone, str):
        return False
    return PHONE_PATTERN.match(phone.strip()) is not None


def validate_date_range(start: Any, end: Any) -> Tuple[bool, Optional[str]]:
    """Проверка диапазона дат: обе даты обязательны, start <= end"""
    if start is None or end is None:
        return False, "Both start and end dates are required"
    
    try:
        if start > end:
            return False, "Start date must be before end date"
    except TypeError:
        return False, "Invalid date values"
    
    return True, None


def validate_file_extension(filename: Any, allowed_extensions: List[str]) -> bool:
    """Проверка расширения файла"""
    if not isinstance(filename, str) or '.' not in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    allowed = {e.strip().lower().lstrip('.') for e in allowed_extensions}
    
    return ext in allowed


def validate_file_size(size: Any, max_size: Optional[int] = None) -> Tuple[bool, Optional[str]]:
    """Проверка размера файла"""
    if size is None:
        return False, "File size is required"
    
    limit = max_size or MAX_FILE_SIZE
    
    if size > limit:
        return False, f"File size exceeds maximum of {limit} bytes"
    
    return True, None


def validate_json_structure(data: Any, required_fields: List[str]) -> Tuple[bool, Optional[str]]:
    """Проверка наличия обязательных полей в JSON-структуре"""
    if not isinstance(data, dict):
        return False, "Data must be a dictionary"
    
    missing = [f for f in required_fields if f not in data or data[f] is None]
    if missing:
        return False, f"Missing required field(s): {', '.join(missing)}"
    
    return True, None


def validate_pattern(value: Any, pattern_type: str) -> bool:
    """Валидация значения по именованному паттерну"""
    if pattern_type == 'email':
        return validate_email(value)
    elif pattern_type == 'username':
        return validate_username(value)
    elif pattern_type == 'url':
        return validate_url(value)
    elif pattern_type == 'hex_color':
        return isinstance(value, str) and HEX_COLOR_PATTERN.match(value.strip()) is not None
    elif pattern_type == 'ipv4':
        if not isinstance(value, str) or not IPV4_PATTERN.match(value):
            return False
        return all(0 <= int(part) <= 255 for part in value.split('.'))
    else:
        raise ValueError(f"Unknown pattern type: {pattern_type}")


__all__ = [
    'ValidationError',
    'Validator',
    'StringValidator',
    'IntegerValidator',
    'BooleanValidator',
    'DateValidator',
    'ListValidator',
    'DictValidator',
    'Schema',
    'EmailValidator',
    'URLValidator',
    'PasswordValidator',
    'validate_email',
    'validate_username',
    'validate_url',
    'validate_phone',
    'validate_date_range',
    'validate_file_extension',
    'validate_file_size',
    'validate_json_structure',
    'validate_pattern',
    'sanitize_html',
    'sanitize_input',
    'validate_data',
    'validate_or_raise',
    'slugify'
]
