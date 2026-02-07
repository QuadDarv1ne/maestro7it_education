# -*- coding: utf-8 -*-
"""
Модуль интеллектуальной оптимизации запросов базы данных
Использует машинное обучение для предсказания и оптимизации производительности запросов
"""
import logging
from typing import Dict, Any, List, Optional, Tuple
from collections import defaultdict, deque
from datetime import datetime, timedelta
import json
import pickle
import hashlib
import time
from threading import Lock
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import psutil

logger = logging.getLogger(__name__)

class IntelligentQueryOptimizer:
    """Интеллектуальный оптимизатор запросов базы данных с машинным обучением"""
    
    def __init__(self, app=None):
        self.app = app
        self.query_history = deque(maxlen=10000)
        self.pattern_cache = {}
        self.ml_model = None
        self.scaler = StandardScaler()
        self.stats_lock = Lock()
        self.performance_stats = defaultdict(lambda: {
            'execution_times': deque(maxlen=100),
            'call_count': 0,
            'avg_time': 0,
            'last_optimized': None
        })
        self.optimization_suggestions = deque(maxlen=1000)
        
        # ML model parameters
        self.ml_features = [
            'query_complexity',
            'table_size',
            'result_size',
            'execution_frequency',
            'time_of_day',
            'day_of_week',
            'system_load'
        ]
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация с Flask приложением"""
        self.app = app
        self._initialize_ml_model()
        logger.info("Интеллектуальный оптимизатор запросов инициализирован")
    
    def _initialize_ml_model(self):
        """Инициализация машинной модели для предсказания производительности"""
        try:
            # Создание простой модели Random Forest для начала
            self.ml_model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
            logger.info("ML модель для оптимизации запросов создана")
        except Exception as e:
            logger.error(f"Ошибка создания ML модели: {e}")
            self.ml_model = None
    
    def analyze_query_pattern(self, query: str, execution_time: float, 
                            table_sizes: Dict[str, int] = None) -> Dict[str, Any]:
        """Анализирует паттерн запроса и собирает статистику"""
        query_hash = self._hash_query(query)
        
        # Сбор метрик запроса
        metrics = {
            'query_hash': query_hash,
            'execution_time': execution_time,
            'timestamp': datetime.now(),
            'query_complexity': self._calculate_complexity(query),
            'table_sizes': table_sizes or {},
            'system_load': self._get_system_load(),
            'time_features': self._get_time_features()
        }
        
        # Сохранение в историю
        with self.stats_lock:
            self.query_history.append(metrics)
            stats = self.performance_stats[query_hash]
            stats['execution_times'].append(execution_time)
            stats['call_count'] += 1
            stats['avg_time'] = np.mean(list(stats['execution_times']))
        
        # Обучение ML модели если есть достаточно данных
        if len(self.query_history) >= 100:
            self._update_ml_model()
        
        return metrics
    
    def _hash_query(self, query: str) -> str:
        """Создает хэш запроса для идентификации"""
        # Нормализация запроса (удаление лишних пробелов, приведение к нижнему регистру)
        normalized = ' '.join(query.lower().split())
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def _calculate_complexity(self, query: str) -> float:
        """Рассчитывает сложность запроса"""
        complexity_score = 0
        
        # Подсчет ключевых слов SQL
        keywords = ['join', 'subquery', 'union', 'group by', 'order by', 'having', 'distinct']
        query_lower = query.lower()
        
        for keyword in keywords:
            complexity_score += query_lower.count(keyword) * 2
        
        # Подсчет вложенных запросов
        complexity_score += query_lower.count('(') * 1.5
        
        # Подсчет условий WHERE
        complexity_score += query_lower.count('where') * 1
        
        return min(complexity_score, 20.0)  # Ограничение максимальной сложности
    
    def _get_system_load(self) -> float:
        """Получает текущую нагрузку на систему"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory_percent = psutil.virtual_memory().percent
            return (cpu_percent + memory_percent) / 200.0  # Нормализация до 0-1
        except:
            return 0.5  # Значение по умолчанию
    
    def _get_time_features(self) -> Dict[str, float]:
        """Получает временные признаки для ML модели"""
        now = datetime.now()
        return {
            'hour': now.hour / 23.0,  # Нормализация до 0-1
            'day_of_week': now.weekday() / 6.0,  # Нормализация до 0-1
            'is_weekend': 1.0 if now.weekday() >= 5 else 0.0
        }
    
    def _update_ml_model(self):
        """Обновляет ML модель на основе собранной статистики"""
        if not self.ml_model or len(self.query_history) < 100:
            return
        
        try:
            # Подготовка данных для обучения
            X, y = self._prepare_training_data()
            
            if len(X) >= 50:  # Минимум 50 примеров для обучения
                # Нормализация признаков
                X_scaled = self.scaler.fit_transform(X)
                
                # Обучение модели
                self.ml_model.fit(X_scaled, y)
                logger.info(f"ML модель обновлена на {len(X)} примерах")
                
        except Exception as e:
            logger.error(f"Ошибка обновления ML модели: {e}")
    
    def _prepare_training_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Подготавливает данные для обучения ML модели"""
        X = []
        y = []
        
        for record in list(self.query_history)[-500:]:  # Последние 500 записей
            features = [
                record['query_complexity'],
                max(record['table_sizes'].values()) if record['table_sizes'] else 1000,
                record['system_load'],
                record['time_features']['hour'],
                record['time_features']['day_of_week'],
                len([q for q in self.query_history 
                     if q['query_hash'] == record['query_hash']]) / len(self.query_history)
            ]
            X.append(features)
            y.append(record['execution_time'])
        
        return np.array(X), np.array(y)
    
    def predict_performance(self, query: str, table_sizes: Dict[str, int] = None) -> Dict[str, Any]:
        """Предсказывает производительность запроса"""
        if not self.ml_model:
            return {'predicted_time': None, 'confidence': 0}
        
        try:
            # Подготовка признаков
            query_complexity = self._calculate_complexity(query)
            features = [
                query_complexity,
                max(table_sizes.values()) if table_sizes else 1000,
                self._get_system_load(),
                datetime.now().hour / 23.0,
                datetime.now().weekday() / 6.0,
                0.1  # Частота выполнения (по умолчанию)
            ]
            
            # Предсказание
            features_scaled = self.scaler.transform([features])
            predicted_time = self.ml_model.predict(features_scaled)[0]
            
            # Расчет доверительного интервала (упрощенный)
            confidence = max(0.5, 1.0 - (query_complexity / 20.0))
            
            return {
                'predicted_time': float(predicted_time),
                'confidence': float(confidence),
                'complexity': query_complexity
            }
            
        except Exception as e:
            logger.error(f"Ошибка предсказания производительности: {e}")
            return {'predicted_time': None, 'confidence': 0}
    
    def suggest_optimizations(self, query: str) -> List[Dict[str, Any]]:
        """Предлагает оптимизации для запроса"""
        suggestions = []
        query_lower = query.lower()
        
        # Анализ на наличие потенциальных проблем
        if 'select *' in query_lower:
            suggestions.append({
                'type': 'column_selection',
                'suggestion': 'Укажите конкретные столбцы вместо SELECT *',
                'impact': 'high',
                'estimated_improvement': '20-50%'
            })
        
        if 'order by' in query_lower and 'limit' not in query_lower:
            suggestions.append({
                'type': 'pagination',
                'suggestion': 'Добавьте LIMIT для ограничения результатов',
                'impact': 'medium',
                'estimated_improvement': '15-30%'
            })
        
        # Проверка на отсутствие индексов
        if 'where' in query_lower and 'id' not in query_lower:
            suggestions.append({
                'type': 'indexing',
                'suggestion': 'Рассмотрите создание индексов для полей в WHERE',
                'impact': 'high',
                'estimated_improvement': '40-70%'
            })
        
        # Анализ JOIN операций
        join_count = query_lower.count('join')
        if join_count > 2:
            suggestions.append({
                'type': 'query_structure',
                'suggestion': 'Рассмотрите денормализацию или материализованные представления',
                'impact': 'high',
                'estimated_improvement': '30-60%'
            })
        
        return suggestions
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Генерирует отчет о производительности запросов"""
        with self.stats_lock:
            slow_queries = []
            fast_queries = []
            
            for query_hash, stats in self.performance_stats.items():
                if stats['call_count'] > 5:  # Только запросы с достаточным количеством вызовов
                    avg_time = stats['avg_time']
                    if avg_time > 0.5:  # Медленные запросы (>500ms)
                        slow_queries.append({
                            'query_hash': query_hash,
                            'avg_time': avg_time,
                            'call_count': stats['call_count'],
                            'last_optimized': stats['last_optimized']
                        })
                    elif avg_time < 0.1:  # Быстрые запросы (<100ms)
                        fast_queries.append({
                            'query_hash': query_hash,
                            'avg_time': avg_time,
                            'call_count': stats['call_count']
                        })
            
            # Сортировка по времени выполнения
            slow_queries.sort(key=lambda x: x['avg_time'], reverse=True)
            fast_queries.sort(key=lambda x: x['avg_time'])
            
            return {
                'total_queries_analyzed': len(self.performance_stats),
                'slow_queries': slow_queries[:20],  # Топ-20 медленных запросов
                'fast_queries': fast_queries[:20],  # Топ-20 быстрых запросов
                'optimization_suggestions': list(self.optimization_suggestions)[-50:],
                'system_performance': {
                    'cpu_usage': psutil.cpu_percent(),
                    'memory_usage': psutil.virtual_memory().percent,
                    'query_cache_hit_rate': self._calculate_cache_hit_rate()
                }
            }
    
    def _calculate_cache_hit_rate(self) -> float:
        """Рассчитывает коэффициент попаданий в кэш"""
        try:
            from app import cache
            if hasattr(cache, 'get_stats'):
                stats = cache.get_stats()
                hits = stats.get('hits', 0)
                misses = stats.get('misses', 0)
                total = hits + misses
                return hits / total if total > 0 else 0
        except:
            pass
        return 0.0
    
    def optimize_query_automatically(self, query: str) -> str:
        """Автоматически оптимизирует запрос"""
        suggestions = self.suggest_optimizations(query)
        optimized_query = query
        
        # Применение простых оптимизаций
        if any(s['type'] == 'column_selection' for s in suggestions):
            # Это упрощенный пример - в реальности нужен более сложный парсер SQL
            optimized_query = query.replace('SELECT *', 'SELECT id')  # Очень базовая оптимизация
        
        # Обновление статистики
        query_hash = self._hash_query(query)
        with self.stats_lock:
            self.performance_stats[query_hash]['last_optimized'] = datetime.now()
        
        return optimized_query

# Глобальный экземпляр
intelligent_optimizer = IntelligentQueryOptimizer()

def register_intelligent_optimization_commands(app):
    """Регистрация CLI команд для интеллектуальной оптимизации"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('intelligent-optimize')
    @with_appcontext
    def run_intelligent_optimization():
        """Запуск интеллектуальной оптимизации запросов"""
        report = intelligent_optimizer.get_performance_report()
        click.echo("Интеллектуальная оптимизация запросов:")
        click.echo(f"  Проанализировано запросов: {report['total_queries_analyzed']}")
        click.echo(f"  Медленных запросов: {len(report['slow_queries'])}")
        click.echo(f"  Быстрых запросов: {len(report['fast_queries'])}")
        
        if report['slow_queries']:
            click.echo("\nТоп медленных запросов:")
            for i, query in enumerate(report['slow_queries'][:5], 1):
                click.echo(f"  {i}. Среднее время: {query['avg_time']:.3f}с ({query['call_count']} вызовов)")
    
    @app.cli.command('predict-query')
    @click.argument('query')
    @with_appcontext
    def predict_query_performance(query):
        """Предсказать производительность запроса"""
        prediction = intelligent_optimizer.predict_performance(query)
        suggestions = intelligent_optimizer.suggest_optimizations(query)
        
        click.echo(f"Предсказанное время выполнения: {prediction['predicted_time']:.3f}с")
        click.echo(f"Уверенность: {prediction['confidence']:.2f}")
        click.echo(f"Сложность: {prediction['complexity']}")
        
        if suggestions:
            click.echo("\nРекомендации по оптимизации:")
            for suggestion in suggestions:
                click.echo(f"  - {suggestion['suggestion']} (влияние: {suggestion['impact']})")

# Flask декоратор для автоматической оптимизации
def auto_optimize_query(f):
    """Декоратор для автоматической оптимизации запросов"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Получение запроса (это упрощенный пример)
        query = str(args[0]) if args else ""
        
        # Анализ и оптимизация
        start_time = time.time()
        result = f(*args, **kwargs)
        execution_time = time.time() - start_time
        
        # Анализ производительности
        intelligent_optimizer.analyze_query_pattern(query, execution_time)
        
        return result
    
    return decorated_function