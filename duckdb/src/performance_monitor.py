# -*- coding: utf-8 -*-
"""
Модуль мониторинга производительности для базы данных товаров Ozon

Этот модуль предоставляет инструменты для мониторинга и анализа 
производительности запросов к базе данных DuckDB.
"""

import time
import psutil
import os
from datetime import datetime
from typing import Dict, List, Callable, Any
import duckdb
import pandas as pd
from config import DATABASE_NAME
from utils import get_logger, get_current_datetime_str


logger = get_logger(__name__)


class PerformanceMonitor:
    """Класс для мониторинга производительности базы данных."""
    
    def __init__(self, db_path: str = DATABASE_NAME):
        """
        Инициализировать монитор производительности.
        
        Args:
            db_path: Путь к базе данных
        """
        self.db_path = db_path
        self.monitoring_results = []
        logger.info(f"Монитор производительности инициализирован для базы: {db_path}")
    
    def measure_query_performance(self, query: str, params: tuple = ()) -> Dict[str, Any]:
        """
        Измерить производительность SQL-запроса.
        
        Args:
            query: SQL-запрос для измерения
            params: Параметры для запроса
            
        Returns:
            Результаты измерения производительности
        """
        # Сохранить начальное состояние системы
        start_time = time.time()
        start_cpu = psutil.cpu_percent()
        start_memory = psutil.virtual_memory().used
        start_process_memory = psutil.Process().memory_info().rss
        
        try:
            # Выполнить запрос
            con = duckdb.connect(self.db_path)
            query_start_time = time.time()
            result = con.execute(query, params).fetchall()
            query_time = time.time() - query_start_time
            con.close()
            
            # Измерить общее время выполнения
            total_time = time.time() - start_time
            
            # Получить текущее состояние системы
            end_cpu = psutil.cpu_percent()
            end_memory = psutil.virtual_memory().used
            end_process_memory = psutil.Process().memory_info().rss
            
            # Рассчитать изменения
            cpu_used = end_cpu - start_cpu
            memory_delta = end_memory - start_memory
            process_memory_delta = end_process_memory - start_process_memory
            
            result = {
                'query': query[:100] + '...' if len(query) > 100 else query,  # Обрезать длинные запросы
                'execution_time': round(total_time, 4),
                'query_time': round(query_time, 4),
                'cpu_used': cpu_used,
                'memory_delta_mb': round(memory_delta / (1024 * 1024), 2),
                'process_memory_delta_mb': round(process_memory_delta / (1024 * 1024), 2),
                'result_count': len(result),
                'timestamp': get_current_datetime_str()
            }
            
            self.monitoring_results.append(result)
            logger.info(f"Запрос выполнен за {total_time:.4f}с, результатов: {len(result)}")
            
            return result
            
        except Exception as e:
            logger.error(f"Ошибка при измерении производительности запроса: {e}")
            raise
    
    def measure_function_performance(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """
        Измерить производительность функции.
        
        Args:
            func: Функция для измерения
            *args: Аргументы функции
            **kwargs: Ключевые аргументы функции
            
        Returns:
            Результаты измерения производительности
        """
        # Сохранить начальное состояние системы
        start_time = time.time()
        start_cpu = psutil.cpu_percent()
        start_memory = psutil.virtual_memory().used
        start_process_memory = psutil.Process().memory_info().rss
        
        try:
            # Выполнить функцию
            func_start_time = time.time()
            result = func(*args, **kwargs)
            func_time = time.time() - func_start_time
            
            # Измерить общее время выполнения
            total_time = time.time() - start_time
            
            # Получить текущее состояние системы
            end_cpu = psutil.cpu_percent()
            end_memory = psutil.virtual_memory().used
            end_process_memory = psutil.Process().memory_info().rss
            
            # Рассчитать изменения
            cpu_used = end_cpu - start_cpu
            memory_delta = end_memory - start_memory
            process_memory_delta = end_process_memory - start_process_memory
            
            result_info = {
                'function_name': func.__name__,
                'execution_time': round(total_time, 4),
                'function_time': round(func_time, 4),
                'cpu_used': cpu_used,
                'memory_delta_mb': round(memory_delta / (1024 * 1024), 2),
                'process_memory_delta_mb': round(process_memory_delta / (1024 * 1024), 2),
                'result_info': f"Результат типа {type(result).__name__}" if result else "Нет результата",
                'timestamp': get_current_datetime_str()
            }
            
            self.monitoring_results.append(result_info)
            logger.info(f"Функция {func.__name__} выполнена за {total_time:.4f}с")
            
            return result_info
            
        except Exception as e:
            logger.error(f"Ошибка при измерении производительности функции: {e}")
            raise
    
    def get_performance_summary(self) -> str:
        """
        Получить сводку по производительности.
        
        Returns:
            Текстовая сводка по производительности
        """
        if not self.monitoring_results:
            return "❌ НЕТ ДАННЫХ О ПРОИЗВОДИТЕЛЬНОСТИ"
        
        # Подготовить данные для анализа
        df = pd.DataFrame(self.monitoring_results)
        
        summary = []
        summary.append("⚡ СВОДКА ПО ПРОИЗВОДИТЕЛЬНОСТИ")
        summary.append("=" * 50)
        summary.append(f"Всего измерений: {len(df)}")
        summary.append("")
        
        # Статистика по времени выполнения
        if 'execution_time' in df.columns:
            summary.append("⏱️  ВРЕМЯ ВЫПОЛНЕНИЯ:")
            summary.append(f"  • Среднее время: {df['execution_time'].mean():.4f}с")
            summary.append(f"  • Минимальное время: {df['execution_time'].min():.4f}с")
            summary.append(f"  • Максимальное время: {df['execution_time'].max():.4f}с")
            summary.append(f"  • Общее время: {df['execution_time'].sum():.4f}с")
            summary.append("")
        
        # Статистика по использованию памяти
        if 'process_memory_delta_mb' in df.columns:
            summary.append("💾 ИСПОЛЬЗОВАНИЕ ПАМЯТИ:")
            summary.append(f"  • Среднее изменение: {df['process_memory_delta_mb'].mean():.2f}MB")
            summary.append(f"  • Максимальное изменение: {df['process_memory_delta_mb'].max():.2f}MB")
            summary.append("")
        
        # Топ медленных запросов/функций
        if 'execution_time' in df.columns:
            slowest = df.nlargest(3, 'execution_time')
            summary.append("🐢 ТОП-3 МЕДЛЕННЫХ ОПЕРАЦИЙ:")
            for _, row in slowest.iterrows():
                op_type = "Запрос" if 'query' in row else "Функция"
                op_desc = row.get('query', row.get('function_name', 'Неизвестно'))
                summary.append(f"  • {op_type}: {row['execution_time']:.4f}с - {op_desc[:50]}...")
            summary.append("")
        
        return "\n".join(summary)
    
    def save_performance_report(self, filename: str = "performance_report.txt") -> str:
        """
        Сохранить отчет о производительности в файл.
        
        Args:
            filename: Имя файла для сохранения отчета
            
        Returns:
            Путь к сохраненному файлу
        """
        report_content = self.get_performance_summary()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Отчет о производительности - {get_current_datetime_str()}\n")
            f.write("=" * 60 + "\n\n")
            f.write(report_content)
            
            if self.monitoring_results:
                f.write("\n\nДЕТАЛЬНЫЕ РЕЗУЛЬТАТЫ:\n")
                f.write("-" * 30 + "\n")
                for result in self.monitoring_results:
                    f.write(f"Время: {result['timestamp']}\n")
                    for key, value in result.items():
                        if key != 'timestamp':
                            f.write(f"  {key}: {value}\n")
                    f.write("\n")
        
        logger.info(f"Отчет о производительности сохранен: {filename}")
        return filename


def main():
    """Основная функция для демонстрации возможностей монитора производительности."""
    from config import LOG_LEVEL
    from utils import setup_logging
    
    # Настроить логирование
    setup_logging(LOG_LEVEL)
    
    logger.info("Запуск монитора производительности")
    
    try:
        monitor = PerformanceMonitor()
        
        print("🚀 ТЕСТИРОВАНИЕ ПРОИЗВОДИТЕЛЬНОСТИ")
        print("="*50)
        
        # Тестировать различные запросы
        queries = [
            ("SELECT COUNT(*) FROM ozon_products;", "Подсчет общего количества товаров"),
            ("SELECT * FROM ozon_products ORDER BY price DESC LIMIT 10;", "Поиск топ-10 дорогих товаров"),
            ("SELECT brand, AVG(price) as avg_price FROM ozon_products GROUP BY brand;", "Средняя цена по брендам"),
            ("SELECT * FROM ozon_products WHERE rating > 4.5 LIMIT 20;", "Товары с высоким рейтингом")
        ]
        
        for query, description in queries:
            print(f"\n🧪 Тест: {description}")
            result = monitor.measure_query_performance(query)
            print(f"   Время выполнения: {result['execution_time']}с")
            print(f"   Результатов: {result['result_count']}")
        
        # Показать сводку
        print(f"\n📋 СВОДКА ПО ПРОИЗВОДИТЕЛЬНОСТИ")
        print("="*50)
        summary = monitor.get_performance_summary()
        print(summary)
        
        # Сохранить отчет
        print(f"\n💾 СОХРАНЕНИЕ ОТЧЕТА О ПРОИЗВОДИТЕЛЬНОСТИ")
        print("="*50)
        report_path = monitor.save_performance_report()
        print(f"✅ Отчет сохранен: {report_path}")
        
        print(f"\n✨ Мониторинг производительности завершен!")
        
    except Exception as e:
        logger.error(f"Ошибка в процессе мониторинга производительности: {e}")
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    main()