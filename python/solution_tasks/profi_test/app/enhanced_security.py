"""
Расширенная безопасность с хэшированием паролей Argon2 и поддержкой 2FA
"""
import argon2
import pyotp
import qrcode
import io
import base64
import hashlib
import secrets
from datetime import datetime, timedelta
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class EnhancedSecurityManager:
    """Продвинутый менеджер безопасности с современным хэшированием паролей и 2FA"""
    
    def __init__(self, app=None):
        self.app = app
        self.ph = None
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация менеджера безопасности с Flask приложением"""
        self.app = app
        
        # Инициализация хэшера паролей Argon2
        self.ph = argon2.PasswordHasher(
            time_cost=3,        # Количество итераций
            memory_cost=65536,  # Использование памяти в KB (64MB)
            parallelism=4,      # Количество параллельных потоков
            hash_len=32,        # Длина хэша в байтах
            salt_len=16         # Длина соли в байтах
        )
        
        logger.info("Продвинутый менеджер безопасности инициализирован с Argon2")
    
    def hash_password(self, password: str) -> str:
        """Хэширование пароля с использованием Argon2"""
        if not self.ph:
            raise RuntimeError("Менеджер безопасности не инициализирован")
        
        try:
            return self.ph.hash(password)
        except Exception as e:
            logger.error(f"Хэширование пароля не удалось: {e}")
            raise
    
    def verify_password(self, hash_str: str, password: str) -> bool:
        """Проверка пароля против хэша Argon2"""
        if not self.ph:
            raise RuntimeError("Менеджер безопасности не инициализирован")
        
        try:
            self.ph.verify(hash_str, password)
            return True
        except argon2.exceptions.VerifyMismatchError:
            return False
        except Exception as e:
            logger.error(f"Проверка пароля не удалась: {e}")
            return False
    
    def needs_rehash(self, hash_str: str) -> bool:
        """Проверка необходимости перехэширования пароля с обновленными параметрами"""
        if not self.ph:
            raise RuntimeError("Менеджер безопасности не инициализирован")
        
        try:
            return self.ph.check_needs_rehash(hash_str)
        except Exception as e:
            logger.error(f"Проверка необходимости перехэширования не удалась: {e}")
            return False
    
    def generate_totp_secret(self) -> str:
        """Генерация секрета TOTP для 2FA"""
        return pyotp.random_base32()
    
    def generate_totp_uri(self, secret: str, username: str, issuer: str = "ProfiTest") -> str:
        """Генерация URI TOTP для генерации QR-кода"""
        return pyotp.totp.TOTP(secret).provisioning_uri(
            name=username,
            issuer_name=issuer
        )
    
    def generate_qr_code(self, uri: str) -> str:
        """Генерация QR-кода в виде base64 data URL"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Конвертация в base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    def verify_totp(self, secret: str, token: str) -> bool:
        """Проверка TOTP токена"""
        try:
            totp = pyotp.TOTP(secret)
            return totp.verify(token, valid_window=1)  # Разрешить 1 окно допуска
        except Exception as e:
            logger.error(f"Проверка TOTP не удалась: {e}")
            return False
    
    def generate_backup_codes(self, count: int = 10) -> list:
        """Генерация резервных кодов для восстановления 2FA"""
        codes = []
        for _ in range(count):
            code = secrets.token_urlsafe(16)[:16]  # 16-символьные коды
            codes.append(code)
        return codes
    
    def hash_backup_code(self, code: str) -> str:
        """Хэширование резервного кода для безопасного хранения"""
        return hashlib.sha256(code.encode()).hexdigest()
    
    def verify_backup_code(self, hashed_code: str, input_code: str) -> bool:
        """Проверка резервного кода против хэшированной версии"""
        return hashlib.sha256(input_code.encode()).hexdigest() == hashed_code
    
    def generate_secure_token(self, length: int = 32) -> str:
        """Генерация криптографически безопасного токена"""
        return secrets.token_urlsafe(length)
    
    def generate_csrf_token(self) -> str:
        """Генерация токена защиты CSRF"""
        return self.generate_secure_token(32)
    
    def secure_compare(self, a: str, b: str) -> bool:
        """Сравнение строк во времени константы для предотвращения атак по времени"""
        return secrets.compare_digest(a, b)
    
    def get_security_config(self) -> Dict[str, Any]:
        """Получение текущей конфигурации безопасности"""
        return {
            'argon2_params': {
                'time_cost': 3,
                'memory_cost': 65536,
                'parallelism': 4,
                'hash_len': 32,
                'salt_len': 16
            },
            'totp_window': 1,
            'backup_codes_count': 10
        }

# Глобальный экземпляр
enhanced_security = EnhancedSecurityManager()

# Flask CLI команды для управления безопасностью
def register_security_commands(app):
    """Регистрация CLI команд управления безопасностью"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('security-config')
    @with_appcontext
    def show_security_config():
        """Показать текущую конфигурацию безопасности"""
        config = enhanced_security.get_security_config()
        click.echo("Конфигурация безопасности:")
        for key, value in config.items():
            click.echo(f"  {key}: {value}")
    
    @app.cli.command('generate-2fa-secret')
    @with_appcontext
    def generate_2fa_secret():
        """Сгенерировать новый секрет 2FA"""
        secret = enhanced_security.generate_totp_secret()
        click.echo(f"Секрет 2FA: {secret}")
        click.echo("Используйте это с приложением аутентификатора")
    
    @app.cli.command('hash-password')
    @click.argument('password')
    @with_appcontext
    def hash_password_cli(password):
        """Хэшировать пароль с использованием Argon2"""
        try:
            hashed = enhanced_security.hash_password(password)
            click.echo(f"Хэшированный пароль: {hashed}")
        except Exception as e:
            click.echo(f"Ошибка: {e}")