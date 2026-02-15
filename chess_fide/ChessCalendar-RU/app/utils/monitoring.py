import logging
import logging.handlers
import os
from datetime import datetime
import json
from functools import wraps

class LoggerSetup:
    @staticmethod
    def setup_logging(log_level=logging.INFO, log_file='chess_calendar.log'):
        """Настройка логирования для приложения"""
        
        # Создаем директорию для логов если не существует
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Формат логов
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(log_format)
        
        # Корневой логгер
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        
        # Файловый обработчик с ротацией
        file_handler = logging.handlers.RotatingFileHandler(
            os.path.join(log_dir, log_file),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
        
        # Консольный обработчик
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        
        logging.info("Logging system initialized")

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
        
    def track_execution_time(self, func_name):
        """Декоратор для отслеживания времени выполнения функций"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = datetime.now()
                try:
                    result = func(*args, **kwargs)
                    execution_time = (datetime.now() - start_time).total_seconds()
                    
                    # Сохраняем метрики
                    if func_name not in self.metrics:
                        self.metrics[func_name] = []
                    self.metrics[func_name].append({
                        'execution_time': execution_time,
                        'timestamp': datetime.now().isoformat(),
                        'success': True
                    })
                    
                    # Логируем медленные операции
                    if execution_time > 5:  # Более 5 секунд
                        logging.warning(f"Slow operation: {func_name} took {execution_time:.2f}s")
                    
                    return result
                except Exception as e:
                    execution_time = (datetime.now() - start_time).total_seconds()
                    self.metrics[func_name].append({
                        'execution_time': execution_time,
                        'timestamp': datetime.now().isoformat(),
                        'success': False,
                        'error': str(e)
                    })
                    logging.error(f"Error in {func_name}: {e}")
                    raise
            return wrapper
        return decorator
    
    def get_metrics_summary(self):
        """Получить сводку по метрикам производительности"""
        summary = {}
        for func_name, metrics in self.metrics.items():
            if metrics:
                execution_times = [m['execution_time'] for m in metrics if m['success']]
                if execution_times:
                    summary[func_name] = {
                        'call_count': len(metrics),
                        'success_count': len([m for m in metrics if m['success']]),
                        'avg_time': sum(execution_times) / len(execution_times),
                        'min_time': min(execution_times),
                        'max_time': max(execution_times),
                        'error_count': len([m for m in metrics if not m['success']])
                    }
        return summary
    
    def clear_metrics(self):
        """Очистить собранные метрики"""
        self.metrics.clear()

class HealthChecker:
    def __init__(self):
        self.checks = {}
        
    def add_health_check(self, name, check_func):
        """Добавить проверку состояния"""
        self.checks[name] = check_func
    
    def run_health_checks(self):
        """Выполнить все проверки состояния"""
        results = {}
        for name, check_func in self.checks.items():
            try:
                result = check_func()
                results[name] = {
                    'status': 'healthy' if result else 'unhealthy',
                    'result': result,
                    'timestamp': datetime.now().isoformat()
                }
            except Exception as e:
                results[name] = {
                    'status': 'error',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
                logging.error(f"Health check {name} failed: {e}")
        
        return results
    
    def get_health_status(self):
        """Получить общий статус здоровья системы"""
        results = self.run_health_checks()
        unhealthy_checks = [name for name, result in results.items() 
                          if result['status'] != 'healthy']
        
        if not unhealthy_checks:
            return 'healthy'
        elif len(unhealthy_checks) == len(results):
            return 'critical'
        else:
            return 'degraded'

# Глобальные экземпляры
logger_setup = LoggerSetup()
performance_monitor = PerformanceMonitor()
health_checker = HealthChecker()

# Предопределенные проверки состояния
def check_database_connection():
    """Проверка соединения с базой данных"""
    try:
        from app import db
        db.session.execute('SELECT 1')
        return True
    except Exception:
        return False

def check_cache_connection():
    """Проверка соединения с кэшем"""
    try:
        from app.utils.cache import cache_service
        return cache_service.get_stats()['connected']
    except Exception:
        return False

def check_parser_status():
    """Проверка работоспособности парсеров"""
    try:
        from app.utils.fide_parser import FIDEParses
        from app.utils.cfr_parser import CFRParser
        
        fide_parser = FIDEParses()
        cfr_parser = CFRParser()
        
        # Простая проверка инициализации
        return fide_parser is not None and cfr_parser is not None
    except Exception:
        return False

# Регистрируем стандартные проверки
health_checker.add_health_check('database', check_database_connection)
health_checker.add_health_check('cache', check_cache_connection)
health_checker.add_health_check('parsers', check_parser_status)

# Декоратор для автоматического логирования
def log_action(action_name):
    """Декоратор для логирования действий"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logging.info(f"Starting action: {action_name}")
            try:
                result = func(*args, **kwargs)
                logging.info(f"Action completed: {action_name}")
                return result
            except Exception as e:
                logging.error(f"Action failed: {action_name} - {e}")
                raise
        return wrapper
    return decorator