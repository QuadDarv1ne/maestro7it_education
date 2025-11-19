"""
API Documentation with Swagger/OpenAPI support.

Provides automatic API documentation generation and Swagger UI.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from flask import Flask


def setup_swagger(app: Flask) -> None:
    """
    Setup Swagger/OpenAPI documentation.

    Args:
        app: Flask application instance.
    """
    try:
        from flasgger import Swagger

        swagger = Swagger(
            app,
            template={
                'swagger': '3.0.0',
                'info': {
                    'title': 'Simple HR API',
                    'version': '2.4.0',
                    'description': 'Comprehensive HR Management System API',
                    'contact': {
                        'name': 'API Support',
                        'url': 'https://github.com/QuadDarv1ne/maestro7it_education',
                    },
                },
                'servers': [
                    {'url': 'http://localhost:5000', 'description': 'Development'},
                    {'url': 'http://0.0.0.0:5000', 'description': 'Production'},
                ],
            },
        )

        app.logger.info("Swagger documentation enabled at /apidocs")

    except ImportError:
        app.logger.warning(
            "Flasgger not installed. Install with: pip install flasgger"
        )


def api_doc(
    summary: str = '',
    description: str = '',
    tags: Optional[list] = None,
    parameters: Optional[list] = None,
    responses: Optional[Dict[str, Any]] = None,
) -> Any:
    """
    Decorator for documenting API endpoints.

    Args:
        summary: Short summary of the endpoint.
        description: Detailed description.
        tags: List of tags for grouping.
        parameters: List of parameter definitions.
        responses: Response definitions by status code.

    Returns:
        Decorator function.
    """
    def decorator(func: Any) -> Any:
        doc = {
            'summary': summary,
            'description': description or func.__doc__,
            'tags': tags or [],
            'parameters': parameters or [],
            'responses': responses or {
                '200': {'description': 'Success'},
                '400': {'description': 'Bad Request'},
                '401': {'description': 'Unauthorized'},
                '404': {'description': 'Not Found'},
                '500': {'description': 'Internal Server Error'},
            },
        }

        func.__swagger__ = doc
        return func

    return decorator


# Common parameter definitions
ID_PARAMETER = {
    'name': 'id',
    'in': 'path',
    'type': 'integer',
    'required': True,
    'description': 'Resource ID',
}

PAGE_PARAMETER = {
    'name': 'page',
    'in': 'query',
    'type': 'integer',
    'default': 1,
    'description': 'Page number',
}

LIMIT_PARAMETER = {
    'name': 'limit',
    'in': 'query',
    'type': 'integer',
    'default': 20,
    'description': 'Items per page',
}

SORT_PARAMETER = {
    'name': 'sort',
    'in': 'query',
    'type': 'string',
    'description': 'Sort field and direction (e.g., name:asc)',
}

SEARCH_PARAMETER = {
    'name': 'search',
    'in': 'query',
    'type': 'string',
    'description': 'Search query',
}

# Common response definitions
SUCCESS_RESPONSE = {
    '200': {
        'description': 'Successful operation',
        'schema': {
            'type': 'object',
            'properties': {
                'data': {'type': 'object'},
                'message': {'type': 'string'},
            },
        },
    },
}

ERROR_RESPONSES = {
    '400': {
        'description': 'Bad Request',
        'schema': {
            'type': 'object',
            'properties': {
                'error': {'type': 'string'},
                'details': {'type': 'object'},
            },
        },
    },
    '401': {
        'description': 'Unauthorized',
        'schema': {
            'type': 'object',
            'properties': {
                'error': {'type': 'string'},
            },
        },
    },
    '404': {
        'description': 'Not Found',
        'schema': {
            'type': 'object',
            'properties': {
                'error': {'type': 'string'},
            },
        },
    },
    '500': {
        'description': 'Internal Server Error',
        'schema': {
            'type': 'object',
            'properties': {
                'error': {'type': 'string'},
            },
        },
    },
}


class APIDocumentation:
    """Helper class for API documentation."""

    @staticmethod
    def employee_schema() -> Dict[str, Any]:
        """Employee model schema."""
        return {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'first_name': {'type': 'string'},
                'last_name': {'type': 'string'},
                'email': {'type': 'string', 'format': 'email'},
                'phone': {'type': 'string'},
                'position_id': {'type': 'integer'},
                'department_id': {'type': 'integer'},
                'hire_date': {'type': 'string', 'format': 'date'},
                'created_at': {'type': 'string', 'format': 'date-time'},
            },
            'required': ['first_name', 'last_name', 'email'],
        }

    @staticmethod
    def vacation_schema() -> Dict[str, Any]:
        """Vacation model schema."""
        return {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'employee_id': {'type': 'integer'},
                'start_date': {'type': 'string', 'format': 'date'},
                'end_date': {'type': 'string', 'format': 'date'},
                'vacation_type': {
                    'type': 'string',
                    'enum': ['paid', 'unpaid', 'sick'],
                },
                'reason': {'type': 'string'},
                'status': {
                    'type': 'string',
                    'enum': ['pending', 'approved', 'rejected'],
                },
                'created_at': {'type': 'string', 'format': 'date-time'},
            },
            'required': ['employee_id', 'start_date', 'end_date'],
        }

    @staticmethod
    def order_schema() -> Dict[str, Any]:
        """Order model schema."""
        return {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'employee_id': {'type': 'integer'},
                'order_type': {
                    'type': 'string',
                    'enum': ['hire', 'transfer', 'fire'],
                },
                'order_date': {'type': 'string', 'format': 'date'},
                'details': {'type': 'string'},
                'status': {
                    'type': 'string',
                    'enum': ['pending', 'executed', 'cancelled'],
                },
                'created_at': {'type': 'string', 'format': 'date-time'},
            },
            'required': ['employee_id', 'order_type'],
        }

    @staticmethod
    def paginated_response(item_schema: Dict[str, Any]) -> Dict[str, Any]:
        """Create paginated response schema."""
        return {
            'type': 'object',
            'properties': {
                'items': {
                    'type': 'array',
                    'items': item_schema,
                },
                'pagination': {
                    'type': 'object',
                    'properties': {
                        'page': {'type': 'integer'},
                        'limit': {'type': 'integer'},
                        'total': {'type': 'integer'},
                        'pages': {'type': 'integer'},
                    },
                },
            },
        }
