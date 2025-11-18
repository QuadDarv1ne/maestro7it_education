"""
Централизованная обработка ошибок для Simple HR
"""

from flask import render_template, jsonify, request
from werkzeug.exceptions import HTTPException
import logging
import traceback
from datetime import datetime

logger = logging.getLogger(__name__)


def init_error_handlers(app):
    """Инициализация обработчиков ошибок"""
    
    @app.errorhandler(400)
    def bad_request(error):
        """Обработка 400 Bad Request"""
        logger.warning(f"Bad Request: {error}")
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({
                'error': 'Bad Request',
                'message': str(error),
                'status': 400
            }), 400
        return render_template('errors/400.html', error=error), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        """Обработка 401 Unauthorized"""
        logger.warning(f"Unauthorized access: {request.path}")
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Authentication required',
                'status': 401
            }), 401
        return render_template('errors/401.html'), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        """Обработка 403 Forbidden"""
        logger.warning(f"Forbidden access: {request.path} by {request.remote_addr}")
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({
                'error': 'Forbidden',
                'message': 'Access denied',
                'status': 403
            }), 403
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(404)
    def not_found(error):
        """Обработка 404 Not Found"""
        logger.info(f"404 Not Found: {request.path}")
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({
                'error': 'Not Found',
                'message': 'Resource not found',
                'status': 404
            }), 404
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Обработка 405 Method Not Allowed"""
        logger.warning(f"Method Not Allowed: {request.method} {request.path}")
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({
                'error': 'Method Not Allowed',
                'message': f'Method {request.method} not allowed for this endpoint',
                'status': 405
            }), 405
        return render_template('errors/405.html', method=request.method), 405
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        """Обработка 413 Request Entity Too Large"""
        logger.warning(f"Request too large: {request.path}")
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({
                'error': 'Request Too Large',
                'message': 'The uploaded file is too large',
                'status': 413
            }), 413
        return render_template('errors/413.html'), 413
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        """Обработка 429 Too Many Requests"""
        logger.warning(f"Rate limit exceeded: {request.remote_addr}")
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({
                'error': 'Too Many Requests',
                'message': 'Rate limit exceeded. Please try again later',
                'status': 429
            }), 429
        return render_template('errors/429.html'), 429
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """Обработка 500 Internal Server Error"""
        # Логирование полного traceback
        error_details = {
            'timestamp': datetime.utcnow().isoformat(),
            'path': request.path,
            'method': request.method,
            'ip': request.remote_addr,
            'user_agent': request.user_agent.string,
            'error': str(error),
            'traceback': traceback.format_exc()
        }
        
        logger.error(f"Internal Server Error: {error_details}")
        
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred',
                'status': 500,
                'timestamp': error_details['timestamp']
            }), 500
        
        return render_template('errors/500.html', 
                             error=error if app.debug else None), 500
    
    @app.errorhandler(502)
    def bad_gateway(error):
        """Обработка 502 Bad Gateway"""
        logger.error(f"Bad Gateway: {error}")
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({
                'error': 'Bad Gateway',
                'message': 'The server received an invalid response',
                'status': 502
            }), 502
        return render_template('errors/502.html'), 502
    
    @app.errorhandler(503)
    def service_unavailable(error):
        """Обработка 503 Service Unavailable"""
        logger.error(f"Service Unavailable: {error}")
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({
                'error': 'Service Unavailable',
                'message': 'The service is temporarily unavailable',
                'status': 503
            }), 503
        return render_template('errors/503.html'), 503
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Обработка всех необработанных исключений"""
        # Логирование полной информации об ошибке
        error_info = {
            'type': type(error).__name__,
            'message': str(error),
            'path': request.path,
            'method': request.method,
            'timestamp': datetime.utcnow().isoformat(),
            'traceback': traceback.format_exc()
        }
        
        logger.exception(f"Unhandled exception: {error_info}")
        
        # Для HTTP исключений используем их код
        if isinstance(error, HTTPException):
            status_code = error.code
            error_message = error.description
        else:
            status_code = 500
            error_message = 'An unexpected error occurred'
        
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({
                'error': error_info['type'],
                'message': error_message if not app.debug else str(error),
                'status': status_code,
                'timestamp': error_info['timestamp']
            }), status_code
        
        # Рендерим соответствующую страницу ошибки
        template_name = f'errors/{status_code}.html'
        try:
            return render_template(template_name, error=error if app.debug else None), status_code
        except:
            # Если шаблон не найден, показываем общую страницу ошибки
            return render_template('errors/500.html', 
                                 error=error if app.debug else None), status_code
    
    logger.info("Error handlers initialized successfully")


class APIError(Exception):
    """Базовый класс для API ошибок"""
    
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        """Преобразование в словарь для JSON ответа"""
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status'] = self.status_code
        rv['error'] = self.__class__.__name__
        return rv


class ValidationError(APIError):
    """Ошибка валидации данных"""
    
    def __init__(self, message, errors=None):
        super().__init__(message, status_code=400, payload={'errors': errors})


class ResourceNotFoundError(APIError):
    """Ресурс не найден"""
    
    def __init__(self, resource_type, resource_id):
        message = f"{resource_type} with ID {resource_id} not found"
        super().__init__(message, status_code=404)


class AuthenticationError(APIError):
    """Ошибка аутентификации"""
    
    def __init__(self, message="Authentication required"):
        super().__init__(message, status_code=401)


class AuthorizationError(APIError):
    """Ошибка авторизации"""
    
    def __init__(self, message="Access denied"):
        super().__init__(message, status_code=403)


class RateLimitError(APIError):
    """Превышен лимит запросов"""
    
    def __init__(self, message="Rate limit exceeded"):
        super().__init__(message, status_code=429)


def register_api_error_handlers(app):
    """Регистрация обработчиков для кастомных API ошибок"""
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        """Обработка кастомных API ошибок"""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    logger.info("API error handlers registered")
