# -*- coding: utf-8 -*-
"""
Модуль оптимизации запросов для базы данных товаров Ozon

Этот модуль предоставляет инструменты для анализа и оптимизации 
SQL-запросов к базе данных DuckDB.
"""

import duckdb
import time
import re
from typing import Dict, List, Tuple, Optional
from config import DATABASE_NAME
from utils import get_logger, format_currency


logger = get_logger(__name__)


class QueryOptimizer:
    """Класс для анализа и оптимизации SQL-запросов."""
    
    def __init__(self, db_path: str = DATABASE_NAME):
        """
        Инициализировать оптимизатор запросов.
        
        Args:
            db_path: Путь к базе данных
        """
        self.db_path = db_path
        self.con = duckdb.connect(db_path)
        logger.info(f"Оптимизатор запросов инициализирован для базы: {db_path}")
    
    def __del__(self):
        """Закрыть соединение при удалении объекта."""
        if hasattr(self, 'con'):
            self.con.close()
    
    def analyze_query(self, query: str) -> Dict[str, any]:
        """
        Проанализировать запрос и предоставить рекомендации по оптимизации.
        
        Args:
            query: SQL-запрос для анализа
            
        Returns:
            Словарь с результатами анализа
        """
        logger.info(f"Анализ запроса: {query[:100]}...")
        
        analysis = {
            'query': query,
            'potential_issues': [],
            'recommendations': [],
            'estimated_complexity': 'low',  # low, medium, high, critical
            'execution_plan': None,
            'estimated_time_ms': None
        }
        
        # Проверить на потенциальные проблемы
        self._check_potential_issues(query, analysis)
        
        # Оценить сложность запроса
        analysis['estimated_complexity'] = self._estimate_complexity(query)
        
        # Выполнить тестовый запуск для оценки производительности
        try:
            start_time = time.time()
            # Использовать EXPLAIN для получения плана выполнения
            explain_query = f"EXPLAIN {query}"
            plan_result = self.con.execute(explain_query).fetchall()
            analysis['execution_plan'] = [row[0] for row in plan_result]
            
            # Выполнить тестовый запрос для оценки времени
            test_start = time.time()
            self.con.execute(query).fetchall()
            test_time = (time.time() - test_start) * 1000  # в миллисекундах
            analysis['estimated_time_ms'] = round(test_time, 2)
            
        except Exception as e:
            logger.warning(f"Не удалось получить план выполнения: {e}")
        
        return analysis
    
    def _check_potential_issues(self, query: str, analysis: Dict):
        """Проверить запрос на потенциальные проблемы производительности."""
        query_lower = query.lower()
        
        # Проверить на использование DISTINCT без необходимости
        if 'distinct' in query_lower:
            analysis['potential_issues'].append({
                'type': 'unneeded_distinct',
                'description': 'Использование DISTINCT может замедлить запрос если не требуется уникальность'
            })
            analysis['recommendations'].append(
                'Рассмотрите необходимость использования DISTINCT'
            )
        
        # Проверить на полные сканирования таблиц
        if 'where' not in query_lower and 'join' not in query_lower:
            analysis['potential_issues'].append({
                'type': 'full_table_scan',
                'description': 'Запрос может выполнять полное сканирование таблицы'
            })
            analysis['recommendations'].append(
                'Добавьте условия WHERE или JOIN для ограничения результатов'
            )
        
        # Проверить на использование LIKE с началом шаблона
        if 'like' in query_lower and "'%" in query_lower:
            analysis['potential_issues'].append({
                'type': 'inefficient_like',
                'description': 'LIKE с шаблоном, начинающимся с %, может быть неэффективным'
            })
            analysis['recommendations'].append(
                'Используйте полнотекстовый поиск или индексы для таких случаев'
            )
        
        # Проверить на использование функций в условиях WHERE
        where_match = re.search(r'where\s+(.+?)(?:\s+order\s+by|\s+group\s+by|\s+having|\s*$)', query_lower, re.IGNORECASE | re.DOTALL)
        if where_match:
            where_clause = where_match.group(1)
            # Проверить на функции в WHERE (например, UPPER(column) = 'value')
            function_patterns = [r'\w+\([^)]*\)\s*[=<>]', r'[=<>]\s*\w+\([^)]*\)']
            for pattern in function_patterns:
                if re.search(pattern, where_clause):
                    analysis['potential_issues'].append({
                        'type': 'function_in_where',
                        'description': 'Использование функций в условиях WHERE может предотвратить использование индексов'
                    })
                    analysis['recommendations'].append(
                        'Попробуйте переписать условия для использования индексов'
                    )
    
    def _estimate_complexity(self, query: str) -> str:
        """Оценить сложность запроса."""
        query_lower = query.lower()
        
        complexity_score = 0
        
        # Увеличить сложность за каждую таблицу в FROM
        from_matches = re.findall(r'from\s+(\w+)', query_lower)
        complexity_score += len(from_matches) * 2
        
        # Увеличить сложность за каждый JOIN
        complexity_score += query_lower.count(' join ') * 3
        
        # Увеличить сложность за GROUP BY
        if 'group by' in query_lower:
            complexity_score += 2
        
        # Увеличить сложность за подзапросы
        complexity_score += query_lower.count('(') * 1.5
        
        # Увеличить сложность за DISTINCT
        if 'distinct' in query_lower:
            complexity_score += 1
        
        # Увеличить сложность за ORDER BY
        if 'order by' in query_lower:
            complexity_score += 1
        
        if complexity_score >= 10:
            return 'critical'
        elif complexity_score >= 6:
            return 'high'
        elif complexity_score >= 3:
            return 'medium'
        else:
            return 'low'
    
    def optimize_query(self, query: str) -> str:
        """
        Предложить оптимизированный вариант запроса.
        
        Args:
            query: Оригинальный SQL-запрос
            
        Returns:
            Оптимизированный SQL-запрос
        """
        logger.info(f"Оптимизация запроса: {query[:100]}...")
        
        optimized_query = query.strip()
        
        # Простые оптимизации
        analysis = self.analyze_query(query)
        
        # Если есть рекомендации по индексам, добавить комментарий
        if any(issue['type'] == 'function_in_where' for issue in analysis['potential_issues']):
            # В DuckDB нет традиционных индексов, но можно порекомендовать оптимизации
            logger.info("Рекомендация: для лучшей производительности рассмотрите фильтрацию сначала по наиболее ограничивающим условиям")
        
        # Если запрос простой, возвратить как есть
        if analysis['estimated_complexity'] in ['low', 'medium']:
            return optimized_query
        
        # Попробовать оптимизировать сложные запросы
        optimized_query = self._apply_basic_optimizations(optimized_query)
        
        return optimized_query
    
    def _apply_basic_optimizations(self, query: str) -> str:
        """Применить базовые оптимизации к запросу."""
        # Упорядочить условия WHERE по эффективности (гипотетически)
        # В реальном приложении это будет более сложной логикой
        
        # Упростить лишние скобки в простых случаях
        # (это упрощенная реализация)
        
        return query
    
    def get_performance_insights(self, query: str) -> Dict[str, any]:
        """
        Получить подробную информацию о производительности запроса.
        
        Args:
            query: SQL-запрос для анализа
            
        Returns:
            Словарь с информацией о производительности
        """
        insights = {
            'query_analysis': self.analyze_query(query),
            'comparison_data': {},
            'optimization_score': 0  # 0-100, где 100 - идеальная оптимизация
        }
        
        # Выполнить несколько тестов для оценки производительности
        try:
            # Тест с LIMIT для быстрой оценки
            limited_query = query.strip()
            if 'order by' in limited_query.lower() and 'limit' not in limited_query.lower():
                limited_query += " LIMIT 100"
            
            start_time = time.time()
            result = self.con.execute(limited_query).fetchall()
            execution_time = (time.time() - start_time) * 1000  # в миллисекундах
            
            insights['comparison_data'] = {
                'execution_time_ms': round(execution_time, 2),
                'result_rows': len(result),
                'result_columns': len(result[0]) if result else 0
            }
            
            # Рассчитать оценку оптимизации (упрощенно)
            base_score = 100
            analysis = insights['query_analysis']
            
            if analysis['estimated_complexity'] == 'critical':
                base_score -= 40
            elif analysis['estimated_complexity'] == 'high':
                base_score -= 20
            elif analysis['estimated_complexity'] == 'medium':
                base_score -= 10
            
            base_score -= len(analysis['potential_issues']) * 5
            base_score = max(0, min(100, base_score))
            
            insights['optimization_score'] = base_score
            
        except Exception as e:
            logger.error(f"Ошибка при получении информации о производительности: {e}")
            insights['comparison_data'] = {'error': str(e)}
        
        return insights


def main():
    """Основная функция для демонстрации возможностей оптимизатора запросов."""
    from config import LOG_LEVEL
    from utils import setup_logging
    
    # Настроить логирование
    setup_logging(LOG_LEVEL)
    
    logger.info("Запуск оптимизатора запросов")
    
    try:
        optimizer = QueryOptimizer()
        
        # Примеры запросов для анализа
        sample_queries = [
            "SELECT * FROM ozon_products;",
            "SELECT name, price FROM ozon_products WHERE price > 10000 ORDER BY price DESC LIMIT 10;",
            "SELECT brand, AVG(price) as avg_price FROM ozon_products GROUP BY brand;",
            "SELECT * FROM ozon_products WHERE LOWER(name) LIKE '%iphone%' AND price BETWEEN 50000 AND 100000;"
        ]
        
        print("🔍 АНАЛИЗ ЗАПРОСОВ")
        print("="*60)
        
        for i, query in enumerate(sample_queries, 1):
            print(f"\n📊 Запрос #{i}: {query[:50]}{'...' if len(query) > 50 else ''}")
            
            analysis = optimizer.analyze_query(query)
            
            print(f"  • Сложность: {analysis['estimated_complexity']}")
            print(f"  • Оценка времени: {analysis['estimated_time_ms']} ms" if analysis['estimated_time_ms'] else "  • Оценка времени: недоступна")
            print(f"  • Потенциальных проблем: {len(analysis['potential_issues'])}")
            
            if analysis['potential_issues']:
                print("  ⚠️  Обнаруженные проблемы:")
                for issue in analysis['potential_issues']:
                    print(f"    - {issue['type']}: {issue['description']}")
            
            if analysis['recommendations']:
                print("  💡 Рекомендации:")
                for rec in analysis['recommendations']:
                    print(f"    - {rec}")
            
            # Получить полную информацию о производительности
            insights = optimizer.get_performance_insights(query)
            print(f"  • Оценка оптимизации: {insights['optimization_score']}/100")
            
            if 'execution_time_ms' in insights['comparison_data']:
                comp_data = insights['comparison_data']
                print(f"  • Время выполнения: {comp_data['execution_time_ms']} ms")
                print(f"  • Результатов: {comp_data['result_rows']}")
        
        print(f"\n✨ Анализ запросов завершен!")
        
    except Exception as e:
        logger.error(f"Ошибка в процессе анализа запросов: {e}")
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    main()