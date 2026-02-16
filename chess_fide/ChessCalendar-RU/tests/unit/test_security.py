"""
Тесты системы безопасности
"""
import pytest
from datetime import datetime, timedelta
from app.utils.security import (
    PasswordManager, RateLimiter, JWTManager, TwoFactorAuth
)
from app.models.audit_log import AuditLog, LoginAttempt, TwoFactorSecret


class TestPasswordManager:
    """Тесты менеджера паролей"""
    
    def test_hash_password(self):
        """Тест хеширования пароля"""
        password = "SecurePassword123"
        hashed = PasswordManager.hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 0
    
    def test_verify_password(self):
        """Тест проверки пароля"""
        password = "SecurePassword123"
        hashed = PasswordManager.hash_password(password)
        
        assert PasswordManager.verify_password(hashed, password)
        assert not PasswordManager.verify_password(hashed, "WrongPassword")
    
    def test_password_strength_validation(self):
        """Тест валидации надежности пароля"""
        # Слабые пароли
        weak_passwords = [
            ("short", False),
            ("12345678", False),
            ("password", False),
            ("NoDigits", False),
            ("nouppercas3", False),
        ]
        
        for password, expected in weak_passwords:
            is_valid, _ = PasswordManager.validate_password_strength(password)
            assert is_valid == expected
        
        # Сильный пароль
        is_valid, _ = PasswordManager.validate_password_strength("SecurePass123!")
        assert is_valid


class TestRateLimiter:
    """Тесты rate limiter"""
    
    def test_rate_limit_memory(self):
        """Тест rate limiting через память"""
        limiter = RateLimiter(redis_client=None)
        key = "test_key"
        
        # Первые 5 попыток должны пройти
        for i in range(5):
            is_limited, remaining = limiter.is_rate_limited(key, max_attempts=5, window=60)
            assert not is_limited
            assert remaining == 4 - i
        
        # 6-я попытка должна быть заблокирована
        is_limited, remaining = limiter.is_rate_limited(key, max_attempts=5, window=60)
        assert is_limited
        assert remaining == 0
    
    def test_rate_limit_reset(self):
        """Тест сброса rate limit"""
        limiter = RateLimiter(redis_client=None)
        key = "test_key"
        
        # Достигаем лимита
        for _ in range(5):
            limiter.is_rate_limited(key, max_attempts=5, window=60)
        
        # Сбрасываем
        limiter.reset(key)
        
        # Должно снова работать
        is_limited, remaining = limiter.is_rate_limited(key, max_attempts=5, window=60)
        assert not is_limited
        assert remaining == 4


class TestJWTManager:
    """Тесты JWT менеджера"""
    
    def test_generate_token(self, app):
        """Тест генерации токена"""
        with app.app_context():
            token = JWTManager.generate_token(
                user_id=1,
                username="testuser",
                is_admin=False,
                expires_in=3600
            )
            
            assert token is not None
            assert isinstance(token, str)
            assert len(token) > 0
    
    def test_verify_token(self, app):
        """Тест проверки токена"""
        with app.app_context():
            token = JWTManager.generate_token(
                user_id=1,
                username="testuser",
                is_admin=False,
                expires_in=3600
            )
            
            payload = JWTManager.verify_token(token)
            
            assert payload is not None
            assert payload['user_id'] == 1
            assert payload['username'] == "testuser"
            assert payload['is_admin'] is False
    
    def test_expired_token(self, app):
        """Тест истекшего токена"""
        with app.app_context():
            token = JWTManager.generate_token(
                user_id=1,
                username="testuser",
                is_admin=False,
                expires_in=-1  # Уже истек
            )
            
            payload = JWTManager.verify_token(token)
            assert payload is None
    
    def test_refresh_token(self, app):
        """Тест refresh токена"""
        with app.app_context():
            token = JWTManager.generate_refresh_token(user_id=1)
            
            assert token is not None
            
            payload = JWTManager.verify_token(token)
            assert payload is not None
            assert payload['user_id'] == 1
            assert payload['type'] == 'refresh'


class TestTwoFactorAuth:
    """Тесты двухфакторной аутентификации"""
    
    def test_generate_secret(self):
        """Тест генерации секрета"""
        secret = TwoFactorAuth.generate_secret()
        
        assert secret is not None
        assert len(secret) > 0
    
    def test_generate_qr_code_url(self):
        """Тест генерации QR кода"""
        secret = TwoFactorAuth.generate_secret()
        url = TwoFactorAuth.generate_qr_code_url("testuser", secret)
        
        assert url.startswith("otpauth://totp/")
        assert "testuser" in url
        assert secret in url
    
    def test_verify_totp(self):
        """Тест проверки TOTP кода"""
        try:
            import pyotp
            
            secret = pyotp.random_base32()
            totp = pyotp.TOTP(secret)
            code = totp.now()
            
            # Правильный код
            assert TwoFactorAuth.verify_totp(secret, code)
            
            # Неправильный код
            assert not TwoFactorAuth.verify_totp(secret, "000000")
        
        except ImportError:
            pytest.skip("pyotp not installed")


class TestAuditLog:
    """Тесты audit log"""
    
    def test_create_audit_log(self, db_session, admin_user):
        """Тест создания audit log"""
        log = AuditLog(
            user_id=admin_user.id,
            action='create',
            resource='tournament',
            resource_id=1,
            details={'name': 'Test Tournament'},
            ip_address='127.0.0.1',
            timestamp=datetime.utcnow()
        )
        
        db_session.add(log)
        db_session.commit()
        
        assert log.id is not None
        assert log.user_id == admin_user.id
        assert log.action == 'create'
    
    def test_get_user_actions(self, db_session, admin_user):
        """Тест получения действий пользователя"""
        # Создаем несколько логов
        for i in range(5):
            log = AuditLog(
                user_id=admin_user.id,
                action='view',
                resource='tournament',
                resource_id=i,
                timestamp=datetime.utcnow()
            )
            db_session.add(log)
        
        db_session.commit()
        
        logs = AuditLog.get_user_actions(admin_user.id, limit=10)
        assert len(logs) >= 5
    
    def test_search_audit_log(self, db_session, admin_user):
        """Тест поиска в audit log"""
        # Создаем логи с разными действиями
        actions = ['create', 'update', 'delete']
        for action in actions:
            log = AuditLog(
                user_id=admin_user.id,
                action=action,
                resource='tournament',
                timestamp=datetime.utcnow()
            )
            db_session.add(log)
        
        db_session.commit()
        
        # Поиск по действию
        logs = AuditLog.search({'action': 'create'}, limit=10)
        assert len(logs) >= 1
        assert all(log.action == 'create' for log in logs)


class TestLoginAttempt:
    """Тесты попыток входа"""
    
    def test_log_attempt(self, db_session):
        """Тест логирования попытки входа"""
        attempt = LoginAttempt.log_attempt(
            username='testuser',
            ip_address='127.0.0.1',
            success=True,
            user_agent='Test Agent'
        )
        
        assert attempt.id is not None
        assert attempt.username == 'testuser'
        assert attempt.success is True
    
    def test_get_failed_attempts(self, db_session):
        """Тест получения неудачных попыток"""
        username = 'testuser'
        ip_address = '127.0.0.1'
        
        # Создаем несколько неудачных попыток
        for _ in range(3):
            LoginAttempt.log_attempt(username, ip_address, False)
        
        # Одна успешная
        LoginAttempt.log_attempt(username, ip_address, True)
        
        count = LoginAttempt.get_failed_attempts(username, ip_address, minutes=15)
        assert count == 3


class TestTwoFactorSecret:
    """Тесты секретов 2FA"""
    
    def test_create_two_factor_secret(self, db_session, regular_user):
        """Тест создания секрета 2FA"""
        secret = TwoFactorSecret(
            user_id=regular_user.id,
            secret='test_secret',
            enabled=False
        )
        
        db_session.add(secret)
        db_session.commit()
        
        assert secret.id is not None
        assert secret.user_id == regular_user.id
        assert secret.enabled is False
    
    def test_generate_backup_codes(self, db_session, regular_user):
        """Тест генерации резервных кодов"""
        secret = TwoFactorSecret(
            user_id=regular_user.id,
            secret='test_secret',
            enabled=True
        )
        
        db_session.add(secret)
        db_session.commit()
        
        codes = secret.generate_backup_codes(count=5)
        
        assert len(codes) == 5
        assert all(isinstance(code, str) for code in codes)
        assert secret.backup_codes is not None
        assert len(secret.backup_codes) == 5
    
    def test_verify_backup_code(self, db_session, regular_user):
        """Тест проверки резервного кода"""
        secret = TwoFactorSecret(
            user_id=regular_user.id,
            secret='test_secret',
            enabled=True
        )
        
        db_session.add(secret)
        db_session.commit()
        
        codes = secret.generate_backup_codes(count=3)
        
        # Проверяем правильный код
        assert secret.verify_backup_code(codes[0])
        
        # Код должен быть удален после использования
        assert len(secret.backup_codes) == 2
        
        # Повторная проверка того же кода должна провалиться
        assert not secret.verify_backup_code(codes[0])
        
        # Неправильный код
        assert not secret.verify_backup_code("WRONGCODE")
