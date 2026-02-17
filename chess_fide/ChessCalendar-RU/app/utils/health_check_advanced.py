"""
Расширенная система health checks для микросервисов
Проверяет состояние всех компонентов системы
"""
import time
import logging
from typing import Dict, Any, List
from datetime import datetime
import requests
from redis import Redis
from sqlalchemy import text

logger = logging.getLogger(__name__)


class HealthCheckStatus:
    """Статусы health check"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class HealthChecker:
    """Централизованная система проверки здоровья сервисов"""
    
    def __init__(self, app=None):
        self.app = app
        self.checks = []
        
    def init_app(self, app):
        """Инициализация с Flask приложением"""
        self.app = app
        
    def register_check(self, name: str, check_func, critical: bool = True):
        """Регистрация новой проверки"""
        self.checks.append({
            'name': name,
            'func': check_func,
            'critical': critical
        })
        
    def check_database(self) -> Dict[str, Any]:
        """Проверка подключения к базе данных"""
        try:
            from app import db
            start = time.time()
            db.session.execute(text('SELECT 1'))
            latency = (time.time() - start) * 1000
            
            return {
                'status': HealthCheckStatus.HEALTHY,
                'latency_ms': round(latency, 2),
                'message': 'Database connection OK'
            }
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                'status': HealthCheckStatus.UNHEALTHY,
                'error': str(e),
                'message': 'Database connection failed'
            }
    
    def check_redis(self) -> Dict[str, Any]:
        """Проверка подключения к Redis"""
        try:
            redis_url = self.app.config.get('REDIS_URL', 'redis://localhost:6379/0')
            redis_client = Redis.from_url(redis_url)
            
            start = time.time()
            redis_client.ping()
            latency = (time.time() - start) * 1000
            
            info = redis_client.info('memory')
            used_memory_mb = info.get('used_memory', 0) / (1024 * 1024)
            
            return {
                'status': HealthCheckStatus.HEALTHY,
                'latency_ms': round(latency, 2),
                'used_memory_mb': round(used_memory_mb, 2),
                'message': 'Redis connection OK'
            }
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return {
                'status': HealthCheckStatus.UNHEALTHY,
                'error': str(e),
                'message': 'Redis connection failed'
            }
    
    def check_celery(self) -> Dict[str, Any]:
        """Проверка Celery workers"""
        try:
            from app.celery_app import celery
            
            start = time.time()
            inspect = celery.control.inspect()
            active = inspect.active()
            latency = (time.time() - start) * 1000
            
            if active is None:
                return {
                    'status': HealthCheckStatus.UNHEALTHY,
                    'message': 'No Celery workers available'
                }
            
            worker_count = len(active.keys())
            total_tasks = sum(len(tasks) for tasks in active.values())
            
            return {
                'status': HealthCheckStatus.HEALTHY,
                'latency_ms': round(latency, 2),
                'workers': worker_count,
                'active_tasks': total_tasks,
                'message': f'{worker_count} workers active'
            }
        except Exception as e:
            logger.error(f"Celery health check failed: {e}")
            return {
                'status': HealthCheckStatus.DEGRADED,
                'error': str(e),
                'message': 'Celery check failed'
            }
    
    def check_microservice(self, name: str, url: str) -> Dict[str, Any]:
        """Проверка микросервиса"""
        try:
            start = time.time()
            response = requests.get(f"{url}/health", timeout=5)
            latency = (time.time() - start) * 1000
            
            if response.status_code == 200:
                return {
                    'status': HealthCheckStatus.HEALTHY,
                    'latency_ms': round(latency, 2),
                    'message': f'{name} is healthy'
                }
            else:
                return {
                    'status': HealthCheckStatus.DEGRADED,
                    'status_code': response.status_code,
                    'message': f'{name} returned {response.status_code}'
                }
        except requests.Timeout:
            return {
                'status': HealthCheckStatus.UNHEALTHY,
                'error': 'timeout',
                'message': f'{name} timeout'
            }
        except Exception as e:
            logger.error(f"{name} health check failed: {e}")
            return {
                'status': HealthCheckStatus.UNHEALTHY,
                'error': str(e),
                'message': f'{name} unreachable'
            }
    
    def check_disk_space(self) -> Dict[str, Any]:
        """Проверка дискового пространства"""
        try:
            import psutil
            disk = psutil.disk_usage('/')
            
            percent_used = disk.percent
            status = HealthCheckStatus.HEALTHY
            
            if percent_used > 90:
                status = HealthCheckStatus.UNHEALTHY
            elif percent_used > 80:
                status = HealthCheckStatus.DEGRADED
            
            return {
                'status': status,
                'percent_used': percent_used,
                'free_gb': round(disk.free / (1024**3), 2),
                'total_gb': round(disk.total / (1024**3), 2),
                'message': f'Disk {percent_used}% used'
            }
        except Exception as e:
            logger.error(f"Disk space check failed: {e}")
            return {
                'status': HealthCheckStatus.DEGRADED,
                'error': str(e),
                'message': 'Disk check failed'
            }
    
    def check_memory(self) -> Dict[str, Any]:
        """Проверка использования памяти"""
        try:
            import psutil
            memory = psutil.virtual_memory()
            
            percent_used = memory.percent
            status = HealthCheckStatus.HEALTHY
            
            if percent_used > 90:
                status = HealthCheckStatus.UNHEALTHY
            elif percent_used > 80:
                status = HealthCheckStatus.DEGRADED
            
            return {
                'status': status,
                'percent_used': percent_used,
                'available_gb': round(memory.available / (1024**3), 2),
                'total_gb': round(memory.total / (1024**3), 2),
                'message': f'Memory {percent_used}% used'
            }
        except Exception as e:
            logger.error(f"Memory check failed: {e}")
            return {
                'status': HealthCheckStatus.DEGRADED,
                'error': str(e),
                'message': 'Memory check failed'
            }
    
    def run_all_checks(self) -> Dict[str, Any]:
        """Запуск всех проверок"""
        results = {
            'timestamp': datetime.utcnow().isoformat(),
            'checks': {},
            'overall_status': HealthCheckStatus.HEALTHY
        }
        
        # Базовые проверки
        checks_to_run = [
            ('database', self.check_database, True),
            ('redis', self.check_redis, True),
            ('celery', self.check_celery, False),
            ('disk', self.check_disk_space, False),
            ('memory', self.check_memory, False),
        ]
        
        # Проверка микросервисов
        if self.app:
            microservices = [
                ('tournament_service', self.app.config.get('TOURNAMENT_SERVICE_URL')),
                ('user_service', self.app.config.get('USER_SERVICE_URL')),
                ('parser_service', self.app.config.get('PARSER_SERVICE_URL')),
                ('notification_service', self.app.config.get('NOTIFICATION_SERVICE_URL')),
            ]
            
            for name, url in microservices:
                if url:
                    checks_to_run.append(
                        (name, lambda u=url, n=name: self.check_microservice(n, u), False)
                    )
        
        # Выполнение проверок
        critical_failed = False
        for check_name, check_func, is_critical in checks_to_run:
            try:
                result = check_func()
                results['checks'][check_name] = result
                
                if result['status'] == HealthCheckStatus.UNHEALTHY:
                    if is_critical:
                        critical_failed = True
                    results['overall_status'] = HealthCheckStatus.UNHEALTHY
                elif result['status'] == HealthCheckStatus.DEGRADED:
                    if results['overall_status'] == HealthCheckStatus.HEALTHY:
                        results['overall_status'] = HealthCheckStatus.DEGRADED
            except Exception as e:
                logger.error(f"Check {check_name} failed: {e}")
                results['checks'][check_name] = {
                    'status': HealthCheckStatus.UNHEALTHY,
                    'error': str(e)
                }
                if is_critical:
                    critical_failed = True
        
        # Дополнительные метрики
        results['summary'] = {
            'total_checks': len(results['checks']),
            'healthy': sum(1 for c in results['checks'].values() 
                          if c['status'] == HealthCheckStatus.HEALTHY),
            'degraded': sum(1 for c in results['checks'].values() 
                           if c['status'] == HealthCheckStatus.DEGRADED),
            'unhealthy': sum(1 for c in results['checks'].values() 
                            if c['status'] == HealthCheckStatus.UNHEALTHY),
        }
        
        return results


# Глобальный экземпляр
health_checker = HealthChecker()
