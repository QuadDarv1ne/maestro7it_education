# -*- coding: utf-8 -*-
"""
Модуль продвинутой оптимизации памяти для веб-приложения
Обеспечивает мониторинг, анализ и оптимизацию использования памяти
"""
import logging
import gc
import psutil
import tracemalloc
from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
import threading
import time
import weakref
import sys
from functools import wraps

logger = logging.getLogger(__name__)

class MemoryOptimizer:
    """Продвинутый оптимизатор памяти с мониторингом и автоматической очисткой"""
    
    def __init__(self, app=None):
        self.app = app
        self.monitoring_active = False
        self.memory_stats = defaultdict(list)
        self.object_tracker = defaultdict(int)
        self.leak_candidates = deque(maxlen=1000)
        self.optimization_history = deque(maxlen=100)
        self.lock = threading.Lock()
        
        # Пороговые значения
        self.thresholds = {
            'memory_warning_mb': 500,
            'memory_critical_mb': 800,
            'gc_frequency_seconds': 300,  # 5 минут
            'object_count_threshold': 10000,
            'leak_detection_window': 3600  # 1 час
        }
        
        # Трекинг памяти
        self.memory_snapshots = deque(maxlen=100)
        self.tracking_enabled = False
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация с Flask приложением"""
        self.app = app
        self._start_monitoring()
        logger.info("Продвинутый оптимизатор памяти инициализирован")
    
    def _start_monitoring(self):
        """Запуск фонового мониторинга памяти"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        
        def monitor_memory():
            while self.monitoring_active:
                try:
                    self._collect_memory_stats()
                    self._detect_memory_leaks()
                    self._check_thresholds()
                    time.sleep(60)  # Проверка каждую минуту
                except Exception as e:
                    logger.error(f"Ошибка мониторинга памяти: {e}")
                    time.sleep(60)
        
        monitor_thread = threading.Thread(target=monitor_memory, daemon=True)
        monitor_thread.start()
    
    def _collect_memory_stats(self):
        """Сбор статистики использования памяти"""
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            
            stats = {
                'timestamp': datetime.now(),
                'rss_mb': memory_info.rss / 1024 / 1024,
                'vms_mb': memory_info.vms / 1024 / 1024,
                'object_count': len(gc.get_objects()),
                'garbage_count': len(gc.garbage),
                'gc_collections': gc.get_count()
            }
            
            with self.lock:
                for key, value in stats.items():
                    self.memory_stats[key].append(value)
                    # Оставляем только последние 1000 измерений
                    if len(self.memory_stats[key]) > 1000:
                        self.memory_stats[key] = self.memory_stats[key][-500:]
            
            # Сохранение снимка памяти если включено трекинг
            if self.tracking_enabled:
                self._take_memory_snapshot()
                
        except Exception as e:
            logger.error(f"Ошибка сбора статистики памяти: {e}")
    
    def _take_memory_snapshot(self):
        """Создание снимка текущего состояния памяти"""
        try:
            if not tracemalloc.is_tracing():
                tracemalloc.start()
            
            snapshot = tracemalloc.take_snapshot()
            top_stats = snapshot.statistics('lineno')
            
            snapshot_data = {
                'timestamp': datetime.now(),
                'top_memory_consumers': [
                    {
                        'filename': stat.traceback.format()[0] if stat.traceback.format() else 'unknown',
                        'size_kb': stat.size / 1024,
                        'count': stat.count
                    }
                    for stat in top_stats[:10]
                ],
                'total_memory_kb': sum(stat.size for stat in top_stats) / 1024
            }
            
            self.memory_snapshots.append(snapshot_data)
            
        except Exception as e:
            logger.error(f"Ошибка создания снимка памяти: {e}")
    
    def _detect_memory_leaks(self):
        """Обнаружение потенциальных утечек памяти"""
        try:
            current_objects = gc.get_objects()
            current_count = len(current_objects)
            
            # Трекинг объектов по типам
            type_counts = defaultdict(int)
            for obj in current_objects:
                try:
                    obj_type = type(obj).__name__
                    type_counts[obj_type] += 1
                except:
                    pass
            
            # Проверка на рост количества объектов
            with self.lock:
                if len(self.memory_stats['object_count']) > 60:  # Последний час
                    previous_count = self.memory_stats['object_count'][-60]
                    growth_rate = (current_count - previous_count) / previous_count
                    
                    if growth_rate > 0.1:  # Рост более 10% за час
                        leak_info = {
                            'timestamp': datetime.now(),
                            'growth_rate': growth_rate,
                            'current_count': current_count,
                            'top_object_types': sorted(
                                type_counts.items(), 
                                key=lambda x: x[1], 
                                reverse=True
                            )[:10]
                        }
                        self.leak_candidates.append(leak_info)
                        logger.warning(f"Обнаружен потенциальный рост объектов: {growth_rate:.2%}")
            
            # Обновление трекера объектов
            self.object_tracker = type_counts
            
        except Exception as e:
            logger.error(f"Ошибка обнаружения утечек: {e}")
    
    def _check_thresholds(self):
        """Проверка пороговых значений памяти"""
        try:
            current_memory = self.get_current_memory_usage()
            
            if current_memory > self.thresholds['memory_critical_mb']:
                logger.critical(f"Критический уровень памяти: {current_memory} MB")
                self._emergency_cleanup()
                
            elif current_memory > self.thresholds['memory_warning_mb']:
                logger.warning(f"Высокий уровень памяти: {current_memory} MB")
                self._perform_cleanup()
                
        except Exception as e:
            logger.error(f"Ошибка проверки порогов: {e}")
    
    def get_current_memory_usage(self) -> float:
        """Получение текущего использования памяти в MB"""
        try:
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024
        except:
            return 0.0
    
    def _perform_cleanup(self):
        """Выполнение стандартной очистки памяти"""
        try:
            cleanup_info = {
                'timestamp': datetime.now(),
                'memory_before_mb': self.get_current_memory_usage(),
                'garbage_collected': 0,
                'weakrefs_cleaned': 0
            }
            
            # Запуск сборщика мусора
            collected = gc.collect()
            cleanup_info['garbage_collected'] = collected
            
            # Очистка слабых ссылок
            cleanup_info['weakrefs_cleaned'] = self._cleanup_weakrefs()
            
            # Очистка кэша Flask
            if hasattr(self.app, 'cache'):
                try:
                    cache_stats_before = self.app.cache.get_stats()
                    self.app.cache.clear()
                    cache_stats_after = self.app.cache.get_stats()
                    cleanup_info['cache_cleared'] = True
                except:
                    cleanup_info['cache_cleared'] = False
            
            cleanup_info['memory_after_mb'] = self.get_current_memory_usage()
            cleanup_info['memory_saved_mb'] = (
                cleanup_info['memory_before_mb'] - cleanup_info['memory_after_mb']
            )
            
            with self.lock:
                self.optimization_history.append(cleanup_info)
            
            logger.info(
                f"Очистка памяти завершена. "
                f"Освобождено: {cleanup_info['memory_saved_mb']:.2f} MB"
            )
            
        except Exception as e:
            logger.error(f"Ошибка очистки памяти: {e}")
    
    def _emergency_cleanup(self):
        """Аварийная очистка памяти"""
        logger.warning("Запуск аварийной очистки памяти")
        
        # Агрессивная очистка
        for _ in range(3):
            gc.collect()
        
        # Очистка всех кэшей
        if hasattr(self.app, 'cache'):
            try:
                self.app.cache.clear()
            except:
                pass
        
        # Сброс статистики Flask
        try:
            from flask import g
            if hasattr(g, '_request_stats'):
                delattr(g, '_request_stats')
        except:
            pass
        
        logger.info("Аварийная очистка завершена")
    
    def _cleanup_weakrefs(self) -> int:
        """Очистка недействительных слабых ссылок"""
        try:
            # Сбор всех слабых ссылок
            weak_refs = [obj for obj in gc.get_objects() if isinstance(obj, weakref.ref)]
            cleaned_count = 0
            
            for ref in weak_refs:
                if ref() is None:  # Недействительная ссылка
                    # Попытка удалить ссылку (если возможно)
                    try:
                        del ref
                        cleaned_count += 1
                    except:
                        pass
            
            return cleaned_count
        except:
            return 0
    
    def get_memory_report(self) -> Dict[str, Any]:
        """Генерация подробного отчета о памяти"""
        with self.lock:
            # Базовая статистика
            current_memory = self.get_current_memory_usage()
            object_count = len(gc.get_objects())
            garbage_count = len(gc.garbage)
            
            # Исторические данные
            memory_history = self.memory_stats.get('rss_mb', [])
            object_history = self.memory_stats.get('object_count', [])
            
            # Расчет трендов
            memory_trend = 0
            object_trend = 0
            
            if len(memory_history) > 60:
                recent_avg = sum(memory_history[-10:]) / 10
                older_avg = sum(memory_history[-60:-50]) / 10
                memory_trend = ((recent_avg - older_avg) / older_avg) * 100 if older_avg > 0 else 0
            
            if len(object_history) > 60:
                recent_avg = sum(object_history[-10:]) / 10
                older_avg = sum(object_history[-60:-50]) / 10
                object_trend = ((recent_avg - older_avg) / older_avg) * 100 if older_avg > 0 else 0
            
            # Топ потребителей памяти
            top_consumers = []
            if self.memory_snapshots:
                latest_snapshot = self.memory_snapshots[-1]
                top_consumers = latest_snapshot.get('top_memory_consumers', [])
            
            # История оптимизаций
            recent_optimizations = list(self.optimization_history)[-10:]
            
            # Потенциальные утечки
            recent_leaks = list(self.leak_candidates)[-20:]
            
            return {
                'current_status': {
                    'memory_mb': current_memory,
                    'object_count': object_count,
                    'garbage_count': garbage_count,
                    'memory_trend_percent': memory_trend,
                    'object_trend_percent': object_trend
                },
                'thresholds': self.thresholds,
                'top_memory_consumers': top_consumers,
                'recent_optimizations': recent_optimizations,
                'potential_leaks': recent_leaks,
                'recommendations': self._generate_recommendations(
                    current_memory, memory_trend, object_trend
                )
            }
    
    def _generate_recommendations(self, current_memory: float, memory_trend: float, 
                               object_trend: float) -> List[str]:
        """Генерация рекомендаций по оптимизации"""
        recommendations = []
        
        if current_memory > self.thresholds['memory_warning_mb']:
            recommendations.append("Рассмотрите увеличение лимитов памяти сервера")
        
        if memory_trend > 5:
            recommendations.append("Исследуйте рост использования памяти - возможна утечка")
        
        if object_trend > 10:
            recommendations.append("Проверьте создание объектов - возможно чрезмерное накопление")
        
        if len(gc.garbage) > 100:
            recommendations.append("Обнаружены циклические ссылки - проверьте управление памятью")
        
        if not recommendations:
            recommendations.append("Память используется эффективно")
        
        return recommendations
    
    def enable_memory_tracking(self):
        """Включение детального трекинга памяти"""
        self.tracking_enabled = True
        if not tracemalloc.is_tracing():
            tracemalloc.start()
        logger.info("Детальный трекинг памяти включен")
    
    def disable_memory_tracking(self):
        """Отключение детального трекинга памяти"""
        self.tracking_enabled = False
        tracemalloc.stop()
        logger.info("Детальный трекинг памяти отключен")
    
    def force_cleanup(self):
        """Принудительная очистка памяти"""
        logger.info("Принудительная очистка памяти запущена")
        self._emergency_cleanup()
        return self.get_memory_report()

# Глобальный экземпляр
memory_optimizer = MemoryOptimizer()

def register_memory_commands(app):
    """Регистрация CLI команд для управления памятью"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('memory-report')
    @with_appcontext
    def show_memory_report():
        """Показать отчет об использовании памяти"""
        report = memory_optimizer.get_memory_report()
        
        click.echo("Отчет об использовании памяти:")
        click.echo(f"  Текущее использование: {report['current_status']['memory_mb']:.2f} MB")
        click.echo(f"  Количество объектов: {report['current_status']['object_count']}")
        click.echo(f"  Циклических ссылок: {report['current_status']['garbage_count']}")
        click.echo(f"  Тренд памяти: {report['current_status']['memory_trend_percent']:+.2f}%")
        click.echo(f"  Тренд объектов: {report['current_status']['object_trend_percent']:+.2f}%")
        
        if report['recommendations']:
            click.echo("\nРекомендации:")
            for rec in report['recommendations']:
                click.echo(f"  - {rec}")
    
    @app.cli.command('memory-cleanup')
    @with_appcontext
    def force_memory_cleanup():
        """Принудительная очистка памяти"""
        report = memory_optimizer.force_cleanup()
        memory_saved = report['current_status']['memory_mb']
        click.echo(f"Очистка завершена. Освобождено: {memory_saved:.2f} MB")
    
    @app.cli.command('memory-track')
    @click.option('--enable/--disable', default=True, help='Включить/отключить трекинг')
    @with_appcontext
    def toggle_memory_tracking(enable):
        """Включение/отключение трекинга памяти"""
        if enable:
            memory_optimizer.enable_memory_tracking()
            click.echo("Трекинг памяти включен")
        else:
            memory_optimizer.disable_memory_tracking()
            click.echo("Трекинг памяти отключен")

# Декоратор для оптимизации функций
def memory_efficient(f):
    """Декоратор для оптимизации использования памяти в функциях"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Сбор базовой статистики
        mem_before = psutil.Process().memory_info().rss
        
        try:
            result = f(*args, **kwargs)
            return result
        finally:
            # Проверка использования памяти после выполнения
            mem_after = psutil.Process().memory_info().rss
            memory_diff = (mem_after - mem_before) / 1024 / 1024
            
            if memory_diff > 10:  # Если функция использовала более 10MB
                logger.warning(
                    f"Функция {f.__name__} использовала {memory_diff:.2f} MB памяти"
                )
                # Принудительная очистка после "тяжелых" функций
                gc.collect()
    
    return decorated_function