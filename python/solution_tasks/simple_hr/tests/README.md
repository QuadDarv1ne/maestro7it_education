# Simple HR Application Tests

This directory contains unit tests for the Simple HR application.

## Running Tests

To run all tests, execute:

```bash
python tests/run_tests.py
```

## Test Structure

- `test_models.py` - Tests for database models
- `test_forms.py` - Tests for form validation
- `test_utils.py` - Tests for utility functions
- `test_routes.py` - Tests for application routes
- `test_config.py` - Test configuration

## Coverage

The test runner automatically generates coverage reports:
- Terminal output shows coverage summary
- HTML coverage report is generated in the `htmlcov` directory

## Requirements

Make sure you have the testing dependencies installed:

```bash
pip install pytest coverage
```