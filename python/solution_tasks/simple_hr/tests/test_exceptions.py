"""
Unit tests for exceptions module.
"""

import pytest

from app.exceptions import (
    ApplicationError,
    ConflictError,
    DatabaseError,
    ForbiddenError,
    NotFoundError,
    OperationError,
    UnauthorizedError,
    ValidationError,
)


class TestApplicationError:
    """Test ApplicationError class."""

    def test_basic_error(self):
        """Test basic error creation."""
        error = ApplicationError("Test error", code=400)
        assert error.message == "Test error"
        assert error.code == 400

    def test_error_with_payload(self):
        """Test error with additional payload."""
        payload = {'details': 'More info'}
        error = ApplicationError("Test error", code=400, payload=payload)
        assert error.payload == payload

    def test_error_to_dict(self):
        """Test error conversion to dictionary."""
        error = ApplicationError("Test error", code=400)
        result = error.to_dict()
        assert result['error'] == "Test error"
        assert result['code'] == 400


class TestValidationError:
    """Test ValidationError class."""

    def test_validation_error_default_message(self):
        """Test ValidationError with default message."""
        error = ValidationError()
        assert error.message == "Validation failed"
        assert error.code == 400

    def test_validation_error_custom_message(self):
        """Test ValidationError with custom message."""
        error = ValidationError("Custom validation message")
        assert error.message == "Custom validation message"

    def test_validation_error_with_details(self):
        """Test ValidationError with details."""
        details = {'field1': 'error1', 'field2': 'error2'}
        error = ValidationError(details=details)
        assert error.payload['details'] == details


class TestNotFoundError:
    """Test NotFoundError class."""

    def test_not_found_default(self):
        """Test NotFoundError with default resource name."""
        error = NotFoundError()
        assert "Resource" in error.message
        assert error.code == 404

    def test_not_found_custom_resource(self):
        """Test NotFoundError with custom resource name."""
        error = NotFoundError("User")
        assert "User" in error.message
        assert "not found" in error.message


class TestUnauthorizedError:
    """Test UnauthorizedError class."""

    def test_unauthorized_default_message(self):
        """Test UnauthorizedError with default message."""
        error = UnauthorizedError()
        assert error.code == 401

    def test_unauthorized_custom_message(self):
        """Test UnauthorizedError with custom message."""
        error = UnauthorizedError("Invalid credentials")
        assert error.message == "Invalid credentials"


class TestForbiddenError:
    """Test ForbiddenError class."""

    def test_forbidden_default_message(self):
        """Test ForbiddenError with default message."""
        error = ForbiddenError()
        assert error.code == 403

    def test_forbidden_custom_message(self):
        """Test ForbiddenError with custom message."""
        error = ForbiddenError("Permission denied")
        assert error.message == "Permission denied"


class TestConflictError:
    """Test ConflictError class."""

    def test_conflict_default_message(self):
        """Test ConflictError with default message."""
        error = ConflictError()
        assert error.code == 409

    def test_conflict_custom_message(self):
        """Test ConflictError with custom message."""
        error = ConflictError("Duplicate entry")
        assert error.message == "Duplicate entry"


class TestDatabaseError:
    """Test DatabaseError class."""

    def test_database_error_default_message(self):
        """Test DatabaseError with default message."""
        error = DatabaseError()
        assert error.code == 500

    def test_database_error_custom_message(self):
        """Test DatabaseError with custom message."""
        error = DatabaseError("Connection failed")
        assert error.message == "Connection failed"


class TestOperationError:
    """Test OperationError class."""

    def test_operation_error_default_message(self):
        """Test OperationError with default message."""
        error = OperationError()
        assert error.code == 400

    def test_operation_error_custom_message(self):
        """Test OperationError with custom message."""
        error = OperationError("Operation timed out")
        assert error.message == "Operation timed out"
