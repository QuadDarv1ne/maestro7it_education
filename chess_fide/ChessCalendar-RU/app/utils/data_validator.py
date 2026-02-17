"""
Валидация данных с детальными ошибками
"""
import re
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime, date
from enum import Enum


class ValidationError(Exception):
    """Ошибка валидации"""
    def __init__(self, errors: Dict[str, List[str]]):
        self.errors = errors
        super().__init__(f"Validation failed: {errors}")


class ValidatorType(Enum):
    """Типы валидаторов"""
    REQUIRED = "required"
    TYPE = "type"
    MIN_LENGTH = "min_length"
    MAX_LENGTH = "max_length"
    MIN_VALUE = "min_value"
    MAX_VALUE = "max_value"
    PATTERN = "pattern"
    EMAIL = "email"
    URL = "url"
    DATE = "date"
    CUSTOM = "custom"


class Validator:
    """Базовый класс валидатора"""
    
    def __init__(self, error_message: Optional[str] = None):
        self.error_message = error_message
    
    def validate(self, value: Any, field_name: str) -> Optional[str]:
        """
        Валидация значения
        
        Returns:
            сообщение об ошибке или None
        """
        raise NotImplementedError


class RequiredValidator(Validator):
    """Проверка обязательного поля"""
    
    def validate(self, value: Any, field_name: str) -> Optional[str]:
        if value is None or value == "" or (isinstance(value, (list, dict)) and len(value) == 0):
            return self.error_message or f"{field_name} is required"
        return None


class TypeValidator(Validator):
    """Проверка типа"""
    
    def __init__(self, expected_type: type, error_message: Optional[str] = None):
        super().__init__(error_message)
        self.expected_type = expected_type
    
    def validate(self, value: Any, field_name: str) -> Optional[str]:
        if value is not None and not isinstance(value, self.expected_type):
            return self.error_message or f"{field_name} must be of type {self.expected_type.__name__}"
        return None


class MinLengthValidator(Validator):
    """Проверка минимальной длины"""
    
    def __init__(self, min_length: int, error_message: Optional[str] = None):
        super().__init__(error_message)
        self.min_length = min_length
    
    def validate(self, value: Any, field_name: str) -> Optional[str]:
        if value is not None and len(str(value)) < self.min_length:
            return self.error_message or f"{field_name} must be at least {self.min_length} characters"
        return None


class MaxLengthValidator(Validator):
    """Проверка максимальной длины"""
    
    def __init__(self, max_length: int, error_message: Optional[str] = None):
        super().__init__(error_message)
        self.max_length = max_length
    
    def validate(self, value: Any, field_name: str) -> Optional[str]:
        if value is not None and len(str(value)) > self.max_length:
            return self.error_message or f"{field_name} must be at most {self.max_length} characters"
        return None


class MinValueValidator(Validator):
    """Проверка минимального значения"""
    
    def __init__(self, min_value: float, error_message: Optional[str] = None):
        super().__init__(error_message)
        self.min_value = min_value
    
    def validate(self, value: Any, field_name: str) -> Optional[str]:
        if value is not None and value < self.min_value:
            return self.error_message or f"{field_name} must be at least {self.min_value}"
        return None


class MaxValueValidator(Validator):
    """Проверка максимального значения"""
    
    def __init__(self, max_value: float, error_message: Optional[str] = None):
        super().__init__(error_message)
        self.max_value = max_value
    
    def validate(self, value: Any, field_name: str) -> Optional[str]:
        if value is not None and value > self.max_value:
            return self.error_message or f"{field_name} must be at most {self.max_value}"
        return None


class PatternValidator(Validator):
    """Проверка по регулярному выражению"""
    
    def __init__(self, pattern: str, error_message: Optional[str] = None):
        super().__init__(error_message)
        self.pattern = re.compile(pattern)
    
    def validate(self, value: Any, field_name: str) -> Optional[str]:
        if value is not None and not self.pattern.match(str(value)):
            return self.error_message or f"{field_name} has invalid format"
        return None


class EmailValidator(Validator):
    """Проверка email"""
    
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    def validate(self, value: Any, field_name: str) -> Optional[str]:
        if value is not None and not self.EMAIL_PATTERN.match(str(value)):
            return self.error_message or f"{field_name} must be a valid email address"
        return None


class URLValidator(Validator):
    """Проверка URL"""
    
    URL_PATTERN = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    
    def validate(self, value: Any, field_name: str) -> Optional[str]:
        if value is not None and not self.URL_PATTERN.match(str(value)):
            return self.error_message or f"{field_name} must be a valid URL"
        return None


class DateValidator(Validator):
    """Проверка даты"""
    
    def __init__(self, date_format: str = "%Y-%m-%d", error_message: Optional[str] = None):
        super().__init__(error_message)
        self.date_format = date_format
    
    def validate(self, value: Any, field_name: str) -> Optional[str]:
        if value is None:
            return None
        
        if isinstance(value, (date, datetime)):
            return None
        
        try:
            datetime.strptime(str(value), self.date_format)
            return None
        except ValueError:
            return self.error_message or f"{field_name} must be a valid date ({self.date_format})"


class CustomValidator(Validator):
    """Пользовательский валидатор"""
    
    def __init__(self, func: Callable[[Any], bool], error_message: Optional[str] = None):
        super().__init__(error_message)
        self.func = func
    
    def validate(self, value: Any, field_name: str) -> Optional[str]:
        if value is not None and not self.func(value):
            return self.error_message or f"{field_name} is invalid"
        return None


class InValidator(Validator):
    """Проверка вхождения в список"""
    
    def __init__(self, choices: List[Any], error_message: Optional[str] = None):
        super().__init__(error_message)
        self.choices = choices
    
    def validate(self, value: Any, field_name: str) -> Optional[str]:
        if value is not None and value not in self.choices:
            return self.error_message or f"{field_name} must be one of {self.choices}"
        return None


class DataValidator:
    """Валидатор данных с правилами"""
    
    def __init__(self):
        self.rules = {}
    
    def add_rule(self, field: str, validators: List[Validator]):
        """Добавить правило валидации для поля"""
        self.rules[field] = validators
    
    def validate(self, data: Dict[str, Any], raise_exception: bool = True) -> Dict[str, List[str]]:
        """
        Валидация данных
        
        Args:
            data: данные для валидации
            raise_exception: выбросить исключение при ошибке
            
        Returns:
            словарь ошибок {field: [errors]}
        """
        errors = {}
        
        for field, validators in self.rules.items():
            field_errors = []
            value = data.get(field)
            
            for validator in validators:
                error = validator.validate(value, field)
                if error:
                    field_errors.append(error)
            
            if field_errors:
                errors[field] = field_errors
        
        if errors and raise_exception:
            raise ValidationError(errors)
        
        return errors
    
    def is_valid(self, data: Dict[str, Any]) -> bool:
        """Проверить валидность данных"""
        errors = self.validate(data, raise_exception=False)
        return len(errors) == 0


class SchemaValidator:
    """Валидатор на основе схемы"""
    
    def __init__(self, schema: Dict[str, Dict[str, Any]]):
        """
        Args:
            schema: схема валидации
            
        Пример схемы:
        {
            'name': {
                'type': str,
                'required': True,
                'min_length': 3,
                'max_length': 100
            },
            'email': {
                'type': str,
                'required': True,
                'email': True
            },
            'age': {
                'type': int,
                'min_value': 0,
                'max_value': 150
            }
        }
        """
        self.schema = schema
        self.validator = self._build_validator()
    
    def _build_validator(self) -> DataValidator:
        """Построить валидатор из схемы"""
        validator = DataValidator()
        
        for field, rules in self.schema.items():
            validators = []
            
            # Required
            if rules.get('required'):
                validators.append(RequiredValidator())
            
            # Type
            if 'type' in rules:
                validators.append(TypeValidator(rules['type']))
            
            # Length
            if 'min_length' in rules:
                validators.append(MinLengthValidator(rules['min_length']))
            if 'max_length' in rules:
                validators.append(MaxLengthValidator(rules['max_length']))
            
            # Value
            if 'min_value' in rules:
                validators.append(MinValueValidator(rules['min_value']))
            if 'max_value' in rules:
                validators.append(MaxValueValidator(rules['max_value']))
            
            # Pattern
            if 'pattern' in rules:
                validators.append(PatternValidator(rules['pattern']))
            
            # Email
            if rules.get('email'):
                validators.append(EmailValidator())
            
            # URL
            if rules.get('url'):
                validators.append(URLValidator())
            
            # Date
            if rules.get('date'):
                date_format = rules.get('date_format', '%Y-%m-%d')
                validators.append(DateValidator(date_format))
            
            # In
            if 'choices' in rules:
                validators.append(InValidator(rules['choices']))
            
            # Custom
            if 'custom' in rules:
                validators.append(CustomValidator(rules['custom']))
            
            validator.add_rule(field, validators)
        
        return validator
    
    def validate(self, data: Dict[str, Any], raise_exception: bool = True) -> Dict[str, List[str]]:
        """Валидация данных по схеме"""
        return self.validator.validate(data, raise_exception)
    
    def is_valid(self, data: Dict[str, Any]) -> bool:
        """Проверить валидность данных"""
        return self.validator.is_valid(data)


# Предопределенные схемы
TOURNAMENT_SCHEMA = {
    'name': {
        'type': str,
        'required': True,
        'min_length': 3,
        'max_length': 200
    },
    'location': {
        'type': str,
        'required': True,
        'min_length': 2,
        'max_length': 100
    },
    'start_date': {
        'required': True,
        'date': True
    },
    'end_date': {
        'required': True,
        'date': True
    },
    'category': {
        'type': str,
        'required': True,
        'choices': ['FIDE', 'National', 'Regional', 'Local', 'Online']
    },
    'status': {
        'type': str,
        'required': True,
        'choices': ['Scheduled', 'Ongoing', 'Completed', 'Cancelled']
    },
    'source_url': {
        'type': str,
        'url': True
    }
}

USER_SCHEMA = {
    'username': {
        'type': str,
        'required': True,
        'min_length': 3,
        'max_length': 50,
        'pattern': r'^[a-zA-Z0-9_-]+$'
    },
    'email': {
        'type': str,
        'required': True,
        'email': True
    },
    'password': {
        'type': str,
        'required': True,
        'min_length': 8,
        'max_length': 128
    }
}

# Создаем валидаторы
tournament_validator = SchemaValidator(TOURNAMENT_SCHEMA)
user_validator = SchemaValidator(USER_SCHEMA)
