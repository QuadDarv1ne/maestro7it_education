# -*- coding: utf-8 -*-
"""
Модуль расширенной безопасности для ПрофиТест
Предоставляет продвинутые возможности аутентификации, авторизации и защиты
"""
import hashlib
import hmac
import secrets
import bcrypt
import jwt
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, Dict, Any, List
import logging
from functools import wraps
from flask import request, session, current_app
from flask_login import current_user


class SecurityLevel(Enum):
    """Уровни безопасности"""
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    MAXIMUM = 'maximum'


class AttackType(Enum):
    """Типы атак"""
    BRUTE_FORCE = 'brute_force'
    SESSION_HIJACKING = 'session_hijacking'
    CSRF = 'csrf'
    XSS = 'xss'
    SQL_INJECTION = 'sql_injection'
    RATE_LIMITING = 'rate_limiting'


class AdvancedSecurityManager:
    """
    Расширенный менеджер безопасности для системы ПрофиТест.
    Обеспечивает многоуровневую защиту приложения.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.failed_attempts = {}  # Словарь для отслеживания неудачных попыток
        self.session_tokens = {}   # Словарь для управления сессиями
        self.rate_limits = {}      # Словарь для ограничения частоты запросов
        self.security_config = {
            'max_login_attempts': 5,
            'lockout_duration': 300,  # 5 минут
            'session_timeout': 3600,  # 1 час
            'password_min_length': 8,
            'require_special_chars': True,
            'require_numbers': True,
            'require_uppercase': True,
            'rate_limit_requests': 100,
            'rate_limit_window': 60,  # 1 минута
            'security_level': SecurityLevel.HIGH
        }
    
    def hash_password(self, password: str) -> str:
        """
        Хэширует пароль с использованием bcrypt.
        
        Args:
            password: Пароль для хэширования
            
        Returns:
            str: Хэшированный пароль
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """
        Проверяет пароль против хэша.
        
        Args:
            password: Введенный пароль
            hashed: Хэшированный пароль
            
        Returns:
            bool: True если пароли совпадают
        """
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except Exception:
            return False
    
    def generate_secure_token(self, length: int = 32) -> str:
        """
        Генерирует криптографически безопасный токен.
        
        Args:
            length: Длина токена
            
        Returns:
            str: Сгенерированный токен
        """
        return secrets.token_urlsafe(length)
    
    def generate_csrf_token(self) -> str:
        """
        Генерирует CSRF токен.
        
        Returns:
            str: CSRF токен
        """
        if 'csrf_token' not in session:
            session['csrf_token'] = self.generate_secure_token()
        return session['csrf_token']
    
    def validate_csrf_token(self, token: str) -> bool:
        """
        Проверяет CSRF токен.
        
        Args:
            token: Токен для проверки
            
        Returns:
            bool: True если токен действителен
        """
        return token and 'csrf_token' in session and hmac.compare_digest(token, session['csrf_token'])
    
    def check_login_attempts(self, identifier: str) -> bool:
        """
        Проверяет количество неудачных попыток входа.
        
        Args:
            identifier: Идентификатор (email, username, IP)
            
        Returns:
            bool: True если аккаунт разблокирован
        """
        if identifier not in self.failed_attempts:
            return True
        
        attempt_info = self.failed_attempts[identifier]
        if datetime.now(datetime.UTC) < attempt_info['reset_time']:
            if attempt_info['count'] >= self.security_config['max_login_attempts']:
                return False
        
        # Сброс счетчика если прошло достаточно времени
        if datetime.now(datetime.UTC) >= attempt_info['reset_time']:
            del self.failed_attempts[identifier]
        
        return True
    
    def record_failed_login(self, identifier: str):
        """
        Фиксирует неудачную попытку входа.
        
        Args:
            identifier: Идентификатор (email, username, IP)
        """
        if identifier not in self.failed_attempts:
            self.failed_attempts[identifier] = {
                'count': 0,
                'reset_time': datetime.now(datetime.UTC) + timedelta(seconds=self.security_config['lockout_duration'])
            }
        
        self.failed_attempts[identifier]['count'] += 1
        self.logger.warning(f"Неудачная попытка входа для {identifier}, попытка #{self.failed_attempts[identifier]['count']}")
    
    def reset_login_attempts(self, identifier: str):
        """
        Сбрасывает счетчик неудачных попыток входа.
        
        Args:
            identifier: Идентификатор (email, username, IP)
        """
        if identifier in self.failed_attempts:
            del self.failed_attempts[identifier]
    
    def is_rate_limited(self, identifier: str) -> bool:
        """
        Проверяет, превышено ли ограничение частоты запросов.
        
        Args:
            identifier: Идентификатор (IP, user_id)
            
        Returns:
            bool: True если лимит превышен
        """
        if identifier not in self.rate_limits:
            self.rate_limits[identifier] = {
                'requests': 0,
                'window_start': datetime.now(datetime.UTC)
            }
        
        rate_info = self.rate_limits[identifier]
        time_passed = (datetime.now(datetime.UTC) - rate_info['window_start']).seconds
        
        if time_passed >= self.security_config['rate_limit_window']:
            # Сброс окна ограничения
            rate_info['requests'] = 1
            rate_info['window_start'] = datetime.now(datetime.UTC)
            return False
        
        rate_info['requests'] += 1
        
        if rate_info['requests'] > self.security_config['rate_limit_requests']:
            self.logger.warning(f"Превышен лимит запросов для {identifier}")
            return True
        
        return False
    
    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """
        Проверяет надежность пароля.
        
        Args:
            password: Пароль для проверки
            
        Returns:
            dict: Результат проверки
        """
        result = {
            'valid': True,
            'errors': [],
            'strength': 0  # 0-100
        }
        
        # Проверка длины
        if len(password) < self.security_config['password_min_length']:
            result['errors'].append(f'Пароль должен быть не менее {self.security_config["password_min_length"]} символов')
            result['valid'] = False
        
        # Проверка наличия чисел
        if self.security_config['require_numbers'] and not any(c.isdigit() for c in password):
            result['errors'].append('Пароль должен содержать хотя бы одну цифру')
            result['valid'] = False
        
        # Проверка наличия заглавных букв
        if self.security_config['require_uppercase'] and not any(c.isupper() for c in password):
            result['errors'].append('Пароль должен содержать хотя бы одну заглавную букву')
            result['valid'] = False
        
        # Проверка наличия специальных символов
        if self.security_config['require_special_chars']:
            special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            if not any(c in special_chars for c in password):
                result['errors'].append('Пароль должен содержать хотя бы один специальный символ')
                result['valid'] = False
        
        # Вычисление силы пароля
        strength = 0
        if len(password) >= 8:
            strength += 25
        if len(password) >= 12:
            strength += 25
        if any(c.isdigit() for c in password):
            strength += 15
        if any(c.isupper() for c in password) and any(c.islower() for c in password):
            strength += 15
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            strength += 20
        
        result['strength'] = min(strength, 100)
        
        return result
    
    def sanitize_input(self, input_str: str, max_length: int = 1000) -> str:
        """
        Санитизирует пользовательский ввод.
        
        Args:
            input_str: Входная строка
            max_length: Максимальная длина
            
        Returns:
            str: Очищенная строка
        """
        if input_str is None:
            return ""
        
        # Обрезка по длине
        input_str = input_str[:max_length]
        
        # Удаление потенциально опасных символов
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '%', '{', '}']
        for char in dangerous_chars:
            input_str = input_str.replace(char, '')
        
        return input_str
    
    def generate_jwt_token(self, user_id: int, expires_in: int = 3600) -> str:
        """
        Генерирует JWT токен для пользователя.
        
        Args:
            user_id: ID пользователя
            expires_in: Время жизни токена в секундах
            
        Returns:
            str: JWT токен
        """
        payload = {
            'user_id': user_id,
            'exp': datetime.now(datetime.UTC) + timedelta(seconds=expires_in),
            'iat': datetime.now(datetime.UTC)
        }
        
        secret = current_app.config.get('SECRET_KEY', 'fallback_secret')
        return jwt.encode(payload, secret, algorithm='HS256')
    
    def verify_jwt_token(self, token: str) -> Optional[int]:
        """
        Проверяет JWT токен и возвращает ID пользователя.
        
        Args:
            token: JWT токен
            
        Returns:
            int: ID пользователя или None если токен недействителен
        """
        try:
            secret = current_app.config.get('SECRET_KEY', 'fallback_secret')
            payload = jwt.decode(token, secret, algorithms=['HS256'])
            return payload.get('user_id')
        except jwt.ExpiredSignatureError:
            self.logger.warning("JWT токен просрочен")
            return None
        except jwt.InvalidTokenError:
            self.logger.warning("Недействительный JWT токен")
            return None
    
    def create_session_token(self, user_id: int) -> str:
        """
        Создает токен сессии.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            str: Токен сессии
        """
        token = self.generate_secure_token()
        self.session_tokens[token] = {
            'user_id': user_id,
            'created_at': datetime.now(datetime.UTC),
            'last_activity': datetime.now(datetime.UTC)
        }
        return token
    
    def validate_session_token(self, token: str) -> bool:
        """
        Проверяет токен сессии.
        
        Args:
            token: Токен сессии
            
        Returns:
            bool: True если токен действителен
        """
        if token not in self.session_tokens:
            return False
        
        session_info = self.session_tokens[token]
        time_since_last_activity = datetime.now(datetime.UTC) - session_info['last_activity']
        
        if time_since_last_activity.total_seconds() > self.security_config['session_timeout']:
            # Удаляем просроченную сессию
            del self.session_tokens[token]
            return False
        
        # Обновляем время последней активности
        session_info['last_activity'] = datetime.now(datetime.UTC)
        return True
    
    def get_user_from_session_token(self, token: str) -> Optional[int]:
        """
        Получает ID пользователя из токена сессии.
        
        Args:
            token: Токен сессии
            
        Returns:
            int: ID пользователя или None
        """
        if self.validate_session_token(token):
            return self.session_tokens[token]['user_id']
        return None
    
    def destroy_session_token(self, token: str):
        """
        Уничтожает токен сессии.
        
        Args:
            token: Токен сессии
        """
        if token in self.session_tokens:
            del self.session_tokens[token]
    
    def detect_suspicious_activity(self, user_id: int, activity_type: str, ip_address: str = None) -> bool:
        """
        Обнаруживает подозрительную активность пользователя.
        
        Args:
            user_id: ID пользователя
            activity_type: Тип активности
            ip_address: IP-адрес пользователя
            
        Returns:
            bool: True если активность подозрительна
        """
        # Здесь может быть реализована логика обнаружения подозрительной активности
        # Например, необычные часы активности, необычные IP-адреса и т.д.
        
        # Заглушка для демонстрации
        if activity_type == 'login_from_new_device':
            self.logger.info(f"Подозрительная активность: пользователь {user_id} вошел с нового устройства")
            return True
        
        return False
    
    def log_security_event(self, event_type: AttackType, severity: str, details: Dict[str, Any]):
        """
        Логирует событие безопасности.
        
        Args:
            event_type: Тип события
            severity: Уровень серьезности
            details: Детали события
        """
        event = {
            'timestamp': datetime.now(datetime.UTC).isoformat(),
            'type': event_type.value,
            'severity': severity,
            'details': details
        }
        
        if severity == 'critical':
            self.logger.critical(f"Критическое событие безопасности: {event}")
        elif severity == 'high':
            self.logger.error(f"Событие безопасности высокого уровня: {event}")
        elif severity == 'medium':
            self.logger.warning(f"Событие безопасности среднего уровня: {event}")
        else:
            self.logger.info(f"Событие безопасности низкого уровня: {event}")
    
    def security_check_decorator(self, require_auth: bool = True, min_security_level: SecurityLevel = SecurityLevel.MEDIUM):
        """
        Декоратор для проверки безопасности.
        
        Args:
            require_auth: Требовать аутентификацию
            min_security_level: Минимальный уровень безопасности
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Проверка уровня безопасности
                if self.security_config['security_level'].value < min_security_level.value:
                    self.logger.warning(f"Недостаточный уровень безопасности для доступа к {func.__name__}")
                    return {'error': 'Недостаточный уровень безопасности'}, 403
                
                # Проверка аутентификации
                if require_auth:
                    if not current_user or not current_user.is_authenticated:
                        self.logger.warning(f"Попытка неавторизованного доступа к {func.__name__}")
                        return {'error': 'Требуется аутентификация'}, 401
                
                # Проверка CSRF токена для POST запросов
                if request.method in ['POST', 'PUT', 'DELETE']:
                    csrf_token = request.headers.get('X-CSRF-Token') or request.form.get('csrf_token')
                    if not self.validate_csrf_token(csrf_token):
                        self.logger.warning(f"Недействительный CSRF токен для {func.__name__}")
                        return {'error': 'Недействительный CSRF токен'}, 403
                
                # Проверка ограничения частоты запросов
                client_ip = request.remote_addr
                if self.is_rate_limited(client_ip):
                    self.logger.warning(f"Превышен лимит запросов от {client_ip} для {func.__name__}")
                    return {'error': 'Слишком много запросов'}, 429
                
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    def get_security_report(self) -> Dict[str, Any]:
        """
        Получает отчет о безопасности.
        
        Returns:
            dict: Отчет о безопасности
        """
        return {
            'timestamp': datetime.now(datetime.UTC).isoformat(),
            'security_level': self.security_config['security_level'].value,
            'failed_login_attempts': len(self.failed_attempts),
            'active_sessions': len(self.session_tokens),
            'rate_limited_requests': sum(1 for v in self.rate_limits.values() 
                                      if v['requests'] > self.security_config['rate_limit_requests']),
            'config': {
                'max_login_attempts': self.security_config['max_login_attempts'],
                'session_timeout': self.security_config['session_timeout'],
                'rate_limit_requests': self.security_config['rate_limit_requests']
            }
        }


# Глобальный экземпляр менеджера безопасности
security_manager = AdvancedSecurityManager()