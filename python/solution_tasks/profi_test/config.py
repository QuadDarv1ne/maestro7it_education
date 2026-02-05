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
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'redis')
    CACHE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', '300'))
    CACHE_THRESHOLD = int(os.environ.get('CACHE_THRESHOLD', '1000'))
    
    @classmethod
    def get_db_engine_options(cls):
        """Возвращает параметры подключения к базе данных в зависимости от типа БД"""
        database_uri = os.environ.get('DATABASE_URL') or cls.SQLALCHEMY_DATABASE_URI
        
        # Если используется SQLite, не применяем параметры пула
        if database_uri.startswith('sqlite:'):
            from sqlalchemy.pool import StaticPool
            return {
                'poolclass': StaticPool,
                'connect_args': {
                    'check_same_thread': False
                }
            }
        else:
            # Для других баз данных (PostgreSQL, MySQL) используем пул соединений
            return {
                'pool_size': int(os.environ.get('DB_POOL_SIZE', '10')),
                'pool_recycle': int(os.environ.get('DB_POOL_RECYCLE', '300')),
                'pool_pre_ping': True,
                'max_overflow': int(os.environ.get('DB_MAX_OVERFLOW', '20')),
                'pool_timeout': int(os.environ.get('DB_POOL_TIMEOUT', '30')),
            }
    
    # Настройки пула соединений с базой данных
    # Значение будет установлено после определения класса
    
    # Настройки Celery для фоновых задач
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    
    # Настройки ограничения частоты запросов
    RATELIMIT_STORAGE_URL = os.environ.get('RATELIMIT_STORAGE_URL', 'redis://localhost:6379/1')
    
    # Настройки производительности
    PERF_MONITORING_ENABLED = os.environ.get('PERF_MONITORING_ENABLED', 'true').lower() == 'true'
    PERF_MONITORING_INTERVAL = int(os.environ.get('PERF_MONITORING_INTERVAL', '30'))
    
    # Настройки логирования производительности
    PERF_LOG_LEVEL = os.environ.get('PERF_LOG_LEVEL', 'INFO')
    PERF_LOG_FILE = os.environ.get('PERF_LOG_FILE', 'performance.log')
    
    # Настройки асинхронной обработки
    ASYNC_TASK_QUEUE = os.environ.get('ASYNC_TASK_QUEUE', 'celery')
    WORKER_CONCURRENCY = int(os.environ.get('WORKER_CONCURRENCY', '4'))
    
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
    
    # Используем подходящие параметры движка для тестов
    # Определяем после создания класса
    
    # Отключаем планировщик задач в тестах
    SCHEDULER_ENABLED = False
    
    # Отключаем медленные компоненты
    DISABLE_ML_MODELS = True
    DISABLE_EXTERNAL_APIS = True
    
    # Ускоряем работу сессий
    PRESERVE_CONTEXT_ON_EXCEPTION = False

# Инициализируем параметры пула соединений после определения классов
Config.SQLALCHEMY_ENGINE_OPTIONS = Config.get_db_engine_options()
TestConfig.SQLALCHEMY_ENGINE_OPTIONS = {
    'poolclass': __import__('sqlalchemy.pool').pool.StaticPool,
    'connect_args': {
        'check_same_thread': False
    }
}