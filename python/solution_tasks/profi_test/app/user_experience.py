# -*- coding: utf-8 -*-
"""
Модуль улучшения пользовательского опыта для ПрофиТест
Предоставляет функции для повышения вовлеченности и удовлетворенности пользователей
"""
from datetime import datetime, timedelta
from flask import session, g
from flask_login import current_user
from app import db
from app.models import User, TestResult, Notification, UserPreference
import json


class UserExperienceManager:
    """
    Менеджер пользовательского опыта для системы ПрофиТест.
    Управляет процессом онбординга и улучшением взаимодействия с пользователем.
    """
    def __init__(self):
        self.onboarding_steps = [
            'registration',
            'profile_completion',
            'first_test_taken',
            'career_goal_set',
            'learning_path_created',
            'portfolio_project_added'
        ]
        
    def get_user_progress(self, user):
        """
        Получает прогресс пользователя на платформе
        """
        try:
            progress = {
                'completed_steps': [],
                'total_steps': len(self.onboarding_steps),
                'completion_percentage': 0,
                'next_suggestions': []
            }
            
            # Check each step
            if user.created_at:
                progress['completed_steps'].append('registration')
            
            # Check if user has taken a test
            if TestResult.query.filter_by(user_id=user.id).count() > 0:
                progress['completed_steps'].append('first_test_taken')
                progress['next_suggestions'].append('View your test results and recommendations')
            
            # Check if user has set career goals
            from app.models import CareerGoal
            if CareerGoal.query.filter_by(user_id=user.id).count() > 0:
                progress['completed_steps'].append('career_goal_set')
                progress['next_suggestions'].append('Create a learning path toward your goals')
            else:
                progress['next_suggestions'].append('Set your first career goal')
            
            # Check if user has created learning paths
            from app.models import LearningPath
            if LearningPath.query.filter_by(user_id=user.id).count() > 0:
                progress['completed_steps'].append('learning_path_created')
            
            # Check if user has added portfolio projects
            from app.models import PortfolioProject
            if PortfolioProject.query.filter_by(user_id=user.id).count() > 0:
                progress['completed_steps'].append('portfolio_project_added')
            
            progress['completion_percentage'] = round(
                (len(progress['completed_steps']) / len(self.onboarding_steps)) * 100, 2
            )
            
            return progress
        except Exception as e:
            print(f"Error getting user progress: {str(e)}")
            return {
                'completed_steps': [],
                'total_steps': len(self.onboarding_steps),
                'completion_percentage': 0,
                'next_suggestions': ['Contact support for assistance']
            }
    
    def get_welcome_message(self, user):
        """
        Get personalized welcome message based on user's progress
        """
        try:
            progress = self.get_user_progress(user)
            completed_count = len(progress['completed_steps'])
            
            if completed_count == 0:
                return "Добро пожаловать! Начните с прохождения профессионального тестирования, чтобы получить персональные рекомендации."
            elif completed_count < 3:
                return "Отлично! Продолжайте заполнять свой профиль, чтобы получить более точные рекомендации."
            elif completed_count < 5:
                return "Хорошая работа! Вы почти завершили начальный этап. Добавьте свои первые карьерные цели."
            else:
                return "Поздравляем! Вы завершили основные шаги. Продолжайте развиваться и достигать своих целей!"
        except Exception as e:
            print(f"Error getting welcome message: {str(e)}")
            return "Добро пожаловать в систему профориентации!"
    
    def get_smart_notifications(self, user):
        """
        Get smart notifications based on user behavior and preferences
        """
        try:
            notifications = []
            
            # Check if user has taken a test recently
            latest_test = TestResult.query.filter_by(user_id=user.id).order_by(TestResult.created_at.desc()).first()
            if latest_test:
                if (datetime.utcnow() - latest_test.created_at).days > 7:
                    # User hasn't taken a test in a week, suggest retaking
                    notifications.append({
                        'type': 'suggestion',
                        'title': 'Пройдите тест снова',
                        'message': 'Прошло некоторое время с вашего последнего теста. Возможно, ваши предпочтения изменились.',
                        'priority': 'medium',
                        'action_url': '/test/holland_test'
                    })
            else:
                # User hasn't taken any tests
                notifications.append({
                    'type': 'onboarding',
                    'title': 'Пройдите первый тест',
                    'message': 'Начните с прохождения профессионального тестирования, чтобы получить рекомендации.',
                    'priority': 'high',
                    'action_url': '/test/holland_test'
                })
            
            # Check for career goals
            from app.models import CareerGoal
            user_goals = CareerGoal.query.filter_by(user_id=user.id).all()
            if not user_goals:
                notifications.append({
                    'type': 'goal_setting',
                    'title': 'Установите карьерные цели',
                    'message': 'Создайте свои первые карьерные цели, чтобы строить планы развития.',
                    'priority': 'high',
                    'action_url': '/career-goals'
                })
            else:
                # Check if any goals are approaching deadlines
                for goal in user_goals:
                    if goal.target_date and goal.current_status == 'in_progress':
                        days_until_deadline = (goal.target_date - datetime.utcnow().date()).days
                        if 0 < days_until_deadline <= 7:  # Within a week
                            notifications.append({
                                'type': 'deadline_reminder',
                                'title': f'Цель "{goal.title}" скоро истекает',
                                'message': f'У вас осталось {days_until_deadline} дней до дедлайна по цели "{goal.title}".',
                                'priority': 'high',
                                'action_url': f'/career-goals/{goal.id}'
                            })
            
            # Check for learning paths
            from app.models import LearningPath
            user_paths = LearningPath.query.filter_by(user_id=user.id).all()
            if not user_paths and user_goals:
                notifications.append({
                    'type': 'suggestion',
                    'title': 'Создайте образовательную траекторию',
                    'message': 'Создайте план обучения, который поможет достичь ваших карьерных целей.',
                    'priority': 'medium',
                    'action_url': '/learning-paths/create'
                })
            else:
                # Check for in-progress learning paths
                in_progress_paths = [p for p in user_paths if p.status == 'in_progress']
                for path in in_progress_paths:
                    notifications.append({
                        'type': 'continuation_reminder',
                        'title': f'Продолжайте "{path.title}"',
                        'message': 'У вас есть активная образовательная траектория. Не забывайте проходить задания.',
                        'priority': 'low',
                        'action_url': f'/learning-paths/{path.id}'
                    })
            
            # Check user preferences for vacancy alerts
            preferences = UserPreference.query.filter_by(user_id=user.id).first()
            if preferences and preferences.vacancy_alerts_enabled:
                # Could integrate with job market API here
                notifications.append({
                    'type': 'market_update',
                    'title': 'Обновления рынка труда',
                    'message': 'Доступны новые вакансии, соответствующие вашим интересам.',
                    'priority': 'medium',
                    'action_url': '/job-market'
                })
            
            return notifications
        except Exception as e:
            print(f"Error getting smart notifications: {str(e)}")
            return []
    
    def get_personalized_dashboard_widgets(self, user):
        """
        Get personalized dashboard widgets based on user's activity
        """
        try:
            widgets = []
            
            # Progress widget
            progress = self.get_user_progress(user)
            widgets.append({
                'type': 'progress_tracker',
                'title': 'Ваш прогресс',
                'data': {
                    'percentage': progress['completion_percentage'],
                    'completed': len(progress['completed_steps']),
                    'total': len(self.onboarding_steps),
                    'steps_completed': progress['completed_steps']
                },
                'position': 'top-left'
            })
            
            # Recent test results widget
            recent_tests = TestResult.query.filter_by(user_id=user.id).order_by(
                TestResult.created_at.desc()
            ).limit(3).all()
            
            if recent_tests:
                widgets.append({
                    'type': 'recent_tests',
                    'title': 'Ваши последние тесты',
                    'data': [{
                        'id': test.id,
                        'methodology': test.methodology,
                        'date': test.created_at.strftime('%d.%m.%Y'),
                        'recommendation': test.recommendation[:100] + '...' if test.recommendation and len(test.recommendation) > 100 else test.recommendation or 'Нет рекомендаций'
                    } for test in recent_tests],
                    'position': 'top-right'
                })
            
            # Goals tracker widget
            from app.models import CareerGoal
            active_goals = CareerGoal.query.filter(
                CareerGoal.user_id == user.id,
                CareerGoal.current_status.in_(['planning', 'in_progress'])
            ).order_by(CareerGoal.priority.desc()).limit(3).all()
            
            if active_goals:
                widgets.append({
                    'type': 'active_goals',
                    'title': 'Ваши активные цели',
                    'data': [{
                        'id': goal.id,
                        'title': goal.title,
                        'status': goal.current_status,
                        'priority': goal.priority,
                        'target_date': goal.target_date.strftime('%d.%m.%Y') if goal.target_date else 'Не указан'
                    } for goal in active_goals],
                    'position': 'middle-left'
                })
            
            # Learning paths widget
            from app.models import LearningPath
            active_paths = LearningPath.query.filter(
                LearningPath.user_id == user.id,
                LearningPath.status.in_(['in_progress', 'not_started'])
            ).limit(3).all()
            
            if active_paths:
                widgets.append({
                    'type': 'learning_paths',
                    'title': 'Ваши образовательные траектории',
                    'data': [{
                        'id': path.id,
                        'title': path.title,
                        'status': path.status,
                        'difficulty': path.difficulty_level,
                        'duration': f"{path.duration_weeks} недель" if path.duration_weeks else 'Не указано'
                    } for path in active_paths],
                    'position': 'middle-right'
                })
            
            # Quick actions widget
            quick_actions = []
            if not recent_tests:
                quick_actions.append({
                    'title': 'Пройти тест',
                    'icon': 'fa-clipboard-list',
                    'url': '/test/holland_test',
                    'color': 'primary'
                })
            if not active_goals:
                quick_actions.append({
                    'title': 'Создать цель',
                    'icon': 'fa-bullseye',
                    'url': '/career-goals/create',
                    'color': 'success'
                })
            if not active_paths:
                quick_actions.append({
                    'title': 'Начать обучение',
                    'icon': 'fa-graduation-cap',
                    'url': '/learning-paths/create',
                    'color': 'info'
                })
            
            if quick_actions:
                widgets.append({
                    'type': 'quick_actions',
                    'title': 'Быстрые действия',
                    'data': quick_actions,
                    'position': 'bottom-center'
                })
            
            return widgets
        except Exception as e:
            print(f"Error getting personalized widgets: {str(e)}")
            return []
    
    def get_adaptive_learning_path(self, user, test_result):
        """
        Generate adaptive learning path based on test results
        """
        try:
            if not test_result or not test_result.results:
                return []
            
            # Parse test results
            try:
                results = json.loads(test_result.results)
            except json.JSONDecodeError:
                return []
            
            learning_modules = []
            
            # Generate modules based on dominant category
            if 'dominant_category' in results:
                category = results['dominant_category']
                
                # Define learning modules for each category
                category_modules = {
                    'Человек-природа': [
                        {'title': 'Биология и экология', 'duration': 4, 'difficulty': 'beginner'},
                        {'title': 'Аграрные науки', 'duration': 3, 'difficulty': 'beginner'},
                        {'title': 'Природопользование', 'duration': 5, 'difficulty': 'intermediate'}
                    ],
                    'Человек-техника': [
                        {'title': 'Основы программирования', 'duration': 6, 'difficulty': 'beginner'},
                        {'title': 'Инженерные науки', 'duration': 4, 'difficulty': 'beginner'},
                        {'title': 'Техническое моделирование', 'duration': 5, 'difficulty': 'intermediate'}
                    ],
                    'Человек-человек': [
                        {'title': 'Психология общения', 'duration': 4, 'difficulty': 'beginner'},
                        {'title': 'Лидерство и управление', 'duration': 5, 'difficulty': 'intermediate'},
                        {'title': 'Образование и обучение', 'duration': 6, 'difficulty': 'intermediate'}
                    ],
                    'Человек-знаковая система': [
                        {'title': 'Математическое моделирование', 'duration': 5, 'difficulty': 'intermediate'},
                        {'title': 'Финансовый анализ', 'duration': 4, 'difficulty': 'beginner'},
                        {'title': 'Аналитика данных', 'duration': 6, 'difficulty': 'intermediate'}
                    ],
                    'Человек-художественный образ': [
                        {'title': 'Дизайн и арт', 'duration': 4, 'difficulty': 'beginner'},
                        {'title': 'Креативные технологии', 'duration': 5, 'difficulty': 'intermediate'},
                        {'title': 'Медиа и коммуникации', 'duration': 4, 'difficulty': 'beginner'}
                    ]
                }
                
                if category in category_modules:
                    learning_modules.extend(category_modules[category][:2])  # Take top 2 modules
            
            # Add modules based on top scores if available
            if 'scores' in results:
                sorted_scores = sorted(results['scores'].items(), key=lambda x: x[1], reverse=True)
                
                # Add modules for top 2 categories
                for i, (category, score) in enumerate(sorted_scores[:2]):
                    if score > 5:  # Only if score is above threshold
                        module = {
                            'title': f'Развитие в сфере "{category}"',
                            'duration': min(6, max(2, int(score / 2))),  # Duration based on score
                            'difficulty': 'beginner' if score < 7 else 'intermediate',
                            'relevance_score': score
                        }
                        learning_modules.append(module)
            
            return learning_modules
        except Exception as e:
            print(f"Error generating adaptive learning path: {str(e)}")
            return []
    
    def get_user_insights_and_tips(self, user):
        """
        Get personalized insights and tips for the user
        """
        try:
            insights = []
            
            # Get user's test results
            test_results = TestResult.query.filter_by(user_id=user.id).order_by(
                TestResult.created_at.desc()
            ).all()
            
            if test_results:
                latest_result = test_results[0]
                
                # Add insight about their dominant category
                if latest_result.results:
                    try:
                        results = json.loads(latest_result.results)
                        if 'dominant_category' in results:
                            insights.append({
                                'type': 'strength_identification',
                                'title': 'Ваша сильная сторона',
                                'tip': f'На основе вашего теста, вы наиболее склонны к сфере "{results["dominant_category"]}". Рассмотрите профессии в этой области.',
                                'category': 'strength'
                            })
                    except json.JSONDecodeError:
                        pass
                
                # Compare with other users if possible
                if len(test_results) > 1:
                    insights.append({
                        'type': 'progress_tracking',
                        'title': 'Прогресс за время использования',
                        'tip': 'Вы уже прошли несколько тестов. Ваше понимание собственных предпочтений становится более точным.',
                        'category': 'progress'
                    })
            
            # Add insights based on goals
            from app.models import CareerGoal
            user_goals = CareerGoal.query.filter_by(user_id=user.id).all()
            
            if user_goals:
                active_goals = [g for g in user_goals if g.current_status == 'in_progress']
                completed_goals = [g for g in user_goals if g.current_status == 'achieved']
                
                if completed_goals:
                    insights.append({
                        'type': 'achievement_recognition',
                        'title': 'Достижения',
                        'tip': f'Поздравляем! Вы достигли {len(completed_goals)} карьерных целей. Продолжайте в том же духе!',
                        'category': 'achievement'
                    })
                
                if active_goals:
                    insights.append({
                        'type': 'goal_support',
                        'title': 'Поддержка целей',
                        'tip': f'У вас есть {len(active_goals)} активных целей. Не забывайте отслеживать прогресс и корректировать планы.',
                        'category': 'support'
                    })
            
            # Add general tips based on platform usage
            total_tests = len(test_results)
            if total_tests == 0:
                insights.append({
                    'type': 'first_step',
                    'title': 'Первый шаг',
                    'tip': 'Начните с прохождения базового теста Холланда, чтобы определить свои профессиональные предпочтения.',
                    'category': 'onboarding'
                })
            elif total_tests == 1:
                insights.append({
                    'type': 'follow_up',
                    'title': 'Продолжение',
                    'tip': 'Отлично! Теперь попробуйте пройти тест Климова для более глубокого понимания ваших склонностей.',
                    'category': 'progression'
                })
            elif total_tests >= 3:
                insights.append({
                    'type': 'advanced_utilization',
                    'title': 'Расширенное использование',
                    'tip': 'Вы активно используете платформу. Рассмотрите создание карьерных целей и образовательных траекторий.',
                    'category': 'advanced'
                })
            
            return insights
        except Exception as e:
            print(f"Error getting user insights: {str(e)}")
            return []


# Global instance
ux_manager = UserExperienceManager()