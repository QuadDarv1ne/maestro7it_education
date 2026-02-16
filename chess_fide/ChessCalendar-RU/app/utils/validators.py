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
