# -*- coding: utf-8 -*-
"""
Модуль расширенной системы бизнес-интеллекта для ПрофиТест
Предоставляет продвинутые аналитические возможности и прогнозирование
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Set, Any, Tuple
import logging
from dataclasses import dataclass, field
from collections import defaultdict
import json
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns


class AnalysisType(Enum):
    """Типы аналитики"""
    USER_BEHAVIOR = 'user_behavior'
    CONTENT_PERFORMANCE = 'content_performance'
    MARKET_TRENDS = 'market_trends'
    PREDICTIVE_ANALYTICS = 'predictive_analytics'
    ANOMALY_DETECTION = 'anomaly_detection'
    SEGMENTATION = 'segmentation'


class TimePeriod(Enum):
    """Периоды времени для анализа"""
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    QUARTERLY = 'quarterly'
    YEARLY = 'yearly'


@dataclass
class AnalyticsReport:
    """Аналитический отчет"""
    id: str
    title: str
    analysis_type: AnalysisType
    period: TimePeriod
    data: Dict[str, Any]
    insights: List[str]
    recommendations: List[str]
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UserSegment:
    """Сегмент пользователей"""
    id: str
    name: str
    description: str
    user_ids: List[int]
    characteristics: Dict[str, Any]
    size: int
    created_at: datetime = field(default_factory=datetime.now)


class BusinessIntelligenceEngine:
    """
    Расширенный движок бизнес-интеллекта для системы ПрофиТест.
    Обеспечивает комплексную аналитику и прогнозирование.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.analytics_reports: Dict[str, AnalyticsReport] = {}
        self.user_segments: Dict[str, UserSegment] = {}
        self.historical_data: Dict[str, pd.DataFrame] = {}
        self.models: Dict[str, Any] = {}
        
        # Инициализация моделей машинного обучения
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=0.95)  # Сохраняем 95% дисперсии
        
        # Инициализация системных данных
        self._initialize_system_data()
    
    def _initialize_system_data(self):
        """Инициализирует системные данные для аналитики."""
        # Создаем тестовые исторические данные
        self._generate_sample_historical_data()
        # Обучаем базовые модели
        self._train_base_models()
    
    def _generate_sample_historical_data(self):
        """Генерирует тестовые исторические данные."""
        # Данные по пользователям
        dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
        
        # Активность пользователей
        user_activity_data = {
            'date': dates,
            'active_users': np.random.poisson(150, len(dates)),
            'new_users': np.random.poisson(25, len(dates)),
            'test_completions': np.random.poisson(80, len(dates)),
            'content_views': np.random.poisson(300, len(dates)),
            'avg_session_duration': np.random.normal(15, 5, len(dates))
        }
        self.historical_data['user_activity'] = pd.DataFrame(user_activity_data)
        
        # Данные по контенту
        content_performance_data = {
            'date': dates,
            'test_views': np.random.poisson(120, len(dates)),
            'article_views': np.random.poisson(90, len(dates)),
            'video_views': np.random.poisson(60, len(dates)),
            'avg_rating': np.random.normal(4.2, 0.3, len(dates)),
            'completion_rate': np.random.beta(8, 2, len(dates))
        }
        self.historical_data['content_performance'] = pd.DataFrame(content_performance_data)
        
        # Рыночные данные
        market_data = {
            'date': dates,
            'job_vacancies': np.random.poisson(200, len(dates)),
            'salary_trends': np.random.normal(60000, 10000, len(dates)),
            'demand_index': np.random.beta(7, 3, len(dates))
        }
        self.historical_data['market_trends'] = pd.DataFrame(market_data)
    
    def _train_base_models(self):
        """Обучает базовые модели машинного обучения."""
        try:
            # Модель для прогнозирования активности пользователей
            if 'user_activity' in self.historical_data:
                df = self.historical_data['user_activity']
                X = df[['date']].copy()
                X['day_of_week'] = X['date'].dt.dayofweek
                X['day_of_month'] = X['date'].dt.day
                X['month'] = X['date'].dt.month
                X = X.drop('date', axis=1)
                
                y = df['active_users']
                
                # Нормализация
                X_scaled = self.scaler.fit_transform(X)
                
                # Обучение модели
                rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
                rf_model.fit(X_scaled, y)
                self.models['user_activity_forecast'] = rf_model
                
                self.logger.info("Базовые модели машинного обучения обучены")
            
        except Exception as e:
            self.logger.error(f"Ошибка при обучении базовых моделей: {str(e)}")
    
    def analyze_user_behavior(self, period: TimePeriod = TimePeriod.MONTHLY, 
                            start_date: datetime = None, end_date: datetime = None) -> AnalyticsReport:
        """
        Анализирует поведение пользователей.
        
        Args:
            period: Период анализа
            start_date: Начальная дата
            end_date: Конечная дата
            
        Returns:
            AnalyticsReport: Аналитический отчет
        """
        try:
            import uuid
            report_id = str(uuid.uuid4())
            
            # Получаем данные
            df = self.historical_data.get('user_activity', pd.DataFrame())
            if df.empty:
                raise ValueError("Нет данных для анализа поведения пользователей")
            
            # Фильтруем по датам
            if start_date:
                df = df[df['date'] >= start_date]
            if end_date:
                df = df[df['date'] <= end_date]
            
            # Агрегируем данные по периоду
            if period == TimePeriod.DAILY:
                df_grouped = df
            elif period == TimePeriod.WEEKLY:
                df_grouped = df.resample('W', on='date').mean()
            elif period == TimePeriod.MONTHLY:
                df_grouped = df.resample('M', on='date').mean()
            else:
                df_grouped = df.resample('Q', on='date').mean()
            
            # Рассчитываем метрики
            metrics = {
                'total_active_users': int(df['active_users'].sum()),
                'avg_daily_active_users': float(df['active_users'].mean()),
                'user_growth_rate': float((df['new_users'].sum() / df['active_users'].sum()) * 100),
                'avg_session_duration': float(df['avg_session_duration'].mean()),
                'total_test_completions': int(df['test_completions'].sum()),
                'completion_rate': float((df['test_completions'].sum() / df['content_views'].sum()) * 100)
            }
            
            # Определяем инсайты
            insights = self._generate_user_behavior_insights(df, metrics)
            
            # Генерируем рекомендации
            recommendations = self._generate_user_behavior_recommendations(metrics, insights)
            
            report = AnalyticsReport(
                id=report_id,
                title=f'Анализ поведения пользователей ({period.value})',
                analysis_type=AnalysisType.USER_BEHAVIOR,
                period=period,
                data={
                    'metrics': metrics,
                    'trends': self._calculate_trends(df),
                    'user_segments': self._identify_user_segments(df)
                },
                insights=insights,
                recommendations=recommendations,
                metadata={
                    'data_points': len(df),
                    'date_range': {
                        'start': df['date'].min().isoformat(),
                        'end': df['date'].max().isoformat()
                    }
                }
            )
            
            self.analytics_reports[report_id] = report
            return report
            
        except Exception as e:
            self.logger.error(f"Ошибка при анализе поведения пользователей: {str(e)}")
            raise
    
    def _generate_user_behavior_insights(self, df: pd.DataFrame, metrics: Dict[str, Any]) -> List[str]:
        """Генерирует инсайты по поведению пользователей."""
        insights = []
        
        # Анализ роста
        if metrics['user_growth_rate'] > 10:
            insights.append("Высокий темп роста пользовательской базы")
        elif metrics['user_growth_rate'] < 2:
            insights.append("Низкий темп роста пользовательской базы")
        
        # Анализ вовлеченности
        if metrics['avg_session_duration'] > 20:
            insights.append("Высокий уровень вовлеченности пользователей")
        elif metrics['avg_session_duration'] < 10:
            insights.append("Низкий уровень вовлеченности пользователей")
        
        # Анализ завершения тестов
        if metrics['completion_rate'] > 70:
            insights.append("Высокий процент завершения тестов")
        elif metrics['completion_rate'] < 40:
            insights.append("Низкий процент завершения тестов")
        
        # Анализ сезонности
        daily_pattern = df.groupby(df['date'].dt.dayofweek)['active_users'].mean()
        if daily_pattern.max() / daily_pattern.min() > 2:
            insights.append("Выраженная недельная сезонность активности")
        
        return insights
    
    def _generate_user_behavior_recommendations(self, metrics: Dict[str, Any], 
                                              insights: List[str]) -> List[str]:
        """Генерирует рекомендации по поведению пользователей."""
        recommendations = []
        
        if metrics['user_growth_rate'] < 5:
            recommendations.append("Рассмотрите усиление маркетинговых активностей")
            recommendations.append("Оптимизируйте процессы регистрации")
        
        if metrics['avg_session_duration'] < 15:
            recommendations.append("Улучшите пользовательский интерфейс")
            recommendations.append("Добавьте больше интерактивного контента")
        
        if metrics['completion_rate'] < 50:
            recommendations.append("Оптимизируйте длину тестов")
            recommendations.append("Добавьте мотивационные элементы")
        
        if "Выраженная недельная сезонность" in str(insights):
            recommendations.append("Планируйте контент с учетом недельных паттернов")
        
        return recommendations
    
    def analyze_content_performance(self, content_type: str = None) -> AnalyticsReport:
        """
        Анализирует эффективность контента.
        
        Args:
            content_type: Тип контента для анализа
            
        Returns:
            AnalyticsReport: Аналитический отчет
        """
        try:
            import uuid
            report_id = str(uuid.uuid4())
            
            df = self.historical_data.get('content_performance', pd.DataFrame())
            if df.empty:
                raise ValueError("Нет данных для анализа эффективности контента")
            
            # Фильтруем по типу контента
            if content_type:
                if content_type == 'test':
                    views_column = 'test_views'
                elif content_type == 'article':
                    views_column = 'article_views'
                elif content_type == 'video':
                    views_column = 'video_views'
                else:
                    views_column = 'test_views'
            else:
                views_column = 'test_views'  # По умолчанию
            
            # Рассчитываем метрики
            metrics = {
                'total_views': int(df[views_column].sum()),
                'avg_views': float(df[views_column].mean()),
                'avg_rating': float(df['avg_rating'].mean()),
                'completion_rate': float(df['completion_rate'].mean() * 100),
                'engagement_score': float((df[views_column] * df['avg_rating'] * df['completion_rate']).mean())
            }
            
            # Определяем инсайты
            insights = self._generate_content_insights(df, metrics, content_type)
            
            # Генерируем рекомендации
            recommendations = self._generate_content_recommendations(metrics, insights)
            
            report = AnalyticsReport(
                id=report_id,
                title=f'Анализ эффективности контента ({content_type or "все типы"})',
                analysis_type=AnalysisType.CONTENT_PERFORMANCE,
                period=TimePeriod.MONTHLY,
                data={
                    'metrics': metrics,
                    'performance_trends': self._calculate_content_trends(df, views_column),
                    'rating_distribution': self._calculate_rating_distribution(df)
                },
                insights=insights,
                recommendations=recommendations,
                metadata={
                    'content_type': content_type,
                    'data_points': len(df)
                }
            )
            
            self.analytics_reports[report_id] = report
            return report
            
        except Exception as e:
            self.logger.error(f"Ошибка при анализе эффективности контента: {str(e)}")
            raise
    
    def _generate_content_insights(self, df: pd.DataFrame, metrics: Dict[str, Any], 
                                 content_type: str) -> List[str]:
        """Генерирует инсайты по контенту."""
        insights = []
        
        if metrics['avg_rating'] > 4.5:
            insights.append("Высокое качество контента")
        elif metrics['avg_rating'] < 3.5:
            insights.append("Низкое качество контента")
        
        if metrics['completion_rate'] > 80:
            insights.append("Высокий уровень вовлеченности в контент")
        elif metrics['completion_rate'] < 50:
            insights.append("Низкий уровень завершения контента")
        
        if metrics['engagement_score'] > 1000:
            insights.append("Высокая общая вовлеченность")
        
        # Анализ трендов
        recent_data = df.tail(30)
        old_data = df.head(30)
        
        if recent_data['avg_rating'].mean() > old_data['avg_rating'].mean() * 1.1:
            insights.append("Улучшение качества контента во времени")
        elif recent_data['avg_rating'].mean() < old_data['avg_rating'].mean() * 0.9:
            insights.append("Ухудшение качества контента во времени")
        
        return insights
    
    def _generate_content_recommendations(self, metrics: Dict[str, Any], 
                                        insights: List[str]) -> List[str]:
        """Генерирует рекомендации по контенту."""
        recommendations = []
        
        if metrics['avg_rating'] < 4.0:
            recommendations.append("Проведите аудит качества контента")
            recommendations.append("Соберите обратную связь от пользователей")
        
        if metrics['completion_rate'] < 60:
            recommendations.append("Оптимизируйте структуру контента")
            recommendations.append("Добавьте интерактивные элементы")
        
        if "Ухудшение качества" in str(insights):
            recommendations.append("Проанализируйте причины снижения качества")
            recommendations.append("Внедрите систему контроля качества")
        
        return recommendations
    
    def forecast_user_activity(self, days_ahead: int = 30) -> Dict[str, Any]:
        """
        Прогнозирует активность пользователей.
        
        Args:
            days_ahead: Количество дней для прогноза
            
        Returns:
            dict: Прогноз активности
        """
        try:
            if 'user_activity_forecast' not in self.models:
                raise ValueError("Модель прогнозирования не обучена")
            
            model = self.models['user_activity_forecast']
            
            # Генерируем даты для прогноза
            last_date = self.historical_data['user_activity']['date'].max()
            future_dates = pd.date_range(start=last_date + timedelta(days=1), 
                                       periods=days_ahead, freq='D')
            
            # Подготавливаем признаки
            X_future = pd.DataFrame({
                'day_of_week': future_dates.dayofweek,
                'day_of_month': future_dates.day,
                'month': future_dates.month
            })
            
            # Нормализуем
            X_future_scaled = self.scaler.transform(X_future)
            
            # Делаем прогноз
            predictions = model.predict(X_future_scaled)
            
            # Рассчитываем доверительные интервалы
            std_prediction = np.std(predictions)
            confidence_lower = predictions - 1.96 * std_prediction
            confidence_upper = predictions + 1.96 * std_prediction
            
            forecast_data = {
                'dates': future_dates.tolist(),
                'predictions': predictions.tolist(),
                'confidence_lower': confidence_lower.tolist(),
                'confidence_upper': confidence_upper.tolist(),
                'total_predicted_users': int(sum(predictions)),
                'avg_predicted_users': float(np.mean(predictions))
            }
            
            return forecast_data
            
        except Exception as e:
            self.logger.error(f"Ошибка при прогнозировании активности: {str(e)}")
            raise
    
    def detect_anomalies(self, data_type: str = 'user_activity') -> List[Dict[str, Any]]:
        """
        Обнаруживает аномалии в данных.
        
        Args:
            data_type: Тип данных для анализа
            
        Returns:
            list: Список обнаруженных аномалий
        """
        try:
            df = self.historical_data.get(data_type)
            if df is None:
                raise ValueError(f"Нет данных типа {data_type}")
            
            # Выбираем числовые колонки для анализа
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            if 'date' in numeric_columns:
                numeric_columns.remove('date')
            
            anomalies = []
            
            for column in numeric_columns:
                # Используем Isolation Forest для обнаружения аномалий
                iso_forest = IsolationForest(contamination=0.1, random_state=42)
                anomaly_scores = iso_forest.fit_predict(df[[column]])
                
                # Находим аномальные точки
                anomaly_indices = np.where(anomaly_scores == -1)[0]
                
                for idx in anomaly_indices:
                    anomalies.append({
                        'date': df.iloc[idx]['date'].isoformat(),
                        'metric': column,
                        'value': float(df.iloc[idx][column]),
                        'anomaly_score': float(iso_forest.decision_function(df[[column]])[idx]),
                        'type': 'statistical_anomaly'
                    })
            
            return anomalies
            
        except Exception as e:
            self.logger.error(f"Ошибка при обнаружении аномалий: {str(e)}")
            raise
    
    def segment_users(self, n_segments: int = 5) -> List[UserSegment]:
        """
        Сегментирует пользователей на основе их поведения.
        
        Args:
            n_segments: Количество сегментов
            
        Returns:
            list: Список сегментов пользователей
        """
        try:
            df = self.historical_data.get('user_activity', pd.DataFrame())
            if df.empty:
                raise ValueError("Нет данных для сегментации")
            
            # Подготавливаем данные для кластеризации
            user_features = df[['active_users', 'new_users', 'test_completions', 'avg_session_duration']].copy()
            
            # Нормализуем данные
            features_scaled = self.scaler.fit_transform(user_features)
            
            # Применяем PCA для снижения размерности
            features_pca = self.pca.fit_transform(features_scaled)
            
            # Кластеризуем
            kmeans = KMeans(n_clusters=n_segments, random_state=42)
            cluster_labels = kmeans.fit_predict(features_pca)
            
            # Создаем сегменты
            segments = []
            for i in range(n_segments):
                segment_indices = np.where(cluster_labels == i)[0]
                segment_data = df.iloc[segment_indices]
                
                segment = UserSegment(
                    id=f'segment_{i}',
                    name=f'Сегмент {i+1}',
                    description=self._generate_segment_description(segment_data),
                    user_ids=[],  # В реальной системе здесь будут реальные ID
                    characteristics={
                        'size': len(segment_data),
                        'avg_active_users': float(segment_data['active_users'].mean()),
                        'avg_session_duration': float(segment_data['avg_session_duration'].mean()),
                        'avg_test_completions': float(segment_data['test_completions'].mean())
                    },
                    size=len(segment_data)
                )
                
                segments.append(segment)
                self.user_segments[segment.id] = segment
            
            return segments
            
        except Exception as e:
            self.logger.error(f"Ошибка при сегментации пользователей: {str(e)}")
            raise
    
    def _generate_segment_description(self, segment_data: pd.DataFrame) -> str:
        """Генерирует описание сегмента."""
        avg_users = segment_data['active_users'].mean()
        avg_duration = segment_data['avg_session_duration'].mean()
        avg_completions = segment_data['test_completions'].mean()
        
        if avg_users > 200 and avg_duration > 20:
            return "Высокоактивные, вовлеченные пользователи"
        elif avg_users > 200 and avg_duration < 10:
            return "Высокоактивные, но малововлеченные пользователи"
        elif avg_users < 100 and avg_duration > 20:
            return "Низкоактивные, но вовлеченные пользователи"
        else:
            return "Низкоактивные, малововлеченные пользователи"
    
    def get_analytics_report(self, report_id: str) -> AnalyticsReport:
        """
        Получает аналитический отчет по ID.
        
        Args:
            report_id: ID отчета
            
        Returns:
            AnalyticsReport: Аналитический отчет
        """
        return self.analytics_reports.get(report_id)
    
    def get_all_reports(self) -> List[AnalyticsReport]:
        """
        Получает все аналитические отчеты.
        
        Returns:
            list: Список всех отчетов
        """
        return list(self.analytics_reports.values())
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Получает статистику по аналитике.
        
        Returns:
            dict: Статистика системы
        """
        return {
            'total_reports': len(self.analytics_reports),
            'reports_by_type': dict(pd.Series([r.analysis_type.value for r in self.analytics_reports.values()]).value_counts()),
            'total_segments': len(self.user_segments),
            'available_data_sources': list(self.historical_data.keys()),
            'trained_models': list(self.models.keys())
        }
    
    def _calculate_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Рассчитывает тренды."""
        trends = {}
        
        for column in ['active_users', 'new_users', 'test_completions']:
            if column in df.columns:
                # Линейный тренд
                x = np.arange(len(df))
                y = df[column].values
                slope = np.polyfit(x, y, 1)[0]
                
                trends[column] = {
                    'slope': float(slope),
                    'direction': 'increasing' if slope > 0 else 'decreasing',
                    'magnitude': abs(float(slope))
                }
        
        return trends
    
    def _calculate_content_trends(self, df: pd.DataFrame, views_column: str) -> Dict[str, Any]:
        """Рассчитывает тренды по контенту."""
        # Анализируем тренд просмотров
        x = np.arange(len(df))
        y = df[views_column].values
        slope = np.polyfit(x, y, 1)[0]
        
        return {
            'views_trend': {
                'slope': float(slope),
                'direction': 'increasing' if slope > 0 else 'decreasing'
            },
            'rating_trend': {
                'slope': float(np.polyfit(x, df['avg_rating'].values, 1)[0]),
                'direction': 'increasing' if np.polyfit(x, df['avg_rating'].values, 1)[0] > 0 else 'decreasing'
            }
        }
    
    def _calculate_rating_distribution(self, df: pd.DataFrame) -> Dict[str, int]:
        """Рассчитывает распределение рейтингов."""
        ratings = df['avg_rating'].round(1)
        return ratings.value_counts().to_dict()
    
    def _identify_user_segments(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Идентифицирует сегменты пользователей."""
        # Простая сегментация по активности
        high_activity = df[df['active_users'] > df['active_users'].quantile(0.75)]
        medium_activity = df[(df['active_users'] > df['active_users'].quantile(0.25)) & 
                           (df['active_users'] <= df['active_users'].quantile(0.75))]
        low_activity = df[df['active_users'] <= df['active_users'].quantile(0.25)]
        
        return [
            {'segment': 'high_activity', 'count': len(high_activity), 'percentage': len(high_activity)/len(df)*100},
            {'segment': 'medium_activity', 'count': len(medium_activity), 'percentage': len(medium_activity)/len(df)*100},
            {'segment': 'low_activity', 'count': len(low_activity), 'percentage': len(low_activity)/len(df)*100}
        ]


# Глобальный экземпляр движка бизнес-интеллекта
bi_engine_v2 = BusinessIntelligenceEngine()