"""
Продвинутая оптимизация запросов с подсказками и анализом планов выполнения
"""
import logging
from sqlalchemy import text, event
from sqlalchemy.engine import Engine
from typing import Dict, List, Any, Optional
from functools import wraps
import time
from collections import defaultdict

logger = logging.getLogger(__name__)

class QueryOptimizer:
    """Продвинутый оптимизатор запросов с анализом и подсказками"""
    
    def __init__(self, app=None):
        self.app = app
        self.query_stats = defaultdict(lambda: {
            'count': 0,
            'total_time': 0,
            'avg_time': 0,
            'min_time': float('inf'),
            'max_time': 0,
            'slow_queries': []
        })
        self.optimization_hints = {}
        self.slow_query_threshold = 0.5  # секунды
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация оптимизатора с Flask приложением"""
        self.app = app
        
        # Регистрация event listener для анализа запросов
        @event.listens_for(Engine, "before_cursor_execute")
        def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            context._query_start_time = time.time()
        
        @event.listens_for(Engine, "after_cursor_execute")
        def receive_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            total_time = time.time() - context._query_start_time
            
            # Статистика запросов
            query_key = self._normalize_query(statement)
            stats = self.query_stats[query_key]
            
            stats['count'] += 1
            stats['total_time'] += total_time
            stats['avg_time'] = stats['total_time'] / stats['count']
            stats['min_time'] = min(stats['min_time'], total_time)
            stats['max_time'] = max(stats['max_time'], total_time)
            
            # Отслеживание медленных запросов
            if total_time > self.slow_query_threshold:
                stats['slow_queries'].append({
                    'time': total_time,
                    'statement': statement,
                    'parameters': parameters,
                    'timestamp': time.time()
                })
                
                # Ограничение количества сохраненных медленных запросов
                if len(stats['slow_queries']) > 100:
                    stats['slow_queries'] = stats['slow_queries'][-50:]
                
                logger.warning(f"Медленный запрос ({total_time:.3f}s): {statement[:100]}...")
        
        logger.info("Продвинутый оптимизатор запросов инициализирован")
    
    def _normalize_query(self, query: str) -> str:
        """Нормализация запроса для группировки статистики"""
        # Удаление лишних пробелов и переводов строк
        normalized = ' '.join(query.split())
        # Замена параметров на placeholder для группировки
        import re
        normalized = re.sub(r"'[^']*'", '?', normalized)
        normalized = re.sub(r'\d+', '?', normalized)
        return normalized
    
    def add_optimization_hint(self, query_pattern: str, hint: str):
        """Добавление подсказки оптимизации для определенного типа запросов"""
        self.optimization_hints[query_pattern] = hint
        logger.info(f"Добавлена подсказка оптимизации для шаблона: {query_pattern}")
    
    def get_query_statistics(self) -> Dict[str, Any]:
        """Получение статистики выполнения запросов"""
        return {
            'total_queries': len(self.query_stats),
            'slow_query_threshold': self.slow_query_threshold,
            'queries': dict(self.query_stats),
            'optimization_hints': self.optimization_hints
        }
    
    def get_slow_queries(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Получение списка медленных запросов"""
        slow_queries = []
        
        for query_key, stats in self.query_stats.items():
            for slow_query in stats['slow_queries']:
                slow_queries.append({
                    'query': query_key,
                    'execution_time': slow_query['time'],
                    'statement': slow_query['statement'],
                    'timestamp': slow_query['timestamp']
                })
        
        # Сортировка по времени выполнения
        slow_queries.sort(key=lambda x: x['execution_time'], reverse=True)
        return slow_queries[:limit]
    
    def analyze_query_plan(self, query: str) -> Dict[str, Any]:
        """Анализ плана выполнения запроса"""
        try:
            from app import db
            
            # Для SQLite используем EXPLAIN QUERY PLAN
            if 'sqlite' in str(db.engine.url):
                result = db.session.execute(text(f"EXPLAIN QUERY PLAN {query}"))
                plan_data = [dict(row) for row in result]
                
                return {
                    'query': query,
                    'engine': 'sqlite',
                    'plan': plan_data,
                    'analysis': self._analyze_sqlite_plan(plan_data)
                }
            
            # Для PostgreSQL используем EXPLAIN ANALYZE
            elif 'postgresql' in str(db.engine.url):
                result = db.session.execute(text(f"EXPLAIN (ANALYZE, FORMAT JSON) {query}"))
                plan_data = result.fetchone()[0]
                
                return {
                    'query': query,
                    'engine': 'postgresql',
                    'plan': plan_data,
                    'analysis': self._analyze_postgresql_plan(plan_data)
                }
            
            # Для MySQL используем EXPLAIN
            elif 'mysql' in str(db.engine.url):
                result = db.session.execute(text(f"EXPLAIN {query}"))
                plan_data = [dict(row) for row in result]
                
                return {
                    'query': query,
                    'engine': 'mysql',
                    'plan': plan_data,
                    'analysis': self._analyze_mysql_plan(plan_data)
                }
            
            else:
                return {
                    'query': query,
                    'engine': 'unknown',
                    'error': 'Движок базы данных не поддерживается для анализа плана'
                }
                
        except Exception as e:
            logger.error(f"Ошибка анализа плана запроса: {e}")
            return {
                'query': query,
                'error': str(e)
            }
    
    def _analyze_sqlite_plan(self, plan_data: List[Dict]) -> Dict[str, Any]:
        """Анализ плана выполнения SQLite"""
        analysis = {
            'scan_types': [],
            'join_strategies': [],
            'index_usage': [],
            'potential_issues': []
        }
        
        for row in plan_data:
            detail = row.get('detail', '')
            
            # Определение типов сканирования
            if 'SCAN' in detail:
                analysis['scan_types'].append(detail)
            elif 'SEARCH' in detail:
                analysis['scan_types'].append(detail)
            
            # Проверка использования индексов
            if 'USING INDEX' in detail:
                analysis['index_usage'].append(detail)
            elif 'TABLE SCAN' in detail:
                analysis['potential_issues'].append('Полное сканирование таблицы')
        
        return analysis
    
    def _analyze_postgresql_plan(self, plan_data: Dict) -> Dict[str, Any]:
        """Анализ плана выполнения PostgreSQL"""
        analysis = {
            'scan_types': [],
            'join_strategies': [],
            'index_usage': [],
            'cost_estimate': 0,
            'potential_issues': []
        }
        
        if plan_data and len(plan_data) > 0:
            plan = plan_data[0]['Plan']
            analysis['cost_estimate'] = plan.get('Total Cost', 0)
            
            # Анализ узлов плана
            def analyze_node(node):
                if 'Node Type' in node:
                    node_type = node['Node Type']
                    if 'Scan' in node_type:
                        analysis['scan_types'].append(node_type)
                    elif 'Join' in node_type:
                        analysis['join_strategies'].append(node_type)
                
                # Рекурсивный анализ дочерних узлов
                if 'Plans' in node:
                    for child in node['Plans']:
                        analyze_node(child)
            
            analyze_node(plan)
        
        return analysis
    
    def _analyze_mysql_plan(self, plan_data: List[Dict]) -> Dict[str, Any]:
        """Анализ плана выполнения MySQL"""
        analysis = {
            'scan_types': [],
            'join_strategies': [],
            'index_usage': [],
            'potential_issues': []
        }
        
        for row in plan_data:
            # Анализ типа сканирования
            select_type = row.get('select_type', '')
            if select_type:
                analysis['scan_types'].append(select_type)
            
            # Анализ использования индексов
            key_used = row.get('key', '')
            if key_used and key_used != 'NULL':
                analysis['index_usage'].append(f"Индекс: {key_used}")
            else:
                analysis['potential_issues'].append('Не используется индекс')
        
        return analysis
    
    def get_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """Получение рекомендаций по оптимизации на основе статистики"""
        recommendations = []
        
        for query_key, stats in self.query_stats.items():
            # Рекомендации для медленных запросов
            if stats['avg_time'] > self.slow_query_threshold:
                recommendations.append({
                    'type': 'slow_query',
                    'query_pattern': query_key,
                    'avg_execution_time': stats['avg_time'],
                    'execution_count': stats['count'],
                    'recommendation': 'Рассмотрите возможность добавления индексов или оптимизации запроса'
                })
            
            # Рекомендации для часто выполняющихся запросов
            if stats['count'] > 1000:
                recommendations.append({
                    'type': 'high_frequency',
                    'query_pattern': query_key,
                    'execution_count': stats['count'],
                    'recommendation': 'Рассмотрите возможность кэширования результатов'
                })
        
        return recommendations

# Глобальный экземпляр оптимизатора
query_optimizer = QueryOptimizer()

# Flask CLI команды для управления оптимизатором
def register_optimizer_commands(app):
    """Регистрация CLI команд управления оптимизатором запросов"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('query-stats')
    @with_appcontext
    def query_statistics():
        """Показать статистику выполнения запросов"""
        stats = query_optimizer.get_query_statistics()
        click.echo("Статистика запросов:")
        click.echo(f"  Всего уникальных запросов: {stats['total_queries']}")
        click.echo(f"  Порог медленных запросов: {stats['slow_query_threshold']}s")
        click.echo(f"  Активных подсказок оптимизации: {len(stats['optimization_hints'])}")
    
    @app.cli.command('slow-queries')
    @click.option('--limit', default=10, help='Количество медленных запросов для показа')
    @with_appcontext
    def show_slow_queries(limit):
        """Показать медленные запросы"""
        slow_queries = query_optimizer.get_slow_queries(limit)
        click.echo(f"Топ {limit} медленных запросов:")
        
        for i, query in enumerate(slow_queries, 1):
            click.echo(f"  {i}. {query['execution_time']:.3f}s - {query['statement'][:80]}...")
    
    @app.cli.command('query-recommendations')
    @with_appcontext
    def optimization_recommendations():
        """Получить рекомендации по оптимизации запросов"""
        recommendations = query_optimizer.get_optimization_recommendations()
        click.echo("Рекомендации по оптимизации:")
        
        for i, rec in enumerate(recommendations, 1):
            click.echo(f"  {i}. [{rec['type']}] {rec['recommendation']}")
            click.echo(f"      Шаблон запроса: {rec['query_pattern'][:60]}...")