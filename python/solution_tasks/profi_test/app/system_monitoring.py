# -*- coding: utf-8 -*-
"""
Модуль системного мониторинга для ПрофиТест
Предоставляет возможности мониторинга состояния системы и диагностики проблем
"""
import psutil
import time
from datetime import datetime
from app import db
from app.models import User, TestResult, Notification
import logging
import json


class SystemMonitor:
    """
    Системный монитор для приложения ПрофиТест.
    Отслеживает производительность, состояние системы и генерирует алерты.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.alert_thresholds = {
            'cpu_usage': 80,  # Процент использования CPU
            'memory_usage': 85,  # Процент использования памяти
            'disk_usage': 90,  # Процент использования диска
            'response_time': 2.0,  # Секунды
            'database_connections': 50,  # Максимальное количество соединений
            'error_rate': 5  # Процент ошибок
        }
    
    def get_system_health(self):
        """
        Получает общее состояние здоровья системы.
        
        Returns:
            dict: Состояние здоровья системы
        """
        try:
            health_status = {
                'timestamp': datetime.utcnow().isoformat(),
                'system_metrics': self._get_system_metrics(),
                'application_metrics': self._get_application_metrics(),
                'database_metrics': self._get_database_metrics(),
                'overall_status': 'healthy',
                'alerts': []
            }
            
            # Проверка пороговых значений и генерация алертов
            alerts = self._check_thresholds(health_status)
            health_status['alerts'] = alerts
            
            # Определение общего статуса
            if any(alert['severity'] == 'critical' for alert in alerts):
                health_status['overall_status'] = 'critical'
            elif any(alert['severity'] == 'warning' for alert in alerts):
                health_status['overall_status'] = 'degraded'
            
            return health_status
            
        except Exception as e:
            self.logger.error(f"Ошибка при получении состояния здоровья системы: {str(e)}")
            return {
                'timestamp': datetime.utcnow().isoformat(),
                'overall_status': 'error',
                'error': str(e)
            }
    
    def _get_system_metrics(self):
        """
        Получает системные метрики.
        
        Returns:
            dict: Системные метрики
        """
        try:
            # Метрики CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Метрики памяти
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available = memory.available / (1024**3)  # ГБ
            memory_total = memory.total / (1024**3)  # ГБ
            
            # Метрики диска
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            disk_free = disk.free / (1024**3)  # ГБ
            
            # Метрики сети
            net_io = psutil.net_io_counters()
            
            return {
                'cpu': {
                    'usage_percent': cpu_percent,
                    'core_count': cpu_count,
                    'status': 'healthy' if cpu_percent < self.alert_thresholds['cpu_usage'] else 'warning'
                },
                'memory': {
                    'usage_percent': memory_percent,
                    'available_gb': round(memory_available, 2),
                    'total_gb': round(memory_total, 2),
                    'status': 'healthy' if memory_percent < self.alert_thresholds['memory_usage'] else 'warning'
                },
                'disk': {
                    'usage_percent': disk_percent,
                    'free_gb': round(disk_free, 2),
                    'status': 'healthy' if disk_percent < self.alert_thresholds['disk_usage'] else 'warning'
                },
                'network': {
                    'bytes_sent': net_io.bytes_sent,
                    'bytes_recv': net_io.bytes_recv
                }
            }
        except Exception as e:
            self.logger.error(f"Ошибка при получении системных метрик: {str(e)}")
            return {'error': str(e)}
    
    def _get_application_metrics(self):
        """
        Получает метрики приложения.
        
        Returns:
            dict: Метрики приложения
        """
        try:
            # Количество пользователей
            total_users = User.query.count()
            active_users = db.session.query(User.id).filter(User.created_at >= datetime.utcnow() - timedelta(days=30)).count()
            
            # Количество тестов
            total_tests = TestResult.query.count()
            recent_tests = TestResult.query.filter(TestResult.created_at >= datetime.utcnow() - timedelta(days=7)).count()
            
            # Количество уведомлений
            total_notifications = Notification.query.count()
            unread_notifications = Notification.query.filter_by(is_read=False).count()
            
            return {
                'users': {
                    'total': total_users,
                    'active_last_30_days': active_users,
                    'active_ratio': round((active_users / total_users * 100) if total_users > 0 else 0, 2)
                },
                'tests': {
                    'total': total_tests,
                    'recent_7_days': recent_tests,
                    'avg_per_user': round(total_tests / total_users, 2) if total_users > 0 else 0
                },
                'notifications': {
                    'total': total_notifications,
                    'unread': unread_notifications,
                    'read_ratio': round(((total_notifications - unread_notifications) / total_notifications * 100) if total_notifications > 0 else 0, 2)
                }
            }
        except Exception as e:
            self.logger.error(f"Ошибка при получении метрик приложения: {str(e)}")
            return {'error': str(e)}
    
    def _get_database_metrics(self):
        """
        Получает метрики базы данных.
        
        Returns:
            dict: Метрики базы данных
        """
        try:
            # Количество записей в различных таблицах
            user_count = User.query.count()
            test_result_count = TestResult.query.count()
            notification_count = Notification.query.count()
            
            # Информация о соединениях (если доступна)
            connection_info = {}
            try:
                # Для PostgreSQL можно использовать: db.session.execute('SELECT count(*) FROM pg_stat_activity;')
                # Пока заглушка
                connection_info = {
                    'active_connections': 10,  # Значение по умолчанию
                    'max_connections': 100,    # Значение по умолчанию
                    'connection_usage': 10     # Значение по умолчанию
                }
            except Exception:
                connection_info = {
                    'active_connections': 'unknown',
                    'max_connections': 'unknown',
                    'connection_usage': 'unknown'
                }
            
            return {
                'tables': {
                    'users': user_count,
                    'test_results': test_result_count,
                    'notifications': notification_count
                },
                'connections': connection_info,
                'status': 'healthy' if connection_info.get('active_connections', 0) < self.alert_thresholds['database_connections'] else 'warning'
            }
        except Exception as e:
            self.logger.error(f"Ошибка при получении метрик базы данных: {str(e)}")
            return {'error': str(e)}
    
    def _check_thresholds(self, health_status):
        """
        Проверяет пороговые значения и генерирует алерты.
        
        Args:
            health_status: Текущее состояние здоровья
            
        Returns:
            list: Список алертов
        """
        alerts = []
        
        try:
            # Проверка системных метрик
            system_metrics = health_status.get('system_metrics', {})
            
            cpu_metrics = system_metrics.get('cpu', {})
            if cpu_metrics.get('usage_percent', 0) > self.alert_thresholds['cpu_usage']:
                alerts.append({
                    'type': 'high_cpu_usage',
                    'severity': 'warning',
                    'message': f"Высокое использование CPU: {cpu_metrics['usage_percent']:.1f}%",
                    'timestamp': datetime.utcnow().isoformat()
                })
            
            memory_metrics = system_metrics.get('memory', {})
            if memory_metrics.get('usage_percent', 0) > self.alert_thresholds['memory_usage']:
                alerts.append({
                    'type': 'high_memory_usage',
                    'severity': 'warning',
                    'message': f"Высокое использование памяти: {memory_metrics['usage_percent']:.1f}%",
                    'timestamp': datetime.utcnow().isoformat()
                })
            
            disk_metrics = system_metrics.get('disk', {})
            if disk_metrics.get('usage_percent', 0) > self.alert_thresholds['disk_usage']:
                alerts.append({
                    'type': 'low_disk_space',
                    'severity': 'critical' if disk_metrics['usage_percent'] > 95 else 'warning',
                    'message': f"Недостаточно места на диске: {disk_metrics['usage_percent']:.1f}% использовано",
                    'timestamp': datetime.utcnow().isoformat()
                })
            
            # Проверка метрик приложения
            app_metrics = health_status.get('application_metrics', {})
            
            user_metrics = app_metrics.get('users', {})
            if user_metrics.get('total', 0) == 0:
                alerts.append({
                    'type': 'no_users',
                    'severity': 'critical',
                    'message': 'В системе нет пользователей',
                    'timestamp': datetime.utcnow().isoformat()
                })
            
            # Проверка метрик базы данных
            db_metrics = health_status.get('database_metrics', {})
            if db_metrics.get('status') == 'warning':
                alerts.append({
                    'type': 'database_load',
                    'severity': 'warning',
                    'message': 'Высокая нагрузка на базу данных',
                    'timestamp': datetime.utcnow().isoformat()
                })
            
        except Exception as e:
            self.logger.error(f"Ошибка при проверке пороговых значений: {str(e)}")
            alerts.append({
                'type': 'monitoring_error',
                'severity': 'warning',
                'message': f'Ошибка в системе мониторинга: {str(e)}',
                'timestamp': datetime.utcnow().isoformat()
            })
        
        return alerts
    
    def get_detailed_performance_report(self):
        """
        Генерирует детальный отчет о производительности системы.
        
        Returns:
            dict: Детальный отчет о производительности
        """
        try:
            start_time = time.time()
            
            # Собираем все данные для отчета
            performance_report = {
                'report_timestamp': datetime.utcnow().isoformat(),
                'generation_time_ms': 0,
                'system_overview': self.get_system_health(),
                'performance_benchmarks': self._run_performance_benchmarks(),
                'resource_trends': self._get_resource_trends(),
                'recommendations': self._generate_performance_recommendations()
            }
            
            # Фиксация времени генерации отчета
            performance_report['generation_time_ms'] = round((time.time() - start_time) * 1000, 2)
            
            return performance_report
            
        except Exception as e:
            self.logger.error(f"Ошибка при генерации отчета о производительности: {str(e)}")
            return {'error': str(e)}
    
    def _run_performance_benchmarks(self):
        """
        Выполняет бенчмарки производительности.
        
        Returns:
            dict: Результаты бенчмарков
        """
        try:
            benchmarks = {}
            
            # Бенчмарк базы данных - подсчет пользователей
            start_time = time.time()
            user_count = User.query.count()
            db_query_time = (time.time() - start_time) * 1000  # мс
            
            benchmarks['database'] = {
                'user_count_query_ms': round(db_query_time, 2),
                'total_users': user_count,
                'performance': 'good' if db_query_time < 100 else 'slow'
            }
            
            # Бенчмарк памяти
            start_time = time.time()
            memory_info = psutil.virtual_memory()
            memory_check_time = (time.time() - start_time) * 1000  # мс
            
            benchmarks['memory'] = {
                'check_time_ms': round(memory_check_time, 2),
                'usage_percent': memory_info.percent,
                'performance': 'good' if memory_check_time < 10 else 'slow'
            }
            
            return benchmarks
            
        except Exception as e:
            self.logger.error(f"Ошибка при выполнении бенчмарков: {str(e)}")
            return {'error': str(e)}
    
    def _get_resource_trends(self):
        """
        Получает тренды использования ресурсов.
        
        Returns:
            dict: Тренды использования ресурсов
        """
        try:
            # В реальной системе здесь будут данные из системы мониторинга
            # Пока возвращаем заглушку с текущими значениями
            current_metrics = self._get_system_metrics()
            
            return {
                'cpu_trend': 'stable',  # stable, increasing, decreasing
                'memory_trend': 'stable',
                'disk_trend': 'stable',
                'current_metrics': current_metrics
            }
        except Exception as e:
            self.logger.error(f"Ошибка при получении трендов ресурсов: {str(e)}")
            return {'error': str(e)}
    
    def _generate_performance_recommendations(self):
        """
        Генерирует рекомендации по оптимизации производительности.
        
        Returns:
            list: Список рекомендаций
        """
        try:
            recommendations = []
            
            # Получаем текущее состояние
            health_status = self.get_system_health()
            
            # Рекомендации на основе системных метрик
            system_metrics = health_status.get('system_metrics', {})
            
            cpu_metrics = system_metrics.get('cpu', {})
            if cpu_metrics.get('usage_percent', 0) > 70:
                recommendations.append({
                    'type': 'cpu_optimization',
                    'priority': 'medium',
                    'description': 'Высокое использование CPU',
                    'actions': [
                        'Оптимизируйте запросы к базе данных',
                        'Рассмотрите масштабирование',
                        'Проверьте фоновые процессы'
                    ]
                })
            
            memory_metrics = system_metrics.get('memory', {})
            if memory_metrics.get('usage_percent', 0) > 80:
                recommendations.append({
                    'type': 'memory_optimization',
                    'priority': 'high',
                    'description': 'Высокое использование памяти',
                    'actions': [
                        'Увеличьте объем оперативной памяти',
                        'Оптимизируйте использование кэша',
                        'Проверьте утечки памяти'
                    ]
                })
            
            disk_metrics = system_metrics.get('disk', {})
            if disk_metrics.get('usage_percent', 0) > 85:
                recommendations.append({
                    'type': 'disk_optimization',
                    'priority': 'high',
                    'description': 'Недостаточно свободного места на диске',
                    'actions': [
                        'Очистите временные файлы',
                        'Архивируйте старые данные',
                        'Рассмотрите расширение дискового пространства'
                    ]
                })
            
            # Рекомендации на основе метрик приложения
            app_metrics = health_status.get('application_metrics', {})
            user_metrics = app_metrics.get('users', {})
            
            if user_metrics.get('active_ratio', 0) < 10:
                recommendations.append({
                    'type': 'user_engagement',
                    'priority': 'medium',
                    'description': 'Низкий уровень вовлеченности пользователей',
                    'actions': [
                        'Внедрите программу мотивации',
                        'Добавьте напоминания',
                        'Улучшите пользовательский интерфейс'
                    ]
                })
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Ошибка при генерации рекомендаций: {str(e)}")
            return []


# Глобальный экземпляр
system_monitor = SystemMonitor()