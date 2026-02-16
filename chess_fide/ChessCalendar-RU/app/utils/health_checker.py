"""
Система проверки здоровья компонентов приложения
Комплексная диагностика всех сервисов и зависимостей
"""

import time
import psutil
from datetime import datetime, timedelta
from typing import Dict, List, Any
from flask import current_app


class HealthStatus:
    """Статусы здоровья компонентов"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class HealthChecker:
    """Система проверки здоровья приложения"""
    
    def __init__(self):
        self.checks = {}
        self.last_check_time = None
        self.check_interval = 60  # секунды
        
    def register_check(self, name: str, check_func: callable, critical: bool = False):
        """Регистрация проверки здоровья"""
        self.checks[name] = {
            'func': check_func,
            'critical': critical,
            'last_result': None,
            'last_check': None
        }
    
    def check_database(self) -> Dict[str, Any]:
        """Проверка подключения к базе данных"""
        try:
            from app import db
            start_time = time.time()
            
            # Простой запрос для проверки
            db.session.execute('SELECT 1')
            response_time = (time.time() - start_time) * 1000
            
            # Проверка количества соединений
            pool = db.engine.pool
            pool_size = pool.size()
            checked_out = pool.checkedout()
            
            status = HealthStatus.HEALTHY
            if response_time > 1000:
                status = HealthStatus.DEGRADED
            if response_time > 5000:
                status = HealthStatus.UNHEALTHY
                
            return {
                'status': status,
                'response_time_ms': round(response_time, 2),
                'pool_size': pool_size,
                'connections_in_use': checked_out,
                'message': 'Database connection OK'
            }
        except Exception as e:
            return {
                'status': HealthStatus.UNHEALTHY,
                'error': str(e),
                'message': 'Database connection failed'
            }
    
    def check_redis(self) -> Dict[str, Any]:
        """Проверка подключения к Redis"""
        try:
            import redis
            from config.config import Config
            
            start_time = time.time()
            r = redis.from_url(Config.REDIS_URL)
            r.ping()
            response_time = (time.time() - start_time) * 1000
            
            # Получение информации о Redis
            info = r.info()
            memory_used = info.get('used_memory_human', 'N/A')
            connected_clients = info.get('connected_clients', 0)
            
            status = HealthStatus.HEALTHY
            if response_time > 100:
                status = HealthStatus.DEGRADED
            if response_time > 500:
                status = HealthStatus.UNHEALTHY
                
            return {
                'status': status,
                'response_time_ms': round(response_time, 2),
                'memory_used': memory_used,
                'connected_clients': connected_clients,
                'message': 'Redis connection OK'
            }
        except Exception as e:
            return {
                'status': HealthStatus.DEGRADED,
                'error': str(e),
                'message': 'Redis not available (using fallback)'
            }
    
    def check_disk_space(self) -> Dict[str, Any]:
        """Проверка свободного места на диске"""
        try:
            disk = psutil.disk_usage('/')
            percent_used = disk.percent
            free_gb = disk.free / (1024 ** 3)
            
            status = HealthStatus.HEALTHY
            if percent_used > 80:
                status = HealthStatus.DEGRADED
            if percent_used > 90:
                status = HealthStatus.UNHEALTHY
                
            return {
                'status': status,
                'percent_used': round(percent_used, 2),
                'free_gb': round(free_gb, 2),
                'total_gb': round(disk.total / (1024 ** 3), 2),
                'message': f'{free_gb:.1f}GB free'
            }
        except Exception as e:
            return {
                'status': HealthStatus.UNKNOWN,
                'error': str(e),
                'message': 'Could not check disk space'
            }
    
    def check_memory(self) -> Dict[str, Any]:
        """Проверка использования памяти"""
        try:
            memory = psutil.virtual_memory()
            percent_used = memory.percent
            available_gb = memory.available / (1024 ** 3)
            
            status = HealthStatus.HEALTHY
            if percent_used > 80:
                status = HealthStatus.DEGRADED
            if percent_used > 90:
                status = HealthStatus.UNHEALTHY
                
            return {
                'status': status,
                'percent_used': round(percent_used, 2),
                'available_gb': round(available_gb, 2),
                'total_gb': round(memory.total / (1024 ** 3), 2),
                'message': f'{available_gb:.1f}GB available'
            }
        except Exception as e:
            return {
                'status': HealthStatus.UNKNOWN,
                'error': str(e),
                'message': 'Could not check memory'
            }
    
    def check_cpu(self) -> Dict[str, Any]:
        """Проверка загрузки CPU"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            status = HealthStatus.HEALTHY
            if cpu_percent > 70:
                status = HealthStatus.DEGRADED
            if cpu_percent > 90:
                status = HealthStatus.UNHEALTHY
                
            return {
                'status': status,
                'percent_used': round(cpu_percent, 2),
                'cpu_count': cpu_count,
                'message': f'{cpu_percent:.1f}% CPU usage'
            }
        except Exception as e:
            return {
                'status': HealthStatus.UNKNOWN,
                'error': str(e),
                'message': 'Could not check CPU'
            }
    
    def check_celery(self) -> Dict[str, Any]:
        """Проверка Celery worker"""
        try:
            from app.celery_app import celery
            
            # Проверка активных worker'ов
            inspect = celery.control.inspect()
            active_workers = inspect.active()
            
            if not active_workers:
                return {
                    'status': HealthStatus.UNHEALTHY,
                    'message': 'No active Celery workers',
                    'workers': 0
                }
            
            worker_count = len(active_workers)
            total_tasks = sum(len(tasks) for tasks in active_workers.values())
            
            return {
                'status': HealthStatus.HEALTHY,
                'workers': worker_count,
                'active_tasks': total_tasks,
                'message': f'{worker_count} workers active'
            }
        except Exception as e:
            return {
                'status': HealthStatus.DEGRADED,
                'error': str(e),
                'message': 'Celery check failed (may not be running)'
            }
    
    def check_all(self) -> Dict[str, Any]:
        """Выполнить все проверки здоровья"""
        results = {
            'timestamp': datetime.utcnow().isoformat(),
            'overall_status': HealthStatus.HEALTHY,
            'checks': {}
        }
        
        # Выполнение всех проверок
        checks_to_run = {
            'database': self.check_database,
            'redis': self.check_redis,
            'disk': self.check_disk_space,
            'memory': self.check_memory,
            'cpu': self.check_cpu,
            'celery': self.check_celery
        }
        
        critical_failed = False
        degraded_count = 0
        
        for name, check_func in checks_to_run.items():
            result = check_func()
            results['checks'][name] = result
            
            # Определение общего статуса
            if result['status'] == HealthStatus.UNHEALTHY:
                if name in ['database']:  # Критичные компоненты
                    critical_failed = True
                degraded_count += 1
            elif result['status'] == HealthStatus.DEGRADED:
                degraded_count += 1
        
        # Установка общего статуса
        if critical_failed:
            results['overall_status'] = HealthStatus.UNHEALTHY
        elif degraded_count > 2:
            results['overall_status'] = HealthStatus.DEGRADED
        elif degraded_count > 0:
            results['overall_status'] = HealthStatus.DEGRADED
        
        self.last_check_time = datetime.utcnow()
        return results
    
    def get_summary(self) -> Dict[str, Any]:
        """Получить краткую сводку здоровья"""
        health = self.check_all()
        
        return {
            'status': health['overall_status'],
            'timestamp': health['timestamp'],
            'healthy_checks': sum(
                1 for check in health['checks'].values()
                if check['status'] == HealthStatus.HEALTHY
            ),
            'total_checks': len(health['checks']),
            'critical_issues': [
                name for name, check in health['checks'].items()
                if check['status'] == HealthStatus.UNHEALTHY
            ]
        }


# Глобальный экземпляр
health_checker = HealthChecker()
