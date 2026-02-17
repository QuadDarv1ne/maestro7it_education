"""
HTTP кэширование с поддержкой ETag и Cache-Control
"""
import hashlib
import json
from functools import wraps
from flask import request, make_response, current_app
from typing import Optional, Callable
import logging

logger = logging.getLogger(__name__)


def generate_etag(data: str) -> str:
    """Генерация ETag из данных"""
    return hashlib.md5(data.encode('utf-8'), usedforsecurity=False).hexdigest()  # nosec B324


def etag_cache(timeout: int = 300, vary_on: Optional[list] = None):
    """
    Декоратор для HTTP кэширования с ETag
    
    Args:
        timeout: Время кэширования в секундах
        vary_on: Список заголовков для Vary (например, ['Accept-Language', 'User-Agent'])
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Выполняем функцию
            response = func(*args, **kwargs)
            
            # Если это не успешный ответ, не кэшируем
            if not isinstance(response, tuple):
                response_obj = make_response(response)
            else:
                response_obj = make_response(*response)
            
            if response_obj.status_code != 200:
                return response_obj
            
            # Генерируем ETag
            data = response_obj.get_data(as_text=True)
            etag = generate_etag(data)
            
            # Проверяем If-None-Match
            if_none_match = request.headers.get('If-None-Match')
            if if_none_match == etag:
                # Данные не изменились
                response_obj = make_response('', 304)
                response_obj.headers['ETag'] = etag
                return response_obj
            
            # Устанавливаем заголовки кэширования
            response_obj.headers['ETag'] = etag
            response_obj.headers['Cache-Control'] = f'public, max-age={timeout}'
            
            if vary_on:
                response_obj.headers['Vary'] = ', '.join(vary_on)
            
            return response_obj
        return wrapper
    return decorator


def cache_control(max_age: int = 300, 
                 public: bool = True,
                 must_revalidate: bool = False,
                 no_cache: bool = False,
                 no_store: bool = False):
    """
    Декоратор для установки Cache-Control заголовков
    
    Args:
        max_age: Максимальное время кэширования в секундах
        public: Может ли кэш быть публичным
        must_revalidate: Требовать ревалидацию после истечения
        no_cache: Не кэшировать без ревалидации
        no_store: Не хранить в кэше вообще
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            
            if not isinstance(response, tuple):
                response_obj = make_response(response)
            else:
                response_obj = make_response(*response)
            
            # Формируем Cache-Control
            directives = []
            
            if no_store:
                directives.append('no-store')
            elif no_cache:
                directives.append('no-cache')
            else:
                directives.append('public' if public else 'private')
                directives.append(f'max-age={max_age}')
                
                if must_revalidate:
                    directives.append('must-revalidate')
            
            response_obj.headers['Cache-Control'] = ', '.join(directives)
            
            return response_obj
        return wrapper
    return decorator


def conditional_request(func: Callable) -> Callable:
    """
    Декоратор для поддержки условных запросов (If-Modified-Since, If-None-Match)
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Получаем заголовки условного запроса
        if_modified_since = request.headers.get('If-Modified-Since')
        if_none_match = request.headers.get('If-None-Match')
        
        # Выполняем функцию
        response = func(*args, **kwargs)
        
        if not isinstance(response, tuple):
            response_obj = make_response(response)
        else:
            response_obj = make_response(*response)
        
        # Проверяем условия
        last_modified = response_obj.headers.get('Last-Modified')
        etag = response_obj.headers.get('ETag')
        
        # If-None-Match имеет приоритет над If-Modified-Since
        if if_none_match and etag:
            if if_none_match == etag:
                return make_response('', 304)
        elif if_modified_since and last_modified:
            if if_modified_since == last_modified:
                return make_response('', 304)
        
        return response_obj
    return wrapper


class HTTPCacheMiddleware:
    """
    Middleware для автоматического HTTP кэширования
    """
    
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация middleware"""
        app.after_request(self.add_cache_headers)
        logger.info("HTTP Cache Middleware initialized")
    
    def add_cache_headers(self, response):
        """Добавление заголовков кэширования к ответам"""
        # Не кэшируем ошибки
        if response.status_code >= 400:
            response.headers['Cache-Control'] = 'no-store'
            return response
        
        # Не кэшируем POST, PUT, DELETE
        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            response.headers['Cache-Control'] = 'no-store'
            return response
        
        # Если заголовки уже установлены, не перезаписываем
        if 'Cache-Control' in response.headers:
            return response
        
        # Определяем стратегию кэширования по пути
        path = request.path
        
        # API endpoints - короткое кэширование
        if path.startswith('/api/'):
            if path.startswith('/api/tournaments'):
                response.headers['Cache-Control'] = 'public, max-age=300'  # 5 минут
            elif path.startswith('/api/users'):
                response.headers['Cache-Control'] = 'private, max-age=60'  # 1 минута
            else:
                response.headers['Cache-Control'] = 'public, max-age=60'
        
        # Статические файлы - долгое кэширование
        elif path.startswith('/static/'):
            response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'  # 1 год
        
        # HTML страницы - среднее кэширование
        elif response.content_type and 'text/html' in response.content_type:
            response.headers['Cache-Control'] = 'public, max-age=300, must-revalidate'
        
        # По умолчанию - не кэшируем
        else:
            response.headers['Cache-Control'] = 'no-cache'
        
        return response


def cache_key_from_request(prefix: str = 'view') -> str:
    """
    Генерация ключа кэша из параметров запроса
    
    Args:
        prefix: Префикс ключа
    
    Returns:
        Строка ключа кэша
    """
    # Базовый ключ из пути
    key_parts = [prefix, request.path]
    
    # Добавляем query параметры
    if request.args:
        args_str = '&'.join(f"{k}={v}" for k, v in sorted(request.args.items()))
        key_parts.append(hashlib.md5(args_str.encode()).hexdigest()[:8])
    
    # Добавляем заголовки (для Vary)
    vary_headers = ['Accept-Language', 'Accept-Encoding']
    for header in vary_headers:
        value = request.headers.get(header)
        if value:
            key_parts.append(hashlib.md5(value.encode()).hexdigest()[:4])
    
    return ':'.join(key_parts)


def cached_view(timeout: int = 300, key_prefix: str = 'view'):
    """
    Декоратор для кэширования view функций
    
    Args:
        timeout: Время кэширования в секундах
        key_prefix: Префикс ключа кэша
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            from app.utils.unified_cache import cache
            
            # Генерируем ключ кэша
            cache_key = cache_key_from_request(key_prefix)
            
            # Проверяем кэш
            cached_response = cache.get(cache_key)
            if cached_response:
                logger.debug(f"View cache hit: {cache_key}")
                return cached_response
            
            # Выполняем view
            response = func(*args, **kwargs)
            
            # Кэшируем только успешные ответы
            if isinstance(response, tuple):
                status_code = response[1] if len(response) > 1 else 200
            else:
                status_code = 200
            
            if status_code == 200:
                cache.set(cache_key, response, timeout)
                logger.debug(f"View cached: {cache_key}")
            
            return response
        return wrapper
    return decorator


# Вспомогательные функции
def invalidate_view_cache(path_pattern: str):
    """
    Инвалидировать кэш view по паттерну пути
    
    Args:
        path_pattern: Паттерн пути (например, '/api/tournaments/*')
    """
    from app.utils.unified_cache import cache
    
    pattern = f"view:{path_pattern}"
    cache.invalidate_by_pattern(pattern)
    logger.info(f"View cache invalidated: {path_pattern}")


def set_cache_headers(response, 
                     max_age: int = 300,
                     public: bool = True,
                     etag: Optional[str] = None):
    """
    Установить заголовки кэширования для response
    
    Args:
        response: Flask response объект
        max_age: Максимальное время кэширования
        public: Публичный или приватный кэш
        etag: ETag значение
    """
    cache_type = 'public' if public else 'private'
    response.headers['Cache-Control'] = f'{cache_type}, max-age={max_age}'
    
    if etag:
        response.headers['ETag'] = etag
    
    return response
