"""
Unit tests for validators module.
"""

import pytest

from app.validators import (
    DateValidator,
    EmailValidator,
    IntegerValidator,
    PhoneValidator,
    StringValidator,
    URLValidator,
    sanitize_input,
    validate_dict,
    validate_employee_data,
    validate_vacation_data,
)


class TestStringValidator:
    """Test StringValidator class."""

    def test_valid_string(self):
        """Test validation of valid string."""
        validator = StringValidator(min_length=1, max_length=100)
        is_valid, error = validator.validate("Hello")
        assert is_valid is True
        assert error is None

    def test_empty_string_not_allowed(self):
        """Test that empty string fails when not allowed."""
        validator = StringValidator(allow_empty=False)
        is_valid, error = validator.validate("")
        assert is_valid is False
        assert error is not None

    def test_empty_string_allowed(self):
        """Test that empty string passes when allowed."""
        validator = StringValidator(allow_empty=True)
        is_valid, error = validator.validate("")
        assert is_valid is True
        assert error is None

    def test_min_length(self):
        """Test minimum length validation."""
        validator = StringValidator(min_length=5)
        is_valid, error = validator.validate("Hi")
        assert is_valid is False
        assert "at least 5" in error

    def test_max_length(self):
        """Test maximum length validation."""
        validator = StringValidator(max_length=3)
        is_valid, error = validator.validate("Hello")
        assert is_valid is False
        assert "at most 3" in error

    def test_pattern_validation(self):
        """Test regex pattern validation."""
        validator = StringValidator(pattern=r'^\d+$')
        is_valid, error = validator.validate("12345")
        assert is_valid is True

        is_valid, error = validator.validate("abc")
        assert is_valid is False


class TestIntegerValidator:
    """Test IntegerValidator class."""

    def test_valid_integer(self):
        """Test validation of valid integer."""
        validator = IntegerValidator(min_value=0, max_value=100)
        is_valid, error = validator.validate(50)
        assert is_valid is True
        assert error is None

    def test_invalid_type(self):
        """Test that non-integer fails."""
        validator = IntegerValidator()
        is_valid, error = validator.validate("123")
        assert is_valid is False
        assert "Must be an integer" in error

    def test_boolean_rejected(self):
        """Test that boolean is rejected."""
        validator = IntegerValidator()
        is_valid, error = validator.validate(True)
        assert is_valid is False

    def test_min_value(self):
        """Test minimum value validation."""
        validator = IntegerValidator(min_value=10)
        is_valid, error = validator.validate(5)
        assert is_valid is False
        assert "at least 10" in error

    def test_max_value(self):
        """Test maximum value validation."""
        validator = IntegerValidator(max_value=100)
        is_valid, error = validator.validate(150)
        assert is_valid is False
        assert "at most 100" in error


class TestEmailValidator:
    """Test EmailValidator class."""

    def test_valid_email(self):
        """Test validation of valid email."""
        validator = EmailValidator()
        is_valid, error = validator.validate("user@example.com")
        assert is_valid is True
        assert error is None

    def test_invalid_email_no_domain(self):
        """Test that email without domain fails."""
        validator = EmailValidator()
        is_valid, error = validator.validate("user@")
        assert is_valid is False

    def test_invalid_email_no_at(self):
        """Test that email without @ fails."""
        validator = EmailValidator()
        is_valid, error = validator.validate("userexample.com")
        assert is_valid is False

    def test_invalid_type(self):
        """Test that non-string fails."""
        validator = EmailValidator()
        is_valid, error = validator.validate(123)
        assert is_valid is False


class TestDateValidator:
    """Test DateValidator class."""

    def test_valid_date(self):
        """Test validation of valid date."""
        validator = DateValidator()
        is_valid, error = validator.validate("2024-12-25")
        assert is_valid is True
        assert error is None

    def test_invalid_format(self):
        """Test that invalid format fails."""
        validator = DateValidator()
        is_valid, error = validator.validate("25-12-2024")
        assert is_valid is False

    def test_invalid_month(self):
        """Test that invalid month fails."""
        validator = DateValidator()
        is_valid, error = validator.validate("2024-13-01")
        assert is_valid is False
        assert "Invalid month" in error

    def test_invalid_day(self):
        """Test that invalid day fails."""
        validator = DateValidator()
        is_valid, error = validator.validate("2024-12-32")
        assert is_valid is False
        assert "Invalid day" in error


class TestPhoneValidator:
    """Test PhoneValidator class."""

    def test_valid_phone(self):
        """Test validation of valid phone."""
        validator = PhoneValidator()
        is_valid, error = validator.validate("+1234567890")
        assert is_valid is True
        assert error is None

    def test_phone_with_spaces(self):
        """Test phone validation with spaces."""
        validator = PhoneValidator()
        is_valid, error = validator.validate("+1 234 567 890")
        assert is_valid is True
        assert error is None

    def test_invalid_phone(self):
        """Test that invalid phone fails."""
        validator = PhoneValidator()
        is_valid, error = validator.validate("abc")
        assert is_valid is False


class TestURLValidator:
    """Test URLValidator class."""

    def test_valid_url(self):
        """Test validation of valid URL."""
        validator = URLValidator()
        is_valid, error = validator.validate("https://example.com")
        assert is_valid is True
        assert error is None

    def test_valid_url_with_path(self):
        """Test validation of URL with path."""
        validator = URLValidator()
        is_valid, error = validator.validate("https://example.com/path/to/page")
        assert is_valid is True
        assert error is None

    def test_invalid_url(self):
        """Test that invalid URL fails."""
        validator = URLValidator()
        is_valid, error = validator.validate("not a url")
        assert is_valid is False


class TestValidateFunctions:
    """Test validation functions."""

    def test_validate_dict_valid(self):
        """Test dictionary validation with valid data."""
        schema = {
            'name': StringValidator,
            'age': IntegerValidator,
            'email': EmailValidator,
        }
        data = {
            'name': 'John',
            'age': 30,
            'email': 'john@example.com',
        }
        is_valid, errors = validate_dict(data, schema)
        assert is_valid is True
        assert errors is None

    def test_validate_dict_invalid(self):
        """Test dictionary validation with invalid data."""
        schema = {
            'email': EmailValidator,
        }
        data = {
            'email': 'invalid-email',
        }
        is_valid, errors = validate_dict(data, schema)
        assert is_valid is False
        assert errors is not None
        assert 'email' in errors

    def test_validate_employee_data_valid(self):
        """Test employee data validation with valid data."""
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone': '+1234567890',
        }
        is_valid, errors = validate_employee_data(data)
        assert is_valid is True
        assert errors is None

    def test_validate_vacation_data_valid(self):
        """Test vacation data validation with valid data."""
        data = {
            'start_date': '2024-01-01',
            'end_date': '2024-01-05',
        }
        is_valid, errors = validate_vacation_data(data)
        assert is_valid is True
        assert errors is None

    def test_validate_vacation_data_end_before_start(self):
        """Test vacation validation with end date before start date."""
        data = {
            'start_date': '2024-01-05',
            'end_date': '2024-01-01',
        }
        is_valid, errors = validate_vacation_data(data)
        assert is_valid is False
        assert errors is not None
        assert 'end_date' in errors


class TestSanitizeInput:
    """Test sanitize_input function."""

    def test_sanitize_string(self):
        """Test sanitization of string."""
        result = sanitize_input("  hello  ")
        assert result == "hello"

    def test_sanitize_max_length(self):
        """Test that string is truncated to max length."""
        result = sanitize_input("a" * 2000, max_length=100)
        assert len(result) == 100

    def test_sanitize_number(self):
        """Test sanitization of number."""
        result = sanitize_input(123)
        assert result == "123"
