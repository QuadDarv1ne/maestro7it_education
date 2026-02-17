#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Централизованная обработка ошибок
"""

import logging
import traceback
from functools import wraps
from flask import jsonify, render_template, request
from werkzeug.exceptions import HTTPException

logger = logging.getLogger('chess_calendar')


def register_error_handlers(app):
    """
    Регистрация обработчиков ошибок для Flask приложения
    
    Args:
        app: Flask приложение
    """
    
    @app.errorhandler(400)
    def bad_request(error):
        """Обработка ошибки 400 Bad Request"""
        logger.warning(f"Bad request: {request.url} - {error}")
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Bad Request',
                'message': str(error),
                'status': 400
            }), 400
        
        return render_template('errors/400.html', error=error), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        """Обработка ошибки 401 Unauthorized"""
        logger.warning(f"Unauthorized access: {request.url}")
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Authentication required',
                'status': 401
            }), 401
        
        return render_template('errors/401.html'), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        """Обработка ошибки 403 Forbidden"""
        logger.warning(f"Forbidden access: {request.url}")
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Forbidden',
                'message': 'Access denied',
                'status': 403
            }), 403
        
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(404)
    def not_found(error):
        """Обработка ошибки 404 Not Found"""
        logger.info(f"Page not found: {request.url}")
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Not Found',
                'message': 'Resource not found',
                'status': 404
            }), 404
        
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        """Обработка ошибки 429 Too Many Requests"""
        logger.warning(f"Rate limit exceeded: {request.remote_addr} - {request.url}")
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Too Many Requests',
                'message': 'Rate limit exceeded. Please try again later.',
                'status': 429
            }), 429
        
        return render_template('errors/429.html'), 429
    
    @app.errorhandler(500)
    def internal_error(error):
        """Обработка ошибки 500 Internal Server Error"""
        logger.error(f"Internal server error: {request.url}")
        logger.error(traceback.format_exc())
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred',
                'status': 500
            }), 500
        
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(503)
    def service_unavailable(error):
        """Обработка ошибки 503 Service Unavailable"""
        logger.error(f"Service unavailable: {request.url}")
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Service Unavailable',
                'message': 'Service temporarily unavailable',
                'status': 503
            }), 503
        
        return render_template('errors/503.html'), 503
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Обработка всех необработанных исключений"""
        # Пропускаем HTTP исключения (они обрабатываются выше)
        if isinstance(error, HTTPException):
            return error
        
        logger.error(f"Unhandled exception: {request.url}")
        logger.error(traceback.format_exc())
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred',
                'status': 500
            }), 500
        
        return render_template('errors/500.html'), 500
    
    logger.info("Error handlers registered")


def handle_errors(default_message="An error occurred"):
    """
    Декоратор для обработки ошибок в функциях
    
    Args:
        default_message: Сообщение по умолчанию при ошибке
    
    Example:
        @handle_errors("Failed to fetch tournaments")
        def get_tournaments():
            # код
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {e}")
                logger.error(traceback.format_exc())
                raise
        return wrapper
    return decorator


def safe_execute(func, default=None, log_error=True):
    """
    Безопасное выполнение функции с обработкой ошибок
    
    Args:
        func: Функция для выполнения
        default: Значение по умолчанию при ошибке
        log_error: Логировать ли ошибку
    
    Returns:
        Результат функции или default при ошибке
    
    Example:
        result = safe_execute(lambda: risky_operation(), default=[])
    """
    try:
        return func()
    except Exception as e:
        if log_error:
            logger.error(f"Error in safe_execute: {e}")
            logger.error(traceback.format_exc())
        return default
