"""
Модуль профилирования производительности с API эндпоинтами
"""
import time
import cProfile
import pstats
import io
import json
from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user
import psutil
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

profiling_api = Blueprint('profiling_api', __name__)

class PerformanceProfiler:
    """Система профилирования производительности приложения"""
    
    def __init__(self):
        self.profiles = {}
        self.profile_stats = {}
        self.resource_monitoring = True
        self.monitoring_data = []
        
    def start_profiling(self, name: str = "default"):
        """Начать профилирование с указанным именем"""
        profiler = cProfile.Profile()
        profiler.enable()
        
        self.profiles[name] = {
            'profiler': profiler,
            'start_time': time.time(),
            'start_resources': self._get_resource_usage()
        }
        
        logger.info(f"Начато профилирование: {name}")
    
    def stop_profiling(self, name: str = "default") -> Dict[str, Any]:
        """Остановить профилирование и получить результаты"""
        if name not in self.profiles:
            return {'error': f'Профилирование {name} не найдено'}
        
        profile_info = self.profiles[name]
        profile_info['profiler'].disable()
        
        # Получение статистики
        s = io.StringIO()
        ps = pstats.Stats(profile_info['profiler'], stream=s)
        ps.sort_stats('cumulative')
        ps.print_stats()
        
        end_time = time.time()
        end_resources = self._get_resource_usage()
        
        # Сбор статистики производительности
        stats = {
            'name': name,
            'duration': end_time - profile_info['start_time'],
            'start_time': profile_info['start_time'],
            'end_time': end_time,
            'resource_usage_start': profile_info['start_resources'],
            'resource_usage_end': end_resources,
            'cpu_diff': {
                'user_time': end_resources['cpu_times'].user - profile_info['start_resources']['cpu_times'].user,
                'system_time': end_resources['cpu_times'].system - profile_info['start_resources']['cpu_times'].system,
            },
            'memory_diff': end_resources['memory_info'].rss - profile_info['start_resources']['memory_info'].rss,
            'profile_stats': s.getvalue()[:10000],  # Ограничение объема данных
            'top_functions': self._get_top_functions(ps)
        }
        
        self.profile_stats[name] = stats
        del self.profiles[name]
        
        logger.info(f"Завершено профилирование: {name}, длительность: {stats['duration']:.2f}с")
        
        # Ограничение количества сохраненных профилей
        if len(self.profile_stats) > 50:
            oldest_key = min(self.profile_stats.keys(), key=lambda k: self.profile_stats[k]['start_time'])
            del self.profile_stats[oldest_key]
        
        return stats
    
    def _get_resource_usage(self) -> Dict[str, Any]:
        """Получение текущего использования ресурсов"""
        process = psutil.Process(os.getpid())
        
        return {
            'cpu_percent': process.cpu_percent(),
            'cpu_times': process.cpu_times(),
            'memory_info': process.memory_info(),
            'memory_percent': process.memory_percent(),
            'num_threads': process.num_threads(),
            'num_fds': process.num_fds() if hasattr(process, 'num_fds') else 0,
            'io_counters': process.io_counters() if hasattr(process, 'io_counters') else None,
            'connections': len(process.connections())
        }
    
    def _get_top_functions(self, stats: pstats.Stats, limit: int = 10) -> List[Dict[str, Any]]:
        """Получение топ функций по времени выполнения"""
        # Сортировка статистики
        stats.sort_stats('cumulative')
        
        top_funcs = []
        for func_tuple in stats.fcn_list[:limit]:
            cc, nc, tt, ct, callers = stats.stats[func_tuple]
            top_funcs.append({
                'function': func_tuple,
                'call_count': cc,
                'primitive_call_count': nc,
                'total_time': ct,
                'local_time': tt
            })
        
        return top_funcs
    
    def get_all_profiles(self) -> Dict[str, Any]:
        """Получение всех сохраненных профилей"""
        return {
            'profiles': self.profile_stats,
            'current_profiles': list(self.profiles.keys()),
            'total_profiles': len(self.profile_stats)
        }
    
    def get_resource_trends(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Получение трендов использования ресурсов"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        trends = []
        
        # Здесь должна быть реализация сбора исторических данных
        # Для демонстрации возвращаем заглушку
        current_resources = self._get_resource_usage()
        trends.append({
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': current_resources['cpu_percent'],
            'memory_rss': current_resources['memory_info'].rss,
            'num_threads': current_resources['num_threads']
        })
        
        return trends
    
    def clear_profiles(self):
        """Очистка всех сохраненных профилей"""
        self.profile_stats.clear()
        self.profiles.clear()
        logger.info("Все профили производительности очищены")

# Глобальный экземпляр профайлера
performance_profiler = PerformanceProfiler()

@profiling_api.route('/profile/start', methods=['POST'])
@login_required
def start_profiling_endpoint():
    """Начать профилирование"""
    if not current_user.is_admin:
        return jsonify({'error': 'Требуются права администратора'}), 403
    
    data = request.get_json() or {}
    name = data.get('name', 'default')
    
    try:
        performance_profiler.start_profiling(name)
        return jsonify({
            'success': True,
            'message': f'Профилирование {name} начато',
            'name': name
        })
    except Exception as e:
        logger.error(f"Ошибка начала профилирования: {e}")
        return jsonify({'error': str(e)}), 500

@profiling_api.route('/profile/stop', methods=['POST'])
@login_required
def stop_profiling_endpoint():
    """Остановить профилирование"""
    if not current_user.is_admin:
        return jsonify({'error': 'Требуются права администратора'}), 403
    
    data = request.get_json() or {}
    name = data.get('name', 'default')
    
    try:
        result = performance_profiler.stop_profiling(name)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Ошибка остановки профилирования: {e}")
        return jsonify({'error': str(e)}), 500

@profiling_api.route('/profile/results')
@login_required
def get_profile_results():
    """Получить результаты профилирования"""
    if not current_user.is_admin:
        return jsonify({'error': 'Требуются права администратора'}), 403
    
    try:
        profiles = performance_profiler.get_all_profiles()
        return jsonify(profiles)
    except Exception as e:
        logger.error(f"Ошибка получения результатов профилирования: {e}")
        return jsonify({'error': str(e)}), 500

@profiling_api.route('/profile/current')
@login_required
def get_current_profiles():
    """Получить список активных профилей"""
    if not current_user.is_admin:
        return jsonify({'error': 'Требуются права администратора'}), 403
    
    try:
        current = list(performance_profiler.profiles.keys())
        return jsonify({
            'current_profiles': current,
            'count': len(current)
        })
    except Exception as e:
        logger.error(f"Ошибка получения активных профилей: {e}")
        return jsonify({'error': str(e)}), 500

@profiling_api.route('/profile/trends')
@login_required
def get_resource_trends():
    """Получить тренды использования ресурсов"""
    if not current_user.is_admin:
        return jsonify({'error': 'Требуются права администратора'}), 403
    
    try:
        hours = int(request.args.get('hours', 24))
        trends = performance_profiler.get_resource_trends(hours)
        return jsonify({
            'trends': trends,
            'hours': hours,
            'total_points': len(trends)
        })
    except Exception as e:
        logger.error(f"Ошибка получения трендов: {e}")
        return jsonify({'error': str(e)}), 500

@profiling_api.route('/profile/clear', methods=['POST'])
@login_required
def clear_profiles():
    """Очистить все профили"""
    if not current_user.is_admin:
        return jsonify({'error': 'Требуются права администратора'}), 403
    
    try:
        performance_profiler.clear_profiles()
        return jsonify({
            'success': True,
            'message': 'Все профили производительности очищены'
        })
    except Exception as e:
        logger.error(f"Ошибка очистки профилей: {e}")
        return jsonify({'error': str(e)}), 500

@profiling_api.route('/system/resources')
@login_required
def get_system_resources():
    """Получить текущие ресурсы системы"""
    if not current_user.is_admin:
        return jsonify({'error': 'Требуются права администратора'}), 403
    
    try:
        resources = performance_profiler._get_resource_usage()
        system_info = {
            'cpu_count': psutil.cpu_count(),
            'cpu_percent': psutil.cpu_percent(),
            'memory_total': psutil.virtual_memory().total,
            'memory_available': psutil.virtual_memory().available,
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'process_resources': resources
        }
        return jsonify(system_info)
    except Exception as e:
        logger.error(f"Ошибка получения ресурсов системы: {e}")
        return jsonify({'error': str(e)}), 500

@profiling_api.route('/profile/function_trace', methods=['POST'])
@login_required
def function_trace():
    """Профилировать выполнение конкретной функции"""
    if not current_user.is_admin:
        return jsonify({'error': 'Требуются права администратора'}), 403
    
    data = request.get_json()
    if not data or 'function_name' not in data:
        return jsonify({'error': 'Требуется имя функции'}), 400
    
    # Здесь должна быть реализация трассировки конкретной функции
    # Для безопасности реализуем только встроенные функции
    
    function_name = data['function_name']
    duration = data.get('duration', 1)  # по умолчанию 1 секунда
    
    # Для демонстрации просто выполняем профилирование в течение заданного времени
    profile_name = f"function_trace_{function_name}_{int(time.time())}"
    
    try:
        performance_profiler.start_profiling(profile_name)
        
        # Имитация выполнения функции
        start_time = time.time()
        while time.time() - start_time < duration:
            # Небольшая нагрузка для профилирования
            _ = [i*i for i in range(1000)]
            time.sleep(0.01)
        
        result = performance_profiler.stop_profiling(profile_name)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Ошибка трассировки функции: {e}")
        return jsonify({'error': str(e)}), 500

# Flask CLI команды для профилирования
def register_profiling_commands(app):
    """Регистрация CLI команд для профилирования"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('profile-app')
    @click.option('--name', default='cli-profile', help='Имя профиля')
    @click.option('--duration', default=5, type=int, help='Длительность профилирования в секундах')
    @with_appcontext
    def profile_application(name, duration):
        """Профилировать приложение в течение указанного времени"""
        click.echo(f"Начало профилирования приложения: {name} на {duration} секунд")
        
        performance_profiler.start_profiling(name)
        
        # Имитация нагрузки на приложение
        import time
        start_time = time.time()
        while time.time() - start_time < duration:
            # Небольшая вычислительная нагрузка
            _ = [i**2 for i in range(10000)]
            time.sleep(0.1)
        
        result = performance_profiler.stop_profiling(name)
        click.echo(f"Профилирование завершено. Длительность: {result['duration']:.2f}с")
        click.echo(f"Пиковое использование памяти: {result['memory_diff']:,} байт")
    
    @app.cli.command('show-profiles')
    @with_appcontext
    def show_profiles():
        """Показать сохраненные профили"""
        profiles = performance_profiler.get_all_profiles()
        click.echo(f"Сохранено профилей: {profiles['total_profiles']}")
        click.echo(f"Активных профилей: {len(profiles['current_profiles'])}")
        
        for name, stats in profiles['profiles'].items():
            click.echo(f"  {name}: {stats['duration']:.2f}с, {stats['memory_diff']:,} байт")
    
    @app.cli.command('clear-profiles')
    @with_appcontext
    def clear_profiles_cli():
        """Очистить все профили"""
        performance_profiler.clear_profiles()
        click.echo("Все профили производительности очищены")