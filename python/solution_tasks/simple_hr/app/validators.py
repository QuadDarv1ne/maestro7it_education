"""
Input data validation module.

Provides functions and classes for validating incoming data
before processing in API endpoints and forms.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Pattern, Tuple, Type

logger_validators = {}


class Validator:
    """Base validator class."""

    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        """
        Validate a value.

        Args:
            value: Value to validate.

        Returns:
            Tuple of (is_valid, error_message).
        """
        raise NotImplementedError


class StringValidator(Validator):
    """Validator for string values."""

    def __init__(
        self,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        pattern: Optional[str] = None,
        allow_empty: bool = False,
    ) -> None:
        """
        Initialize StringValidator.

        Args:
            min_length: Minimum string length.
            max_length: Maximum string length.
            pattern: Regex pattern for validation.
            allow_empty: Whether to allow empty strings.
        """
        self.min_length = min_length
        self.max_length = max_length
        self.pattern = re.compile(pattern) if pattern else None
        self.allow_empty = allow_empty

    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        """Validate string value."""
        if not isinstance(value, str):
            return False, "Must be a string"

        if not self.allow_empty and not value:
            return False, "Cannot be empty"

        if self.min_length and len(value) < self.min_length:
            return False, f"Must be at least {self.min_length} characters"

        if self.max_length and len(value) > self.max_length:
            return False, f"Must be at most {self.max_length} characters"

        if self.pattern and not self.pattern.match(value):
            return False, "Invalid format"

        return True, None


class IntegerValidator(Validator):
    """Validator for integer values."""

    def __init__(
        self,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
    ) -> None:
        """
        Initialize IntegerValidator.

        Args:
            min_value: Minimum value.
            max_value: Maximum value.
        """
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        """Validate integer value."""
        if not isinstance(value, int) or isinstance(value, bool):
            return False, "Must be an integer"

        if self.min_value is not None and value < self.min_value:
            return False, f"Must be at least {self.min_value}"

        if self.max_value is not None and value > self.max_value:
            return False, f"Must be at most {self.max_value}"

        return True, None


class EmailValidator(Validator):
    """Validator for email addresses."""

    EMAIL_PATTERN: Pattern = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )

    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        """Validate email address."""
        if not isinstance(value, str):
            return False, "Email must be a string"

        if not self.EMAIL_PATTERN.match(value):
            return False, "Invalid email format"

        if len(value) > 255:
            return False, "Email is too long"

        return True, None


class DateValidator(Validator):
    """Validator for date values."""

    DATE_PATTERN: Pattern = re.compile(
        r'^\d{4}-\d{2}-\d{2}$'
    )

    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        """Validate date in YYYY-MM-DD format."""
        if not isinstance(value, str):
            return False, "Date must be a string"

        if not self.DATE_PATTERN.match(value):
            return False, "Date must be in YYYY-MM-DD format"

        try:
            parts = value.split('-')
            year, month, day = int(parts[0]), int(parts[1]), int(parts[2])

            if not (1 <= month <= 12):
                return False, "Invalid month"

            if not (1 <= day <= 31):
                return False, "Invalid day"

            return True, None
        except (ValueError, IndexError):
            return False, "Invalid date format"


class PhoneValidator(Validator):
    """Validator for phone numbers."""

    PHONE_PATTERN: Pattern = re.compile(
        r'^\+?[1-9]\d{1,14}$'
    )

    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        """Validate phone number."""
        if not isinstance(value, str):
            return False, "Phone must be a string"

        # Remove spaces, dashes, and parentheses
        cleaned = re.sub(r'[\s\-\(\)]', '', value)

        if not self.PHONE_PATTERN.match(cleaned):
            return False, "Invalid phone format"

        return True, None


class URLValidator(Validator):
    """Validator for URLs."""

    URL_PATTERN: Pattern = re.compile(
        r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'
    )

    def validate(self, value: Any) -> Tuple[bool, Optional[str]]:
        """Validate URL."""
        if not isinstance(value, str):
            return False, "URL must be a string"

        if not self.URL_PATTERN.match(value):
            return False, "Invalid URL format"

        if len(value) > 2048:
            return False, "URL is too long"

        return True, None


def validate_dict(
    data: Dict[str, Any],
    schema: Dict[str, Type[Validator]],
) -> Tuple[bool, Optional[Dict[str, str]]]:
    """
    Validate a dictionary against a schema.

    Args:
        data: Dictionary to validate.
        schema: Dictionary mapping field names to validator classes.

    Returns:
        Tuple of (is_valid, error_messages_dict).
    """
    errors: Dict[str, str] = {}

    for field, validator_class in schema.items():
        if field not in data:
            errors[field] = "Required field"
            continue

        validator = validator_class()
        is_valid, error_msg = validator.validate(data[field])

        if not is_valid:
            errors[field] = error_msg or "Invalid value"

    return len(errors) == 0, errors if errors else None


def validate_employee_data(data: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, str]]]:
    """
    Validate employee form data.

    Args:
        data: Employee data to validate.

    Returns:
        Tuple of (is_valid, error_messages_dict).
    """
    schema = {
        'first_name': StringValidator,
        'last_name': StringValidator,
        'email': EmailValidator,
        'phone': PhoneValidator,
    }

    return validate_dict(data, schema)


def validate_vacation_data(data: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, str]]]:
    """
    Validate vacation form data.

    Args:
        data: Vacation data to validate.

    Returns:
        Tuple of (is_valid, error_messages_dict).
    """
    schema = {
        'start_date': DateValidator,
        'end_date': DateValidator,
    }

    is_valid, errors = validate_dict(data, schema)

    # Additional business logic validation
    if is_valid:
        try:
            start = data['start_date']
            end = data['end_date']
            if start > end:
                errors = errors or {}
                errors['end_date'] = "End date must be after start date"
                is_valid = False
        except (KeyError, TypeError):
            pass

    return is_valid, errors


def sanitize_input(value: str, max_length: int = 1000) -> str:
    """
    Sanitize user input by removing dangerous characters.

    Args:
        value: Input value to sanitize.
        max_length: Maximum allowed length.

    Returns:
        Sanitized string.
    """
    if not isinstance(value, str):
        return str(value)[:max_length]

    # Remove leading/trailing whitespace
    value = value.strip()

    # Limit length
    value = value[:max_length]

    return value
