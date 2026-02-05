"""
Умная стратегия прогрева кэша для оптимизации производительности
"""
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Callable, Optional
from threading import Thread
import schedule
from functools import wraps

logger = logging.getLogger(__name__)

class SmartCacheWarmer:
    """Умная система прогрева кэша с предиктивной аналитикой"""
    
    def __init__(self, app=None):
        self.app = app
        self.warming_strategies = {}
        self.cache_access_patterns = {}
        self.warming_schedule = {}
        self.is_warming = False
        self.warming_thread = None
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация системы прогрева кэша"""
        self.app = app
        
        # Регистрация обработчиков доступа к кэшу
        self._register_cache_access_handlers()
        
        # Запуск планировщика прогрева
        self._start_warming_scheduler()
        
        logger.info("Умная система прогрева кэша инициализирована")
    
    def _register_cache_access_handlers(self):
        """Регистрация обработчиков для отслеживания доступа к кэшу"""
        # Оборачиваем методы кэша для сбора статистики
        from app import cache
        
        original_get = cache.get
        original_set = cache.set
        
        @wraps(original_get)
        def tracking_get(key, *args, **kwargs):
            result = original_get(key, *args, **kwargs)
            self._record_cache_access(key, 'get', result is not None)
            return result
        
        @wraps(original_set)
        def tracking_set(key, value, *args, **kwargs):
            result = original_set(key, value, *args, **kwargs)
            self._record_cache_access(key, 'set', True)
            return result
        
        cache.get = tracking_get
        cache.set = tracking_set
    
    def _record_cache_access(self, key: str, operation: str, hit: bool):
        """Запись информации о доступе к кэшу"""
        if key not in self.cache_access_patterns:
            self.cache_access_patterns[key] = {
                'access_count': 0,
                'hit_count': 0,
                'last_access': None,
                'access_times': [],
                'patterns': {}
            }
        
        pattern = self.cache_access_patterns[key]
        pattern['access_count'] += 1
        pattern['last_access'] = datetime.now()
        
        if hit:
            pattern['hit_count'] += 1
        
        # Сохранение временных меток доступа
        pattern['access_times'].append(datetime.now())
        
        # Ограничение количества сохраненных временных меток
        if len(pattern['access_times']) > 1000:
            pattern['access_times'] = pattern['access_times'][-500:]
        
        # Анализ паттернов доступа
        self._analyze_access_patterns(key, pattern)
    
    def _analyze_access_patterns(self, key: str, pattern: Dict):
        """Анализ паттернов доступа к кэшу"""
        if len(pattern['access_times']) < 10:
            return
        
        # Расчет частоты доступа
        access_times = pattern['access_times']
        time_span = (access_times[-1] - access_times[0]).total_seconds()
        access_frequency = len(access_times) / (time_span or 1)
        
        # Определение периода активности
        hourly_activity = self._calculate_hourly_activity(access_times)
        
        pattern['patterns'] = {
            'frequency': access_frequency,
            'hourly_activity': hourly_activity,
            'hit_rate': pattern['hit_count'] / pattern['access_count'],
            'trend': self._calculate_trend(access_times)
        }
    
    def _calculate_hourly_activity(self, access_times: List[datetime]) -> Dict[int, int]:
        """Расчет активности по часам"""
        hourly_count = {i: 0 for i in range(24)}
        
        for access_time in access_times:
            hour = access_time.hour
            hourly_count[hour] += 1
            
        return hourly_count
    
    def _calculate_trend(self, access_times: List[datetime]) -> str:
        """Расчет тренда использования"""
        if len(access_times) < 3:
            return 'unknown'
        
        # Простой анализ тренда на основе первых и последних 1/3 данных
        third = len(access_times) // 3
        first_period = len([t for t in access_times[:third] 
                           if t > access_times[0] + timedelta(minutes=30)])
        last_period = len([t for t in access_times[-third:] 
                          if t > access_times[-third] + timedelta(minutes=30)])
        
        if last_period > first_period * 1.5:
            return 'increasing'
        elif last_period < first_period * 0.5:
            return 'decreasing'
        else:
            return 'stable'
    
    def register_warming_strategy(self, name: str, strategy_func: Callable, 
                                schedule_pattern: str = 'daily', 
                                priority: int = 5):
        """Регистрация стратегии прогрева кэша"""
        self.warming_strategies[name] = {
            'function': strategy_func,
            'schedule': schedule_pattern,
            'priority': priority,
            'last_run': None,
            'success_count': 0,
            'failure_count': 0
        }
        
        # Добавление в планировщик
        self._schedule_warming_strategy(name, strategy_func, schedule_pattern)
        
        logger.info(f"Зарегистрирована стратегия прогрева кэша: {name}")
    
    def _schedule_warming_strategy(self, name: str, strategy_func: Callable, 
                                 schedule_pattern: str):
        """Планирование выполнения стратегии прогрева"""
        if schedule_pattern == 'daily':
            schedule.every().day.at("02:00").do(self._execute_warming_strategy, name, strategy_func)
        elif schedule_pattern == 'hourly':
            schedule.every().hour.do(self._execute_warming_strategy, name, strategy_func)
        elif schedule_pattern == 'realtime':
            # Выполнение в реальном времени при анализе паттернов
            pass
    
    def _execute_warming_strategy(self, name: str, strategy_func: Callable):
        """Выполнение стратегии прогрева кэша"""
        try:
            logger.info(f"Начало прогрева кэша: {name}")
            start_time = time.time()
            
            # Выполнение стратегии
            result = strategy_func()
            
            # Обновление статистики
            strategy = self.warming_strategies[name]
            strategy['last_run'] = datetime.now()
            strategy['success_count'] += 1
            strategy['last_duration'] = time.time() - start_time
            
            logger.info(f"Прогрев кэша завершен: {name} за {strategy['last_duration']:.2f} секунд")
            
            return result
            
        except Exception as e:
            logger.error(f"Ошибка при прогреве кэша {name}: {e}")
            strategy = self.warming_strategies[name]
            strategy['failure_count'] += 1
            strategy['last_error'] = str(e)
            return None
    
    def predict_cache_needs(self) -> List[Dict[str, Any]]:
        """Предсказание потребностей кэша на основе паттернов"""
        predictions = []
        
        for key, pattern in self.cache_access_patterns.items():
            if pattern['patterns']:
                # Определение критичных записей для прогрева
                frequency = pattern['patterns']['frequency']
                hit_rate = pattern['patterns']['hit_rate']
                trend = pattern['patterns']['trend']
                
                # Пороги для предсказания
                if (frequency > 0.1 and hit_rate > 0.7 and trend in ['stable', 'increasing']) or \
                   (frequency > 0.5):  # Часто запрашиваемые данные
                    predictions.append({
                        'key': key,
                        'priority': self._calculate_priority(pattern),
                        'predicted_access_time': self._predict_next_access(pattern),
                        'recommendation': 'Прогреть кэш'
                    })
        
        # Сортировка по приоритету
        predictions.sort(key=lambda x: x['priority'], reverse=True)
        return predictions
    
    def _calculate_priority(self, pattern: Dict) -> float:
        """Расчет приоритета прогрева для записи кэша"""
        base_priority = 1.0
        
        # Приоритет на основе частоты доступа
        base_priority += pattern['patterns']['frequency'] * 10
        
        # Приоритет на основе рейтинга попаданий
        base_priority += pattern['patterns']['hit_rate'] * 5
        
        # Приоритет на основе тренда
        if pattern['patterns']['trend'] == 'increasing':
            base_priority += 3
        elif pattern['patterns']['trend'] == 'stable':
            base_priority += 1
            
        return base_priority
    
    def _predict_next_access(self, pattern: Dict) -> datetime:
        """Предсказание времени следующего доступа"""
        access_times = pattern['access_times']
        if len(access_times) < 2:
            return datetime.now() + timedelta(hours=1)
        
        # Простое предсказание на основе среднего интервала
        intervals = [(access_times[i+1] - access_times[i]).total_seconds() 
                    for i in range(len(access_times)-1)]
        avg_interval = sum(intervals) / len(intervals)
        
        return access_times[-1] + timedelta(seconds=avg_interval)
    
    def warm_cache_proactively(self):
        """Проактивный прогрев кэша на основе предсказаний"""
        predictions = self.predict_cache_needs()
        
        for prediction in predictions[:10]:  # Ограничиваем 10 лучшими предсказаниями
            key = prediction['key']
            try:
                # Прогрев данных, которые, вероятно, скоро понадобятся
                from app import cache
                if not cache.get(key):
                    # Логика прогрева - здесь должен быть реальный запрос к данным
                    logger.info(f"Проактивный прогрев ключа: {key}")
                    # cache.set(key, fetch_data_function(), timeout=3600)
                    
            except Exception as e:
                logger.error(f"Ошибка проактивного прогрева для {key}: {e}")
    
    def get_cache_intelligence_report(self) -> Dict[str, Any]:
        """Получение отчета интеллектуального анализа кэша"""
        return {
            'timestamp': datetime.now().isoformat(),
            'total_cache_keys': len(self.cache_access_patterns),
            'analyzed_patterns': len([p for p in self.cache_access_patterns.values() 
                                   if p['patterns']]),
            'warming_strategies': len(self.warming_strategies),
            'predictions': self.predict_cache_needs()[:20],
            'active_strategies': {name: strat for name, strat in self.warming_strategies.items() 
                                if strat['last_run']},
            'cache_access_statistics': self._get_cache_access_stats()
        }
    
    def _get_cache_access_stats(self) -> Dict[str, Any]:
        """Получение статистики доступа к кэшу"""
        total_accesses = sum(p['access_count'] for p in self.cache_access_patterns.values())
        total_hits = sum(p['hit_count'] for p in self.cache_access_patterns.values())
        
        return {
            'total_accesses': total_accesses,
            'total_hits': total_hits,
            'overall_hit_rate': total_hits / (total_accesses or 1),
            'active_keys': len([p for p in self.cache_access_patterns.values() 
                              if p['last_access'] and 
                              p['last_access'] > datetime.now() - timedelta(hours=1)])
        }
    
    def _start_warming_scheduler(self):
        """Запуск планировщика прогрева в отдельном потоке"""
        def scheduler_worker():
            while True:
                try:
                    schedule.run_pending()
                    time.sleep(60)  # Проверка каждую минуту
                except Exception as e:
                    logger.error(f"Ошибка планировщика прогрева: {e}")
                    time.sleep(300)  # Пауза при ошибке
        
        self.warming_thread = Thread(target=scheduler_worker, daemon=True)
        self.warming_thread.start()
        logger.info("Планировщик прогрева кэша запущен")

# Глобальный экземпляр
cache_warmer = SmartCacheWarmer()

# Flask CLI команды для управления прогревом кэша
def register_cache_warming_commands(app):
    """Регистрация CLI команд управления прогревом кэша"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('cache-intelligence')
    @with_appcontext
    def cache_intelligence_report():
        """Показать отчет интеллектуального анализа кэша"""
        report = cache_warmer.get_cache_intelligence_report()
        click.echo("Интеллектуальный анализ кэша:")
        click.echo(f"  Всего ключей кэша: {report['total_cache_keys']}")
        click.echo(f"  Проанализированные паттерны: {report['analyzed_patterns']}")
        click.echo(f"  Активные стратегии: {len(report['active_strategies'])}")
        click.echo(f"  Общий рейтинг попаданий: {report['cache_access_statistics']['overall_hit_rate']:.2%}")
        
        # Показать топ предсказаний
        predictions = report['predictions'][:5]
        if predictions:
            click.echo("\nТоп предсказаний для прогрева:")
            for i, pred in enumerate(predictions, 1):
                click.echo(f"  {i}. {pred['key'][:50]}... (приоритет: {pred['priority']:.1f})")
    
    @app.cli.command('warm-cache')
    @with_appcontext
    def manual_cache_warm():
        """Ручной прогрев кэша"""
        click.echo("Начало ручного прогрева кэша...")
        cache_warmer.warm_cache_proactively()
        click.echo("Ручной прогрев кэша завершен")
    
    @app.cli.command('cache-patterns')
    @with_appcontext
    def show_cache_patterns():
        """Показать паттерны доступа к кэшу"""
        patterns = cache_warmer.cache_access_patterns
        active_patterns = {k: v for k, v in patterns.items() 
                          if v['last_access'] and 
                          v['last_access'] > datetime.now() - timedelta(hours=1)}
        
        click.echo(f"Активные паттерны кэша (за последний час): {len(active_patterns)}")
        click.echo(f"Всего паттернов: {len(patterns)}")
        
        # Показать топ активных ключей
        sorted_patterns = sorted(active_patterns.items(), 
                               key=lambda x: x[1]['access_count'], reverse=True)[:10]
        
        for key, pattern in sorted_patterns:
            click.echo(f"  {key[:40]}... - доступов: {pattern['access_count']}, "
                      f"попаданий: {pattern['hit_count']}")