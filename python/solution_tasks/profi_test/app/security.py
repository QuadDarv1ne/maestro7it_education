# -*- coding: utf-8 -*-
"""
Модуль безопасности для приложения ProfiTest
Содержит реализации защиты от DDoS, rate limiting и API защиты
"""

import time
import threading
from collections import defaultdict, deque
from flask import request, jsonify
from functools import wraps
import re

class RateLimiter:
    """Реализация ограничения частоты запросов"""
    
    def __init__(self):
        self.requests = defaultdict(deque)
        self.lock = threading.Lock()
        # Конфигурация лимитов
        self.limits = {
            'default': {'requests': 5, 'window': 60},    # 5 запросов в минуту для тестов
            'strict': {'requests': 10, 'window': 60},    # 10 запросов в минуту
            'api': {'requests': 1000, 'window': 3600},   # 1000 запросов в час
        }
    
    def check_rate_limit(self, key, limit_type='default'):
        """
        Проверяет ограничение частоты запросов для заданного ключа
        
        Args:
            key: Ключ для идентификации клиента (IP, user_id, etc.)
            limit_type: Тип ограничения ('default', 'strict', 'api')
            
        Returns:
            bool: True если запрос разрешен, False если заблокирован
        """
        with self.lock:
            now = time.time()
            limit_config = self.limits.get(limit_type, self.limits['default'])
            window = limit_config['window']
            max_requests = limit_config['requests']
            
            # Очищаем старые запросы
            if key in self.requests:
                # Удаляем запросы старше окна
                while self.requests[key] and now - self.requests[key][0] > window:
                    self.requests[key].popleft()
            
            # Проверяем лимит
            if len(self.requests[key]) >= max_requests:
                return False
            
            # Добавляем текущий запрос
            self.requests[key].append(now)
            return True
    
    def get_client_key(self, request_obj=None):
        """
        Генерирует ключ клиента на основе IP и User-Agent
        
        Args:
            request_obj: Объект запроса Flask
            
        Returns:
            str: Уникальный ключ клиента
        """
        if request_obj is None:
            request_obj = request
        
        # Получаем IP адрес
        if request_obj.headers.get('X-Forwarded-For'):
            ip = request_obj.headers.get('X-Forwarded-For').split(',')[0].strip()
        elif request_obj.headers.get('X-Real-IP'):
            ip = request_obj.headers.get('X-Real-IP')
        else:
            ip = request_obj.remote_addr
        
        # Добавляем User-Agent для дополнительной идентификации
        user_agent = request_obj.headers.get('User-Agent', 'unknown')
        return f"{ip}:{user_agent[:50]}"  # Ограничиваем длину User-Agent

class APIProtector:
    """Защита API от вредоносных запросов"""
    
    def __init__(self):
        self.blocked_ips = set()
        self.suspicious_patterns = [
            r'(DROP|DELETE|UPDATE|INSERT)\s+(TABLE|FROM|INTO)',
            r'(\||&|;)\s*(rm|del|kill)',
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'(union|select|from|where)\s+(select|from|where)',
            r'\.\./',
            r'etc/passwd',
            r'cmd\.exe',
        ]
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.suspicious_patterns]
    
    def _check_suspicious_data(self, data):
        """
        Проверяет данные на наличие подозрительных паттернов
        
        Args:
            data: Данные для проверки (строка или словарь)
            
        Returns:
            bool: True если данные подозрительны
        """
        if isinstance(data, dict):
            # Рекурсивно проверяем все значения в словаре
            for value in data.values():
                if self._check_suspicious_data(value):
                    return True
            return False
        elif isinstance(data, str):
            # Проверяем строку на подозрительные паттерны
            for pattern in self.compiled_patterns:
                if pattern.search(data):
                    return True
            return False
        else:
            return False
    
    def is_ip_blocked(self, ip):
        """Проверяет, заблокирован ли IP адрес"""
        return ip in self.blocked_ips
    
    def block_ip(self, ip):
        """Блокирует IP адрес"""
        self.blocked_ips.add(ip)
    
    def unblock_ip(self, ip):
        """Разблокирует IP адрес"""
        self.blocked_ips.discard(ip)
    
    def protect_api(self, f):
        """
        Декоратор для защиты API endpoint'ов
        
        Args:
            f: Функция endpoint'а
            
        Returns:
            Обернутая функция с защитой
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Проверяем IP блокировку
            client_ip = request.remote_addr
            if self.is_ip_blocked(client_ip):
                return jsonify({
                    'error': 'Access denied',
                    'message': 'Your IP has been blocked due to suspicious activity'
                }), 403
            
            # Проверяем подозрительные данные в запросе
            if request.is_json:
                try:
                    json_data = request.get_json()
                    if self._check_suspicious_data(json_data):
                        self.block_ip(client_ip)
                        return jsonify({
                            'error': 'Malicious content detected',
                            'message': 'Request blocked due to security concerns'
                        }), 400
                except Exception:
                    pass  # Если не можем распарсить JSON, продолжаем
            
            # Проверяем query параметры
            if self._check_suspicious_data(dict(request.args)):
                self.block_ip(client_ip)
                return jsonify({
                    'error': 'Malicious content detected',
                    'message': 'Request blocked due to security concerns'
                }), 400
            
            return f(*args, **kwargs)
        return decorated_function

# Глобальные экземпляры
rate_limiter = RateLimiter()
api_protector = APIProtector()

# Экспортируем классы и экземпляры
__all__ = ['RateLimiter', 'APIProtector', 'rate_limiter', 'api_protector']