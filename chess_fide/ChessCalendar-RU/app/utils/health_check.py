#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Health Check система для мониторинга состояния приложения
"""

import logging
import time
from datetime import datetime
from typing import Dict, Any, List
import psutil

logger = logging.getLogger('chess_calendar')


class HealthCheck:
    """Класс для проверки здоровья приложения"""
    
    def __init__(self, app=None, db=None):
        self.app = app
        self.db = db
        self.checks = []
        self.start_time = time.time()
    
    def register_check(self, name: str, check_func, critical: bool = True):
        """
        Регистрация проверки здоровья
        
        Args:
            name: Название проверки
            check_func: Функция проверки (должна возвращать bool)
            critical: Критична ли проверка для работы приложения
        """
        self.checks.append({
            'name': name,
            'func': check_func,
            'critical': critical
        })
    
    def check_database(self) -> Dict[str, Any]:
        """Проверка подключения к базе данных"""
        try:
            if not self.db:
                return {
                    'status': 'unknown',
                    'message': 'Database not initialized',
                    'healthy': False
                }
            
            # Пробуем выполнить простой запрос
            from sqlalchemy import text
            with self.app.app_context():
                result = self.db.session.execute(text('SELECT 1')).scalar()
                
                if result == 1:
                    return {
                        'status': 'healthy',
                        'message': 'Database connection OK',
                        'healthy': True
                    }
                else:
                    return {
                        'status': 'unhealthy',
                        'message': 'Database query returned unexpected result',
                        'healthy': False
                    }
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                'status': 'unhealthy',
                'message': f'Database error: {str(e)}',
                'healthy': False
            }
    
    def check_redis(self) -> Dict[str, Any]:
        """Проверка подключения к Redis"""
        try:
            import redis
            redis_url = self.app.config.get('REDIS_URL', 'redis://localhost:6379/0')
            r = redis.from_url(redis_url)
            r.ping()
            
            # Получаем информацию о Redis
            info = r.info()
            
            return {
                'status': 'healthy',
                'message': 'Redis connection OK',
                'healthy': True,
                'details': {
                    'version': info.get('redis_version'),
                    'used_memory': info.get('used_memory_human'),
                    'connected_clients': info.get('connected_clients')
                }
            }
        except Exception as e:
            logger.warning(f"Redis health check failed: {e}")
            return {
                'status': 'degraded',
                'message': f'Redis unavailable: {str(e)}',
                'healthy': False
            }
    
    def check_disk_space(self) -> Dict[str, Any]:
        """Проверка свободного места на диске"""
        try:
            disk = psutil.disk_usage('/')
            percent_used = disk.percent
            
            if percent_used > 90:
                status = 'critical'
                healthy = False
            elif percent_used > 80:
                status = 'warning'
                healthy = True
            else:
                status = 'healthy'
                healthy = True
            
            return {
                'status': status,
                'message': f'Disk usage: {percent_used}%',
                'healthy': healthy,
                'details': {
                    'total': f'{disk.total / (1024**3):.2f} GB',
                    'used': f'{disk.used / (1024**3):.2f} GB',
                    'free': f'{disk.free / (1024**3):.2f} GB',
                    'percent': percent_used
                }
            }
        except Exception as e:
            logger.error(f"Disk space check failed: {e}")
            return {
                'status': 'unknown',
                'message': f'Could not check disk space: {str(e)}',
                'healthy': True  # Не критично
            }
    
    def check_memory(self) -> Dict[str, Any]:
        """Проверка использования памяти"""
        try:
            memory = psutil.virtual_memory()
            percent_used = memory.percent
            
            if percent_used > 90:
                status = 'critical'
                healthy = False
            elif percent_used > 80:
                status = 'warning'
                healthy = True
            else:
                status = 'healthy'
                healthy = True
            
            return {
                'status': status,
                'message': f'Memory usage: {percent_used}%',
                'healthy': healthy,
                'details': {
                    'total': f'{memory.total / (1024**3):.2f} GB',
                    'available': f'{memory.available / (1024**3):.2f} GB',
                    'used': f'{memory.used / (1024**3):.2f} GB',
                    'percent': percent_used
                }
            }
        except Exception as e:
            logger.error(f"Memory check failed: {e}")
            return {
                'status': 'unknown',
                'message': f'Could not check memory: {str(e)}',
                'healthy': True  # Не критично
            }
    
    def check_cpu(self) -> Dict[str, Any]:
        """Проверка загрузки CPU"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            if cpu_percent > 90:
                status = 'critical'
                healthy = False
            elif cpu_percent > 80:
                status = 'warning'
                healthy = True
            else:
                status = 'healthy'
                healthy = True
            
            return {
                'status': status,
                'message': f'CPU usage: {cpu_percent}%',
                'healthy': healthy,
                'details': {
                    'percent': cpu_percent,
                    'count': cpu_count
                }
            }
        except Exception as e:
            logger.error(f"CPU check failed: {e}")
            return {
                'status': 'unknown',
                'message': f'Could not check CPU: {str(e)}',
                'healthy': True  # Не критично
            }
    
    def get_uptime(self) -> Dict[str, Any]:
        """Получить время работы приложения"""
        uptime_seconds = time.time() - self.start_time
        uptime_hours = uptime_seconds / 3600
        uptime_days = uptime_hours / 24
        
        return {
            'seconds': int(uptime_seconds),
            'hours': round(uptime_hours, 2),
            'days': round(uptime_days, 2),
            'formatted': self._format_uptime(uptime_seconds)
        }
    
    def _format_uptime(self, seconds: float) -> str:
        """Форматирование времени работы"""
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        parts.append(f"{secs}s")
        
        return " ".join(parts)
    
    def run_all_checks(self) -> Dict[str, Any]:
        """Запустить все проверки здоровья"""
        results = {
            'timestamp': datetime.utcnow().isoformat(),
            'uptime': self.get_uptime(),
            'checks': {},
            'overall_status': 'healthy',
            'healthy': True
        }
        
        # Встроенные проверки
        checks_to_run = [
            ('database', self.check_database, True),
            ('redis', self.check_redis, False),
            ('disk', self.check_disk_space, False),
            ('memory', self.check_memory, False),
            ('cpu', self.check_cpu, False)
        ]
        
        # Добавляем пользовательские проверки
        for check in self.checks:
            checks_to_run.append((
                check['name'],
                check['func'],
                check['critical']
            ))
        
        # Выполняем все проверки
        critical_failed = False
        any_failed = False
        
        for name, check_func, critical in checks_to_run:
            try:
                result = check_func()
                results['checks'][name] = result
                
                if not result.get('healthy', True):
                    any_failed = True
                    if critical:
                        critical_failed = True
            except Exception as e:
                logger.error(f"Health check '{name}' failed: {e}")
                results['checks'][name] = {
                    'status': 'error',
                    'message': f'Check failed: {str(e)}',
                    'healthy': False
                }
                any_failed = True
                if critical:
                    critical_failed = True
        
        # Определяем общий статус
        if critical_failed:
            results['overall_status'] = 'unhealthy'
            results['healthy'] = False
        elif any_failed:
            results['overall_status'] = 'degraded'
            results['healthy'] = True
        else:
            results['overall_status'] = 'healthy'
            results['healthy'] = True
        
        return results
    
    def get_simple_status(self) -> Dict[str, Any]:
        """Получить простой статус (быстрая проверка)"""
        try:
            # Только критичные проверки
            db_check = self.check_database()
            
            return {
                'status': 'ok' if db_check['healthy'] else 'error',
                'timestamp': datetime.utcnow().isoformat(),
                'uptime': self.get_uptime()['formatted']
            }
        except Exception as e:
            logger.error(f"Simple health check failed: {e}")
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }


# Глобальный экземпляр
health_check = None


def init_health_check(app, db):
    """
    Инициализация health check системы
    
    Args:
        app: Flask приложение
        db: SQLAlchemy объект
    """
    global health_check
    health_check = HealthCheck(app, db)
    logger.info("Health check system initialized")
    return health_check


def get_health_check():
    """Получить глобальный экземпляр health check"""
    return health_check
