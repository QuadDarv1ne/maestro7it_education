"""
Модуль анализа планов выполнения запросов для оптимизации производительности
"""
import logging
from sqlalchemy import text
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class QueryPlanAnalyzer:
    """Анализатор планов выполнения запросов для оптимизации производительности"""
    
    def __init__(self, app=None):
        self.app = app
        self.analysis_history = []
        self.recommendations = []
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация анализатора с Flask приложением"""
        self.app = app
        logger.info("Анализатор планов запросов инициализирован")
    
    def analyze_query_plan(self, query: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Анализ плана выполнения конкретного запроса"""
        from app import db
        
        try:
            # Определение типа базы данных
            db_type = self._get_db_type(db)
            
            analysis = {
                'query': query,
                'params': params or {},
                'db_type': db_type,
                'timestamp': datetime.now().isoformat(),
                'plan_details': {},
                'performance_analysis': {},
                'recommendations': []
            }
            
            if db_type == 'sqlite':
                analysis['plan_details'] = self._analyze_sqlite_plan(query, params)
            elif db_type == 'postgresql':
                analysis['plan_details'] = self._analyze_postgresql_plan(query, params)
            elif db_type == 'mysql':
                analysis['plan_details'] = self._analyze_mysql_plan(query, params)
            else:
                analysis['error'] = f'Тип базы данных {db_type} не поддерживается для анализа плана'
                return analysis
            
            # Добавление анализа производительности
            analysis['performance_analysis'] = self._perform_performance_analysis(analysis['plan_details'])
            
            # Генерация рекомендаций
            analysis['recommendations'] = self._generate_recommendations(analysis)
            
            # Сохранение в историю
            self.analysis_history.append(analysis)
            
            # Ограничение истории до 100 последних анализов
            if len(self.analysis_history) > 100:
                self.analysis_history = self.analysis_history[-50:]
            
            return analysis
            
        except Exception as e:
            logger.error(f"Ошибка анализа плана запроса: {e}")
            return {
                'query': query,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _get_db_type(self, db) -> str:
        """Определение типа базы данных"""
        db_url = str(db.engine.url)
        if 'sqlite' in db_url:
            return 'sqlite'
        elif 'postgresql' in db_url:
            return 'postgresql'
        elif 'mysql' in db_url:
            return 'mysql'
        else:
            return 'unknown'
    
    def _analyze_sqlite_plan(self, query: str, params: Optional[Dict]) -> Dict[str, Any]:
        """Анализ плана выполнения для SQLite"""
        from app import db
        
        result = db.session.execute(text(f"EXPLAIN QUERY PLAN {query}"), params or {})
        plan_rows = [dict(row) for row in result]
        
        # Анализ деталей плана
        plan_analysis = {
            'raw_plan': plan_rows,
            'operations': [],
            'potential_issues': [],
            'index_usage': []
        }
        
        for row in plan_rows:
            detail = row.get('detail', '').upper()
            
            # Определение операций
            if 'SCAN' in detail or 'SEARCH' in detail:
                operation = {
                    'type': 'scan' if 'SCAN' in detail else 'search',
                    'table': self._extract_table_name(detail),
                    'index': self._extract_index_name(detail),
                    'detail': detail
                }
                plan_analysis['operations'].append(operation)
                
                # Проверка использования индексов
                if 'USING INDEX' in detail:
                    plan_analysis['index_usage'].append(operation['index'])
                elif 'SCAN TABLE' in detail or 'TABLE SCAN' in detail:
                    plan_analysis['potential_issues'].append({
                        'type': 'full_table_scan',
                        'table': operation['table'],
                        'description': f'Полное сканирование таблицы {operation["table"]} без использования индекса'
                    })
        
        return plan_analysis
    
    def _analyze_postgresql_plan(self, query: str, params: Optional[Dict]) -> Dict[str, Any]:
        """Анализ плана выполнения для PostgreSQL"""
        from app import db
        
        try:
            # Используем EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) для подробного анализа
            result = db.session.execute(
                text(f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {query}"), 
                params or {}
            )
            plan_data = result.fetchone()[0]
            
            plan_analysis = {
                'raw_plan': plan_data,
                'execution_time': plan_data[0].get('Execution Time', 0) if plan_data else 0,
                'planning_time': plan_data[0].get('Planning Time', 0) if plan_data else 0,
                'nodes': self._parse_postgresql_nodes(plan_data[0]['Plan'] if plan_data else {}),
                'potential_issues': [],
                'index_usage': []
            }
            
            # Анализ узлов плана
            self._analyze_postgresql_nodes(plan_analysis['nodes'], plan_analysis)
            
            return plan_analysis
            
        except Exception as e:
            logger.error(f"Ошибка анализа плана PostgreSQL: {e}")
            # Возвращаем анализ с помощью обычного EXPLAIN
            result = db.session.execute(text(f"EXPLAIN {query}"), params or {})
            raw_plan = [dict(row) for row in result]
            return {
                'raw_plan': raw_plan,
                'error': str(e),
                'nodes': {},
                'potential_issues': [],
                'index_usage': []
            }
    
    def _analyze_mysql_plan(self, query: str, params: Optional[Dict]) -> Dict[str, Any]:
        """Анализ плана выполнения для MySQL"""
        from app import db
        
        try:
            result = db.session.execute(text(f"EXPLAIN FORMAT=JSON {query}"), params or {})
            plan_data = result.fetchone()
            
            if plan_data:
                plan_json = json.loads(plan_data[0]) if isinstance(plan_data[0], str) else plan_data[0]
                plan_analysis = {
                    'raw_plan': plan_json,
                    'query_block': plan_json.get('query_block', {}),
                    'potential_issues': [],
                    'index_usage': []
                }
                
                # Анализ блока запроса
                self._analyze_mysql_query_block(plan_analysis['query_block'], plan_analysis)
                
                return plan_analysis
            else:
                # Резервный вариант с обычным EXPLAIN
                result = db.session.execute(text(f"EXPLAIN {query}"), params or {})
                raw_plan = [dict(row) for row in result]
                
                return {
                    'raw_plan': raw_plan,
                    'potential_issues': [],
                    'index_usage': []
                }
                
        except Exception as e:
            logger.error(f"Ошибка анализа плана MySQL: {e}")
            result = db.session.execute(text(f"EXPLAIN {query}"), params or {})
            raw_plan = [dict(row) for row in result]
            return {
                'raw_plan': raw_plan,
                'error': str(e),
                'potential_issues': [],
                'index_usage': []
            }
    
    def _parse_postgresql_nodes(self, plan_node: Dict, parent_operation: str = None) -> Dict[str, Any]:
        """Разбор узлов плана PostgreSQL"""
        node_info = {
            'node_type': plan_node.get('Node Type', ''),
            'operation': plan_node.get('Operation', ''),
            'relation_name': plan_node.get('Relation Name', ''),
            'schema': plan_node.get('Schema', ''),
            'alias': plan_node.get('Alias', ''),
            'startup_cost': plan_node.get('Startup Cost', 0),
            'total_cost': plan_node.get('Total Cost', 0),
            'plan_rows': plan_node.get('Plan Rows', 0),
            'plan_width': plan_node.get('Plan Width', 0),
            'children': []
        }
        
        # Рекурсивный разбор дочерних узлов
        if 'Plans' in plan_node:
            for child_plan in plan_node['Plans']:
                child_node = self._parse_postgresql_nodes(child_plan)
                node_info['children'].append(child_node)
        
        return node_info
    
    def _analyze_postgresql_nodes(self, nodes: Dict, analysis: Dict):
        """Анализ узлов плана PostgreSQL для выявления проблем"""
        def analyze_node_recursive(node):
            node_type = node['node_type'].upper()
            
            # Проверка на полное сканирование
            if 'SEQ SCAN' in node_type:
                analysis['potential_issues'].append({
                    'type': 'sequential_scan',
                    'table': node.get('relation_name', 'unknown'),
                    'description': f'Последовательное сканирование таблицы {node.get("relation_name", "unknown")} может быть неэффективным'
                })
            
            # Проверка на использование индексов
            if 'INDEX' in node_type:
                index_name = node.get('index_name', 'unknown')
                analysis['index_usage'].append(index_name)
            
            # Рекурсивный анализ дочерних узлов
            for child in node.get('children', []):
                analyze_node_recursive(child)
        
        analyze_node_recursive(nodes)
    
    def _analyze_mysql_query_block(self, query_block: Dict, analysis: Dict):
        """Анализ блока запроса MySQL для выявления проблем"""
        def analyze_unit(unit):
            if 'table' in unit:
                table_info = unit['table']
                table_name = table_info.get('table_name', 'unknown')
                
                # Проверка метода доступа
                access_type = table_info.get('access_type', 'unknown')
                if access_type in ['ALL', 'index']:  # Полное сканирование
                    analysis['potential_issues'].append({
                        'type': 'full_table_scan',
                        'table': table_name,
                        'description': f'Полное сканирование таблицы {table_name} (метод доступа: {access_type})'
                    })
                
                # Проверка использования индексов
                if 'key' in table_info and table_info['key'] != 'NULL':
                    analysis['index_usage'].append(table_info['key'])
            
            # Рекурсивный анализ вложенных блоков
            if 'nested_loop' in unit:
                for nested in unit['nested_loop']:
                    analyze_unit(nested)
        
        if 'table_access' in query_block:
            for unit in query_block['table_access']:
                analyze_unit(unit)
        elif 'nested_loop' in query_block:
            for unit in query_block['nested_loop']:
                analyze_unit(unit)
    
    def _perform_performance_analysis(self, plan_details: Dict) -> Dict[str, Any]:
        """Выполнение анализа производительности на основе плана"""
        performance_analysis = {
            'complexity_assessment': 'unknown',
            'estimated_cost': 0,
            'potential_bottlenecks': [],
            'optimization_priority': 'medium'
        }
        
        # Оценка сложности на основе количества операций
        if 'operations' in plan_details:
            scan_operations = [op for op in plan_details['operations'] if op['type'] == 'scan']
            if len(scan_operations) > 3:
                performance_analysis['complexity_assessment'] = 'high'
                performance_analysis['optimization_priority'] = 'high'
            elif len(scan_operations) > 1:
                performance_analysis['complexity_assessment'] = 'medium'
            else:
                performance_analysis['complexity_assessment'] = 'low'
        
        # Анализ потенциальных узких мест
        if 'potential_issues' in plan_details:
            for issue in plan_details['potential_issues']:
                performance_analysis['potential_bottlenecks'].append(issue['description'])
        
        return performance_analysis
    
    def _generate_recommendations(self, analysis: Dict) -> List[Dict[str, str]]:
        """Генерация рекомендаций на основе анализа"""
        recommendations = []
        
        # Рекомендации на основе потенциальных проблем
        if 'plan_details' in analysis and 'potential_issues' in analysis['plan_details']:
            for issue in analysis['plan_details']['potential_issues']:
                if issue['type'] == 'full_table_scan':
                    recommendations.append({
                        'type': 'index_suggestion',
                        'description': f'Рассмотрите создание индекса для таблицы {issue["table"]} на столбцах, используемых в WHERE/JOIN условиях',
                        'severity': 'high'
                    })
        
        # Рекомендации на основе анализа производительности
        perf_analysis = analysis.get('performance_analysis', {})
        if perf_analysis.get('optimization_priority') == 'high':
            recommendations.append({
                'type': 'optimization_urgent',
                'description': 'Запрос требует срочной оптимизации из-за высокой сложности',
                'severity': 'high'
            })
        
        return recommendations
    
    def _extract_table_name(self, detail: str) -> str:
        """Извлечение имени таблицы из детали плана"""
        # Простой парсер для извлечения имени таблицы
        import re
        match = re.search(r'TABLE ([^\s]+)', detail, re.IGNORECASE)
        if match:
            return match.group(1)
        match = re.search(r'SCAN ([^\s]+)', detail, re.IGNORECASE)
        if match:
            return match.group(1)
        return 'unknown'
    
    def _extract_index_name(self, detail: str) -> str:
        """Извлечение имени индекса из детали плана"""
        import re
        match = re.search(r'INDEX ([^\s]+)', detail, re.IGNORECASE)
        if match:
            return match.group(1)
        match = re.search(r'USING INDEX ([^\s]+)', detail, re.IGNORECASE)
        if match:
            return match.group(1)
        return 'none'
    
    def get_analysis_report(self) -> Dict[str, Any]:
        """Получение отчета об анализе планов запросов"""
        return {
            'total_analyzed': len(self.analysis_history),
            'recent_analyses': self.analysis_history[-10:],  # Последние 10 анализов
            'common_issues': self._get_common_issues(),
            'recommendation_summary': self._get_recommendation_summary()
        }
    
    def _get_common_issues(self) -> Dict[str, int]:
        """Получение статистики по распространенным проблемам"""
        issue_counts = {}
        
        for analysis in self.analysis_history:
            if 'plan_details' in analysis and 'potential_issues' in analysis['plan_details']:
                for issue in analysis['plan_details']['potential_issues']:
                    issue_type = issue['type']
                    issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1
        
        return issue_counts
    
    def _get_recommendation_summary(self) -> Dict[str, int]:
        """Получение статистики по рекомендациям"""
        rec_counts = {}
        
        for analysis in self.analysis_history:
            for rec in analysis.get('recommendations', []):
                rec_type = rec['type']
                rec_counts[rec_type] = rec_counts.get(rec_type, 0) + 1
        
        return rec_counts

# Глобальный экземпляр анализатора
query_plan_analyzer = QueryPlanAnalyzer()

# Flask CLI команды для анализа планов запросов
def register_query_plan_commands(app):
    """Регистрация CLI команд для анализа планов запросов"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('analyze-query-plan')
    @click.argument('query')
    @with_appcontext
    def analyze_query_plan_command(query):
        """Анализ плана выполнения SQL запроса"""
        click.echo(f"Анализ плана запроса: {query[:50]}...")
        
        analysis = query_plan_analyzer.analyze_query_plan(query)
        
        if 'error' in analysis:
            click.echo(f"Ошибка: {analysis['error']}")
            return
        
        click.echo(f"Тип БД: {analysis['db_type']}")
        click.echo(f"Время выполнения: {analysis['timestamp']}")
        
        # Показать основные проблемы
        if analysis['plan_details']['potential_issues']:
            click.echo("\nОбнаруженные проблемы:")
            for issue in analysis['plan_details']['potential_issues']:
                click.echo(f"  - {issue['type']}: {issue['description']}")
        
        # Показать рекомендации
        if analysis['recommendations']:
            click.echo("\nРекомендации:")
            for rec in analysis['recommendations']:
                click.echo(f"  - [{rec['severity']}] {rec['type']}: {rec['description']}")
    
    @app.cli.command('query-analysis-report')
    @with_appcontext
    def query_analysis_report():
        """Показать отчет об анализе запросов"""
        report = query_plan_analyzer.get_analysis_report()
        
        click.echo("Отчет об анализе планов запросов:")
        click.echo(f"  Всего проанализировано: {report['total_analyzed']}")
        
        if report['common_issues']:
            click.echo("  Распространенные проблемы:")
            for issue_type, count in report['common_issues'].items():
                click.echo(f"    {issue_type}: {count}")
        
        if report['recommendation_summary']:
            click.echo("  Рекомендации:")
            for rec_type, count in report['recommendation_summary'].items():
                click.echo(f"    {rec_type}: {count}")