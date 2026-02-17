"""
Сканер безопасности для обнаружения уязвимостей
"""
import re
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)


class SecurityIssue:
    """Проблема безопасности"""
    
    def __init__(
        self,
        severity: str,
        category: str,
        description: str,
        location: Optional[str] = None,
        recommendation: Optional[str] = None
    ):
        self.severity = severity  # critical, high, medium, low
        self.category = category
        self.description = description
        self.location = location
        self.recommendation = recommendation
        self.timestamp = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'severity': self.severity,
            'category': self.category,
            'description': self.description,
            'location': self.location,
            'recommendation': self.recommendation,
            'timestamp': self.timestamp.isoformat()
        }


class SecurityScanner:
    """Сканер безопасности"""
    
    # SQL Injection паттерны
    SQL_INJECTION_PATTERNS = [
        r"(\bUNION\b.*\bSELECT\b)",
        r"(\bSELECT\b.*\bFROM\b.*\bWHERE\b)",
        r"(\bINSERT\b.*\bINTO\b.*\bVALUES\b)",
        r"(\bUPDATE\b.*\bSET\b)",
        r"(\bDELETE\b.*\bFROM\b)",
        r"(\bDROP\b.*\bTABLE\b)",
        r"(--|\#|\/\*)",
        r"(\bOR\b.*=.*)",
        r"(\bAND\b.*=.*)",
        r"('.*OR.*'.*=.*')",
    ]
    
    # XSS паттерны
    XSS_PATTERNS = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"onerror\s*=",
        r"onload\s*=",
        r"onclick\s*=",
        r"<iframe[^>]*>",
        r"<embed[^>]*>",
        r"<object[^>]*>",
    ]
    
    # Path Traversal паттерны
    PATH_TRAVERSAL_PATTERNS = [
        r"\.\./",
        r"\.\.\\",
        r"%2e%2e/",
        r"%2e%2e\\",
    ]
    
    # Command Injection паттерны
    COMMAND_INJECTION_PATTERNS = [
        r";\s*\w+",
        r"\|\s*\w+",
        r"&&\s*\w+",
        r"\$\(",
        r"`.*`",
    ]
    
    def __init__(self):
        self.issues = []
    
    def scan_sql_injection(self, text: str, location: str = None) -> List[SecurityIssue]:
        """Сканирование на SQL Injection"""
        issues = []
        
        for pattern in self.SQL_INJECTION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                issue = SecurityIssue(
                    severity='critical',
                    category='SQL Injection',
                    description=f'Potential SQL injection detected: {pattern}',
                    location=location,
                    recommendation='Use parameterized queries or ORM'
                )
                issues.append(issue)
                logger.warning(f"SQL Injection detected: {location}")
        
        return issues
    
    def scan_xss(self, text: str, location: str = None) -> List[SecurityIssue]:
        """Сканирование на XSS"""
        issues = []
        
        for pattern in self.XSS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                issue = SecurityIssue(
                    severity='high',
                    category='Cross-Site Scripting (XSS)',
                    description=f'Potential XSS detected: {pattern}',
                    location=location,
                    recommendation='Sanitize user input and use Content Security Policy'
                )
                issues.append(issue)
                logger.warning(f"XSS detected: {location}")
        
        return issues
    
    def scan_path_traversal(self, text: str, location: str = None) -> List[SecurityIssue]:
        """Сканирование на Path Traversal"""
        issues = []
        
        for pattern in self.PATH_TRAVERSAL_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                issue = SecurityIssue(
                    severity='high',
                    category='Path Traversal',
                    description=f'Potential path traversal detected: {pattern}',
                    location=location,
                    recommendation='Validate and sanitize file paths'
                )
                issues.append(issue)
                logger.warning(f"Path Traversal detected: {location}")
        
        return issues
    
    def scan_command_injection(self, text: str, location: str = None) -> List[SecurityIssue]:
        """Сканирование на Command Injection"""
        issues = []
        
        for pattern in self.COMMAND_INJECTION_PATTERNS:
            if re.search(pattern, text):
                issue = SecurityIssue(
                    severity='critical',
                    category='Command Injection',
                    description=f'Potential command injection detected: {pattern}',
                    location=location,
                    recommendation='Avoid executing shell commands with user input'
                )
                issues.append(issue)
                logger.warning(f"Command Injection detected: {location}")
        
        return issues
    
    def scan_weak_password(self, password: str) -> List[SecurityIssue]:
        """Проверка слабого пароля"""
        issues = []
        
        if len(password) < 8:
            issues.append(SecurityIssue(
                severity='medium',
                category='Weak Password',
                description='Password is too short (minimum 8 characters)',
                recommendation='Use at least 8 characters'
            ))
        
        if not re.search(r'[A-Z]', password):
            issues.append(SecurityIssue(
                severity='low',
                category='Weak Password',
                description='Password should contain uppercase letters',
                recommendation='Add uppercase letters'
            ))
        
        if not re.search(r'[a-z]', password):
            issues.append(SecurityIssue(
                severity='low',
                category='Weak Password',
                description='Password should contain lowercase letters',
                recommendation='Add lowercase letters'
            ))
        
        if not re.search(r'\d', password):
            issues.append(SecurityIssue(
                severity='low',
                category='Weak Password',
                description='Password should contain numbers',
                recommendation='Add numbers'
            ))
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            issues.append(SecurityIssue(
                severity='low',
                category='Weak Password',
                description='Password should contain special characters',
                recommendation='Add special characters'
            ))
        
        # Проверка на общие пароли
        common_passwords = [
            'password', '123456', '12345678', 'qwerty', 'abc123',
            'password123', 'admin', 'letmein', 'welcome', 'monkey'
        ]
        
        if password.lower() in common_passwords:
            issues.append(SecurityIssue(
                severity='critical',
                category='Weak Password',
                description='Password is too common',
                recommendation='Use a unique password'
            ))
        
        return issues
    
    def scan_sensitive_data_exposure(self, data: Dict[str, Any]) -> List[SecurityIssue]:
        """Проверка на утечку чувствительных данных"""
        issues = []
        
        sensitive_keys = [
            'password', 'secret', 'token', 'api_key', 'private_key',
            'credit_card', 'ssn', 'passport'
        ]
        
        for key, value in data.items():
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                if value and not self._is_hashed(str(value)):
                    issues.append(SecurityIssue(
                        severity='critical',
                        category='Sensitive Data Exposure',
                        description=f'Sensitive data "{key}" may be exposed',
                        location=key,
                        recommendation='Hash or encrypt sensitive data'
                    ))
        
        return issues
    
    def _is_hashed(self, value: str) -> bool:
        """Проверка, является ли значение хэшем"""
        # Проверяем длину (хэши обычно длинные)
        if len(value) < 32:
            return False
        
        # Проверяем на hex формат
        try:
            int(value, 16)
            return True
        except ValueError:
            pass
        
        # Проверяем на bcrypt формат
        if value.startswith('$2b$') or value.startswith('$2a$'):
            return True
        
        return False
    
    def scan_insecure_configuration(self, config: Dict[str, Any]) -> List[SecurityIssue]:
        """Проверка небезопасной конфигурации"""
        issues = []
        
        # Проверка DEBUG режима
        if config.get('DEBUG', False):
            issues.append(SecurityIssue(
                severity='high',
                category='Insecure Configuration',
                description='DEBUG mode is enabled',
                recommendation='Disable DEBUG in production'
            ))
        
        # Проверка SECRET_KEY
        secret_key = config.get('SECRET_KEY', '')
        if not secret_key or len(secret_key) < 32:
            issues.append(SecurityIssue(
                severity='critical',
                category='Insecure Configuration',
                description='SECRET_KEY is weak or missing',
                recommendation='Use a strong random SECRET_KEY (32+ characters)'
            ))
        
        # Проверка HTTPS
        if not config.get('SESSION_COOKIE_SECURE', False):
            issues.append(SecurityIssue(
                severity='medium',
                category='Insecure Configuration',
                description='SESSION_COOKIE_SECURE is not enabled',
                recommendation='Enable HTTPS and set SESSION_COOKIE_SECURE=True'
            ))
        
        return issues
    
    def scan_request(self, request_data: Dict[str, Any]) -> List[SecurityIssue]:
        """Комплексное сканирование запроса"""
        issues = []
        
        for key, value in request_data.items():
            if isinstance(value, str):
                # SQL Injection
                issues.extend(self.scan_sql_injection(value, f"request.{key}"))
                
                # XSS
                issues.extend(self.scan_xss(value, f"request.{key}"))
                
                # Path Traversal
                issues.extend(self.scan_path_traversal(value, f"request.{key}"))
                
                # Command Injection
                issues.extend(self.scan_command_injection(value, f"request.{key}"))
        
        return issues
    
    def generate_report(self, issues: List[SecurityIssue]) -> Dict[str, Any]:
        """Генерация отчета о безопасности"""
        if not issues:
            return {
                'status': 'secure',
                'total_issues': 0,
                'issues': []
            }
        
        # Группируем по severity
        by_severity = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': []
        }
        
        for issue in issues:
            by_severity[issue.severity].append(issue.to_dict())
        
        return {
            'status': 'vulnerable',
            'total_issues': len(issues),
            'by_severity': {
                'critical': len(by_severity['critical']),
                'high': len(by_severity['high']),
                'medium': len(by_severity['medium']),
                'low': len(by_severity['low'])
            },
            'issues': [issue.to_dict() for issue in issues],
            'timestamp': datetime.utcnow().isoformat()
        }


class SecurityMiddleware:
    """Middleware для автоматического сканирования запросов"""
    
    def __init__(self, app=None):
        self.scanner = SecurityScanner()
        self.app = app
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация с Flask приложением"""
        app.before_request(self.scan_request)
    
    def scan_request(self):
        """Сканирование входящего запроса"""
        from flask import request, jsonify
        
        # Собираем данные запроса
        request_data = {}
        
        # Query параметры
        request_data.update(request.args.to_dict())
        
        # Form данные
        if request.form:
            request_data.update(request.form.to_dict())
        
        # JSON данные
        if request.is_json:
            try:
                request_data.update(request.get_json())
            except (ValueError, TypeError, AttributeError):
                pass
        
        # Сканируем
        issues = self.scanner.scan_request(request_data)
        
        # Если найдены критические проблемы - блокируем
        critical_issues = [i for i in issues if i.severity == 'critical']
        
        if critical_issues:
            logger.error(f"Critical security issues detected: {len(critical_issues)}")
            return jsonify({
                'error': 'Security violation detected',
                'message': 'Your request has been blocked for security reasons'
            }), 403


# Глобальный экземпляр
security_scanner = SecurityScanner()
