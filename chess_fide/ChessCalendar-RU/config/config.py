import os
import secrets

class Config:
    # Генерируем случайный SECRET_KEY если не задан через переменную окружения
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///chess_calendar.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Настройки пула подключений
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'max_overflow': 40,
        'pool_timeout': 30
    }
    
    FIDE_CALENDAR_URL = 'https://calendar.fide.com/calendar.php'
    CFR_URL = 'https://ruchess.ru/'
    
    # Настройки Redis для кэширования
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # Настройки Celery для фоновых задач
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/0'
    
    # Настройки сессий
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Настройки CORS для API
    CORS_HEADERS = 'Content-Type'
    
    # Email уведомления
    EMAIL_NOTIFICATIONS_ENABLED = os.environ.get('EMAIL_NOTIFICATIONS_ENABLED', 'False').lower() == 'true'
    EMAIL_FROM = os.environ.get('EMAIL_FROM', 'noreply@chesscalendar.ru')
    
    # SMTP настройки (опционально)
    SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
    SMTP_USER = os.environ.get('SMTP_USER', '')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')