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