"""
Улучшенная система логирования для Simple HR
Поддержка структурированных логов, ротации файлов, различных уровней логирования
"""

import logging
import logging.handlers
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class StructuredFormatter(logging.Formatter):
    """
    Форматтер для структурированных логов в JSON формате.
    Удобен для парсинга и анализа логов автоматическими системами.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Добавляем информацию об исключении, если есть
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # Добавляем дополнительные поля, если они были переданы
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
        if hasattr(record, 'ip_address'):
            log_data['ip_address'] = record.ip_address
        
        return json.dumps(log_data, ensure_ascii=False)


class ColoredFormatter(logging.Formatter):
    """
    Форматтер с цветовым выделением для консольного вывода.
    Помогает быстро идентифицировать уровень важности сообщения.
    """
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record: logging.LogRecord) -> str:
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        return super().format(record)


def setup_logging(app):
    """
    Настройка системы логирования для Flask приложения.
    
    Создает:
    - Ротируемые файлы логов для общих сообщений
    - Отдельный файл для ошибок
    - Структурированные логи в JSON
    - Цветной вывод в консоль для разработки
    """
    
    # Создаем директорию для логов
    log_dir = Path(app.root_path).parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    # Получаем корневой логгер приложения
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if app.debug else logging.INFO)
    
    # Очищаем существующие обработчики
    logger.handlers.clear()
    
    # 1. Ротируемый файл для всех логов (текстовый формат)
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / 'simple_hr.log',
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=10,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    logger.addHandler(file_handler)
    
    # 2. Отдельный файл только для ошибок
    error_handler = logging.handlers.RotatingFileHandler(
        log_dir / 'errors.log',
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(
        '%(asctime)s | %(levelname)s | %(name)s | %(pathname)s:%(lineno)d\n'
        '%(message)s\n'
        '%(exc_info)s\n' + '-' * 80,
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    logger.addHandler(error_handler)
    
    # 3. Структурированные логи в JSON (для production и анализа)
    if not app.debug:
        json_handler = logging.handlers.RotatingFileHandler(
            log_dir / 'simple_hr.json',
            maxBytes=20 * 1024 * 1024,  # 20 MB
            backupCount=10,
            encoding='utf-8'
        )
        json_handler.setLevel(logging.INFO)
        json_handler.setFormatter(StructuredFormatter())
        logger.addHandler(json_handler)
    
    # 4. Цветной вывод в консоль (только для разработки)
    if app.debug:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(ColoredFormatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
            datefmt='%H:%M:%S'
        ))
        logger.addHandler(console_handler)
    
    # 5. Логирование запросов (опционально)
    request_handler = logging.handlers.RotatingFileHandler(
        log_dir / 'requests.log',
        maxBytes=20 * 1024 * 1024,  # 20 MB
        backupCount=5,
        encoding='utf-8'
    )
    request_handler.setLevel(logging.INFO)
    request_handler.setFormatter(logging.Formatter(
        '%(asctime)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    
    # Создаем отдельный логгер для запросов
    request_logger = logging.getLogger('werkzeug')
    request_logger.addHandler(request_handler)
    request_logger.setLevel(logging.INFO)
    
    # Настройка уровней для сторонних библиотек
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    app.logger.info('Logging system initialized')
    app.logger.info(f'Log directory: {log_dir}')
    app.logger.info(f'Debug mode: {app.debug}')


def get_request_logger():
    """Получить логгер для HTTP запросов"""
    return logging.getLogger('requests')


def log_user_action(user_id: int, action: str, details: str = ''):
    """
    Логирование действий пользователя для аудита.
    
    Args:
        user_id: ID пользователя
        action: Выполненное действие
        details: Дополнительные детали
    """
    logger = logging.getLogger('audit')
    extra = {'user_id': user_id}
    logger.info(f'User action: {action}. Details: {details}', extra=extra)


def log_security_event(event_type: str, ip_address: str, details: str = ''):
    """
    Логирование событий безопасности.
    
    Args:
        event_type: Тип события (failed_login, suspicious_activity, etc.)
        ip_address: IP адрес
        details: Дополнительные детали
    """
    logger = logging.getLogger('security')
    extra = {'ip_address': ip_address}
    logger.warning(f'Security event: {event_type}. Details: {details}', extra=extra)
