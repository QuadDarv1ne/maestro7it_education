# -*- coding: utf-8 -*-
"""
Модуль расширенной аналитики и отчетов для ПрофиТест
Предоставляет продвинутые возможности анализа данных и генерации отчетов
"""
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Set, Any, Tuple
import logging
from dataclasses import dataclass, field
from collections import defaultdict
import json
import statistics
from decimal import Decimal, ROUND_HALF_UP


class ReportType(Enum):
    """Типы отчетов"""
    USER_ACTIVITY = 'user_activity'
    TEST_PERFORMANCE = 'test_performance'
    CONTENT_ANALYTICS = 'content_analytics'
    SYSTEM_PERFORMANCE = 'system_performance'
    BUSINESS_METRICS = 'business_metrics'
    USER_ENGAGEMENT = 'user_engagement'
    RETENTION_ANALYSIS = 'retention_analysis'
    REVENUE_ANALYSIS = 'revenue_analysis'


class ReportFrequency(Enum):
    """Частота генерации отчетов"""
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    QUARTERLY = 'quarterly'
    YEARLY = 'yearly'
    CUSTOM = 'custom'


class AnalyticsDimension(Enum):
    """Измерения аналитики"""
    TIME = 'time'
    USER = 'user'
    CONTENT = 'content'
    GEOGRAPHY = 'geography'
    DEVICE = 'device'
    CHANNEL = 'channel'


@dataclass
class Report:
    """Класс отчета"""
    id: str
    report_type: ReportType
    title: str
    description: str
    generated_at: datetime
    period_start: datetime
    period_end: datetime
    data: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    is_scheduled: bool = False
    frequency: Optional[ReportFrequency] = None


@dataclass
class AnalyticsQuery:
    """Класс запроса аналитики"""
    id: str
    dimensions: List[AnalyticsDimension]
    metrics: List[str]
    filters: Dict[str, Any]
    date_range: Tuple[datetime, datetime]
    created_at: datetime = field(default_factory=datetime.now)


class DataAggregator:
    """Агрегатор данных для аналитики"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.cached_data: Dict[str, Any] = {}
        self.cache_ttl = 3600  # 1 час
    
    def aggregate_user_metrics(self, users_data: List[Dict], 
                             date_range: Tuple[datetime, datetime]) -> Dict[str, Any]:
        """
        Агрегирует метрики пользователей.
        
        Args:
            users_data: Данные пользователей
            date_range: Диапазон дат
            
        Returns:
            dict: Агрегированные метрики
        """
        if not users_data:
            return {}
        
        start_date, end_date = date_range
        period_users = [u for u in users_data 
                       if start_date <= u.get('created_at', datetime.min) <= end_date]
        
        if not period_users:
            return {}
        
        # Основные метрики
        total_users = len(period_users)
        active_users = len([u for u in period_users if u.get('is_active', False)])
        verified_users = len([u for u in period_users if u.get('is_verified', False)])
        
        # Статистика по датам регистрации
        registration_dates = [u.get('created_at').date() for u in period_users 
                            if u.get('created_at')]
        daily_registrations = defaultdict(int)
        for date in registration_dates:
            daily_registrations[date] += 1
        
        # Статистика по ролям
        role_distribution = defaultdict(int)
        for user in period_users:
            role = user.get('role', 'user')
            role_distribution[role] += 1
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'inactive_users': total_users - active_users,
            'verified_users': verified_users,
            'unverified_users': total_users - verified_users,
            'activation_rate': round((active_users / total_users * 100), 2) if total_users > 0 else 0,
            'verification_rate': round((verified_users / total_users * 100), 2) if total_users > 0 else 0,
            'daily_registrations': dict(daily_registrations),
            'role_distribution': dict(role_distribution),
            'average_daily_registrations': round(statistics.mean(daily_registrations.values()) 
                                               if daily_registrations else 0, 2)
        }
    
    def aggregate_test_metrics(self, tests_data: List[Dict], 
                             date_range: Tuple[datetime, datetime]) -> Dict[str, Any]:
        """
        Агрегирует метрики тестов.
        
        Args:
            tests_data: Данные тестов
            date_range: Диапазон дат
            
        Returns:
            dict: Агрегированные метрики
        """
        if not tests_data:
            return {}
        
        start_date, end_date = date_range
        period_tests = [t for t in tests_data 
                       if start_date <= t.get('created_at', datetime.min) <= end_date]
        
        if not period_tests:
            return {}
        
        total_tests = len(period_tests)
        published_tests = len([t for t in period_tests if t.get('status') == 'published'])
        draft_tests = len([t for t in period_tests if t.get('status') == 'draft'])
        
        # Статистика по категориям
        category_distribution = defaultdict(int)
        for test in period_tests:
            category = test.get('category', 'uncategorized')
            category_distribution[category] += 1
        
        # Статистика по сложности
        difficulty_distribution = defaultdict(int)
        for test in period_tests:
            difficulty = test.get('difficulty', 'medium')
            difficulty_distribution[difficulty] += 1
        
        # Статистика прохождений
        total_attempts = sum(t.get('attempts', 0) for t in period_tests)
        total_completions = sum(t.get('completions', 0) for t in period_tests)
        completion_rate = (total_completions / total_attempts * 100) if total_attempts > 0 else 0
        
        return {
            'total_tests': total_tests,
            'published_tests': published_tests,
            'draft_tests': draft_tests,
            'published_rate': round((published_tests / total_tests * 100), 2) if total_tests > 0 else 0,
            'category_distribution': dict(category_distribution),
            'difficulty_distribution': dict(difficulty_distribution),
            'total_attempts': total_attempts,
            'total_completions': total_completions,
            'completion_rate': round(completion_rate, 2),
            'average_attempts_per_test': round(total_attempts / total_tests, 2) if total_tests > 0 else 0
        }
    
    def aggregate_content_metrics(self, content_data: List[Dict], 
                                date_range: Tuple[datetime, datetime]) -> Dict[str, Any]:
        """
        Агрегирует метрики контента.
        
        Args:
            content_data: Данные контента
            date_range: Диапазон дат
            
        Returns:
            dict: Агрегированные метрики
        """
        if not content_data:
            return {}
        
        start_date, end_date = date_range
        period_content = [c for c in content_data 
                         if start_date <= c.get('created_at', datetime.min) <= end_date]
        
        if not period_content:
            return {}
        
        total_content = len(period_content)
        published_content = len([c for c in period_content if c.get('status') == 'published'])
        premium_content = len([c for c in period_content if c.get('is_premium', False)])
        
        # Статистика по типам контента
        type_distribution = defaultdict(int)
        for content in period_content:
            content_type = content.get('content_type', 'unknown')
            type_distribution[content_type] += 1
        
        # Статистика взаимодействия
        total_views = sum(c.get('views', 0) for c in period_content)
        total_likes = sum(c.get('likes', 0) for c in period_content)
        total_comments = sum(c.get('comments_count', 0) for c in period_content)
        
        avg_rating = statistics.mean([c.get('rating', 0) for c in period_content if c.get('rating', 0) > 0]) if period_content else 0
        
        return {
            'total_content': total_content,
            'published_content': published_content,
            'unpublished_content': total_content - published_content,
            'premium_content': premium_content,
            'publication_rate': round((published_content / total_content * 100), 2) if total_content > 0 else 0,
            'premium_rate': round((premium_content / total_content * 100), 2) if total_content > 0 else 0,
            'type_distribution': dict(type_distribution),
            'total_views': total_views,
            'total_likes': total_likes,
            'total_comments': total_comments,
            'average_views_per_content': round(total_views / total_content, 2) if total_content > 0 else 0,
            'average_likes_per_content': round(total_likes / total_content, 2) if total_content > 0 else 0,
            'average_rating': round(avg_rating, 2),
            'engagement_rate': round(((total_likes + total_comments) / total_views * 100) if total_views > 0 else 0, 2)
        }


class AdvancedAnalyticsEngine:
    """
    Расширенный движок аналитики для системы ПрофиТест.
    Обеспечивает комплексный анализ данных и генерацию отчетов.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.reports: Dict[str, Report] = {}
        self.analytics_queries: Dict[str, AnalyticsQuery] = {}
        self.data_aggregator = DataAggregator()
        
        # Инициализация системной аналитики
        self._initialize_system_analytics()
    
    def _initialize_system_analytics(self):
        """Инициализирует системную аналитику"""
        pass  # Пока пусто, можно добавить инициализацию позже
    
    def generate_report(self, report_type: ReportType, title: str, 
                       description: str, date_range: Tuple[datetime, datetime],
                       data_source: str = 'database') -> Optional[str]:
        """
        Генерирует отчет.
        
        Args:
            report_type: Тип отчета
            title: Заголовок отчета
            description: Описание отчета
            date_range: Диапазон дат
            data_source: Источник данных
            
        Returns:
            str: ID отчета или None
        """
        try:
            import uuid
            report_id = str(uuid.uuid4())
            
            start_date, end_date = date_range
            
            # Генерируем данные в зависимости от типа отчета
            report_data = self._generate_report_data(report_type, date_range, data_source)
            
            report = Report(
                id=report_id,
                report_type=report_type,
                title=title,
                description=description,
                generated_at=datetime.now(),
                period_start=start_date,
                period_end=end_date,
                data=report_data,
                metadata={
                    'data_source': data_source,
                    'generated_by': 'system',
                    'version': '1.0'
                }
            )
            
            # Сохраняем отчет
            self.reports[report_id] = report
            
            self.logger.info(f"Отчет {report_id} типа {report_type.value} сгенерирован")
            return report_id
            
        except Exception as e:
            self.logger.error(f"Ошибка при генерации отчета: {str(e)}")
            return None
    
    def _generate_report_data(self, report_type: ReportType, 
                            date_range: Tuple[datetime, datetime],
                            data_source: str) -> Dict[str, Any]:
        """
        Генерирует данные для отчета.
        
        Args:
            report_type: Тип отчета
            date_range: Диапазон дат
            data_source: Источник данных
            
        Returns:
            dict: Данные отчета
        """
        # В реальной системе здесь будет получение данных из источника
        # Пока возвращаем тестовые данные
        
        start_date, end_date = date_range
        period_days = (end_date - start_date).days + 1
        
        if report_type == ReportType.USER_ACTIVITY:
            return self._generate_user_activity_report(date_range)
        elif report_type == ReportType.TEST_PERFORMANCE:
            return self._generate_test_performance_report(date_range)
        elif report_type == ReportType.CONTENT_ANALYTICS:
            return self._generate_content_analytics_report(date_range)
        elif report_type == ReportType.BUSINESS_METRICS:
            return self._generate_business_metrics_report(date_range)
        else:
            # Общий шаблон для других типов
            return {
                'period_days': period_days,
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'total_records': 0,
                'key_metrics': {},
                'trends': {},
                'recommendations': ['Нет данных для анализа']
            }
    
    def _generate_user_activity_report(self, date_range: Tuple[datetime, datetime]) -> Dict[str, Any]:
        """Генерирует отчет по активности пользователей"""
        # Тестовые данные пользователей
        users_data = [
            {'id': i, 'created_at': datetime.now() - timedelta(days=i % 30), 
             'is_active': i % 3 != 0, 'is_verified': i % 2 == 0, 'role': 'user' if i % 5 != 0 else 'premium_user'}
            for i in range(1, 101)
        ]
        
        metrics = self.data_aggregator.aggregate_user_metrics(users_data, date_range)
        
        return {
            'report_type': 'user_activity',
            'metrics': metrics,
            'key_insights': [
                f"Общее количество пользователей: {metrics.get('total_users', 0)}",
                f"Активных пользователей: {metrics.get('active_users', 0)} ({metrics.get('activation_rate', 0)}%)",
                f"Верифицированных пользователей: {metrics.get('verified_users', 0)} ({metrics.get('verification_rate', 0)}%)"
            ],
            'recommendations': [
                "Увеличить активность неактивных пользователей через email-рассылки",
                "Улучшить процесс верификации для повышения доверия",
                "Анализировать пики регистраций для оптимизации маркетинга"
            ]
        }
    
    def _generate_test_performance_report(self, date_range: Tuple[datetime, datetime]) -> Dict[str, Any]:
        """Генерирует отчет по производительности тестов"""
        # Тестовые данные тестов
        tests_data = [
            {'id': i, 'created_at': datetime.now() - timedelta(days=i % 60),
             'status': 'published' if i % 3 != 0 else 'draft',
             'category': ['psychology', 'career', 'education'][i % 3],
             'difficulty': ['easy', 'medium', 'hard'][i % 3],
             'attempts': i * 2,
             'completions': i * 1.5}
            for i in range(1, 51)
        ]
        
        metrics = self.data_aggregator.aggregate_test_metrics(tests_data, date_range)
        
        return {
            'report_type': 'test_performance',
            'metrics': metrics,
            'key_insights': [
                f"Общее количество тестов: {metrics.get('total_tests', 0)}",
                f"Опубликованных тестов: {metrics.get('published_tests', 0)} ({metrics.get('published_rate', 0)}%)",
                f"Общий уровень завершения: {metrics.get('completion_rate', 0)}%"
            ],
            'recommendations': [
                "Оптимизировать тесты с низким уровнем завершения",
                "Расширить категории тестов на основе популярности",
                "Улучшить алгоритмы рекомендаций тестов"
            ]
        }
    
    def _generate_content_analytics_report(self, date_range: Tuple[datetime, datetime]) -> Dict[str, Any]:
        """Генерирует отчет по аналитике контента"""
        # Тестовые данные контента
        content_data = [
            {'id': i, 'created_at': datetime.now() - timedelta(days=i % 90),
             'status': 'published' if i % 4 != 0 else 'draft',
             'is_premium': i % 5 == 0,
             'content_type': ['article', 'video', 'test', 'course'][i % 4],
             'views': i * 10,
             'likes': i * 3,
             'comments_count': i,
             'rating': 3.0 + (i % 20) / 10}
            for i in range(1, 76)
        ]
        
        metrics = self.data_aggregator.aggregate_content_metrics(content_data, date_range)
        
        return {
            'report_type': 'content_analytics',
            'metrics': metrics,
            'key_insights': [
                f"Общее количество контента: {metrics.get('total_content', 0)}",
                f"Опубликованного контента: {metrics.get('published_content', 0)} ({metrics.get('publication_rate', 0)}%)",
                f"Уровень вовлеченности: {metrics.get('engagement_rate', 0)}%"
            ],
            'recommendations': [
                "Создавать больше премиум контента для увеличения доходов",
                "Оптимизировать контент с низким рейтингом",
                "Анализировать наиболее популярные типы контента"
            ]
        }
    
    def _generate_business_metrics_report(self, date_range: Tuple[datetime, datetime]) -> Dict[str, Any]:
        """Генерирует отчет по бизнес-метрикам"""
        start_date, end_date = date_range
        period_days = (end_date - start_date).days + 1
        
        # Тестовые бизнес-метрики
        revenue = period_days * 1000  # 1000 руб/день
        users = 1000 + period_days * 5  # Рост 5 пользователей в день
        conversions = users * 0.05  # 5% конверсия
        churn_rate = 2.5  # 2.5% оттока
        
        return {
            'report_type': 'business_metrics',
            'period_metrics': {
                'revenue': revenue,
                'total_users': users,
                'new_users': period_days * 5,
                'conversions': conversions,
                'churn_rate': churn_rate,
                'arpu': round(revenue / users, 2) if users > 0 else 0,
                'conversion_rate': round(conversions / users * 100, 2) if users > 0 else 0
            },
            'key_insights': [
                f"Выручка за период: {revenue} руб",
                f"Общее количество пользователей: {users}",
                f"Конверсия: {round(conversions / users * 100, 2) if users > 0 else 0}%",
                f"Уровень оттока: {churn_rate}%"
            ],
            'recommendations': [
                "Оптимизировать цены для увеличения ARPU",
                "Улучшить удержание пользователей для снижения оттока",
                "Расширить каналы привлечения пользователей"
            ]
        }
    
    def get_report(self, report_id: str) -> Optional[Report]:
        """
        Получает отчет по ID.
        
        Args:
            report_id: ID отчета
            
        Returns:
            Report: Объект отчета или None
        """
        return self.reports.get(report_id)
    
    def get_reports_by_type(self, report_type: ReportType) -> List[Report]:
        """
        Получает отчеты по типу.
        
        Args:
            report_type: Тип отчета
            
        Returns:
            list: Список отчетов
        """
        return [r for r in self.reports.values() if r.report_type == report_type]
    
    def get_recent_reports(self, limit: int = 10) -> List[Report]:
        """
        Получает последние отчеты.
        
        Args:
            limit: Максимальное количество
            
        Returns:
            list: Список последних отчетов
        """
        reports = list(self.reports.values())
        reports.sort(key=lambda x: x.generated_at, reverse=True)
        return reports[:limit]
    
    def schedule_report(self, report_type: ReportType, title: str,
                       description: str, frequency: ReportFrequency,
                       start_date: datetime, end_date: Optional[datetime] = None) -> Optional[str]:
        """
        Планирует регулярную генерацию отчета.
        
        Args:
            report_type: Тип отчета
            title: Заголовок
            description: Описание
            frequency: Частота
            start_date: Дата начала
            end_date: Дата окончания (опционально)
            
        Returns:
            str: ID запланированного отчета или None
        """
        try:
            import uuid
            schedule_id = str(uuid.uuid4())
            
            # В реальной системе здесь будет логика планирования
            # Пока просто создаем отчет с пометкой о планировании
            
            report_data = {
                'schedule_info': {
                    'frequency': frequency.value,
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat() if end_date else None,
                    'is_active': True
                }
            }
            
            report = Report(
                id=schedule_id,
                report_type=report_type,
                title=title,
                description=description,
                generated_at=datetime.now(),
                period_start=start_date,
                period_end=end_date or datetime.now(),
                data=report_data,
                is_scheduled=True,
                frequency=frequency
            )
            
            self.reports[schedule_id] = report
            
            self.logger.info(f"Запланирован отчет {schedule_id} с частотой {frequency.value}")
            return schedule_id
            
        except Exception as e:
            self.logger.error(f"Ошибка при планировании отчета: {str(e)}")
            return None
    
    def execute_analytics_query(self, dimensions: List[AnalyticsDimension],
                              metrics: List[str], filters: Dict[str, Any],
                              date_range: Tuple[datetime, datetime]) -> Optional[str]:
        """
        Выполняет аналитический запрос.
        
        Args:
            dimensions: Измерения
            metrics: Метрики
            filters: Фильтры
            date_range: Диапазон дат
            
        Returns:
            str: ID запроса или None
        """
        try:
            import uuid
            query_id = str(uuid.uuid4())
            
            query = AnalyticsQuery(
                id=query_id,
                dimensions=dimensions,
                metrics=metrics,
                filters=filters,
                date_range=date_range
            )
            
            self.analytics_queries[query_id] = query
            
            # В реальной системе здесь будет выполнение запроса к аналитической системе
            self.logger.info(f"Выполнен аналитический запрос {query_id}")
            return query_id
            
        except Exception as e:
            self.logger.error(f"Ошибка при выполнении аналитического запроса: {str(e)}")
            return None
    
    def get_query_results(self, query_id: str) -> Optional[Dict[str, Any]]:
        """
        Получает результаты аналитического запроса.
        
        Args:
            query_id: ID запроса
            
        Returns:
            dict: Результаты запроса или None
        """
        query = self.analytics_queries.get(query_id)
        if not query:
            return None
        
        # В реальной системе здесь будут реальные результаты
        # Пока возвращаем тестовые данные
        return {
            'query_id': query_id,
            'dimensions': [d.value for d in query.dimensions],
            'metrics': query.metrics,
            'filters': query.filters,
            'date_range': {
                'start': query.date_range[0].isoformat(),
                'end': query.date_range[1].isoformat()
            },
            'results': {
                'total_records': 1000,
                'aggregated_data': {
                    'metric1': 123.45,
                    'metric2': 67.89
                },
                'trends': {
                    'upward': ['metric1'],
                    'downward': ['metric2'],
                    'stable': []
                }
            }
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Получает статистику по аналитике.
        
        Returns:
            dict: Статистика системы
        """
        total_reports = len(self.reports)
        scheduled_reports = len([r for r in self.reports.values() if r.is_scheduled])
        total_queries = len(self.analytics_queries)
        
        # Статистика по типам отчетов
        report_types = defaultdict(int)
        for report in self.reports.values():
            report_types[report.report_type.value] += 1
        
        # Статистика по частоте отчетов
        report_frequencies = defaultdict(int)
        for report in self.reports.values():
            if report.frequency:
                report_frequencies[report.frequency.value] += 1
        
        return {
            'total_reports': total_reports,
            'scheduled_reports': scheduled_reports,
            'manual_reports': total_reports - scheduled_reports,
            'total_queries': total_queries,
            'reports_by_type': dict(report_types),
            'reports_by_frequency': dict(report_frequencies),
            'recent_reports_count': len(self.get_recent_reports(5)),
            'active_schedules': scheduled_reports
        }


# Глобальный экземпляр движка аналитики
analytics_engine = AdvancedAnalyticsEngine()