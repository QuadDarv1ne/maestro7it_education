# -*- coding: utf-8 -*-
"""
Модуль валидации данных для базы данных товаров Ozon

Этот модуль предоставляет функции для проверки качества данных
в базе данных товаров Ozon.
"""

import duckdb
import pandas as pd
from typing import Dict, List, Tuple, Optional
from config import DATABASE_NAME
from utils import get_logger


logger = get_logger(__name__)


class DataValidator:
    """Класс для проверки качества данных в базе данных."""
    
    def __init__(self, db_path: str = DATABASE_NAME):
        """
        Инициализировать валидатор данных.
        
        Args:
            db_path: Путь к базе данных
        """
        self.db_path = db_path
        self.con = duckdb.connect(db_path)
        logger.info(f"Валидатор данных инициализирован для базы: {db_path}")
    
    def __del__(self):
        """Закрыть соединение при удалении объекта."""
        if hasattr(self, 'con'):
            self.con.close()
    
    def validate_product_data(self) -> Dict[str, List[Dict]]:
        """
        Проверить качество данных товаров.
        
        Returns:
            Результаты валидации
        """
        logger.info("Проверка качества данных товаров")
        
        results = {
            'missing_values': [],
            'outliers': [],
            'inconsistencies': [],
            'summary': {}
        }
        
        # Проверить количество записей
        count_query = "SELECT COUNT(*) as total_count FROM ozon_products;"
        total_count = self.con.execute(count_query).fetchone()[0]
        results['summary']['total_records'] = total_count
        logger.info(f"Всего записей: {total_count}")
        
        # Проверить пропущенные значения
        missing_checks = [
            {'column': 'name', 'query': "SELECT product_id, name FROM ozon_products WHERE name IS NULL OR name = '';"},
            {'column': 'brand', 'query': "SELECT product_id, brand FROM ozon_products WHERE brand IS NULL OR brand = '';"},
            {'column': 'category', 'query': "SELECT product_id, category FROM ozon_products WHERE category IS NULL OR category = '';"},
            {'column': 'price', 'query': "SELECT product_id, price FROM ozon_products WHERE price IS NULL OR price <= 0;"},
            {'column': 'rating', 'query': "SELECT product_id, rating FROM ozon_products WHERE rating IS NULL OR rating < 0 OR rating > 5;"},
            {'column': 'review_count', 'query': "SELECT product_id, review_count FROM ozon_products WHERE review_count IS NULL OR review_count < 0;"},
        ]
        
        for check in missing_checks:
            missing_data = self.con.execute(check['query']).fetchall()
            if missing_data:
                results['missing_values'].append({
                    'column': check['column'],
                    'count': len(missing_data),
                    'samples': missing_data[:5]  # Показать первые 5 примеров
                })
        
        # Проверить выбросы в ценах
        price_outlier_query = """
            SELECT product_id, name, price
            FROM ozon_products
            WHERE price > (
                SELECT AVG(price) + 3 * STDDEV_POP(price) 
                FROM ozon_products 
                WHERE price > 0
            );
        """
        price_outliers = self.con.execute(price_outlier_query).fetchall()
        if price_outliers:
            results['outliers'].append({
                'column': 'price',
                'type': 'high_value',
                'count': len(price_outliers),
                'samples': price_outliers[:5]
            })
        
        # Проверить выбросы в рейтинге
        rating_outlier_query = """
            SELECT product_id, name, rating
            FROM ozon_products
            WHERE rating > 5 OR rating < 0;
        """
        rating_outliers = self.con.execute(rating_outlier_query).fetchall()
        if rating_outliers:
            results['outliers'].append({
                'column': 'rating',
                'type': 'invalid_range',
                'count': len(rating_outliers),
                'samples': rating_outliers[:5]
            })
        
        # Проверить логические несоответствия
        inconsistency_checks = [
            {
                'type': 'negative_discount',
                'query': "SELECT product_id, name, price, old_price FROM ozon_products WHERE old_price > 0 AND price > old_price;",
                'description': 'Цена больше старой цены (отрицательная скидка)'
            },
            {
                'type': 'zero_price_with_positive_old',
                'query': "SELECT product_id, name, price, old_price FROM ozon_products WHERE price = 0 AND old_price > 0;",
                'description': 'Нулевая цена при положительной старой цене'
            }
        ]
        
        for check in inconsistency_checks:
            inconsistencies = self.con.execute(check['query']).fetchall()
            if inconsistencies:
                results['inconsistencies'].append({
                    'type': check['type'],
                    'description': check['description'],
                    'count': len(inconsistencies),
                    'samples': inconsistencies[:5]
                })
        
        # Добавить сводную информацию
        results['summary']['missing_value_issues'] = len(results['missing_values'])
        results['summary']['outlier_issues'] = len(results['outliers'])
        results['summary']['inconsistency_issues'] = len(results['inconsistencies'])
        
        logger.info(f"Валидация завершена. Найдено проблем: "
                   f"{results['summary']['missing_value_issues']} пропущенных значений, "
                   f"{results['summary']['outlier_issues']} выбросов, "
                   f"{results['summary']['inconsistency_issues']} несоответствий")
        
        return results
    
    def generate_data_quality_report(self) -> str:
        """
        Сгенерировать текстовый отчет о качестве данных.
        
        Returns:
            Текстовый отчет о качестве данных
        """
        validation_results = self.validate_product_data()
        
        report = []
        report.append("📊 ОТЧЕТ О КАЧЕСТВЕ ДАННЫХ")
        report.append("=" * 50)
        report.append(f"Всего записей: {validation_results['summary']['total_records']}")
        report.append("")
        
        # Отчет о пропущенных значениях
        if validation_results['missing_values']:
            report.append("❌ ПРОПУЩЕННЫЕ ЗНАЧЕНИЯ:")
            for issue in validation_results['missing_values']:
                report.append(f"  • {issue['column']}: {issue['count']} записей")
                for sample in issue['samples']:
                    report.append(f"    - ID {sample[0]}: {sample[1][:50]}{'...' if len(str(sample[1])) > 50 else ''}")
            report.append("")
        else:
            report.append("✅ НЕТ ПРОПУЩЕННЫХ ЗНАЧЕНИЙ")
            report.append("")
        
        # Отчет о выбросах
        if validation_results['outliers']:
            report.append("⚠️  ВЫБРОСЫ:")
            for issue in validation_results['outliers']:
                report.append(f"  • {issue['column']} ({issue['type']}): {issue['count']} записей")
                for sample in issue['samples']:
                    report.append(f"    - ID {sample[0]}: {sample[1]} - {sample[2]}")
            report.append("")
        else:
            report.append("✅ НЕТ ВЫБРОСОВ")
            report.append("")
        
        # Отчет о несоответствиях
        if validation_results['inconsistencies']:
            report.append("❗ ЛОГИЧЕСКИЕ НЕСООТВЕТСТВИЯ:")
            for issue in validation_results['inconsistencies']:
                report.append(f"  • {issue['type']}: {issue['count']} записей ({issue['description']})")
                for sample in issue['samples']:
                    report.append(f"    - ID {sample[0]}: {sample[1][:30]}{'...' if len(str(sample[1])) > 30 else ''}")
            report.append("")
        else:
            report.append("✅ НЕТ ЛОГИЧЕСКИХ НЕСООТВЕТСТВИЙ")
            report.append("")
        
        # Сводка
        report.append("📋 СВОДКА:")
        report.append(f"  • Пропущенные значения: {validation_results['summary']['missing_value_issues']} категорий")
        report.append(f"  • Выбросы: {validation_results['summary']['outlier_issues']} категорий")
        report.append(f"  • Несоответствия: {validation_results['summary']['inconsistency_issues']} категорий")
        
        return "\n".join(report)
    
    def fix_common_issues(self) -> Dict[str, int]:
        """
        Исправить распространенные проблемы с данными.
        
        Returns:
            Результаты исправления проблем
        """
        logger.info("Исправление распространенных проблем с данными")
        
        fixes_applied = {}
        
        # Исправить отрицательные скидки (поменять местами цену и старую цену)
        try:
            fix_query = """
                UPDATE ozon_products 
                SET price = old_price, old_price = price 
                WHERE old_price > 0 AND price > old_price;
            """
            result = self.con.execute(fix_query)
            self.con.commit()
            fixes_applied['negative_discounts_fixed'] = result.fetchall() if result else 0
            logger.info("Исправлены отрицательные скидки")
        except Exception as e:
            logger.warning(f"Не удалось исправить отрицательные скидки: {e}")
        
        # Заменить отрицательные значения на NULL
        try:
            self.con.execute("UPDATE ozon_products SET price = NULL WHERE price < 0;")
            self.con.execute("UPDATE ozon_products SET rating = NULL WHERE rating < 0 OR rating > 5;")
            self.con.execute("UPDATE ozon_products SET review_count = NULL WHERE review_count < 0;")
            self.con.commit()
            logger.info("Исправлены отрицательные значения")
        except Exception as e:
            logger.warning(f"Не удалось исправить отрицательные значения: {e}")
        
        return fixes_applied


def main():
    """Основная функция для демонстрации возможностей валидатора данных."""
    from config import LOG_LEVEL
    from utils import setup_logging
    
    # Настроить логирование
    setup_logging(LOG_LEVEL)
    
    logger.info("Запуск валидатора данных")
    
    try:
        validator = DataValidator()
        
        # Сгенерировать отчет о качестве данных
        report = validator.generate_data_quality_report()
        print(report)
        
        # Исправить распространенные проблемы
        print(f"\n🔧 ИСПРАВЛЕНИЕ РАСПРОСТРАНЕННЫХ ПРОБЛЕМ")
        print("="*50)
        fixes = validator.fix_common_issues()
        print("✅ Распространенные проблемы исправлены")
        
        # Повторная проверка после исправления
        print(f"\n🔍 ПОВТОРНАЯ ПРОВЕРКА ПОСЛЕ ИСПРАВЛЕНИЯ")
        print("="*50)
        updated_report = validator.generate_data_quality_report()
        
        # Вывести только сводку
        lines = updated_report.split('\n')
        summary_started = False
        for line in lines:
            if 'СВОДКА:' in line:
                summary_started = True
            if summary_started:
                print(line)
        
        print(f"\n✨ Валидация данных завершена!")
        
    except Exception as e:
        logger.error(f"Ошибка в процессе валидации данных: {e}")
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    main()