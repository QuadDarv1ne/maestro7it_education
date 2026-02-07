# -*- coding: utf-8 -*-
"""
Модуль комплексного мониторинга здоровья системы
Обеспечивает всестороннюю диагностику и мониторинг состояния приложения
"""
import logging
import psutil
import os
import time
import threading
import subprocess
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from collections import defaultdict, deque
import json
import gc
import sys
from dataclasses import dataclass
from enum import Enum
import platform
import socket
from functools import wraps

logger = logging.getLogger(__name__)

class HealthStatus(Enum):
    """Статус здоровья системы"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"

@dataclass
class HealthCheckResult:
    """Результат проверки здоровья"""
    component: str
    status: HealthStatus
    message: str
    details: Dict[str, Any]
    timestamp: str
    duration_ms: float

class SystemHealthMonitor:
    """Комплексный мониторинг здоровья системы"""
    
    def __init__(self, app=None):
        self.app = app
        self.health_checks = {}
        self.health_history = deque(maxlen=1000)
        self.system_metrics = defaultdict(deque)
        self.alerts = deque(maxlen=100)
        self.check_intervals = {}
        self.monitoring_active = False
        self.lock = threading.Lock()
        
        # Пороговые значения
        self.thresholds = {
            'cpu_percent': 85.0,
            'memory_percent': 85.0,
            'disk_percent': 90.0,
            'process_count': 1000,
            'thread_count': 500,
            'open_files': 1000,
            'response_time_ms': 2000,
            'error_rate': 0.05,
            'database_connections': 0.9,  # 90% от максимума
            'cache_hit_rate': 0.8,  # 80%
            'queue_size': 100
        }
        
        # Компоненты для проверки
        self.components = [
            'system_resources',
            'database',
            'cache',
            'network',
            'storage',
            'processes',
            'threads',
            'memory',
            'application',
            'external_services'
        ]
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация с Flask приложением"""
        self.app = app
        self.start_monitoring()
        logger.info("Комплексный мониторинг здоровья системы инициализирован")
    
    def start_monitoring(self):
        """Запуск постоянного мониторинга"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        
        def monitor_loop():
            while self.monitoring_active:
                try:
                    # Выполнение регулярных проверок
                    self.run_periodic_health_checks()
                    time.sleep(60)  # Проверка каждую минуту
                except Exception as e:
                    logger.error(f"Ошибка в цикле мониторинга: {e}")
                    time.sleep(60)
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
    
    def register_health_check(self, name: str, check_func, interval: int = 300):
        """Регистрация пользовательской проверки здоровья"""
        self.health_checks[name] = check_func
        self.check_intervals[name] = interval
    
    def run_health_check(self, component: str) -> HealthCheckResult:
        """Выполнение одной проверки здоровья"""
        start_time = time.time()
        
        try:
            if component == 'system_resources':
                result = self.check_system_resources()
            elif component == 'database':
                result = self.check_database_health()
            elif component == 'cache':
                result = self.check_cache_health()
            elif component == 'network':
                result = self.check_network_health()
            elif component == 'storage':
                result = self.check_storage_health()
            elif component == 'processes':
                result = self.check_processes()
            elif component == 'threads':
                result = self.check_threads()
            elif component == 'memory':
                result = self.check_memory()
            elif component == 'application':
                result = self.check_application_health()
            elif component == 'external_services':
                result = self.check_external_services()
            else:
                result = self.check_custom_component(component)
            
            duration_ms = (time.time() - start_time) * 1000
            
            health_result = HealthCheckResult(
                component=component,
                status=result['status'],
                message=result['message'],
                details=result['details'],
                timestamp=datetime.utcnow().isoformat(),
                duration_ms=duration_ms
            )
            
            # Сохранение результата
            with self.lock:
                self.health_history.append(health_result)
            
            return health_result
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            error_result = HealthCheckResult(
                component=component,
                status=HealthStatus.CRITICAL,
                message=f"Ошибка проверки: {str(e)}",
                details={'error': str(e)},
                timestamp=datetime.utcnow().isoformat(),
                duration_ms=duration_ms
            )
            
            with self.lock:
                self.health_history.append(error_result)
            
            return error_result
    
    def check_system_resources(self) -> Dict[str, Any]:
        """Проверка системных ресурсов"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('.').percent
        
        # Сбор метрик
        metrics = {
            'cpu_percent': cpu_percent,
            'memory_percent': memory_percent,
            'disk_percent': disk_percent,
            'load_average': getattr(os, 'getloadavg', lambda: (0, 0, 0))(),
            'boot_time': psutil.boot_time()
        }
        
        # Проверка порогов
        issues = []
        if cpu_percent > self.thresholds['cpu_percent']:
            issues.append(f"Высокая загрузка CPU: {cpu_percent}%")
        if memory_percent > self.thresholds['memory_percent']:
            issues.append(f"Высокое использование памяти: {memory_percent}%")
        if disk_percent > self.thresholds['disk_percent']:
            issues.append(f"Высокое использование диска: {disk_percent}%")
        
        status = HealthStatus.CRITICAL if issues else HealthStatus.HEALTHY
        message = "Системные ресурсы в норме" if not issues else f"Проблемы с ресурсами: {', '.join(issues)}"
        
        # Сохранение метрик
        with self.lock:
            self.system_metrics['cpu_percent'].append(cpu_percent)
            self.system_metrics['memory_percent'].append(memory_percent)
            self.system_metrics['disk_percent'].append(disk_percent)
        
        return {
            'status': status,
            'message': message,
            'details': metrics
        }
    
    def check_database_health(self) -> Dict[str, Any]:
        """Проверка здоровья базы данных"""
        if not hasattr(self.app, 'db') or self.app.db is None:
            return {
                'status': HealthStatus.UNKNOWN,
                'message': 'База данных не инициализирована',
                'details': {'initialized': False}
            }
        
        try:
            # Проверка подключения
            from sqlalchemy import text
            with self.app.app_context():
                result = self.app.db.session.execute(text('SELECT 1'))
                db_connected = True
        except Exception as e:
            db_connected = False
            error_message = str(e)
        
        # Проверка пула соединений
        pool_status = {}
        if hasattr(self.app, 'db_pool_manager'):
            try:
                pool_status = self.app.db_pool_manager.get_pool_stats()
            except:
                pool_status = {}
        
        details = {
            'connected': db_connected,
            'pool_status': pool_status
        }
        
        if not db_connected:
            return {
                'status': HealthStatus.CRITICAL,
                'message': f'База данных недоступна: {error_message}',
                'details': details
            }
        
        # Проверка производительности запросов
        slow_query_count = 0
        if hasattr(self.app, 'performance_monitor'):
            try:
                perf_stats = self.app.performance_monitor.get_stats()
                slow_query_count = len(perf_stats.get('slow_queries', []))
            except:
                pass
        
        if slow_query_count > 10:
            return {
                'status': HealthStatus.WARNING,
                'message': f'Обнаружено {slow_query_count} медленных запросов',
                'details': details
            }
        
        return {
            'status': HealthStatus.HEALTHY,
            'message': 'База данных в рабочем состоянии',
            'details': details
        }
    
    def check_cache_health(self) -> Dict[str, Any]:
        """Проверка здоровья кэша"""
        cache_status = {}
        
        if hasattr(self.app, 'cache'):
            try:
                # Проверка доступности кэша
                test_key = 'health_check_test'
                test_value = 'test_value_' + str(int(time.time()))
                
                self.app.cache.set(test_key, test_value, timeout=30)
                retrieved_value = self.app.cache.get(test_key)
                
                cache_accessible = retrieved_value == test_value
                cache_status['accessible'] = cache_accessible
                
                # Статистика кэша
                if hasattr(self.app.cache, 'get_stats'):
                    cache_status['stats'] = self.app.cache.get_stats()
                
            except Exception as e:
                cache_status['accessible'] = False
                cache_status['error'] = str(e)
        else:
            cache_status['available'] = False
        
        if not cache_status.get('accessible', True):
            return {
                'status': HealthStatus.CRITICAL,
                'message': 'Кэш недоступен',
                'details': cache_status
            }
        
        # Проверка hit rate
        cache_hit_rate = cache_status.get('stats', {}).get('hit_rate', 1.0)
        if cache_hit_rate < self.thresholds['cache_hit_rate']:
            return {
                'status': HealthStatus.WARNING,
                'message': f'Низкий коэффициент попаданий в кэш: {cache_hit_rate:.2%}',
                'details': cache_status
            }
        
        return {
            'status': HealthStatus.HEALTHY,
            'message': 'Кэш в рабочем состоянии',
            'details': cache_status
        }
    
    def check_network_health(self) -> Dict[str, Any]:
        """Проверка сетевого здоровья"""
        network_status = {
            'hostname': socket.gethostname(),
            'ip_address': socket.gethostbyname(socket.gethostname()),
            'network_interfaces': []
        }
        
        # Проверка сетевых интерфейсов
        try:
            net_io = psutil.net_io_counters(pernic=True)
            for interface, stats in net_io.items():
                network_status['network_interfaces'].append({
                    'interface': interface,
                    'bytes_sent': stats.bytes_sent,
                    'bytes_recv': stats.bytes_recv,
                    'packets_sent': stats.packets_sent,
                    'packets_recv': stats.packets_recv
                })
        except:
            pass
        
        # Проверка доступности внешнего сервиса (например, Google DNS)
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            external_connectivity = True
        except:
            external_connectivity = False
        
        network_status['external_connectivity'] = external_connectivity
        
        if not external_connectivity:
            return {
                'status': HealthStatus.WARNING,
                'message': 'Нет подключения к внешним ресурсам',
                'details': network_status
            }
        
        return {
            'status': HealthStatus.HEALTHY,
            'message': 'Сеть в рабочем состоянии',
            'details': network_status
        }
    
    def check_storage_health(self) -> Dict[str, Any]:
        """Проверка здоровья хранилища"""
        disk_usage = psutil.disk_usage('/')
        disk_percent = disk_usage.percent
        
        storage_details = {
            'total_gb': disk_usage.total / (1024**3),
            'used_gb': disk_usage.used / (1024**3),
            'free_gb': disk_usage.free / (1024**3),
            'percent_used': disk_percent
        }
        
        if disk_percent > self.thresholds['disk_percent']:
            return {
                'status': HealthStatus.CRITICAL,
                'message': f'Высокое использование диска: {disk_percent}%',
                'details': storage_details
            }
        
        # Проверка скорости диска (упрощенная)
        try:
            # Проверка доступности основных директорий
            critical_dirs = [os.getcwd(), '/tmp' if os.name != 'nt' else os.environ.get('TEMP', '.')]
            for directory in critical_dirs:
                if os.access(directory, os.W_OK | os.R_OK):
                    storage_details[f'{directory}_accessible'] = True
                else:
                    storage_details[f'{directory}_accessible'] = False
        except:
            pass
        
        return {
            'status': HealthStatus.HEALTHY,
            'message': 'Хранилище в рабочем состоянии',
            'details': storage_details
        }
    
    def check_processes(self) -> Dict[str, Any]:
        """Проверка процессов"""
        current_process = psutil.Process()
        process_count = len(psutil.pids())
        current_fds = current_process.num_fds() if hasattr(current_process, 'num_fds') else 0
        current_connections = len(current_process.connections())
        
        process_details = {
            'current_pid': os.getpid(),
            'process_count': process_count,
            'current_fds': current_fds,
            'current_connections': current_connections,
            'parent_pid': current_process.ppid()
        }
        
        if process_count > self.thresholds['process_count']:
            return {
                'status': HealthStatus.WARNING,
                'message': f'Высокое количество процессов: {process_count}',
                'details': process_details
            }
        
        if current_fds > self.thresholds['open_files']:
            return {
                'status': HealthStatus.WARNING,
                'message': f'Высокое количество открытых файлов: {current_fds}',
                'details': process_details
            }
        
        return {
            'status': HealthStatus.HEALTHY,
            'message': 'Процессы в норме',
            'details': process_details
        }
    
    def check_threads(self) -> Dict[str, Any]:
        """Проверка потоков"""
        thread_count = threading.active_count()
        current_threads = threading.enumerate()
        
        thread_details = {
            'thread_count': thread_count,
            'daemon_threads': sum(1 for t in current_threads if t.daemon),
            'alive_threads': sum(1 for t in current_threads if t.is_alive())
        }
        
        if thread_count > self.thresholds['thread_count']:
            return {
                'status': HealthStatus.WARNING,
                'message': f'Высокое количество потоков: {thread_count}',
                'details': thread_details
            }
        
        return {
            'status': HealthStatus.HEALTHY,
            'message': 'Потоки в норме',
            'details': thread_details
        }
    
    def check_memory(self) -> Dict[str, Any]:
        """Проверка памяти"""
        current_process = psutil.Process()
        memory_info = current_process.memory_info()
        
        memory_details = {
            'rss_mb': memory_info.rss / 1024 / 1024,
            'vms_mb': memory_info.vms / 1024 / 1024,
            'percent': current_process.memory_percent(),
            'object_count': len(gc.get_objects()),
            'garbage_count': len(gc.garbage)
        }
        
        if memory_details['percent'] > self.thresholds['memory_percent']:
            return {
                'status': HealthStatus.WARNING,
                'message': f'Высокое использование памяти процессом: {memory_details["percent"]:.1f}%',
                'details': memory_details
            }
        
        return {
            'status': HealthStatus.HEALTHY,
            'message': 'Память в норме',
            'details': memory_details
        }
    
    def check_application_health(self) -> Dict[str, Any]:
        """Проверка здоровья приложения"""
        app_details = {
            'uptime_seconds': time.time() - getattr(self, '_start_time', time.time()),
            'python_version': platform.python_version(),
            'platform': platform.platform(),
            'flask_version': getattr(self.app, 'version', 'unknown') if self.app else 'unknown',
            'request_queue_size': getattr(self.app, 'request_queue_size', 0) if self.app else 0
        }
        
        # Проверка зарегистрированных маршрутов
        if self.app and hasattr(self.app, 'url_map'):
            app_details['route_count'] = len(self.app.url_map._rules)
        
        # Проверка ошибок приложения
        error_count = 0
        if hasattr(self.app, 'error_count'):
            error_count = getattr(self.app, 'error_count', 0)
        
        if error_count > 100:  # Пример порога
            return {
                'status': HealthStatus.WARNING,
                'message': f'Высокое количество ошибок приложения: {error_count}',
                'details': app_details
            }
        
        return {
            'status': HealthStatus.HEALTHY,
            'message': 'Приложение в рабочем состоянии',
            'details': app_details
        }
    
    def check_external_services(self) -> Dict[str, Any]:
        """Проверка внешних сервисов"""
        external_services = {}
        
        # Проверка Redis если доступен
        if hasattr(self.app, 'redis'):
            try:
                self.app.redis.ping()
                external_services['redis'] = {'status': 'healthy', 'ping': True}
            except Exception as e:
                external_services['redis'] = {'status': 'unhealthy', 'error': str(e)}
        
        # Проверка других внешних сервисов
        services_status = all(
            service.get('status') == 'healthy' 
            for service in external_services.values()
            if isinstance(service, dict)
        )
        
        if not services_status:
            unhealthy = [name for name, status in external_services.items() 
                        if status.get('status') != 'healthy']
            return {
                'status': HealthStatus.WARNING,
                'message': f'Внешние сервисы недоступны: {", ".join(unhealthy)}',
                'details': {'external_services': external_services}
            }
        
        return {
            'status': HealthStatus.HEALTHY,
            'message': 'Внешние сервисы в рабочем состоянии',
            'details': {'external_services': external_services}
        }
    
    def check_custom_component(self, component: str) -> Dict[str, Any]:
        """Проверка пользовательского компонента"""
        if component in self.health_checks:
            try:
                result = self.health_checks[component]()
                return {
                    'status': result.get('status', HealthStatus.UNKNOWN),
                    'message': result.get('message', 'Custom check result'),
                    'details': result.get('details', {})
                }
            except Exception as e:
                return {
                    'status': HealthStatus.CRITICAL,
                    'message': f'Ошибка пользовательской проверки: {str(e)}',
                    'details': {'error': str(e)}
                }
        else:
            return {
                'status': HealthStatus.UNKNOWN,
                'message': f'Компонент не найден: {component}',
                'details': {'available_components': list(self.health_checks.keys())}
            }
    
    def run_periodic_health_checks(self):
        """Выполнение периодических проверок здоровья"""
        results = {}
        
        for component in self.components:
            result = self.run_health_check(component)
            results[component] = result
        
        # Проверка общего состояния системы
        overall_status = self._calculate_overall_health(results)
        
        # Создание алерта если состояние ухудшилось
        if overall_status in [HealthStatus.WARNING, HealthStatus.CRITICAL]:
            self._create_health_alert(overall_status, results)
        
        return results
    
    def _calculate_overall_health(self, results: Dict[str, HealthCheckResult]) -> HealthStatus:
        """Расчет общего состояния системы"""
        statuses = [result.status for result in results.values()]
        
        if HealthStatus.CRITICAL in statuses:
            return HealthStatus.CRITICAL
        elif HealthStatus.WARNING in statuses:
            return HealthStatus.WARNING
        elif HealthStatus.UNKNOWN in statuses:
            return HealthStatus.UNKNOWN
        else:
            return HealthStatus.HEALTHY
    
    def _create_health_alert(self, status: HealthStatus, results: Dict[str, HealthCheckResult]):
        """Создание алерта о состоянии здоровья"""
        alert = {
            'timestamp': datetime.utcnow().isoformat(),
            'status': status.value,
            'affected_components': [
                comp for comp, result in results.items() 
                if result.status in [HealthStatus.WARNING, HealthStatus.CRITICAL]
            ],
            'details': {
                comp: {
                    'message': result.message,
                    'duration_ms': result.duration_ms
                }
                for comp, result in results.items()
                if result.status in [HealthStatus.WARNING, HealthStatus.CRITICAL]
            }
        }
        
        with self.lock:
            self.alerts.append(alert)
    
    def get_health_report(self) -> Dict[str, Any]:
        """Получение полного отчета о здоровье"""
        with self.lock:
            # Последние результаты проверок
            recent_results = {}
            for result in reversed(list(self.health_history)):
                if result.component not in recent_results:
                    recent_results[result.component] = result
                if len(recent_results) == len(self.components):
                    break
            
            # Сводка по статусам
            status_summary = {}
            for result in self.health_history:
                status = result.status.value
                status_summary[status] = status_summary.get(status, 0) + 1
            
            return {
                'timestamp': datetime.utcnow().isoformat(),
                'overall_status': self._calculate_overall_health(recent_results).value,
                'components': {
                    comp: {
                        'status': result.status.value,
                        'message': result.message,
                        'last_checked': result.timestamp,
                        'duration_ms': result.duration_ms
                    }
                    for comp, result in recent_results.items()
                },
                'status_summary': status_summary,
                'recent_alerts': list(self.alerts)[-10:],
                'system_metrics': {
                    key: list(values)[-10:] if values else []
                    for key, values in self.system_metrics.items()
                },
                'health_check_count': len(self.health_history)
            }
    
    def get_detailed_health_status(self) -> Dict[str, Any]:
        """Получение детального статуса здоровья"""
        report = self.get_health_report()
        
        # Добавление дополнительной информации
        if hasattr(self.app, 'db_pool_manager'):
            try:
                report['database_pool_status'] = self.app.db_pool_manager.get_pool_stats()
            except:
                pass
        
        if hasattr(self.app, 'redis_cache_manager'):
            try:
                report['redis_status'] = self.app.redis_cache_manager.get_stats()
            except:
                pass
        
        if hasattr(self.app, 'performance_monitor'):
            try:
                report['performance_stats'] = self.app.performance_monitor.get_stats()
            except:
                pass
        
        return report

# Глобальный экземпляр
health_monitor = SystemHealthMonitor()

def register_health_monitor_commands(app):
    """Регистрация CLI команд для мониторинга здоровья"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('health-check')
    @click.option('--component', '-c', help='Проверить конкретный компонент')
    @with_appcontext
    def run_health_check(component):
        """Выполнить проверку здоровья системы"""
        if component:
            result = health_monitor.run_health_check(component)
            click.echo(f"Проверка компонента {component}:")
            click.echo(f"  Статус: {result.status.value}")
            click.echo(f"  Сообщение: {result.message}")
            click.echo(f"  Длительность: {result.duration_ms:.2f}ms")
        else:
            report = health_monitor.get_health_report()
            click.echo("Отчет о здоровье системы:")
            click.echo(f"  Общий статус: {report['overall_status']}")
            click.echo(f"  Всего проверок: {report['health_check_count']}")
            
            click.echo("\nКомпоненты:")
            for comp, status_info in report['components'].items():
                status_icon = {
                    'healthy': '✓',
                    'warning': '⚠',
                    'critical': '✗',
                    'unknown': '?'
                }.get(status_info['status'], '?')
                
                click.echo(f"  {status_icon} {comp}: {status_info['status']} - {status_info['message']}")
    
    @app.cli.command('health-report')
    @with_appcontext
    def show_health_report():
        """Показать подробный отчет о здоровье"""
        report = health_monitor.get_detailed_health_status()
        click.echo(json.dumps(report, indent=2, ensure_ascii=False))

def health_check_required(f):
    """Декоратор для требовательной проверки здоровья перед выполнением функции"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Проверка общего состояния системы
        report = health_monitor.get_health_report()
        
        if report['overall_status'] == 'critical':
            logger.error(f"Функция {f.__name__} отменена из-за критического состояния системы")
            raise RuntimeError("Система в критическом состоянии")
        elif report['overall_status'] == 'warning':
            logger.warning(f"Функция {f.__name__} выполняется при предупреждении о состоянии системы")
        
        return f(*args, **kwargs)
    
    return decorated_function

def register_default_health_checks(app):
    """Регистрация стандартных проверок здоровья"""
    def check_flask_app():
        """Проверка работоспособности Flask приложения"""
        try:
            # Простая проверка - попытка получить доступ к контексту приложения
            with app.app_context():
                # Проверка базовых компонентов
                checks = {
                    'db_initialized': hasattr(app, 'db') and app.db is not None,
                    'config_loaded': app.config is not None,
                    'secret_key_set': app.secret_key is not None
                }
                
                healthy = all(checks.values())
                
                return {
                    'status': HealthStatus.HEALTHY if healthy else HealthStatus.WARNING,
                    'message': 'Flask приложение в рабочем состоянии' if healthy else 'Проблемы с инициализацией Flask',
                    'details': checks
                }
        except Exception as e:
            return {
                'status': HealthStatus.CRITICAL,
                'message': f'Ошибка проверки Flask приложения: {str(e)}',
                'details': {'error': str(e)}
            }
    
    health_monitor.register_health_check('flask_app', check_flask_app)