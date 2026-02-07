# -*- coding: utf-8 -*-
"""
Модуль персонализации и улучшения пользовательского опыта для ПрофиТест
Обеспечивает адаптивный UX, персонализированные рекомендации и улучшенную навигацию
"""
import logging
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from collections import defaultdict, deque
import threading
from dataclasses import dataclass
from enum import Enum
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from flask import request, session, g
from functools import wraps

logger = logging.getLogger(__name__)

class UXFeature(Enum):
    """Функции пользовательского опыта"""
    PERSONALIZATION = "personalization"
    RECOMMENDATIONS = "recommendations"
    NAVIGATION = "navigation"
    ACCESSIBILITY = "accessibility"
    FEEDBACK = "feedback"
    PROGRESS_TRACKING = "progress_tracking"

class RecommendationType(Enum):
    """Типы рекомендаций"""
    TEST_SUGGESTIONS = "test_suggestions"
    CAREER_PATHS = "career_paths"
    LEARNING_RESOURCES = "learning_resources"
    PEER_COMPARISONS = "peer_comparisons"
    GOAL_SETTING = "goal_setting"

@dataclass
class UXRecommendation:
    """Рекомендация UX"""
    id: str
    type: RecommendationType
    title: str
    description: str
    score: float
    metadata: Dict[str, Any]
    created_at: str

class UXManager:
    """Менеджер пользовательского опыта с персонализацией"""
    
    def __init__(self, app=None):
        self.app = app
        self.user_profiles = {}
        self.behavior_patterns = defaultdict(deque)
        self.recommendations_cache = {}
        self.personalization_models = {}
        self.ux_features = {}
        self.feedback_data = defaultdict(list)
        self.ab_testing = {}
        self.lock = threading.Lock()
        
        # Конфигурация UX
        self.config = {
            'personalization': {
                'profile_completeness_weight': 0.3,
                'behavior_weight': 0.4,
                'demographic_weight': 0.3,
                'update_frequency_hours': 24
            },
            'recommendations': {
                'max_items': 10,
                'freshness_hours': 6,
                'similarity_threshold': 0.6,
                'diversity_factor': 0.7
            },
            'ux_features': {
                'adaptive_ui': True,
                'smart_navigation': True,
                'contextual_help': True,
                'progressive_disclosure': True
            },
            'feedback': {
                'collection_frequency': 7,  # дней
                'rating_scale': 5,
                'feedback_categories': ['ease_of_use', 'relevance', 'accuracy', 'design']
            }
        }
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация с Flask приложением"""
        self.app = app
        self.setup_ux_middleware()
        logger.info("Менеджер пользовательского опыта инициализирован")
    
    def setup_ux_middleware(self):
        """Настройка middleware UX"""
        @self.app.before_request
        def track_user_behavior():
            if request.endpoint:
                self.record_user_interaction(
                    user_id=getattr(g, 'user_id', None),
                    endpoint=request.endpoint,
                    method=request.method,
                    url=request.url
                )
    
    def create_user_profile(self, user_id: int, demographic_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Создание профиля пользователя для персонализации"""
        profile = {
            'user_id': user_id,
            'created_at': datetime.utcnow().isoformat(),
            'demographics': demographic_data or {},
            'preferences': {
                'test_preferences': [],
                'career_interests': [],
                'learning_styles': [],
                'communication_preferences': []
            },
            'behavioral_data': {
                'interaction_history': [],
                'preferred_times': [],
                'device_preferences': {},
                'navigation_patterns': {}
            },
            'engagement_metrics': {
                'session_count': 0,
                'total_time_spent': 0,
                'completion_rates': {},
                'favorite_sections': []
            },
            'personalization_score': 0.0,
            'last_updated': datetime.utcnow().isoformat()
        }
        
        with self.lock:
            self.user_profiles[user_id] = profile
        
        return profile
    
    def update_user_profile(self, user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Обновление профиля пользователя"""
        if user_id not in self.user_profiles:
            self.create_user_profile(user_id)
        
        profile = self.user_profiles[user_id]
        
        # Обновление предпочтений
        if 'preferences' in data:
            for key, value in data['preferences'].items():
                if key in profile['preferences']:
                    if isinstance(profile['preferences'][key], list):
                        profile['preferences'][key].extend(value)
                        # Уникализация
                        profile['preferences'][key] = list(set(profile['preferences'][key]))
                    else:
                        profile['preferences'][key] = value
        
        # Обновление демографических данных
        if 'demographics' in data:
            profile['demographics'].update(data['demographics'])
        
        # Обновление метрик вовлеченности
        if 'engagement_metrics' in data:
            profile['engagement_metrics'].update(data['engagement_metrics'])
        
        profile['last_updated'] = datetime.utcnow().isoformat()
        
        # Пересчет персонализации
        profile['personalization_score'] = self.calculate_personalization_score(profile)
        
        return profile
    
    def calculate_personalization_score(self, profile: Dict[str, Any]) -> float:
        """Расчет оценки персонализации"""
        score = 0.0
        
        # Полнота профиля
        if profile['demographics']:
            score += 0.2
        
        # Заполненность предпочтений
        pref_count = sum(len(v) if isinstance(v, list) else 1 for v in profile['preferences'].values())
        score += min(pref_count * 0.05, 0.3)
        
        # История взаимодействий
        interaction_count = len(profile['behavioral_data']['interaction_history'])
        score += min(interaction_count * 0.01, 0.3)
        
        # Метрики вовлеченности
        engagement = profile['engagement_metrics']
        if engagement['session_count'] > 5:
            score += 0.1
        if engagement['total_time_spent'] > 3600:  # больше часа
            score += 0.1
        
        return min(score, 1.0)
    
    def record_user_interaction(self, user_id: Optional[int], endpoint: str, method: str = 'GET', url: str = '') -> bool:
        """Запись взаимодействия пользователя"""
        if user_id is None:
            return False
        
        interaction = {
            'timestamp': datetime.utcnow().isoformat(),
            'endpoint': endpoint,
            'method': method,
            'url': url,
            'ip_address': request.remote_addr if request else None,
            'user_agent': request.headers.get('User-Agent', '') if request else None
        }
        
        with self.lock:
            if user_id not in self.user_profiles:
                self.create_user_profile(user_id)
            
            profile = self.user_profiles[user_id]
            profile['behavioral_data']['interaction_history'].append(interaction)
            
            # Обновление счетчиков
            profile['engagement_metrics']['session_count'] += 1
            profile['last_updated'] = datetime.utcnow().isoformat()
        
        return True
    
    def get_personalized_recommendations(self, user_id: int, 
                                       recommendation_type: RecommendationType = None,
                                       limit: int = 5) -> List[UXRecommendation]:
        """Получение персонализированных рекомендаций"""
        if user_id not in self.user_profiles:
            # Создаем базовый профиль
            self.create_user_profile(user_id)
        
        profile = self.user_profiles[user_id]
        
        recommendations = []
        
        if recommendation_type is None or recommendation_type == RecommendationType.TEST_SUGGESTIONS:
            # Рекомендации тестов
            test_recs = self._generate_test_recommendations(profile, limit)
            recommendations.extend(test_recs)
        
        if recommendation_type is None or recommendation_type == RecommendationType.CAREER_PATHS:
            # Карьерные рекомендации
            career_recs = self._generate_career_recommendations(profile, limit)
            recommendations.extend(career_recs)
        
        if recommendation_type is None or recommendation_type == RecommendationType.LEARNING_RESOURCES:
            # Ресурсы для обучения
            learning_recs = self._generate_learning_recommendations(profile, limit)
            recommendations.extend(learning_recs)
        
        # Сортировка по оценке
        recommendations.sort(key=lambda x: x.score, reverse=True)
        
        # Ограничение количества
        return recommendations[:limit]
    
    def _generate_test_recommendations(self, profile: Dict[str, Any], limit: int) -> List[UXRecommendation]:
        """Генерация рекомендаций тестов"""
        recommendations = []
        
        # На основе интересов пользователя
        interests = profile['preferences']['career_interests']
        if interests:
            for i, interest in enumerate(interests[:limit]):
                rec = UXRecommendation(
                    id=f"test_rec_{i}",
                    type=RecommendationType.TEST_SUGGESTIONS,
                    title=f"Тест по {interest}",
                    description=f"Рекомендуем пройти тест для оценки соответствия в сфере {interest}",
                    score=max(0.8 - (i * 0.1), 0.5),
                    metadata={
                        'test_category': interest,
                        'suggested_methodology': 'holland' if 'творчество' in interest else 'klimov'
                    },
                    created_at=datetime.utcnow().isoformat()
                )
                recommendations.append(rec)
        
        # На основе истории взаимодействий
        interactions = profile['behavioral_data']['interaction_history']
        if interactions:
            recent_interactions = interactions[-5:]  # последние 5
            for i, interaction in enumerate(recent_interactions):
                if 'test' in interaction['endpoint'].lower():
                    rec = UXRecommendation(
                        id=f"similar_test_{i}",
                        type=RecommendationType.TEST_SUGGESTIONS,
                        title="Похожий тест",
                        description="Вам может понравиться этот тест, основываясь на ваших предыдущих выборах",
                        score=max(0.7 - (i * 0.1), 0.4),
                        metadata={'based_on': interaction['endpoint']},
                        created_at=datetime.utcnow().isoformat()
                    )
                    recommendations.append(rec)
        
        return recommendations
    
    def _generate_career_recommendations(self, profile: Dict[str, Any], limit: int) -> List[UXRecommendation]:
        """Генерация карьерных рекомендаций"""
        recommendations = []
        
        # На основе интересов и навыков
        interests = profile['preferences']['career_interests']
        skills = profile['preferences'].get('skills', [])
        
        for i in range(min(limit, len(interests))):
            interest = interests[i]
            rec = UXRecommendation(
                id=f"career_rec_{i}",
                type=RecommendationType.CAREER_PATHS,
                title=f"Карьерный путь в {interest}",
                description=f"Детальный план развития в сфере {interest} с рекомендуемыми шагами",
                score=max(0.9 - (i * 0.1), 0.6),
                metadata={
                    'field': interest,
                    'recommended_skills': skills,
                    'typical_roles': [f'Junior {interest}', f'Middle {interest}']
                },
                created_at=datetime.utcnow().isoformat()
            )
            recommendations.append(rec)
        
        return recommendations
    
    def _generate_learning_recommendations(self, profile: Dict[str, Any], limit: int) -> List[UXRecommendation]:
        """Генерация рекомендаций по обучению"""
        recommendations = []
        
        # На основе слабых сторон
        for i in range(limit):
            rec = UXRecommendation(
                id=f"learning_rec_{i}",
                type=RecommendationType.LEARNING_RESOURCES,
                title=f"Ресурс для развития #{i+1}",
                description="Персонализированные образовательные материалы для вашего развития",
                score=max(0.8 - (i * 0.1), 0.5),
                metadata={
                    'resource_type': 'course',
                    'difficulty_level': 'beginner',
                    'estimated_time': '2-3 hours'
                },
                created_at=datetime.utcnow().isoformat()
            )
            recommendations.append(rec)
        
        return recommendations
    
    def get_adaptive_ui_config(self, user_id: int) -> Dict[str, Any]:
        """Получение адаптивной конфигурации интерфейса"""
        if user_id not in self.user_profiles:
            self.create_user_profile(user_id)
        
        profile = self.user_profiles[user_id]
        
        ui_config = {
            'theme': self._determine_theme(profile),
            'layout': self._determine_layout(profile),
            'navigation': self._determine_navigation(profile),
            'content_priority': self._determine_content_priority(profile),
            'accessibility': self._determine_accessibility(profile)
        }
        
        return ui_config
    
    def _determine_theme(self, profile: Dict[str, Any]) -> str:
        """Определение темы интерфейса"""
        # На основе предпочтений и времени суток
        hour = datetime.now().hour
        if 6 <= hour < 18:
            return 'light' if profile['preferences'].get('theme_preference') != 'dark' else 'dark'
        else:
            return 'dark' if profile['preferences'].get('theme_preference') != 'light' else 'light'
    
    def _determine_layout(self, profile: Dict[str, Any]) -> str:
        """Определение макета"""
        # На основе устройств и предпочтений
        device_pref = profile['behavioral_data']['device_preferences'].get('primary_device', 'desktop')
        return 'compact' if device_pref == 'mobile' else 'spacious'
    
    def _determine_navigation(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Определение навигации"""
        # На основе частоты использования разделов
        favorite_sections = profile['engagement_metrics'].get('favorite_sections', [])
        return {
            'primary_menu': favorite_sections[:3] if favorite_sections else ['dashboard', 'tests', 'profile'],
            'quick_links': favorite_sections[3:6] if len(favorite_sections) > 3 else [],
            'show_search': True,
            'show_breadcrumbs': True
        }
    
    def _determine_content_priority(self, profile: Dict[str, Any]) -> List[str]:
        """Определение приоритета контента"""
        # На основе интересов и истории взаимодействий
        interests = profile['preferences']['career_interests']
        return interests[:5] if interests else ['general', 'popular', 'recommended']
    
    def _determine_accessibility(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Определение настроек доступности"""
        return {
            'high_contrast': False,
            'larger_text': profile['demographics'].get('age', 30) > 50,
            'screen_reader_friendly': True,
            'keyboard_navigation': True
        }
    
    def collect_user_feedback(self, user_id: int, feedback_data: Dict[str, Any]) -> bool:
        """Сбор обратной связи от пользователя"""
        feedback_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'feedback_data': feedback_data,
            'session_context': {
                'last_interaction': getattr(g, 'last_interaction', None),
                'current_page': request.path if request else None
            }
        }
        
        with self.lock:
            self.feedback_data[user_id].append(feedback_entry)
        
        logger.info(f"Получена обратная связь от пользователя {user_id}")
        return True
    
    def get_user_progress_insights(self, user_id: int) -> Dict[str, Any]:
        """Получение инсайтов по прогрессу пользователя"""
        if user_id not in self.user_profiles:
            return {}
        
        profile = self.user_profiles[user_id]
        
        # Анализ прогресса
        engagement = profile['engagement_metrics']
        
        insights = {
            'engagement_trends': self._analyze_engagement_trends(profile),
            'achievement_milestones': self._identify_milestones(profile),
            'improvement_areas': self._identify_improvement_areas(profile),
            'motivation_factors': self._analyze_motivation_factors(profile)
        }
        
        return insights
    
    def _analyze_engagement_trends(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ тенденций вовлеченности"""
        interactions = profile['behavioral_data']['interaction_history']
        
        if not interactions:
            return {'trend': 'neutral', 'message': 'Недостаточно данных для анализа'}
        
        # Анализ последних 30 дней
        recent_interactions = [i for i in interactions 
                              if datetime.fromisoformat(i['timestamp'].replace('Z', '+00:00')) > 
                              datetime.utcnow() - timedelta(days=30)]
        
        if len(recent_interactions) < 10:
            return {'trend': 'insufficient_data', 'message': 'Нужно больше данных'}
        
        # Расчет тенденции
        current_period = len([i for i in recent_interactions 
                             if datetime.fromisoformat(i['timestamp'].replace('Z', '+00:00')) > 
                             datetime.utcnow() - timedelta(days=7)])
        previous_period = len([i for i in recent_interactions 
                              if datetime.fromisoformat(i['timestamp'].replace('Z', '+00:00')) > 
                              datetime.utcnow() - timedelta(days=14) and
                              datetime.fromisoformat(i['timestamp'].replace('Z', '+00:00')) <= 
                              datetime.utcnow() - timedelta(days=7)])
        
        if current_period > previous_period * 1.2:
            trend = 'increasing'
            message = 'Ваша активность значительно возросла!'
        elif current_period < previous_period * 0.8:
            trend = 'decreasing'
            message = 'Ваша активность снизилась. Хотите вернуться к целям?'
        else:
            trend = 'stable'
            message = 'Ваша активность остается стабильной'
        
        return {
            'trend': trend,
            'message': message,
            'current_week_interactions': current_period,
            'previous_week_interactions': previous_period
        }
    
    def _identify_milestones(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Идентификация вех достижений"""
        milestones = []
        
        engagement = profile['engagement_metrics']
        
        if engagement['session_count'] >= 10:
            milestones.append({
                'title': 'Десять посещений',
                'description': 'Вы посетили платформу 10 раз!',
                'icon': '🎯',
                'achieved': True
            })
        
        if engagement['total_time_spent'] >= 3600:  # 1 час
            milestones.append({
                'title': 'Час изучения',
                'description': 'Вы провели на платформе более часа!',
                'icon': '⏱️',
                'achieved': True
            })
        
        # Добавление вех на основе пройденных тестов
        test_completions = engagement.get('completion_rates', {}).get('tests_completed', 0)
        if test_completions >= 5:
            milestones.append({
                'title': 'Пять тестов',
                'description': 'Вы прошли 5 профессиональных тестов!',
                'icon': '📊',
                'achieved': True
            })
        
        return milestones
    
    def _identify_improvement_areas(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Идентификация областей для улучшения"""
        areas = []
        
        # На основе неполного профиля
        if not profile['demographics']:
            areas.append({
                'area': 'profile_completeness',
                'title': 'Заполните профиль',
                'description': 'Заполните информацию о себе для персонализированных рекомендаций',
                'priority': 'high'
            })
        
        # На основе низкой активности
        if profile['engagement_metrics']['session_count'] < 3:
            areas.append({
                'area': 'engagement',
                'title': 'Повысьте активность',
                'description': 'Попробуйте пройти первый тест для начала',
                'priority': 'medium'
            })
        
        return areas
    
    def _analyze_motivation_factors(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Анализ факторов мотивации"""
        factors = []
        
        # На основе интересов
        interests = profile['preferences']['career_interests']
        if interests:
            factors.append({
                'factor': 'interest_alignment',
                'title': 'Соответствие интересам',
                'description': f'Ваши интересы: {", ".join(interests[:3])}',
                'value': len(interests)
            })
        
        # На основе прогресса
        if profile['engagement_metrics']['session_count'] > 5:
            factors.append({
                'factor': 'habit_formation',
                'title': 'Формирование привычки',
                'description': 'Вы уже установили регулярную практику',
                'value': 'positive'
            })
        
        return factors
    
    def get_ux_report(self, user_id: int = None) -> Dict[str, Any]:
        """Получение отчета UX для пользователя или системы"""
        if user_id:
            if user_id not in self.user_profiles:
                return {'error': 'User profile not found'}
            
            profile = self.user_profiles[user_id]
            return {
                'user_id': user_id,
                'personalization_score': profile['personalization_score'],
                'engagement_metrics': profile['engagement_metrics'],
                'preferences_summary': {
                    'interests_count': len(profile['preferences']['career_interests']),
                    'test_preferences_count': len(profile['preferences']['test_preferences']),
                    'last_updated': profile['last_updated']
                }
            }
        else:
            # Системный отчет
            return {
                'total_users': len(self.user_profiles),
                'avg_personalization_score': np.mean([p['personalization_score'] for p in self.user_profiles.values()]) if self.user_profiles else 0,
                'active_users_today': self._count_active_users_today(),
                'feedback_entries': sum(len(entries) for entries in self.feedback_data.values()),
                'generated_at': datetime.utcnow().isoformat()
            }
    
    def _count_active_users_today(self) -> int:
        """Подсчет активных пользователей сегодня"""
        today = datetime.utcnow().date()
        count = 0
        
        for profile in self.user_profiles.values():
            last_update = datetime.fromisoformat(profile['last_updated'].replace('Z', '+00:00')).date()
            if last_update == today:
                count += 1
        
        return count

# Глобальный экземпляр
ux_manager = UXManager()

def register_ux_commands(app):
    """Регистрация CLI команд UX"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('ux-report')
    @click.option('--user-id', type=int, help='ID пользователя для отдельного отчета')
    @with_appcontext
    def show_ux_report(user_id):
        """Показать отчет UX"""
        report = ux_manager.get_ux_report(user_id)
        click.echo("Отчет пользовательского опыта:")
        
        if user_id:
            click.echo(f"  Персонализация: {report['personalization_score']:.2%}")
            click.echo(f"  Сессий: {report['engagement_metrics']['session_count']}")
        else:
            click.echo(f"  Всего пользователей: {report['total_users']}")
            click.echo(f"  Средняя персонализация: {report['avg_personalization_score']:.2%}")
            click.echo(f"  Активных сегодня: {report['active_users_today']}")
    
    @app.cli.command('ux-recommendations')
    @click.argument('user_id', type=int)
    @click.option('--type', '-t', default=None, type=click.Choice([t.value for t in RecommendationType]))
    @click.option('--limit', '-l', default=5, type=int)
    @with_appcontext
    def show_recommendations(user_id, type, limit):
        """Показать рекомендации для пользователя"""
        rec_type = RecommendationType(type) if type else None
        recommendations = ux_manager.get_personalized_recommendations(user_id, rec_type, limit)
        
        click.echo(f"Рекомендации для пользователя {user_id}:")
        for rec in recommendations:
            click.echo(f"  [{rec.type.value}] {rec.title} (оценка: {rec.score:.2f})")
            click.echo(f"      {rec.description}")

def require_personalization(f):
    """Декоратор для требований персонализации"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = getattr(g, 'user_id', None)
        if user_id:
            # Обновление профиля при каждом обращении
            if user_id not in ux_manager.user_profiles:
                ux_manager.create_user_profile(user_id)
        
        return f(*args, **kwargs)
    
    return decorated_function

def track_user_engagement(f):
    """Декоратор для отслеживания вовлеченности пользователя"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = getattr(g, 'user_id', None)
        if user_id:
            # Запись взаимодействия
            ux_manager.record_user_interaction(
                user_id=user_id,
                endpoint=f.__name__,
                method=request.method if request else 'UNKNOWN'
            )
        
        return f(*args, **kwargs)
    
    return decorated_function

def get_adaptive_interface(user_id: int) -> Dict[str, Any]:
    """Получение адаптивного интерфейса для пользователя"""
    return ux_manager.get_adaptive_ui_config(user_id)

def get_personalized_content(user_id: int) -> Dict[str, Any]:
    """Получение персонализированного контента"""
    recommendations = ux_manager.get_personalized_recommendations(user_id)
    progress_insights = ux_manager.get_user_progress_insights(user_id)
    
    return {
        'recommendations': [rec.__dict__ for rec in recommendations],
        'progress_insights': progress_insights,
        'adapted_interface': ux_manager.get_adaptive_ui_config(user_id)
    }