# -*- coding: utf-8 -*-
"""
Расширенная система структурированного логирования с мониторингом производительности
Обеспечивает детальное логирование, метрики и алертинг для высоконагруженных приложений
"""
import logging
import json
import time
import threading
from datetime import datetime
from typing import Dict, Any, Optional, List
from collections import defaultdict, deque
import psutil
import os
from functools import wraps
from dataclasses import dataclass, asdict
from enum import Enum
import traceback
import sys

class LogLevel(Enum):
    """Уровни логирования"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    PERFORMANCE = "PERFORMANCE"
    SECURITY = "SECURITY"

@dataclass
class LogEntry:
    """Структура лог-записи"""
    timestamp: str
    level: str
    message: str
    module: str
    function: str
    thread_id: int
    process_id: int
    correlation_id: Optional[str] = None
    user_id: Optional[int] = None
    request_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    performance_data: Optional[Dict[str, Any]] = None
    trace_id: Optional[str] = None

class AdvancedStructuredLogger:
    """Расширенный структурированный логгер с мониторингом производительности"""
    
    def __init__(self, app=None):
        self.app = app
        self.logger = logging.getLogger('structured_logger')
        self.logger.setLevel(logging.DEBUG)
        
        # Очереди для разных типов логов
        self.log_queues = {
            'main': deque(maxlen=10000),
            'performance': deque(maxlen=5000),
            'security': deque(maxlen=2000),
            'errors': deque(maxlen=3000)
        }
        
        # Статистика
        self.stats = defaultdict(int)
        self.performance_metrics = defaultdict(list)
        self.alerts = deque(maxlen=1000)
        
        # Конфигурация
        self.config = {
            'log_format': 'json',
            'enable_performance_logging': True,
            'enable_security_logging': True,
            'alert_thresholds': {
                'error_rate': 0.05,  # 5% ошибок
                'response_time_ms': 1000,  # 1 секунда
                'memory_usage_percent': 80,  # 80% использования
                'cpu_usage_percent': 85,    # 85% использования
            },
            'batch_processing': True,
            'max_log_size_mb': 100,
            'retention_days': 30
        }
        
        # Блокировка для потокобезопасности
        self.lock = threading.Lock()
        
        # Мониторинг ресурсов
        self.resource_monitor = {
            'cpu_samples': deque(maxlen=100),
            'memory_samples': deque(maxlen=100),
            'disk_samples': deque(maxlen=100)
        }
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация с Flask приложением"""
        self.app = app
        self.setup_handlers()
        self.start_resource_monitoring()
        self.logger.info("Расширенный структурированный логгер инициализирован")
    
    def setup_handlers(self):
        """Настройка обработчиков логов"""
        # Очистка существующих обработчиков
        self.logger.handlers.clear()
        
        # Форматтер JSON
        json_formatter = StructuredJSONFormatter()
        
        # Обработчик для консоли
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(json_formatter)
        self.logger.addHandler(console_handler)
    
    def start_resource_monitoring(self):
        """Запуск мониторинга системных ресурсов"""
        def monitor_resources():
            while True:
                try:
                    # Сбор метрик
                    cpu_percent = psutil.cpu_percent(interval=1)
                    memory_percent = psutil.virtual_memory().percent
                    disk_percent = psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('.').percent
                    
                    # Сохранение данных
                    with self.lock:
                        self.resource_monitor['cpu_samples'].append({
                            'timestamp': time.time(),
                            'value': cpu_percent
                        })
                        self.resource_monitor['memory_samples'].append({
                            'timestamp': time.time(),
                            'value': memory_percent
                        })
                        self.resource_monitor['disk_samples'].append({
                            'timestamp': time.time(),
                            'value': disk_percent
                        })
                    
                    # Проверка порогов
                    self.check_resource_alerts(cpu_percent, memory_percent, disk_percent)
                    
                    time.sleep(10)  # Проверка каждые 10 секунд
                    
                except Exception as e:
                    self.error(f"Ошибка мониторинга ресурсов: {e}")
        
        monitor_thread = threading.Thread(target=monitor_resources, daemon=True)
        monitor_thread.start()
    
    def check_resource_alerts(self, cpu: float, memory: float, disk: float):
        """Проверка порогов системных ресурсов"""
        alerts = []
        
        if cpu > self.config['alert_thresholds']['cpu_usage_percent']:
            alerts.append(f"Высокое использование CPU: {cpu}%")
        
        if memory > self.config['alert_thresholds']['memory_usage_percent']:
            alerts.append(f"Высокое использование памяти: {memory}%")
        
        if disk > 90:  # Жесткий порог для диска
            alerts.append(f"Высокое использование диска: {disk}%")
        
        for alert in alerts:
            self.create_alert('RESOURCE_EXCEEDED', alert, {
                'cpu': cpu,
                'memory': memory,
                'disk': disk
            })
    
    def log(self, level: LogLevel, message: str, module: str = "", function: str = "",
            metadata: Optional[Dict[str, Any]] = None, **kwargs):
        """Создание лог-записи"""
        # Определяем поля, которые принимает LogEntry
        log_entry_fields = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': level.value,
            'message': message,
            'module': module or getattr(self, '_current_module', ''),
            'function': function or getattr(self, '_current_function', ''),
            'thread_id': threading.current_thread().ident,
            'process_id': os.getpid(),
            'metadata': metadata or {},
        }
        
        # Добавляем только те поля из kwargs, которые определены в LogEntry
        for key, value in kwargs.items():
            if key in ['correlation_id', 'user_id', 'request_id', 'performance_data', 'trace_id']:
                log_entry_fields[key] = value
        
        entry = LogEntry(**log_entry_fields)
        
        # Добавление в очередь
        queue_name = self._get_queue_name(level)
        with self.lock:
            self.log_queues[queue_name].append(asdict(entry))
            self.stats[f'{level.value.lower()}_count'] += 1
        
        # Запись в логгер
        self._write_to_logger(entry)
        
        return entry
    
    def _log_direct(self, level: LogLevel, message: str, **kwargs):
        """Вспомогательный метод для прямой записи в логгер без создания LogEntry"""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': level.value,
            'message': message,
            'module': kwargs.get('module', ''),
            'function': kwargs.get('function', ''),
            'thread_id': threading.current_thread().ident,
            'process_id': os.getpid(),
            'metadata': kwargs.get('metadata', {}),
            'correlation_id': kwargs.get('correlation_id'),
            'user_id': kwargs.get('user_id'),
            'request_id': kwargs.get('request_id'),
            'performance_data': kwargs.get('performance_data'),
            'trace_id': kwargs.get('trace_id'),
        }
        
        # Добавление любых дополнительных полей
        for key, value in kwargs.items():
            if key not in log_entry:
                log_entry[key] = value
        
        # Добавление в очередь
        queue_name = self._get_queue_name(level)
        with self.lock:
            self.log_queues[queue_name].append(log_entry)
            self.stats[f'{level.value.lower()}_count'] += 1
        
        # Запись в логгер
        log_msg = json.dumps(log_entry, ensure_ascii=False)
        if level == LogLevel.DEBUG:
            self.logger.debug(log_msg)
        elif level == LogLevel.INFO:
            self.logger.info(log_msg)
        elif level == LogLevel.WARNING:
            self.logger.warning(log_msg)
        elif level == LogLevel.ERROR:
            self.logger.error(log_msg)
        elif level == LogLevel.CRITICAL:
            self.logger.critical(log_msg)
        else:
            self.logger.info(log_msg)
        
        return log_entry
    
    def _get_queue_name(self, level: LogLevel) -> str:
        """Определение очереди для уровня логирования"""
        if level == LogLevel.PERFORMANCE:
            return 'performance'
        elif level == LogLevel.SECURITY:
            return 'security'
        elif level in [LogLevel.ERROR, LogLevel.CRITICAL]:
            return 'errors'
        else:
            return 'main'
    
    def _write_to_logger(self, entry: LogEntry):
        """Запись в стандартный логгер"""
        log_msg = json.dumps(asdict(entry), ensure_ascii=False)
        
        if entry.level == 'DEBUG':
            self.logger.debug(log_msg)
        elif entry.level == 'INFO':
            self.logger.info(log_msg)
        elif entry.level == 'WARNING':
            self.logger.warning(log_msg)
        elif entry.level == 'ERROR':
            self.logger.error(log_msg)
        elif entry.level == 'CRITICAL':
            self.logger.critical(log_msg)
        else:
            self.logger.info(log_msg)
    
    def debug(self, message: str, **kwargs):
        """Логирование DEBUG уровня"""
        return self.log(LogLevel.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Логирование INFO уровня"""
        return self.log(LogLevel.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Логирование WARNING уровня"""
        return self.log(LogLevel.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Логирование ERROR уровня"""
        return self.log(LogLevel.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Логирование CRITICAL уровня"""
        return self.log(LogLevel.CRITICAL, message, **kwargs)
    
    def performance(self, message: str, duration_ms: float, **kwargs):
        """Логирование метрик производительности"""
        if self.config['enable_performance_logging']:
            kwargs['performance_data'] = {
                'duration_ms': duration_ms,
                'timestamp': time.time()
            }
            return self.log(LogLevel.PERFORMANCE, message, **kwargs)
    
    def security(self, message: str, **kwargs):
        """Логирование событий безопасности"""
        if self.config['enable_security_logging']:
            return self.log(LogLevel.SECURITY, message, **kwargs)
    
    def create_alert(self, alert_type: str, message: str, metadata: Optional[Dict[str, Any]] = None):
        """Создание алерта"""
        alert = {
            'timestamp': datetime.utcnow().isoformat(),
            'type': alert_type,
            'message': message,
            'metadata': metadata or {},
            'severity': self._get_alert_severity(alert_type)
        }
        
        with self.lock:
            self.alerts.append(alert)
            self.stats['alerts_count'] += 1
        
        # Логирование алерта
        self._log_direct(LogLevel.WARNING, f"ALERT: {message}", metadata=metadata, alert_type=alert_type)
    
    def _get_alert_severity(self, alert_type: str) -> str:
        """Определение серьезности алерта"""
        high_severity = ['SECURITY_BREACH', 'RESOURCE_EXCEEDED', 'CRITICAL_ERROR']
        medium_severity = ['PERFORMANCE_DEGRADATION', 'UNUSUAL_ACTIVITY']
        
        if alert_type in high_severity:
            return 'HIGH'
        elif alert_type in medium_severity:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def get_logs(self, log_type: str = 'main', limit: int = 100) -> List[Dict[str, Any]]:
        """Получение логов"""
        with self.lock:
            logs = list(self.log_queues[log_type])[-limit:]
        return logs
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Получение метрик производительности"""
        with self.lock:
            return {
                'stats': dict(self.stats),
                'resource_monitor': {
                    'cpu_avg': self._calculate_average(self.resource_monitor['cpu_samples']),
                    'memory_avg': self._calculate_average(self.resource_monitor['memory_samples']),
                    'disk_avg': self._calculate_average(self.resource_monitor['disk_samples'])
                },
                'performance_history': list(self.performance_metrics['requests'])[-50:],
                'alerts': list(self.alerts)[-20:],
                'log_counts': {
                    queue_name: len(queue) 
                    for queue_name, queue in self.log_queues.items()
                }
            }
    
    def _calculate_average(self, samples: deque) -> float:
        """Расчет среднего значения"""
        if not samples:
            return 0.0
        return sum(sample['value'] for sample in samples) / len(samples)
    
    def get_alerts(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Получение алертов"""
        with self.lock:
            return list(self.alerts)[-limit:]
    
    def reset_stats(self):
        """Сброс статистики"""
        with self.lock:
            self.stats.clear()
            for key in ['debug_count', 'info_count', 'warning_count', 'error_count', 'critical_count', 'alerts_count']:
                self.stats[key] = 0

class StructuredJSONFormatter(logging.Formatter):
    """Форматтер для структурированного JSON логирования"""
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'thread': record.thread,
            'process': record.process
        }
        
        # Добавление дополнительных полей если они есть
        if hasattr(record, 'correlation_id'):
            log_entry['correlation_id'] = record.correlation_id
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        if hasattr(record, 'metadata'):
            log_entry['metadata'] = record.metadata
        if hasattr(record, 'performance_data'):
            log_entry['performance_data'] = record.performance_data
        if hasattr(record, 'trace_id'):
            log_entry['trace_id'] = record.trace_id
        
        return json.dumps(log_entry, ensure_ascii=False)

# Глобальный экземпляр
structured_logger = AdvancedStructuredLogger()

def register_structured_logging_commands(app):
    """Регистрация CLI команд для структурированного логирования"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('log-report')
    @click.option('--type', '-t', default='main', 
                  type=click.Choice(['main', 'performance', 'security', 'errors']),
                  help='Тип логов для отображения')
    @click.option('--limit', '-l', default=20, help='Количество записей')
    @with_appcontext
    def show_log_report(type, limit):
        """Показать отчет по логам"""
        logs = structured_logger.get_logs(type, limit)
        click.echo(f"Логи типа '{type}' (последние {limit}):")
        for log in logs:
            click.echo(f"  [{log['timestamp']}] {log['level']}: {log['message']}")
    
    @app.cli.command('perf-report')
    @with_appcontext
    def show_perf_report():
        """Показать отчет о производительности"""
        metrics = structured_logger.get_performance_metrics()
        click.echo("Отчет о производительности:")
        click.echo(f"  Статистика: {metrics['stats']}")
        click.echo(f"  Средняя загрузка CPU: {metrics['resource_monitor']['cpu_avg']:.2f}%")
        click.echo(f"  Средняя загрузка памяти: {metrics['resource_monitor']['memory_avg']:.2f}%")
        click.echo(f"  Количество алертов: {len(metrics['alerts'])}")

def log_performance(duration_threshold_ms: float = 100.0):
    """Декоратор для логирования производительности функций"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = (time.time() - start_time) * 1000  # в миллисекундах
                
                if execution_time > duration_threshold_ms:
                    structured_logger.performance(
                        f"Slow function execution: {func.__name__}",
                        duration_ms=execution_time,
                        function=func.__name__,
                        module=func.__module__,
                        args_count=len(args),
                        kwargs_count=len(kwargs)
                    )
                
                return result
            except Exception as e:
                execution_time = (time.time() - start_time) * 1000
                structured_logger.error(
                    f"Function failed: {func.__name__}",
                    duration_ms=execution_time,
                    function=func.__name__,
                    error=str(e),
                    traceback=traceback.format_exc()
                )
                raise
        
        return wrapper
    return decorator

def log_security_event(event_type: str, severity: str = "INFO"):
    """Декоратор для логирования событий безопасности"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                
                structured_logger.security(
                    f"Security event: {event_type}",
                    event_type=event_type,
                    severity=severity,
                    function=func.__name__,
                    module=func.__module__
                )
                
                return result
            except Exception as e:
                structured_logger.security(
                    f"Security-related error in {func.__name__}: {str(e)}",
                    event_type=f"{event_type}_ERROR",
                    severity="CRITICAL",
                    function=func.__name__,
                    error=str(e)
                )
                raise
        
        return wrapper
    return decorator