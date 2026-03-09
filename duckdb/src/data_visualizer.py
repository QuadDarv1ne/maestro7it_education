# -*- coding: utf-8 -*-
"""
Модуль визуализации данных для базы данных товаров Ozon

Этот модуль предоставляет инструменты для создания графиков и диаграмм 
из данных товаров Ozon с использованием matplotlib.
"""

import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Dict, List, Optional, Tuple
from config import DATABASE_NAME, CHARTS_DIR
from utils import get_logger
import os
from datetime import datetime


logger = get_logger(__name__)


class DataVisualizer:
    """Класс для создания визуализаций из данных базы данных."""
    
    def __init__(self, db_path: str = DATABASE_NAME, charts_dir: str = "charts"):
        """
        Инициализировать визуализатор данных.
        
        Args:
            db_path: Путь к базе данных
            charts_dir: Директория для сохранения графиков
        """
        self.db_path = db_path
        self.charts_dir = charts_dir
        os.makedirs(charts_dir, exist_ok=True)
        
        # Настроить стили matplotlib
        plt.style.use('seaborn-v0_8')
        logger.info(f"Визуализатор данных инициализирован для базы: {db_path}, charts: {charts_dir}")
    
    def create_price_distribution_chart(self, save_path: Optional[str] = None) -> str:
        """
        Создать график распределения цен.
        
        Args:
            save_path: Путь для сохранения графика (опционально)
            
        Returns:
            Путь к сохраненному графику
        """
        logger.info("Создание графика распределения цен")
        
        # Получить данные из базы данных
        con = duckdb.connect(self.db_path)
        query = "SELECT price FROM ozon_products WHERE price IS NOT NULL;"
        df = con.execute(query).fetchdf()
        con.close()
        
        # Создать график
        plt.figure(figsize=(12, 6))
        
        # Гистограмма распределения цен
        plt.subplot(1, 2, 1)
        plt.hist(df['price'], bins=30, edgecolor='black', alpha=0.7)
        plt.title('Распределение цен товаров', fontsize=14, fontweight='bold')
        plt.xlabel('Цена (руб.)')
        plt.ylabel('Количество товаров')
        plt.grid(True, alpha=0.3)
        
        # Box plot цен
        plt.subplot(1, 2, 2)
        plt.boxplot(df['price'], vert=True)
        plt.title('Ящик с усами - распределение цен', fontsize=14, fontweight='bold')
        plt.ylabel('Цена (руб.)')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Сохранить график
        if save_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.charts_dir, f"price_distribution_{timestamp}.png")
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"График распределения цен сохранен: {save_path}")
        return save_path
    
    def create_rating_vs_price_chart(self, save_path: Optional[str] = None) -> str:
        """
        Создать график зависимости рейтинга от цены.
        
        Args:
            save_path: Путь для сохранения графика (опционально)
            
        Returns:
            Путь к сохраненному графику
        """
        logger.info("Создание графика зависимости рейтинга от цены")
        
        # Получить данные из базы данных
        con = duckdb.connect(self.db_path)
        query = """
            SELECT 
                price, 
                rating 
            FROM ozon_products 
            WHERE price IS NOT NULL AND rating IS NOT NULL
            AND price > 0 AND rating > 0;
        """
        df = con.execute(query).fetchdf()
        con.close()
        
        # Создать график
        plt.figure(figsize=(10, 6))
        
        # Scatter plot
        plt.scatter(df['price'], df['rating'], alpha=0.6, s=50, edgecolors='w', linewidth=0.5)
        plt.title('Зависимость рейтинга от цены товаров', fontsize=14, fontweight='bold')
        plt.xlabel('Цена (руб.)')
        plt.ylabel('Рейтинг')
        plt.grid(True, alpha=0.3)
        
        # Добавить тренд (линию регрессии)
        try:
            z = np.polyfit(df['price'], df['rating'], 1)
            p = np.poly1d(z)
            plt.plot(df['price'], p(df['price']), "r--", alpha=0.8, label=f'Тренд')
            plt.legend()
        except (ValueError, np.RankWarning) as e:
            logger.warning(f"Не удалось построить тренд: {e}")

        # Сохранить график
        if save_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.charts_dir, f"rating_vs_price_{timestamp}.png")
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"График зависимости рейтинга от цены сохранен: {save_path}")
        return save_path
    
    def create_top_brands_chart(self, limit: int = 10, save_path: Optional[str] = None) -> str:
        """
        Создать график топ брендов по количеству товаров.
        
        Args:
            limit: Количество брендов для отображения
            save_path: Путь для сохранения графика (опционально)
            
        Returns:
            Путь к сохраненному графику
        """
        logger.info(f"Создание графика топ-{limit} брендов")
        
        # Получить данные из базы данных
        con = duckdb.connect(self.db_path)
        query = f"""
            SELECT 
                brand,
                COUNT(*) as product_count,
                AVG(price) as avg_price,
                AVG(rating) as avg_rating
            FROM ozon_products 
            WHERE brand IS NOT NULL
            GROUP BY brand
            ORDER BY product_count DESC
            LIMIT {limit};
        """
        df = con.execute(query).fetchdf()
        con.close()
        
        # Создать график
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Горизонтальный bar chart
        bars = ax.barh(range(len(df)), df['product_count'], color='skyblue', edgecolor='navy', height=0.7)
        
        # Добавить значения на бары
        for i, (bar, count) in enumerate(zip(bars, df['product_count'])):
            width = bar.get_width()
            ax.text(width + max(df['product_count']) * 0.01, bar.get_y() + bar.get_height()/2, 
                   f'{int(count)}', ha='left', va='center', fontweight='bold')
        
        ax.set_yticks(range(len(df)))
        ax.set_yticklabels(df['brand'])
        ax.set_xlabel('Количество товаров')
        ax.set_title(f'Топ-{limit} брендов по количеству товаров', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        
        # Сохранить график
        if save_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.charts_dir, f"top_brands_{limit}_{timestamp}.png")
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"График топ брендов сохранен: {save_path}")
        return save_path
    
    def create_category_analysis_chart(self, save_path: Optional[str] = None) -> str:
        """
        Создать график анализа по категориям (количество товаров, средняя цена).
        
        Args:
            save_path: Путь для сохранения графика (опционально)
            
        Returns:
            Путь к сохраненному графику
        """
        logger.info("Создание графика анализа по категориям")
        
        # Получить данные из базы данных
        con = duckdb.connect(self.db_path)
        query = """
            SELECT 
                category,
                COUNT(*) as product_count,
                AVG(price) as avg_price,
                AVG(rating) as avg_rating
            FROM ozon_products 
            WHERE category IS NOT NULL
            GROUP BY category
            ORDER BY product_count DESC
            LIMIT 10;
        """
        df = con.execute(query).fetchdf()
        con.close()
        
        # Создать график
        fig, ax1 = plt.subplots(figsize=(14, 8))
        
        # Основной bar chart для количества товаров
        color = 'tab:blue'
        ax1.set_xlabel('Категория')
        ax1.set_ylabel('Количество товаров', color=color)
        bars = ax1.bar(df['category'], df['product_count'], color='lightblue', alpha=0.7, label='Количество товаров')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.tick_params(axis='x', rotation=45)
        
        # Вторая ось для средней цены
        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('Средняя цена (руб.)', color=color)
        line = ax2.plot(df['category'], df['avg_price'], color=color, marker='o', linewidth=2, markersize=6, label='Средняя цена')
        ax2.tick_params(axis='y', labelcolor=color)
        
        plt.title('Анализ категорий товаров - количество и средняя цена', fontsize=14, fontweight='bold')
        fig.tight_layout()
        
        # Добавить легенду
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        # Сохранить график
        if save_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.charts_dir, f"category_analysis_{timestamp}.png")
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"График анализа по категориям сохранен: {save_path}")
        return save_path
    
    def create_comprehensive_dashboard(self) -> List[str]:
        """
        Создать комплексную панель управления с несколькими графиками.
        
        Returns:
            Список путей к сохраненным графикам
        """
        logger.info("Создание комплексной панели управления")
        
        chart_paths = []
        
        # Создать все основные графики
        chart_paths.append(self.create_price_distribution_chart())
        chart_paths.append(self.create_rating_vs_price_chart())
        chart_paths.append(self.create_top_brands_chart(limit=8))
        chart_paths.append(self.create_category_analysis_chart())
        
        logger.info(f"Комплексная панель управления создана. Сохранено графиков: {len(chart_paths)}")
        return chart_paths


def main():
    """Основная функция для демонстрации возможностей визуализатора данных."""
    from config import LOG_LEVEL
    from utils import setup_logging
    import numpy as np
    
    # Настроить логирование
    setup_logging(LOG_LEVEL)
    
    logger.info("Запуск визуализатора данных")
    
    try:
        visualizer = DataVisualizer()
        
        print("📊 СОЗДАНИЕ ГРАФИКОВ ВИЗУАЛИЗАЦИИ")
        print("="*60)
        
        # Создать основные графики
        print("1. Распределение цен...")
        price_chart = visualizer.create_price_distribution_chart()
        print(f"   ✅ График сохранен: {os.path.basename(price_chart)}")
        
        print("2. Зависимость рейтинга от цены...")
        rating_chart = visualizer.create_rating_vs_price_chart()
        print(f"   ✅ График сохранен: {os.path.basename(rating_chart)}")
        
        print("3. Топ брендов...")
        brands_chart = visualizer.create_top_brands_chart(limit=8)
        print(f"   ✅ График сохранен: {os.path.basename(brands_chart)}")
        
        print("4. Анализ по категориям...")
        category_chart = visualizer.create_category_analysis_chart()
        print(f"   ✅ График сохранен: {os.path.basename(category_chart)}")
        
        print(f"\n📈 КОМПЛЕКСНАЯ ПАНЕЛЬ УПРАВЛЕНИЯ")
        print("="*60)
        dashboard_charts = visualizer.create_comprehensive_dashboard()
        print(f"   Создано {len(dashboard_charts)} графиков для панели управления")
        
        print(f"\n📁 ДИРЕКТОРИЯ С ГРАФИКАМИ: {visualizer.charts_dir}")
        print("   Все графики сохранены в формате PNG с высоким разрешением")
        
        print(f"\n✨ Визуализация данных завершена!")
        
    except ImportError as e:
        logger.error(f"Для визуализации данных необходимо установить matplotlib и seaborn: {e}")
        print(f"❌ Ошибка: {e}")
        print("   Установите необходимые библиотеки: pip install matplotlib seaborn")
    except Exception as e:
        logger.error(f"Ошибка в процессе визуализации данных: {e}")
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    main()