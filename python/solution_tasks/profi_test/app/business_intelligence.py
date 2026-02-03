# -*- coding: utf-8 -*-
"""
Модуль бизнес-аналитики для ПрофиТест
Предоставляет продвинутые аналитические инструменты для принятия решений
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any, Optional
import logging
from collections import defaultdict
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass
from enum import Enum


class AnalysisType(Enum):
    """Типы анализа"""
    DESCRIPTIVE = 'descriptive'
    PREDICTIVE = 'predictive'
    PRESCRIPTIVE = 'prescriptive'
    DIAGNOSTIC = 'diagnostic'


class BusinessMetric(Enum):
    """Бизнес-метрики"""
    USER_ENGAGEMENT = 'user_engagement'
    TEST_COMPLETION_RATE = 'test_completion_rate'
    RETENTION_RATE = 'retention_rate'
    REVENUE_PER_USER = 'revenue_per_user'
    CONVERSION_RATE = 'conversion_rate'
    SATISFACTION_SCORE = 'satisfaction_score'


@dataclass
class AnalysisResult:
    """Результат анализа"""
    metric: BusinessMetric
    value: float
    trend: str  # 'increasing', 'decreasing', 'stable'
    confidence: float
    insights: List[str]
    recommendations: List[str]
    timestamp: datetime


class BusinessIntelligenceEngine:
    """
    Движок бизнес-аналитики для системы ПрофиТест.
    Обеспечивает комплексный анализ данных и генерацию рекомендаций.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.data_cache = {}
        self.analysis_results = []
        self.kpi_thresholds = {
            BusinessMetric.USER_ENGAGEMENT: 0.7,
            BusinessMetric.TEST_COMPLETION_RATE: 0.8,
            BusinessMetric.RETENTION_RATE: 0.6,
            BusinessMetric.CONVERSION_RATE: 0.05,
            BusinessMetric.SATISFACTION_SCORE: 4.0
        }
    
    def load_user_data(self, db_connection) -> pd.DataFrame:
        """
        Загружает данные пользователей из базы данных.
        
        Args:
            db_connection: Подключение к базе данных
            
        Returns:
            DataFrame: Данные пользователей
        """
        try:
            # В реальной реализации будет запрос к базе данных
            # Пока возвращаем заглушку с фейковыми данными
            user_data = pd.DataFrame({
                'user_id': range(1, 1001),
                'registration_date': pd.date_range(start='2023-01-01', periods=1000, freq='D'),
                'last_active': pd.date_range(start='2023-06-01', periods=1000, freq='D'),
                'tests_completed': np.random.randint(0, 20, 1000),
                'time_spent_minutes': np.random.randint(0, 300, 1000),
                'satisfaction_score': np.random.uniform(1.0, 5.0, 1000),
                'premium_user': np.random.choice([True, False], 1000, p=[0.2, 0.8])
            })
            
            return user_data
        except Exception as e:
            self.logger.error(f"Ошибка при загрузке данных пользователей: {str(e)}")
            return pd.DataFrame()
    
    def load_test_data(self, db_connection) -> pd.DataFrame:
        """
        Загружает данные тестов из базы данных.
        
        Args:
            db_connection: Подключение к базе данных
            
        Returns:
            DataFrame: Данные тестов
        """
        try:
            # В реальной реализации будет запрос к базе данных
            # Пока возвращаем заглушку с фейковыми данными
            test_data = pd.DataFrame({
                'test_id': range(1, 51),
                'test_name': [f'Test_{i}' for i in range(1, 51)],
                'attempts': np.random.randint(10, 1000, 50),
                'completion_rate': np.random.uniform(0.5, 1.0, 50),
                'average_score': np.random.uniform(3.0, 5.0, 50),
                'difficulty': np.random.choice(['easy', 'medium', 'hard'], 50, p=[0.3, 0.5, 0.2])
            })
            
            return test_data
        except Exception as e:
            self.logger.error(f"Ошибка при загрузке данных тестов: {str(e)}")
            return pd.DataFrame()
    
    def calculate_kpi(self, user_data: pd.DataFrame, test_data: pd.DataFrame) -> Dict[str, float]:
        """
        Рассчитывает ключевые показатели эффективности.
        
        Args:
            user_data: Данные пользователей
            test_data: Данные тестов
            
        Returns:
            dict: Рассчитанные KPI
        """
        if user_data.empty or test_data.empty:
            return {}
        
        kpis = {}
        
        # Рассчитываем метрики
        total_users = len(user_data)
        active_users = len(user_data[user_data['last_active'] >= datetime.now() - timedelta(days=30)])
        total_tests_taken = user_data['tests_completed'].sum()
        premium_users = len(user_data[user_data['premium_user']])
        
        # Пользовательская вовлеченность
        kpis['user_engagement_rate'] = active_users / total_users if total_users > 0 else 0
        
        # Среднее количество тестов на пользователя
        kpis['avg_tests_per_user'] = total_tests_taken / total_users if total_users > 0 else 0
        
        # Доля премиум-пользователей
        kpis['premium_user_ratio'] = premium_users / total_users if total_users > 0 else 0
        
        # Средняя оценка удовлетворенности
        kpis['avg_satisfaction_score'] = user_data['satisfaction_score'].mean()
        
        # Среднее время в приложении
        kpis['avg_time_spent_minutes'] = user_data['time_spent_minutes'].mean()
        
        # Уровень удержания (доля пользователей, активных за последние 30 дней)
        retention_period = datetime.now() - timedelta(days=90)
        new_users = len(user_data[user_data['registration_date'] >= retention_period])
        retained_users = len(user_data[
            (user_data['registration_date'] >= retention_period) & 
            (user_data['last_active'] >= datetime.now() - timedelta(days=30))
        ])
        kpis['retention_rate'] = retained_users / new_users if new_users > 0 else 0
        
        # Уровень завершения тестов
        avg_completion_rate = test_data['completion_rate'].mean()
        kpis['test_completion_rate'] = avg_completion_rate
        
        # Конверсия (премиум-пользователи / все пользователи)
        kpis['conversion_rate'] = kpis['premium_user_ratio']
        
        return kpis
    
    def analyze_user_behavior(self, user_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Анализирует поведение пользователей.
        
        Args:
            user_data: Данные пользователей
            
        Returns:
            dict: Результаты анализа поведения
        """
        if user_data.empty:
            return {}
        
        analysis = {}
        
        # Кластеризация пользователей по активности
        features = ['tests_completed', 'time_spent_minutes', 'satisfaction_score']
        user_features = user_data[features].fillna(0)
        
        # Нормализация признаков
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(user_features)
        
        # Кластеризация
        n_clusters = min(5, len(user_data))
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(scaled_features)
        
        # Добавляем кластеры к данным
        user_data_clustered = user_data.copy()
        user_data_clustered['cluster'] = clusters
        
        # Анализ каждого кластера
        cluster_analysis = {}
        for cluster_id in range(n_clusters):
            cluster_data = user_data_clustered[user_data_clustered['cluster'] == cluster_id]
            cluster_analysis[f'cluster_{cluster_id}'] = {
                'size': len(cluster_data),
                'avg_tests_completed': cluster_data['tests_completed'].mean(),
                'avg_time_spent': cluster_data['time_spent_minutes'].mean(),
                'avg_satisfaction': cluster_data['satisfaction_score'].mean(),
                'premium_ratio': cluster_data['premium_user'].mean()
            }
        
        analysis['clusters'] = cluster_analysis
        analysis['total_clusters'] = n_clusters
        
        # Анализ временных паттернов
        user_data['registration_month'] = user_data['registration_date'].dt.month
        monthly_registration = user_data.groupby('registration_month').size()
        analysis['monthly_registration_trend'] = monthly_registration.to_dict()
        
        # Анализ активности
        user_data['days_since_registration'] = (datetime.now() - user_data['registration_date']).dt.days
        analysis['avg_days_since_registration'] = user_data['days_since_registration'].mean()
        
        return analysis
    
    def predict_user_retention(self, user_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Предсказывает удержание пользователей.
        
        Args:
            user_data: Данные пользователей
            
        Returns:
            dict: Результаты предсказания
        """
        if user_data.empty:
            return {}
        
        # Простая модель предсказания на основе активности
        predictions = {}
        
        # Пользователи с низкой активностью имеют высокий риск ухода
        low_activity_users = user_data[
            (user_data['tests_completed'] < 3) & 
            (user_data['time_spent_minutes'] < 60)
        ]
        
        predictions['churn_risk_users'] = len(low_activity_users)
        predictions['churn_risk_percentage'] = len(low_activity_users) / len(user_data) * 100
        
        # Пользователи с высокой активностью - хорошие кандидаты для удержания
        high_activity_users = user_data[
            (user_data['tests_completed'] > 10) & 
            (user_data['time_spent_minutes'] > 200) &
            (user_data['satisfaction_score'] > 4.0)
        ]
        
        predictions['loyal_users'] = len(high_activity_users)
        predictions['loyal_user_percentage'] = len(high_activity_users) / len(user_data) * 100
        
        # Рекомендации по удержанию
        recommendations = []
        if predictions['churn_risk_percentage'] > 20:
            recommendations.append("Высокий риск оттока пользователей. Рекомендуется внедрить программу удержания.")
        
        if predictions['loyal_user_percentage'] < 30:
            recommendations.append("Низкий процент лояльных пользователей. Рекомендуется улучшить качество сервиса.")
        
        predictions['recommendations'] = recommendations
        
        return predictions
    
    def generate_insights(self, kpis: Dict[str, float], user_analysis: Dict[str, Any]) -> List[str]:
        """
        Генерирует инсайты на основе анализа.
        
        Args:
            kpis: Ключевые показатели
            user_analysis: Анализ пользователей
            
        Returns:
            list: Список инсайтов
        """
        insights = []
        
        # Анализ пользовательской вовлеченности
        engagement_rate = kpis.get('user_engagement_rate', 0)
        if engagement_rate < 0.5:
            insights.append(f"Низкая вовлеченность пользователей: {engagement_rate:.2%}. Необходимы меры по увеличению активности.")
        elif engagement_rate > 0.8:
            insights.append(f"Высокая вовлеченность пользователей: {engagement_rate:.2%}. Хороший результат!")
        
        # Анализ завершения тестов
        completion_rate = kpis.get('test_completion_rate', 0)
        if completion_rate < 0.7:
            insights.append(f"Низкий уровень завершения тестов: {completion_rate:.2%}. Рекомендуется упростить тесты.")
        elif completion_rate > 0.9:
            insights.append(f"Высокий уровень завершения тестов: {completion_rate:.2%}. Отличная вовлеченность.")
        
        # Анализ удержания
        retention_rate = kpis.get('retention_rate', 0)
        if retention_rate < 0.5:
            insights.append(f"Низкий уровень удержания: {retention_rate:.2%}. Необходима программа удержания.")
        
        # Анализ премиум-пользователей
        premium_ratio = kpis.get('premium_user_ratio', 0)
        if premium_ratio < 0.1:
            insights.append(f"Низкий процент премиум-пользователей: {premium_ratio:.2%}. Рекомендуется улучшить премиум-функции.")
        
        # Анализ кластеров пользователей
        if 'clusters' in user_analysis:
            clusters = user_analysis['clusters']
            for cluster_id, cluster_info in clusters.items():
                if cluster_info['size'] > len(user_analysis.get('total_clusters', [])) * 0.3:
                    insights.append(f"Кластер {cluster_id} содержит {cluster_info['size']} пользователей с характеристиками: "
                                 f"среднее тестов: {cluster_info['avg_tests_completed']:.1f}, "
                                 f"среднее время: {cluster_info['avg_time_spent']:.1f} мин.")
        
        return insights
    
    def generate_recommendations(self, kpis: Dict[str, float], insights: List[str]) -> List[str]:
        """
        Генерирует рекомендации на основе анализа.
        
        Args:
            kpis: Ключевые показатели
            insights: Инсайты
            
        Returns:
            list: Список рекомендаций
        """
        recommendations = []
        
        # Рекомендации на основе KPI
        if kpis.get('user_engagement_rate', 0) < 0.6:
            recommendations.append("Внедрить систему вознаграждений за активность пользователей")
            recommendations.append("Добавить социальные функции для увеличения вовлеченности")
        
        if kpis.get('test_completion_rate', 0) < 0.75:
            recommendations.append("Упростить наиболее сложные вопросы в тестах")
            recommendations.append("Добавить подсказки и объяснения в процессе тестирования")
        
        if kpis.get('retention_rate', 0) < 0.6:
            recommendations.append("Разработать программу удержания для новых пользователей")
            recommendations.append("Добавить персонализированные рекомендации")
        
        if kpis.get('premium_user_ratio', 0) < 0.15:
            recommendations.append("Улучшить премиум-функции и маркетинговые предложения")
            recommendations.append("Добавить ограниченные по времени премиум-функции для демонстрации ценности")
        
        if kpis.get('avg_satisfaction_score', 0) < 4.0:
            recommendations.append("Провести опрос пользователей для выявления проблем")
            recommendations.append("Улучшить интерфейс и пользовательский опыт")
        
        # Добавляем рекомендации из инсайтов
        for insight in insights:
            if "рекомендуется" in insight.lower():
                recommendations.append(insight.split("рекомендуется ")[1].capitalize())
        
        return recommendations
    
    def perform_comprehensive_analysis(self, db_connection) -> Dict[str, Any]:
        """
        Выполняет комплексный анализ системы.
        
        Args:
            db_connection: Подключение к базе данных
            
        Returns:
            dict: Полный результат анализа
        """
        try:
            # Загрузка данных
            user_data = self.load_user_data(db_connection)
            test_data = self.load_test_data(db_connection)
            
            if user_data.empty or test_data.empty:
                return {'error': 'Недостаточно данных для анализа'}
            
            # Расчет KPI
            kpis = self.calculate_kpi(user_data, test_data)
            
            # Анализ пользовательского поведения
            user_analysis = self.analyze_user_behavior(user_data)
            
            # Предсказание удержания
            retention_predictions = self.predict_user_retention(user_data)
            
            # Генерация инсайтов
            insights = self.generate_insights(kpis, user_analysis)
            
            # Генерация рекомендаций
            recommendations = self.generate_recommendations(kpis, insights)
            
            # Сбор результатов
            analysis_result = {
                'timestamp': datetime.now().isoformat(),
                'kpis': kpis,
                'user_analysis': user_analysis,
                'retention_predictions': retention_predictions,
                'insights': insights,
                'recommendations': recommendations,
                'data_quality': {
                    'user_records': len(user_data),
                    'test_records': len(test_data),
                    'date_range': {
                        'users_start': user_data['registration_date'].min().isoformat(),
                        'users_end': user_data['registration_date'].max().isoformat()
                    }
                }
            }
            
            # Сохраняем результат
            self.analysis_results.append(analysis_result)
            
            return analysis_result
            
        except Exception as e:
            self.logger.error(f"Ошибка при выполнении комплексного анализа: {str(e)}")
            return {'error': str(e)}
    
    def get_trend_analysis(self, historical_data: List[Dict]) -> Dict[str, Any]:
        """
        Выполняет анализ трендов на основе исторических данных.
        
        Args:
            historical_data: Исторические данные анализа
            
        Returns:
            dict: Результат анализа трендов
        """
        if not historical_data:
            return {}
        
        trends = {}
        
        # Собираем данные по ключевым метрикам
        metrics_over_time = defaultdict(list)
        timestamps = []
        
        for data_point in historical_data:
            if 'kpis' in data_point:
                kpis = data_point['kpis']
                for metric, value in kpis.items():
                    metrics_over_time[metric].append(value)
                timestamps.append(datetime.fromisoformat(data_point['timestamp']))
        
        # Анализ трендов для каждого метрика
        for metric, values in metrics_over_time.items():
            if len(values) < 2:
                continue
            
            # Простой анализ тренда (линейная регрессия)
            x = list(range(len(values)))
            y = values
            
            # Рассчитываем наклон
            if len(x) > 1:
                slope = np.polyfit(x, y, 1)[0]
                
                trend_direction = 'stable'
                if slope > 0.01:  # Порог для значимого изменения
                    trend_direction = 'increasing'
                elif slope < -0.01:
                    trend_direction = 'decreasing'
                
                trends[metric] = {
                    'slope': slope,
                    'direction': trend_direction,
                    'values': values,
                    'latest_value': values[-1],
                    'oldest_value': values[0]
                }
        
        return {
            'trends': trends,
            'analysis_period': {
                'start': min(timestamps).isoformat() if timestamps else None,
                'end': max(timestamps).isoformat() if timestamps else None
            }
        }
    
    def generate_dashboard_data(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Генерирует данные для дашборда.
        
        Args:
            analysis_result: Результат анализа
            
        Returns:
            dict: Данные для дашборда
        """
        if 'error' in analysis_result:
            return {'error': analysis_result['error']}
        
        kpis = analysis_result.get('kpis', {})
        insights = analysis_result.get('insights', [])
        recommendations = analysis_result.get('recommendations', [])
        
        # Подготавливаем основные метрики для дашборда
        dashboard_data = {
            'metrics': [
                {
                    'name': 'Вовлеченность пользователей',
                    'value': f"{kpis.get('user_engagement_rate', 0):.1%}",
                    'change': '+2.5%',  # В реальной системе это будет рассчитываться
                    'trend': 'up',
                    'threshold': self.kpi_thresholds.get(BusinessMetric.USER_ENGAGEMENT, 0.7)
                },
                {
                    'name': 'Уровень завершения тестов',
                    'value': f"{kpis.get('test_completion_rate', 0):.1%}",
                    'change': '-1.2%',
                    'trend': 'down',
                    'threshold': self.kpi_thresholds.get(BusinessMetric.TEST_COMPLETION_RATE, 0.8)
                },
                {
                    'name': 'Уровень удержания',
                    'value': f"{kpis.get('retention_rate', 0):.1%}",
                    'change': '+5.0%',
                    'trend': 'up',
                    'threshold': self.kpi_thresholds.get(BusinessMetric.RETENTION_RATE, 0.6)
                },
                {
                    'name': 'Конверсия',
                    'value': f"{kpis.get('conversion_rate', 0):.1%}",
                    'change': '+0.8%',
                    'trend': 'up',
                    'threshold': self.kpi_thresholds.get(BusinessMetric.CONVERSION_RATE, 0.05)
                },
                {
                    'name': 'Удовлетворенность',
                    'value': f"{kpis.get('avg_satisfaction_score', 0):.1f}/5",
                    'change': '+0.2',
                    'trend': 'up',
                    'threshold': self.kpi_thresholds.get(BusinessMetric.SATISFACTION_SCORE, 4.0)
                }
            ],
            'quick_insights': insights[:5],  # Первые 5 инсайтов
            'top_recommendations': recommendations[:3],  # Топ 3 рекомендации
            'risk_indicators': analysis_result.get('retention_predictions', {}).get('churn_risk_percentage', 0),
            'data_freshness': analysis_result['timestamp']
        }
        
        return dashboard_data
    
    def export_analysis_report(self, analysis_result: Dict[str, Any], format: str = 'json') -> str:
        """
        Экспортирует отчет анализа.
        
        Args:
            analysis_result: Результат анализа
            format: Формат экспорта (json, csv, excel)
            
        Returns:
            str: Путь к файлу отчета
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bi_report_{timestamp}.{format}"
            
            if format == 'json':
                import json
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(analysis_result, f, ensure_ascii=False, indent=2, default=str)
            elif format == 'csv':
                # Экспорт основных KPI в CSV
                kpis_df = pd.DataFrame([analysis_result.get('kpis', {})])
                kpis_df.to_csv(filename, index=False)
            elif format == 'excel':
                # Создание Excel файла с несколькими листами
                with pd.ExcelWriter(filename) as writer:
                    kpis_df = pd.DataFrame([analysis_result.get('kpis', {})])
                    kpis_df.to_excel(writer, sheet_name='KPIs', index=False)
                    
                    if 'insights' in analysis_result:
                        insights_df = pd.DataFrame(analysis_result['insights'], columns=['Insights'])
                        insights_df.to_excel(writer, sheet_name='Insights', index=False)
                    
                    if 'recommendations' in analysis_result:
                        rec_df = pd.DataFrame(analysis_result['recommendations'], columns=['Recommendations'])
                        rec_df.to_excel(writer, sheet_name='Recommendations', index=False)
            
            return filename
            
        except Exception as e:
            self.logger.error(f"Ошибка при экспорте отчета: {str(e)}")
            return ""


# Глобальный экземпляр движка бизнес-аналитики
bi_engine = BusinessIntelligenceEngine()