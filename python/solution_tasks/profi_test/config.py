import os
from datetime import timedelta

class Config:
    """Класс конфигурации приложения"""
    # Секретный ключ для Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # Настройки базы данных
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///profi_test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Настройки сессий
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Настройки электронной почты (опционально)
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # API ключи (опционально)
    HH_API_KEY = os.environ.get('HH_API_KEY')
    SUPERJOB_API_KEY = os.environ.get('SUPERJOB_API_KEY')
    
    # Настройки кэширования
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_THRESHOLD = 1000
    
    # Настройки безопасности
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_SECURE = False  # Установите в True для HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Настройки логирования
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'app.log')
    
    # Настройки производительности
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    SEND_FILE_MAX_AGE_DEFAULT = 600  # 10 minutes cache
    
    # Настройки API
    API_RATE_LIMIT = '100/hour'
    API_VERSION = 'v1'
    API_ENABLE_CORS = True
    
    # Настройки планировщика задач
    SCHEDULER_ENABLED = True
    SCHEDULER_JOBSTORES = {
        'default': {
            'type': 'sqlalchemy',
            'url': SQLALCHEMY_DATABASE_URI
        }
    }
    SCHEDULER_EXECUTORS = {
        'default': {
            'type': 'threadpool',
            'max_workers': 20
        }
    }
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 3
    }
    SCHEDULER_API_ENABLED = True

class TestConfig(Config):
    """Конфигурация для тестирования"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    CACHE_TYPE = 'simple'
    SERVER_NAME = 'localhost.localdomain'
    SECRET_KEY = 'test-secret-key'
    
    # Отключаем планировщик задач в тестах
    SCHEDULER_ENABLED = False
    
    # Отключаем медленные компоненты
    DISABLE_ML_MODELS = True
    DISABLE_EXTERNAL_APIS = True
    
    # Ускоряем работу сессий
    PRESERVE_CONTEXT_ON_EXCEPTION = False