# -*- coding: utf-8 -*-
"""
Модуль продвинутой безопасности и аудита для ПрофиТест
Обеспечивает многоуровневую защиту, аудит безопасности и защиту от различных видов атак
"""
import logging
import hashlib
import secrets
import jwt
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from collections import defaultdict, deque
import time
import ipaddress
from functools import wraps
from dataclasses import dataclass
import re
import bcrypt
from flask import request, g, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import threading
from enum import Enum

logger = logging.getLogger(__name__)

class SecurityLevel(Enum):
    """Уровни безопасности"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AttackType(Enum):
    """Типы атак"""
    BRUTE_FORCE = "brute_force"
    XSS = "xss"
    SQL_INJECTION = "sql_injection"
    CSRF = "csrf"
    SESSION_HIJACKING = "session_hijacking"
    DDOS = "ddos"
    RECONNAISSANCE = "reconnaissance"

@dataclass
class SecurityEvent:
    """Событие безопасности"""
    timestamp: str
    event_type: str
    severity: SecurityLevel
    ip_address: str
    user_id: Optional[int]
    description: str
    details: Dict[str, Any]

class AdvancedSecurityManager:
    """Продвинутый менеджер безопасности с многоуровневой защитой"""
    
    def __init__(self, app=None):
        self.app = app
        self.security_events = deque(maxlen=10000)
        self.suspicious_activities = deque(maxlen=1000)
        self.security_policies = {}
        self.rate_limits = {}
        self.ip_reputation = defaultdict(int)
        self.user_risk_scores = defaultdict(float)
        self.session_tokens = {}
        self.security_headers = {}
        self.lock = threading.Lock()
        
        # Конфигурация безопасности
        self.config = {
            'password_policy': {
                'min_length': 12,
                'require_uppercase': True,
                'require_lowercase': True,
                'require_digits': True,
                'require_special_chars': True,
                'max_age_days': 90
            },
            'rate_limiting': {
                'login_attempts': 5,  # за 15 минут
                'failed_attempts_window': 900,  # 15 минут
                'lockout_duration': 3600,  # 1 час
                'request_rate': 100  # за 5 минут
            },
            'session_security': {
                'token_entropy': 256,
                'max_idle_time': 1800,  # 30 минут
                'regenerate_interval': 900,  # 15 минут
                'secure_cookies': True,
                'same_site_policy': 'Strict'
            },
            'input_validation': {
                'xss_patterns': [
                    r'<script[^>]*>.*?</script>',
                    r'javascript:',
                    r'on\w+\s*=',
                    r'<iframe[^>]*>.*?</iframe>'
                ],
                'sql_patterns': [
                    r'\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)\b',
                    r'(UNION|EXEC|DECLARE|OPEN)',
                    r'(\-\-|\#|/\*|\*/)'
                ]
            },
            'threat_detection': {
                'suspicious_user_agents': [
                    'sqlmap', 'nikto', 'nessus', 'nmap', 'hydra',
                    'medusa', 'patator', 'crowbar', 'brutus'
                ],
                'suspicious_paths': [
                    r'/etc/passwd', r'c:\\windows\\', r'\.\./', r'%2e%2e%2f',
                    r'admin/', r'phpmyadmin/', r'wp-admin/'
                ]
            }
        }
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация с Flask приложением"""
        self.app = app
        self.setup_security_middleware()
        self.load_security_policies()
        logger.info("Продвинутый менеджер безопасности инициализирован")
    
    def setup_security_middleware(self):
        """Настройка middleware безопасности"""
        # Добавляем безопасные заголовки
        @self.app.after_request
        def add_security_headers(response):
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'DENY'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'"
            return response
        
        # Middleware для проверки безопасности
        @self.app.before_request
        def security_check():
            self.check_request_security()
    
    def load_security_policies(self):
        """Загрузка политик безопасности"""
        self.security_policies = {
            'password_strength': self.validate_password_strength,
            'input_sanitization': self.sanitize_input,
            'access_control': self.check_access_control,
            'rate_limiting': self.check_rate_limit
        }
    
    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """Проверка надежности пароля"""
        policy = self.config['password_policy']
        result = {
            'valid': True,
            'strength_score': 0,
            'requirements_met': [],
            'requirements_missing': []
        }
        
        requirements = {
            'length': len(password) >= policy['min_length'],
            'uppercase': bool(re.search(r'[A-Z]', password)) if policy['require_uppercase'] else True,
            'lowercase': bool(re.search(r'[a-z]', password)) if policy['require_lowercase'] else True,
            'digits': bool(re.search(r'\d', password)) if policy['require_digits'] else True,
            'special_chars': bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)) if policy['require_special_chars'] else True
        }
        
        for req, met in requirements.items():
            if met:
                result['requirements_met'].append(req)
                result['strength_score'] += 1
            else:
                result['requirements_missing'].append(req)
        
        result['valid'] = all(requirements.values())
        result['strength_percentage'] = (result['strength_score'] / len(requirements)) * 100
        
        return result
    
    def hash_password(self, password: str) -> str:
        """Хеширование пароля с использованием bcrypt"""
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Проверка пароля"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def sanitize_input(self, input_data: str) -> str:
        """Санитизация входных данных"""
        # Удаление потенциально опасных символов
        sanitized = input_data.strip()
        
        # Проверка на XSS
        for pattern in self.config['input_validation']['xss_patterns']:
            if re.search(pattern, sanitized, re.IGNORECASE):
                self.log_security_event(
                    AttackType.XSS,
                    SecurityLevel.HIGH,
                    f"Обнаружена XSS-атака: {sanitized[:100]}"
                )
                # Удаляем подозрительный контент
                sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        # Проверка на SQL-инъекции
        for pattern in self.config['input_validation']['sql_patterns']:
            if re.search(pattern, sanitized, re.IGNORECASE):
                self.log_security_event(
                    AttackType.SQL_INJECTION,
                    SecurityLevel.HIGH,
                    f"Обнаружена SQL-инъекция: {sanitized[:100]}"
                )
                # Экранируем подозрительный контент
                sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        return sanitized
    
    def check_request_security(self):
        """Проверка безопасности запроса"""
        # Проверка IP-адреса
        ip_address = request.remote_addr
        if self.is_suspicious_ip(ip_address):
            self.log_security_event(
                AttackType.RECONNAISSANCE,
                SecurityLevel.MEDIUM,
                f"Подозрительный IP-адрес: {ip_address}"
            )
        
        # Проверка User-Agent
        user_agent = request.headers.get('User-Agent', '')
        if self.is_suspicious_user_agent(user_agent):
            self.log_security_event(
                AttackType.RECONNAISSANCE,
                SecurityLevel.LOW,
                f"Подозрительный User-Agent: {user_agent}"
            )
        
        # Проверка путей
        path = request.path
        if self.is_suspicious_path(path):
            self.log_security_event(
                AttackType.RECONNAISSANCE,
                SecurityLevel.MEDIUM,
                f"Подозрительный путь: {path}"
            )
    
    def is_suspicious_ip(self, ip_address: str) -> bool:
        """Проверка IP-адреса на подозрительность"""
        try:
            ip_obj = ipaddress.ip_address(ip_address)
            # Проверяем, является ли IP-адресом локальным или частным
            if ip_obj.is_private or ip_obj.is_loopback:
                return False
            # Проверяем репутацию IP
            return self.ip_reputation[ip_address] > 5
        except ValueError:
            return True
    
    def is_suspicious_user_agent(self, user_agent: str) -> bool:
        """Проверка User-Agent на подозрительность"""
        suspicious_agents = self.config['threat_detection']['suspicious_user_agents']
        return any(agent.lower() in user_agent.lower() for agent in suspicious_agents)
    
    def is_suspicious_path(self, path: str) -> bool:
        """Проверка пути на подозрительность"""
        suspicious_patterns = self.config['threat_detection']['suspicious_paths']
        return any(re.search(pattern, path, re.IGNORECASE) for pattern in suspicious_patterns)
    
    def check_rate_limit(self, identifier: str, limit: int = 100, window: int = 300) -> bool:
        """Проверка ограничения частоты запросов"""
        current_time = time.time()
        
        if identifier not in self.rate_limits:
            self.rate_limits[identifier] = []
        
        # Очистка старых записей
        self.rate_limits[identifier] = [
            timestamp for timestamp in self.rate_limits[identifier]
            if current_time - timestamp < window
        ]
        
        # Проверка лимита
        if len(self.rate_limits[identifier]) >= limit:
            self.log_security_event(
                AttackType.DDOS,
                SecurityLevel.HIGH,
                f"Превышен лимит запросов для {identifier}"
            )
            return False
        
        # Регистрация запроса
        self.rate_limits[identifier].append(current_time)
        return True
    
    def check_access_control(self, user_id: int, resource: str, action: str) -> bool:
        """Проверка контроля доступа"""
        # Здесь должна быть реализация RBAC или ABAC
        # Пока возвращаем True для демонстрации
        return True
    
    def generate_secure_token(self, entropy_bits: int = 256) -> str:
        """Генерация безопасного токена"""
        token_bytes = secrets.token_bytes(entropy_bits // 8)
        return hashlib.sha256(token_bytes).hexdigest()
    
    def create_session_token(self, user_id: int) -> str:
        """Создание безопасного токена сессии"""
        token = self.generate_secure_token(self.config['session_security']['token_entropy'])
        expiration = time.time() + self.config['session_security']['max_idle_time']
        
        self.session_tokens[token] = {
            'user_id': user_id,
            'created_at': time.time(),
            'expires_at': expiration,
            'last_activity': time.time()
        }
        
        return token
    
    def validate_session_token(self, token: str) -> bool:
        """Проверка токена сессии"""
        if token not in self.session_tokens:
            return False
        
        session_data = self.session_tokens[token]
        
        # Проверка срока действия
        if time.time() > session_data['expires_at']:
            del self.session_tokens[token]
            return False
        
        # Обновление времени последней активности
        session_data['last_activity'] = time.time()
        
        return True
    
    def log_security_event(self, attack_type: AttackType, severity: SecurityLevel, 
                          description: str, **details) -> SecurityEvent:
        """Логирование события безопасности"""
        event = SecurityEvent(
            timestamp=datetime.utcnow().isoformat(),
            event_type=attack_type.value,
            severity=severity,
            ip_address=request.remote_addr if request else 'unknown',
            user_id=getattr(g, 'user_id', None),
            description=description,
            details=details
        )
        
        with self.lock:
            self.security_events.append(event)
            
            # Увеличиваем счетчик репутации IP при подозрительной активности
            if request and hasattr(request, 'remote_addr'):
                self.ip_reputation[request.remote_addr] += 1
        
        logger.warning(f"Security Event: {attack_type.value} - {description}")
        return event
    
    def detect_brute_force(self, identifier: str, max_attempts: int = 5, 
                          window_seconds: int = 900) -> bool:
        """Обнаружение атак методом перебора"""
        current_time = time.time()
        
        if identifier not in self.rate_limits:
            self.rate_limits[identifier] = []
        
        # Очистка старых попыток
        self.rate_limits[identifier] = [
            timestamp for timestamp in self.rate_limits[identifier]
            if current_time - timestamp < window_seconds
        ]
        
        # Проверка количества попыток
        if len(self.rate_limits[identifier]) >= max_attempts:
            self.log_security_event(
                AttackType.BRUTE_FORCE,
                SecurityLevel.HIGH,
                f"Обнаружена атака методом перебора для {identifier}"
            )
            return True
        
        return False
    
    def get_security_report(self) -> Dict[str, Any]:
        """Получение отчета по безопасности"""
        with self.lock:
            recent_events = list(self.security_events)[-50:]
            
            # Подсчет по типам
            event_counts = defaultdict(int)
            severity_counts = defaultdict(int)
            
            for event in recent_events:
                event_counts[event.event_type] += 1
                severity_counts[event.severity.value] += 1
            
            # Активные IP-адреса
            active_ips = set(event.ip_address for event in recent_events if event.ip_address != 'unknown')
            
            return {
                'timestamp': datetime.utcnow().isoformat(),
                'total_security_events': len(self.security_events),
                'recent_events': len(recent_events),
                'event_counts': dict(event_counts),
                'severity_distribution': dict(severity_counts),
                'active_suspicious_ips': list(active_ips)[:20],  # первые 20
                'ip_reputation_summary': dict(list(self.ip_reputation.items())[:20]),
                'rate_limit_status': {
                    identifier: len(attempts) 
                    for identifier, attempts in list(self.rate_limits.items())[:10]
                }
            }
    
    def get_threat_intelligence(self) -> Dict[str, Any]:
        """Получение информации о угрозах"""
        security_report = self.get_security_report()
        
        # Анализ паттернов атак
        threat_patterns = {}
        for event_type, count in security_report['event_counts'].items():
            if count > 5:  # Если больше 5 событий одного типа
                threat_patterns[event_type] = count
        
        return {
            'threat_level': self._calculate_threat_level(security_report),
            'active_threats': threat_patterns,
            'recommended_actions': self._get_recommendations(threat_patterns),
            'security_score': self._calculate_security_score(security_report)
        }
    
    def _calculate_threat_level(self, report: Dict[str, Any]) -> str:
        """Расчет уровня угрозы"""
        high_severity = report['severity_distribution'].get('high', 0)
        critical_severity = report['severity_distribution'].get('critical', 0)
        
        if critical_severity > 0:
            return 'CRITICAL'
        elif high_severity > 10:
            return 'HIGH'
        elif high_severity > 5:
            return 'MEDIUM'
        elif high_severity > 0:
            return 'LOW'
        else:
            return 'NONE'
    
    def _get_recommendations(self, threats: Dict[str, int]) -> List[str]:
        """Получение рекомендаций по безопасности"""
        recommendations = []
        
        if 'brute_force' in threats:
            recommendations.append("Установить более строгие ограничения на попытки входа")
        if 'xss' in threats:
            recommendations.append("Усилить фильтрацию входных данных")
        if 'sql_injection' in threats:
            recommendations.append("Проверить подготовленные выражения SQL")
        if 'ddos' in threats:
            recommendations.append("Настроить DDoS-защиту на уровне сети")
        
        return recommendations or ["Поддерживать текущий уровень безопасности"]
    
    def _calculate_security_score(self, report: Dict[str, Any]) -> float:
        """Расчет рейтинга безопасности"""
        total_events = report['total_security_events']
        high_critical_events = (
            report['severity_distribution'].get('high', 0) +
            report['severity_distribution'].get('critical', 0)
        )
        
        if total_events == 0:
            return 100.0
        
        # Чем больше высоких/критических событий, тем ниже рейтинг
        score = max(0, 100 - (high_critical_events / total_events * 100))
        return round(score, 2)

# Глобальный экземпляр
security_manager = AdvancedSecurityManager()

def register_security_commands(app):
    """Регистрация CLI команд безопасности"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('security-report')
    @with_appcontext
    def show_security_report():
        """Показать отчет по безопасности"""
        report = security_manager.get_security_report()
        click.echo("Отчет по безопасности системы:")
        click.echo(f"  Всего событий: {report['total_security_events']}")
        click.echo(f"  Последних событий: {report['recent_events']}")
        click.echo(f"  Активные подозрительные IP: {len(report['active_suspicious_ips'])}")
        
        click.echo("\nРаспределение по типам:")
        for event_type, count in report['event_counts'].items():
            click.echo(f"  {event_type}: {count}")
        
        click.echo("\nРаспределение по уровню:")
        for severity, count in report['severity_distribution'].items():
            click.echo(f"  {severity}: {count}")
    
    @app.cli.command('threat-intel')
    @with_appcontext
    def show_threat_intelligence():
        """Показать информацию о угрозах"""
        intel = security_manager.get_threat_intelligence()
        click.echo("Информация о угрозах:")
        click.echo(f"  Уровень угрозы: {intel['threat_level']}")
        click.echo(f"  Рейтинг безопасности: {intel['security_score']}/100")
        
        if intel['active_threats']:
            click.echo("\nАктивные угрозы:")
            for threat, count in intel['active_threats'].items():
                click.echo(f"  {threat}: {count} событий")
        
        if intel['recommended_actions']:
            click.echo("\nРекомендации:")
            for action in intel['recommended_actions']:
                click.echo(f"  - {action}")

def require_security_check(f):
    """Декоратор для обязательной проверки безопасности"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Проверка безопасности запроса
        security_manager.check_request_security()
        
        # Проверка лимитов
        identifier = get_remote_address()
        if not security_manager.check_rate_limit(identifier):
            logger.warning(f"Превышен лимит запросов для {identifier}")
            return {"error": "Превышен лимит запросов"}, 429
        
        return f(*args, **kwargs)
    
    return decorated_function

def require_authentication(f):
    """Декоратор для обязательной аутентификации"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Проверка токена сессии
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token or not security_manager.validate_session_token(token):
            logger.warning(f"Неавторизованный доступ к защищенному ресурсу: {request.endpoint}")
            return {"error": "Требуется авторизация"}, 401
        
        return f(*args, **kwargs)
    
    return decorated_function

def log_security_event(event_type: str, severity: SecurityLevel = SecurityLevel.MEDIUM):
    """Декоратор для логирования событий безопасности"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                result = f(*args, **kwargs)
                return result
            except Exception as e:
                security_manager.log_security_event(
                    AttackType.SESSION_HIJACKING if 'session' in f.__name__.lower() else AttackType.RECONNAISSANCE,
                    severity,
                    f"Ошибка в {f.__name__}: {str(e)}",
                    function=f.__name__,
                    args_count=len(args)
                )
                raise
        return decorated_function
    return decorator