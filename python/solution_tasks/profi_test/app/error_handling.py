# -*- coding: utf-8 -*-
"""
Модуль расширенной обработки ошибок для ПрофиТест
Предоставляет продвинутые возможности обработки исключений и логирования ошибок
"""
import traceback
import sys
from datetime import datetime
from functools import wraps
import logging
from flask import jsonify, request
from app import db


class ErrorSeverity:
    """Класс для определения уровней серьезности ошибок"""
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CRITICAL = 'critical'


class ErrorType:
    """Класс для определения типов ошибок"""
    VALIDATION_ERROR = 'validation_error'
    DATABASE_ERROR = 'database_error'
    AUTHENTICATION_ERROR = 'authentication_error'
    AUTHORIZATION_ERROR = 'authorization_error'
    NOT_FOUND_ERROR = 'not_found_error'
    BUSINESS_LOGIC_ERROR = 'business_logic_error'
    EXTERNAL_SERVICE_ERROR = 'external_service_error'
    SYSTEM_ERROR = 'system_error'


class AdvancedErrorHandler:
    """
    Расширенный обработчик ошибок для системы ПрофиТест.
    Обеспечивает централизованную обработку исключений с детальным логированием.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_handlers = {}
        self.register_default_handlers()
    
    def register_default_handlers(self):
        """Регистрирует обработчики по умолчанию для различных типов исключений"""
        # Обработчики для стандартных исключений Python
        self.register_handler(ValueError, self.handle_validation_error)
        self.register_handler(TypeError, self.handle_validation_error)
        self.register_handler(KeyError, self.handle_not_found_error)
        self.register_handler(PermissionError, self.handle_authorization_error)
        
        # Обработчики для Flask и SQLAlchemy
        try:
            from sqlalchemy.exc import SQLAlchemyError
            self.register_handler(SQLAlchemyError, self.handle_database_error)
        except ImportError:
            pass
        
        try:
            from flask_login import Unauthorized
            self.register_handler(Unauthorized, self.handle_authentication_error)
        except ImportError:
            pass
    
    def register_handler(self, exception_type, handler_func):
        """
        Регистрирует обработчик для конкретного типа исключения.
        
        Args:
            exception_type: Тип исключения
            handler_func: Функция-обработчик
        """
        self.error_handlers[exception_type] = handler_func
    
    def handle_exception(self, exception, context=None):
        """
        Обрабатывает исключение с учетом контекста.
        
        Args:
            exception: Исключение для обработки
            context: Дополнительный контекст (например, request data)
            
        Returns:
            dict: Обработанный результат ошибки
        """
        try:
            # Определяем тип исключения
            exception_type = type(exception)
            
            # Ищем специфичный обработчик
            handler = self._find_handler(exception_type)
            if handler:
                return handler(exception, context)
            
            # Если специфичный обработчик не найден, используем обработчик по умолчанию
            return self.handle_generic_error(exception, context)
            
        except Exception as handler_error:
            self.logger.error(f"Ошибка в обработчике исключений: {str(handler_error)}")
            return self.handle_generic_error(exception, context)
    
    def _find_handler(self, exception_type):
        """
        Находит подходящий обработчик для типа исключения.
        
        Args:
            exception_type: Тип исключения
            
        Returns:
            function: Найденный обработчик или None
        """
        # Прямое совпадение
        if exception_type in self.error_handlers:
            return self.error_handlers[exception_type]
        
        # Поиск по иерархии наследования
        for registered_type, handler in self.error_handlers.items():
            if issubclass(exception_type, registered_type):
                return handler
        
        return None
    
    def handle_validation_error(self, exception, context=None):
        """Обрабатывает ошибки валидации"""
        error_info = {
            'type': ErrorType.VALIDATION_ERROR,
            'severity': ErrorSeverity.MEDIUM,
            'message': str(exception),
            'code': 400,
            'timestamp': datetime.now(datetime.UTC).isoformat(),
            'details': {
                'field': getattr(exception, 'field', None),
                'value': getattr(exception, 'value', None)
            }
        }
        
        self._log_error(error_info, exception, context)
        return error_info
    
    def handle_database_error(self, exception, context=None):
        """Обрабатывает ошибки базы данных"""
        error_info = {
            'type': ErrorType.DATABASE_ERROR,
            'severity': ErrorSeverity.HIGH,
            'message': 'Ошибка базы данных',
            'code': 500,
            'timestamp': datetime.now(datetime.UTC).isoformat(),
            'details': {
                'db_error': str(exception),
                'error_code': getattr(exception, 'code', None)
            }
        }
        
        self._log_error(error_info, exception, context)
        return error_info
    
    def handle_authentication_error(self, exception, context=None):
        """Обрабатывает ошибки аутентификации"""
        error_info = {
            'type': ErrorType.AUTHENTICATION_ERROR,
            'severity': ErrorSeverity.MEDIUM,
            'message': 'Ошибка аутентификации',
            'code': 401,
            'timestamp': datetime.now(datetime.UTC).isoformat(),
            'details': {
                'reason': str(exception)
            }
        }
        
        self._log_error(error_info, exception, context)
        return error_info
    
    def handle_authorization_error(self, exception, context=None):
        """Обрабатывает ошибки авторизации"""
        error_info = {
            'type': ErrorType.AUTHORIZATION_ERROR,
            'severity': ErrorSeverity.HIGH,
            'message': 'Ошибка авторизации',
            'code': 403,
            'timestamp': datetime.now(datetime.UTC).isoformat(),
            'details': {
                'reason': str(exception),
                'required_permissions': getattr(exception, 'required_permissions', None)
            }
        }
        
        self._log_error(error_info, exception, context)
        return error_info
    
    def handle_not_found_error(self, exception, context=None):
        """Обрабатывает ошибки "не найдено" """
        error_info = {
            'type': ErrorType.NOT_FOUND_ERROR,
            'severity': ErrorSeverity.LOW,
            'message': 'Ресурс не найден',
            'code': 404,
            'timestamp': datetime.now(datetime.UTC).isoformat(),
            'details': {
                'resource': str(exception)
            }
        }
        
        self._log_error(error_info, exception, context)
        return error_info
    
    def handle_business_logic_error(self, exception, context=None):
        """Обрабатывает ошибки бизнес-логики"""
        error_info = {
            'type': ErrorType.BUSINESS_LOGIC_ERROR,
            'severity': ErrorSeverity.MEDIUM,
            'message': str(exception),
            'code': 422,  # Unprocessable Entity
            'timestamp': datetime.now(datetime.UTC).isoformat(),
            'details': {
                'business_rule': getattr(exception, 'rule', None),
                'context': getattr(exception, 'context', None)
            }
        }
        
        self._log_error(error_info, exception, context)
        return error_info
    
    def handle_external_service_error(self, exception, context=None):
        """Обрабатывает ошибки внешних сервисов"""
        error_info = {
            'type': ErrorType.EXTERNAL_SERVICE_ERROR,
            'severity': ErrorSeverity.HIGH,
            'message': 'Ошибка внешнего сервиса',
            'code': 502,  # Bad Gateway
            'timestamp': datetime.now(datetime.UTC).isoformat(),
            'details': {
                'service': getattr(exception, 'service', None),
                'error_details': str(exception)
            }
        }
        
        self._log_error(error_info, exception, context)
        return error_info
    
    def handle_generic_error(self, exception, context=None):
        """Обрабатывает общие ошибки"""
        error_info = {
            'type': ErrorType.SYSTEM_ERROR,
            'severity': ErrorSeverity.CRITICAL,
            'message': 'Внутренняя ошибка сервера',
            'code': 500,
            'timestamp': datetime.now(datetime.UTC).isoformat(),
            'details': {
                'exception_type': type(exception).__name__,
                'exception_message': str(exception)
            }
        }
        
        self._log_error(error_info, exception, context)
        return error_info
    
    def _log_error(self, error_info, exception, context):
        """
        Логирует информацию об ошибке.
        
        Args:
            error_info: Информация об ошибке
            exception: Исключение
            context: Контекст ошибки
        """
        try:
            # Подготовка данных для логирования
            log_data = {
                'error_type': error_info['type'],
                'severity': error_info['severity'],
                'message': error_info['message'],
                'timestamp': error_info['timestamp'],
                'details': error_info['details'],
                'exception_traceback': self._get_traceback(exception)
            }
            
            # Добавление контекста запроса если доступен
            if context:
                log_data['context'] = context
            elif request:
                log_data['request_context'] = {
                    'url': request.url,
                    'method': request.method,
                    'remote_addr': request.remote_addr,
                    'user_agent': request.user_agent.string,
                    'headers': dict(request.headers)
                }
            
            # Логирование с соответствующим уровнем
            severity = error_info['severity']
            if severity == ErrorSeverity.CRITICAL:
                self.logger.critical(f"Критическая ошибка: {log_data}")
            elif severity == ErrorSeverity.HIGH:
                self.logger.error(f"Высокая серьезность ошибки: {log_data}")
            elif severity == ErrorSeverity.MEDIUM:
                self.logger.warning(f"Средняя серьезность ошибки: {log_data}")
            else:
                self.logger.info(f"Низкая серьезность ошибки: {log_data}")
                
        except Exception as log_error:
            self.logger.error(f"Ошибка при логировании исключения: {str(log_error)}")
    
    def _get_traceback(self, exception):
        """
        Получает трассировку стека для исключения.
        
        Args:
            exception: Исключение
            
        Returns:
            str: Трассировка стека
        """
        try:
            return traceback.format_exception(type(exception), exception, exception.__traceback__)
        except Exception:
            return "Не удалось получить трассировку стека"
    
    def create_error_response(self, error_info):
        """
        Создает HTTP ответ для ошибки.
        
        Args:
            error_info: Информация об ошибке
            
        Returns:
            tuple: (response_dict, status_code)
        """
        response = {
            'success': False,
            'error': {
                'type': error_info['type'],
                'message': error_info['message'],
                'severity': error_info['severity'],
                'timestamp': error_info['timestamp'],
                'details': error_info['details']
            }
        }
        
        return response, error_info['code']
    
    def wrap_api_function(self, func):
        """
        Декоратор для оборачивания API функций в обработку ошибок.
        
        Args:
            func: Функция для оборачивания
            
        Returns:
            function: Обернутая функция
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Обработка исключения
                context = {
                    'function_name': func.__name__,
                    'args': args,
                    'kwargs': kwargs
                }
                
                error_info = self.handle_exception(e, context)
                response, status_code = self.create_error_response(error_info)
                return jsonify(response), status_code
        
        return wrapper
    
    def handle_flask_error(self, error):
        """
        Обработчик ошибок для Flask приложения.
        
        Args:
            error: Ошибка Flask
            
        Returns:
            tuple: (response, status_code)
        """
        try:
            # Определяем тип ошибки Flask
            if hasattr(error, 'code'):
                status_code = error.code
            else:
                status_code = 500
            
            # Создаем соответствующую ошибку
            if status_code == 400:
                error_info = self.handle_validation_error(error)
            elif status_code == 401:
                error_info = self.handle_authentication_error(error)
            elif status_code == 403:
                error_info = self.handle_authorization_error(error)
            elif status_code == 404:
                error_info = self.handle_not_found_error(error)
            else:
                error_info = self.handle_generic_error(error)
            
            response, _ = self.create_error_response(error_info)
            return jsonify(response), status_code
            
        except Exception as handler_error:
            self.logger.error(f"Ошибка в обработчике Flask ошибок: {str(handler_error)}")
            # Возврат минимального ответа в случае критической ошибки обработчика
            return jsonify({
                'success': False,
                'error': {
                    'type': 'SYSTEM_ERROR',
                    'message': 'Внутренняя ошибка обработчика ошибок',
                    'severity': 'critical'
                }
            }), 500


# Глобальный экземпляр обработчика ошибок
error_handler = AdvancedErrorHandler()