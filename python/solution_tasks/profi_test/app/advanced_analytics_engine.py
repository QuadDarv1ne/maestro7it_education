# -*- coding: utf-8 -*-
"""
Модуль продвинутой аналитики и бизнес-интеллекта для ПрофиТест
Обеспечивает комплексный анализ данных, визуализацию и бизнес-аналитику
"""
import logging
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from collections import defaultdict, Counter
import json
import time
from dataclasses import dataclass
import threading
from enum import Enum
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class AnalyticsCategory(Enum):
    """Категории аналитики"""
    USER_ENGAGEMENT = "user_engagement"
    TEST_PERFORMANCE = "test_performance"
    CAREER_INSIGHTS = "career_insights"
    SYSTEM_METRICS = "system_metrics"
    BUSINESS_INTELLIGENCE = "business_intelligence"

@dataclass
class AnalyticsReport:
    """Отчет аналитики"""
    report_id: str
    category: AnalyticsCategory
    generated_at: str
    data: Dict[str, Any]
    charts: List[Dict[str, str]]
    insights: List[str]
    recommendations: List[str]

class AdvancedAnalyticsEngine:
    """Продвинутый движок аналитики с BI-возможностями"""
    
    def __init__(self, app=None):
        self.app = app
        self.analytics_data = {}
        self.reports_history = []
        self.dashboards = {}
        self.clustering_models = {}
        self.scalers = {}
        self.analytics_cache = {}
        self.lock = threading.Lock()
        
        # Конфигурация аналитики
        self.config = {
            'data_retention_days': 365,
            'cache_duration_minutes': 60,
            'clustering': {
                'n_clusters': 5,
                'max_iterations': 300
            },
            'visualization': {
                'chart_width': 1200,
                'chart_height': 800,
                'color_scheme': 'viridis'
            },
            'insights': {
                'trend_analysis_days': 30,
                'anomaly_detection_threshold': 2.0,
                'correlation_analysis': True
            }
        }
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация с Flask приложением"""
        self.app = app
        logger.info("Продвинутый движок аналитики инициализирован")
    
    def generate_user_engagement_report(self, start_date: str, end_date: str) -> AnalyticsReport:
        """Генерация отчета по вовлеченности пользователей"""
        # В реальном приложении здесь будут запросы к базе данных
        # Для демонстрации используем симуляцию данных
        
        # Симуляция данных
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        daily_users = np.random.randint(50, 200, len(dates))
        daily_sessions = daily_users * np.random.uniform(1.2, 2.5, len(dates))
        avg_session_duration = np.random.uniform(15, 45, len(dates))  # минуты
        test_completions = daily_users * np.random.uniform(0.3, 0.8, len(dates))
        
        df = pd.DataFrame({
            'date': dates,
            'daily_users': daily_users,
            'daily_sessions': daily_sessions,
            'avg_session_duration': avg_session_duration,
            'test_completions': test_completions
        })
        
        # Рассчет метрик
        total_users = df['daily_users'].sum()
        avg_daily_users = df['daily_users'].mean()
        avg_session_duration = df['avg_session_duration'].mean()
        completion_rate = df['test_completions'].sum() / df['daily_users'].sum()
        
        # Визуализация
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Ежедневные пользователи', 'Продолжительность сессии', 
                          'Завершенные тесты', 'Коэффициент завершения'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        fig.add_trace(go.Scatter(x=df['date'], y=df['daily_users'], name='Дневные пользователи'), row=1, col=1)
        fig.add_trace(go.Scatter(x=df['date'], y=df['avg_session_duration'], name='Средняя продолжительность'), row=1, col=2)
        fig.add_trace(go.Bar(x=df['date'], y=df['test_completions'], name='Завершенные тесты'), row=2, col=1)
        fig.add_trace(go.Scatter(x=df['date'], y=df['test_completions']/df['daily_users']*100, name='Коэффициент (%)'), row=2, col=2)
        
        fig.update_layout(height=800, showlegend=True, title_text="Аналитика вовлеченности пользователей")
        
        # Инсайты
        insights = [
            f"Среднее количество ежедневных пользователей: {avg_daily_users:.1f}",
            f"Средняя продолжительность сессии: {avg_session_duration:.1f} минут",
            f"Коэффициент завершения тестов: {completion_rate:.2%}",
            f"Общее количество уникальных пользователей: {total_users}"
        ]
        
        # Рекомендации
        recommendations = []
        if avg_session_duration < 20:
            recommendations.append("Увеличить продолжительность сессии пользователей")
        if completion_rate < 0.5:
            recommendations.append("Улучшить коэффициент завершения тестов")
        
        report_data = {
            'summary': {
                'total_users': int(total_users),
                'avg_daily_users': float(avg_daily_users),
                'avg_session_duration': float(avg_session_duration),
                'completion_rate': float(completion_rate)
            },
            'daily_data': df.to_dict('records')
        }
        
        report = AnalyticsReport(
            report_id=f"user_engagement_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            category=AnalyticsCategory.USER_ENGAGEMENT,
            generated_at=datetime.utcnow().isoformat(),
            data=report_data,
            charts=[{'type': 'engagement_dashboard', 'figure': fig.to_json()}],
            insights=insights,
            recommendations=recommendations
        )
        
        return report
    
    def generate_test_performance_report(self, start_date: str, end_date: str) -> AnalyticsReport:
        """Генерация отчета по производительности тестов"""
        # Симуляция данных тестов
        test_types = ['holland', 'klimov', 'personality', 'skills', 'interests']
        test_data = []
        
        for test_type in test_types:
            for day in pd.date_range(start=start_date, end=end_date, freq='D'):
                test_data.append({
                    'date': day,
                    'test_type': test_type,
                    'attempts': np.random.randint(10, 50),
                    'completions': np.random.randint(5, 40),
                    'avg_completion_time': np.random.uniform(10, 45),
                    'success_rate': np.random.uniform(0.6, 0.95)
                })
        
        df = pd.DataFrame(test_data)
        
        # Агрегация данных
        agg_data = df.groupby('test_type').agg({
            'attempts': 'sum',
            'completions': 'sum',
            'avg_completion_time': 'mean',
            'success_rate': 'mean'
        }).reset_index()
        
        # Визуализация
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Количество попыток', 'Коэффициент успеха', 
                          'Среднее время завершения', 'Типы тестов'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        fig.add_trace(go.Bar(x=agg_data['test_type'], y=agg_data['attempts'], name='Попытки'), row=1, col=1)
        fig.add_trace(go.Bar(x=agg_data['test_type'], y=agg_data['success_rate'], name='Успех'), row=1, col=2)
        fig.add_trace(go.Bar(x=agg_data['test_type'], y=agg_data['avg_completion_time'], name='Время'), row=2, col=1)
        fig.add_trace(go.Pie(labels=agg_data['test_type'], values=agg_data['completions'], name='Завершенные'), row=2, col=2)
        
        fig.update_layout(height=800, showlegend=True, title_text="Аналитика производительности тестов")
        
        # Инсайты
        insights = [
            f"Всего попыток тестов: {agg_data['attempts'].sum()}",
            f"Средний коэффициент успеха: {agg_data['success_rate'].mean():.2%}",
            f"Среднее время завершения: {agg_data['avg_completion_time'].mean():.1f} мин",
            f"Самый популярный тест: {agg_data.loc[agg_data['attempts'].idxmax(), 'test_type']}"
        ]
        
        # Рекомендации
        recommendations = []
        low_success_tests = agg_data[agg_data['success_rate'] < 0.7]['test_type'].tolist()
        if low_success_tests:
            recommendations.append(f"Улучшить тесты с низким коэффициентом успеха: {', '.join(low_success_tests)}")
        
        report_data = {
            'summary': {
                'total_attempts': int(agg_data['attempts'].sum()),
                'avg_success_rate': float(agg_data['success_rate'].mean()),
                'avg_completion_time': float(agg_data['avg_completion_time'].mean())
            },
            'by_test_type': agg_data.to_dict('records')
        }
        
        report = AnalyticsReport(
            report_id=f"test_performance_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            category=AnalyticsCategory.TEST_PERFORMANCE,
            generated_at=datetime.utcnow().isoformat(),
            data=report_data,
            charts=[{'type': 'test_performance_dashboard', 'figure': fig.to_json()}],
            insights=insights,
            recommendations=recommendations
        )
        
        return report
    
    def generate_career_insights_report(self, start_date: str, end_date: str) -> AnalyticsReport:
        """Генерация отчета по карьерным инсайтам"""
        # Симуляция данных карьерного анализа
        career_fields = ['IT', 'Finance', 'Marketing', 'Engineering', 'Healthcare', 'Education', 'Legal', 'Creative']
        
        career_data = []
        for field in career_fields:
            for day in pd.date_range(start=start_date, end=end_date, freq='D'):
                career_data.append({
                    'date': day,
                    'field': field,
                    'interest_score': np.random.uniform(3.0, 9.0),
                    'match_count': np.random.randint(5, 50),
                    'recommendation_clicks': np.random.randint(2, 30),
                    'conversion_rate': np.random.uniform(0.1, 0.4)
                })
        
        df = pd.DataFrame(career_data)
        
        # Агрегация
        field_summary = df.groupby('field').agg({
            'interest_score': 'mean',
            'match_count': 'sum',
            'recommendation_clicks': 'sum',
            'conversion_rate': 'mean'
        }).reset_index()
        
        # Кластеризация карьерных направлений
        features = ['interest_score', 'match_count', 'recommendation_clicks', 'conversion_rate']
        X = df[features].values
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        kmeans = KMeans(n_clusters=3, random_state=42)
        clusters = kmeans.fit_predict(X_scaled)
        df['cluster'] = clusters
        
        # Визуализация
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Интерес по направлениям', 'Конверсии', 
                          'Кластеризация направлений', 'Рекомендации'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        fig.add_trace(go.Bar(x=field_summary['field'], y=field_summary['interest_score'], name='Интерес'), row=1, col=1)
        fig.add_trace(go.Bar(x=field_summary['field'], y=field_summary['conversion_rate'], name='Конверсия'), row=1, col=2)
        fig.add_trace(go.Scatter(x=df['interest_score'], y=df['conversion_rate'], 
                                mode='markers', marker=dict(color=df['cluster']), 
                                name='Кластеры'), row=2, col=1)
        fig.add_trace(go.Bar(x=field_summary['field'], y=field_summary['recommendation_clicks'], name='Клики'), row=2, col=2)
        
        fig.update_layout(height=800, showlegend=True, title_text="Аналитика карьерных инсайтов")
        
        # Инсайты
        top_field = field_summary.loc[field_summary['interest_score'].idxmax(), 'field']
        best_conversion = field_summary.loc[field_summary['conversion_rate'].idxmax(), 'field']
        
        insights = [
            f"Наиболее интересное направление: {top_field} (средний балл: {field_summary['interest_score'].max():.2f})",
            f"Лучшая конверсия в: {best_conversion} ({field_summary['conversion_rate'].max():.2%})",
            f"Всего рекомендаций: {field_summary['recommendation_clicks'].sum()}",
            f"Средний уровень интереса: {field_summary['interest_score'].mean():.2f}"
        ]
        
        # Рекомендации
        recommendations = [
            f"Сфокусироваться на развитии направления {top_field}",
            f"Анализировать факторы успеха в {best_conversion} для применения в других направлениях"
        ]
        
        report_data = {
            'summary': {
                'top_interest_field': top_field,
                'best_conversion_field': best_conversion,
                'total_recommendations': int(field_summary['recommendation_clicks'].sum()),
                'avg_interest': float(field_summary['interest_score'].mean())
            },
            'by_field': field_summary.to_dict('records'),
            'clusters': df.groupby('cluster')[features].mean().to_dict('records')
        }
        
        report = AnalyticsReport(
            report_id=f"career_insights_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            category=AnalyticsCategory.CAREER_INSIGHTS,
            generated_at=datetime.utcnow().isoformat(),
            data=report_data,
            charts=[{'type': 'career_insights_dashboard', 'figure': fig.to_json()}],
            insights=insights,
            recommendations=recommendations
        )
        
        return report
    
    def generate_business_intelligence_report(self, start_date: str, end_date: str) -> AnalyticsReport:
        """Генерация отчета бизнес-интеллекта"""
        # Комплексный отчет с различными метриками
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Симуляция бизнес-метрик
        metrics = {
            'date': dates,
            'revenue': np.random.uniform(1000, 5000, len(dates)),  # условные единицы
            'new_users': np.random.randint(20, 100, len(dates)),
            'churn_rate': np.random.uniform(0.02, 0.15, len(dates)),
            'customer_lifetime_value': np.random.uniform(50, 200, len(dates)),
            'support_tickets': np.random.randint(5, 25, len(dates)),
            'satisfaction_score': np.random.uniform(3.5, 4.8, len(dates))  # из 5
        }
        
        df = pd.DataFrame(metrics)
        
        # Расчет дополнительных метрик
        df['revenue_growth'] = df['revenue'].pct_change() * 100
        df['user_acquisition_cost'] = df['revenue'] / df['new_users']
        
        # Визуализация
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=('Доход', 'Новые пользователи', 'Отток', 
                          'CLV', 'Обращения в поддержку', 'Удовлетворенность'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        fig.add_trace(go.Scatter(x=df['date'], y=df['revenue'], name='Доход'), row=1, col=1)
        fig.add_trace(go.Scatter(x=df['date'], y=df['new_users'], name='Новые пользователи'), row=1, col=2)
        fig.add_trace(go.Scatter(x=df['date'], y=df['churn_rate'], name='Отток'), row=2, col=1)
        fig.add_trace(go.Scatter(x=df['date'], y=df['customer_lifetime_value'], name='CLV'), row=2, col=2)
        fig.add_trace(go.Scatter(x=df['date'], y=df['support_tickets'], name='Обращения'), row=3, col=1)
        fig.add_trace(go.Scatter(x=df['date'], y=df['satisfaction_score'], name='Удовлетворенность'), row=3, col=2)
        
        fig.update_layout(height=1200, showlegend=True, title_text="Бизнес-аналитика")
        
        # Инсайты
        avg_revenue = df['revenue'].mean()
        avg_churn = df['churn_rate'].mean()
        avg_clv = df['customer_lifetime_value'].mean()
        avg_satisfaction = df['satisfaction_score'].mean()
        
        insights = [
            f"Средний доход: {avg_revenue:.2f} у.е.",
            f"Средний уровень оттока: {avg_churn:.2%}",
            f"Средний CLV: {avg_clv:.2f} у.е.",
            f"Средняя удовлетворенность: {avg_satisfaction:.2f}/5.0",
            f"Всего новых пользователей: {df['new_users'].sum()}"
        ]
        
        # Рекомендации
        recommendations = []
        if avg_churn > 0.1:
            recommendations.append("Принять меры по снижению уровня оттока")
        if avg_satisfaction < 4.0:
            recommendations.append("Улучшить качество сервиса для повышения удовлетворенности")
        
        report_data = {
            'summary': {
                'avg_revenue': float(avg_revenue),
                'avg_churn_rate': float(avg_churn),
                'avg_clv': float(avg_clv),
                'avg_satisfaction': float(avg_satisfaction),
                'total_new_users': int(df['new_users'].sum())
            },
            'daily_metrics': df.to_dict('records')
        }
        
        report = AnalyticsReport(
            report_id=f"business_intelligence_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            category=AnalyticsCategory.BUSINESS_INTELLIGENCE,
            generated_at=datetime.utcnow().isoformat(),
            data=report_data,
            charts=[{'type': 'business_intelligence_dashboard', 'figure': fig.to_json()}],
            insights=insights,
            recommendations=recommendations
        )
        
        return report
    
    def generate_comprehensive_dashboard(self) -> Dict[str, Any]:
        """Генерация комплексной панели управления"""
        # Получение всех типов отчетов
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        reports = {
            'user_engagement': self.generate_user_engagement_report(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')),
            'test_performance': self.generate_test_performance_report(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')),
            'career_insights': self.generate_career_insights_report(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')),
            'business_intelligence': self.generate_business_intelligence_report(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        }
        
        # Создание главной панели
        main_fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Активные пользователи', 'Коэффициент завершения', 
                          'Доход', 'Удовлетворенность'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Извлечение данных для главной панели
        user_data = reports['user_engagement'].data['daily_data']
        test_data = reports['test_performance'].data['by_test_type']
        bi_data = reports['business_intelligence'].data['daily_metrics']
        
        # Добавление графиков (упрощенно)
        main_fig.update_layout(height=800, showlegend=True, title_text="Комплексная панель управления")
        
        dashboard_data = {
            'reports': {cat.value: rep.data for cat, rep in reports.items()},
            'summary_insights': [insight for rep in reports.values() for insight in rep.insights[:3]],
            'key_recommendations': [rec for rep in reports.values() for rec in rep.recommendations],
            'generated_at': datetime.utcnow().isoformat()
        }
        
        return dashboard_data
    
    def get_analytics_dashboard(self) -> Dict[str, Any]:
        """Получение аналитической панели"""
        return self.generate_comprehensive_dashboard()
    
    def export_report(self, report: AnalyticsReport, format_type: str = 'json') -> str:
        """Экспорт отчета в указанный формат"""
        if format_type == 'json':
            return json.dumps(asdict(report), ensure_ascii=False, indent=2)
        elif format_type == 'csv':
            # Для CSV нужно преобразовать данные
            df = pd.DataFrame(report.data.get('daily_data', []))
            return df.to_csv(index=False)
        else:
            raise ValueError(f"Неподдерживаемый формат экспорта: {format_type}")

# Глобальный экземпляр
analytics_engine = AdvancedAnalyticsEngine()

def register_analytics_commands(app):
    """Регистрация CLI команд аналитики"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('analytics-dashboard')
    @with_appcontext
    def show_analytics_dashboard():
        """Показать комплексную аналитическую панель"""
        dashboard = analytics_engine.get_analytics_dashboard()
        click.echo("Комплексная аналитическая панель:")
        click.echo(f"  Сгенерировано: {dashboard['generated_at']}")
        click.echo(f"  Отчетов: {len(dashboard['reports'])}")
        click.echo(f"  Инсайтов: {len(dashboard['summary_insights'])}")
        
        click.echo("\nКлючевые инсайты:")
        for insight in dashboard['summary_insights'][:5]:
            click.echo(f"  - {insight}")
        
        click.echo("\nРекомендации:")
        for recommendation in dashboard['key_recommendations'][:5]:
            click.echo(f"  - {recommendation}")
    
    @app.cli.command('generate-report')
    @click.argument('report_type')
    @click.option('--start-date', default=(datetime.utcnow() - timedelta(days=30)).strftime('%Y-%m-%d'))
    @click.option('--end-date', default=datetime.utcnow().strftime('%Y-%m-%d'))
    @with_appcontext
    def generate_specific_report(report_type, start_date, end_date):
        """Генерация конкретного типа отчета"""
        if report_type == 'user-engagement':
            report = analytics_engine.generate_user_engagement_report(start_date, end_date)
        elif report_type == 'test-performance':
            report = analytics_engine.generate_test_performance_report(start_date, end_date)
        elif report_type == 'career-insights':
            report = analytics_engine.generate_career_insights_report(start_date, end_date)
        elif report_type == 'business-intelligence':
            report = analytics_engine.generate_business_intelligence_report(start_date, end_date)
        else:
            click.echo(f"Неизвестный тип отчета: {report_type}")
            return
        
        click.echo(f"Отчет '{report.category.value}' сгенерирован:")
        click.echo(f"  ID: {report.report_id}")
        click.echo(f"  Время: {report.generated_at}")
        click.echo(f"  Инсайтов: {len(report.insights)}")
        click.echo(f"  Рекомендаций: {len(report.recommendations)}")
        
        click.echo("\nИнсайты:")
        for insight in report.insights:
            click.echo(f"  - {insight}")
        
        click.echo("\nРекомендации:")
        for rec in report.recommendations:
            click.echo(f"  - {rec}")

def require_analytics_access(f):
    """Декоратор для проверки доступа к аналитике"""
    from functools import wraps
    from flask import request, abort
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Здесь должна быть проверка прав доступа
        # Пока просто разрешаем всем
        return f(*args, **kwargs)
    
    return decorated_function

def track_analytics_event(event_type: str, **properties):
    """Декоратор для отслеживания аналитических событий"""
    def decorator(f):
        from functools import wraps
        
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            try:
                result = f(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # Логирование события (в реальном приложении отправка в аналитическую систему)
                event_data = {
                    'event_type': event_type,
                    'function': f.__name__,
                    'execution_time': execution_time,
                    'timestamp': datetime.utcnow().isoformat(),
                    'properties': properties
                }
                
                logger.info(f"Analytics event: {json.dumps(event_data, ensure_ascii=False)}")
                
                return result
            except Exception as e:
                # Логирование ошибок
                error_data = {
                    'event_type': f"{event_type}_error",
                    'function': f.__name__,
                    'error': str(e),
                    'timestamp': datetime.utcnow().isoformat()
                }
                logger.error(f"Analytics error: {json.dumps(error_data, ensure_ascii=False)}")
                raise
        
        return decorated_function
    return decorator