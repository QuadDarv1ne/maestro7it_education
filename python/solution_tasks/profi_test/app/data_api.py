# -*- coding: utf-8 -*-
"""
API конечные точки обработки данных для ПрофиТест
Предоставляет доступ к расширенным функциям обработки и анализа данных
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.data_processor import data_processor
from app import db
from app.models import User
import json

data_api = Blueprint('data_api', __name__)


@data_api.route('/process-batch', methods=['POST'])
@login_required
def process_user_data_batch():
    """
    Обрабатывает данные пользователей пакетами.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        data = request.get_json()
        user_ids = data.get('user_ids')
        batch_size = data.get('batch_size', 100)
        
        results = data_processor.process_user_data_batch(user_ids, batch_size)
        
        if 'error' in results:
            return jsonify({
                'success': False,
                'message': results['error']
            }), 500
        
        return jsonify({
            'success': True,
            'results': results
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@data_api.route('/user/<int:user_id>/analytics', methods=['GET'])
@login_required
def get_user_profile_analytics(user_id):
    """
    Получает аналитику профиля пользователя.
    """
    try:
        if not current_user.is_admin and current_user.id != user_id:
            return jsonify({
                'success': False,
                'message': 'Доступ запрещен'
            }), 403
        
        analytics = data_processor.generate_user_profile_analytics(user_id)
        
        if 'error' in analytics:
            return jsonify({
                'success': False,
                'message': analytics['error']
            }), 404
        
        return jsonify({
            'success': True,
            'analytics': analytics
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@data_api.route('/system/analytics', methods=['GET'])
@login_required
def get_system_analytics():
    """
    Получает системную аналитику для всех пользователей.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        # Обработка всех пользователей
        results = data_processor.process_user_data_batch(batch_size=50)
        
        if 'error' in results:
            return jsonify({
                'success': False,
                'message': results['error']
            }), 500
        
        # Формирование системной аналитики
        system_analytics = {
            'total_users': results['processing_stats']['total_users'],
            'total_tests': results['processing_stats']['total_tests'],
            'total_goals': results['processing_stats']['total_goals'],
            'total_paths': results['processing_stats']['total_paths'],
            'average_engagement_score': results['processing_stats']['avg_activity_score'],
            'insights': results['user_insights'],
            'user_distribution': {
                'high_engagement': len([ins for ins in results['user_insights'] if ins['type'] == 'high_engagement']),
                'low_engagement': len([ins for ins in results['user_insights'] if ins['type'] == 'low_engagement']),
                'moderate_engagement': results['processing_stats']['total_users'] - 
                    len([ins for ins in results['user_insights'] if ins['type'] in ['high_engagement', 'low_engagement']])
            }
        }
        
        return jsonify({
            'success': True,
            'analytics': system_analytics
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@data_api.route('/user/<int:user_id>/engagement-score', methods=['GET'])
@login_required
def get_user_engagement_score(user_id):
    """
    Получает балл вовлеченности пользователя.
    """
    try:
        if not current_user.is_admin and current_user.id != user_id:
            return jsonify({
                'success': False,
                'message': 'Доступ запрещен'
            }), 403
        
        analytics = data_processor.generate_user_profile_analytics(user_id)
        
        if 'error' in analytics:
            return jsonify({
                'success': False,
                'message': analytics['error']
            }), 404
        
        return jsonify({
            'success': True,
            'engagement_score': analytics['engagement_score'],
            'max_score': 10
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@data_api.route('/user/<int:user_id>/recommendations', methods=['GET'])
@login_required
def get_user_recommendations(user_id):
    """
    Получает персонализированные рекомендации для пользователя.
    """
    try:
        if not current_user.is_admin and current_user.id != user_id:
            return jsonify({
                'success': False,
                'message': 'Доступ запрещен'
            }), 403
        
        analytics = data_processor.generate_user_profile_analytics(user_id)
        
        if 'error' in analytics:
            return jsonify({
                'success': False,
                'message': analytics['error']
            }), 404
        
        return jsonify({
            'success': True,
            'recommendations': analytics['recommendations']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@data_api.route('/compare-users', methods=['POST'])
@login_required
def compare_users():
    """
    Сравнивает пользователей между собой.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        data = request.get_json()
        user_ids = data.get('user_ids', [])
        
        if len(user_ids) < 2:
            return jsonify({
                'success': False,
                'message': 'Для сравнения требуется минимум 2 пользователя'
            }), 400
        
        if len(user_ids) > 10:
            return jsonify({
                'success': False,
                'message': 'Максимум 10 пользователей для сравнения'
            }), 400
        
        comparison_data = []
        for user_id in user_ids:
            analytics = data_processor.generate_user_profile_analytics(user_id)
            if 'error' not in analytics:
                comparison_data.append({
                    'user_id': user_id,
                    'engagement_score': analytics['engagement_score'],
                    'test_count': analytics['test_analytics']['total_tests'],
                    'goal_count': analytics['career_analytics']['total_goals'],
                    'path_count': analytics['learning_analytics']['total_paths']
                })
        
        # Сортировка по баллу вовлеченности
        comparison_data.sort(key=lambda x: x['engagement_score'], reverse=True)
        
        return jsonify({
            'success': True,
            'comparison': comparison_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@data_api.route('/user/<int:user_id>/progress-trends', methods=['GET'])
@login_required
def get_user_progress_trends(user_id):
    """
    Получает тренды прогресса пользователя со временем.
    """
    try:
        if not current_user.is_admin and current_user.id != user_id:
            return jsonify({
                'success': False,
                'message': 'Доступ запрещен'
            }), 403
        
        # Получение аналитики на разных временных интервалах
        from datetime import datetime, timedelta
        
        # Анализ за последние 30, 60 и 90 дней
        periods = [30, 60, 90]
        trend_data = {}
        
        for days in periods:
            # Получаем пользователей, зарегистрированных в указанный период
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            users_in_period = User.query.filter(User.created_at >= cutoff_date).all()
            
            if users_in_period:
                user_ids = [user.id for user in users_in_period]
                batch_results = data_processor.process_user_data_batch(user_ids, batch_size=50)
                
                if 'error' not in batch_results:
                    trend_data[f'{days}_days'] = {
                        'users_count': len(users_in_period),
                        'average_engagement': batch_results['processing_stats']['avg_activity_score'],
                        'total_activities': (
                            batch_results['processing_stats']['total_tests'] +
                            batch_results['processing_stats']['total_goals'] +
                            batch_results['processing_stats']['total_paths']
                        )
                    }
        
        return jsonify({
            'success': True,
            'trends': trend_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@data_api.route('/user/<int:user_id>/activity-patterns', methods=['GET'])
@login_required
def get_user_activity_patterns(user_id):
    """
    Получает паттерны активности пользователя.
    """
    try:
        if not current_user.is_admin and current_user.id != user_id:
            return jsonify({
                'success': False,
                'message': 'Доступ запрещен'
            }), 403
        
        from app.models import TestResult, CareerGoal, LearningPath
        from datetime import datetime
        
        # Получение данных активности
        test_results = TestResult.query.filter_by(user_id=user_id).all()
        career_goals = CareerGoal.query.filter_by(user_id=user_id).all()
        learning_paths = LearningPath.query.filter_by(user_id=user_id).all()
        
        # Анализ паттернов по дням недели
        activity_patterns = {
            'test_days': {},
            'goal_creation_days': {},
            'path_creation_days': {},
            'time_distribution': {},
            'month_comparison': {}
        }
        
        # Анализ дней недели для тестов
        for test in test_results:
            day_of_week = test.created_at.weekday()
            day_name = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'][day_of_week]
            activity_patterns['test_days'][day_name] = activity_patterns['test_days'].get(day_name, 0) + 1
        
        # Анализ дней недели для целей
        for goal in career_goals:
            if goal.created_at:
                day_of_week = goal.created_at.weekday()
                day_name = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'][day_of_week]
                activity_patterns['goal_creation_days'][day_name] = activity_patterns['goal_creation_days'].get(day_name, 0) + 1
        
        # Анализ дней недели для траекторий
        for path in learning_paths:
            if path.created_at:
                day_of_week = path.created_at.weekday()
                day_name = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'][day_of_week]
                activity_patterns['path_creation_days'][day_name] = activity_patterns['path_creation_days'].get(day_name, 0) + 1
        
        # Анализ распределения по времени суток (упрощенно)
        hour_distribution = {}
        for test in test_results:
            hour = test.created_at.hour
            hour_distribution[hour] = hour_distribution.get(hour, 0) + 1
        
        activity_patterns['time_distribution'] = hour_distribution
        
        # Анализ по месяцам
        month_names = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 
                      'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        
        monthly_activity = {}
        for test in test_results:
            month_key = f"{test.created_at.year}-{test.created_at.month:02d}"
            month_name = f"{month_names[test.created_at.month - 1]} {test.created_at.year}"
            monthly_activity[month_name] = monthly_activity.get(month_name, 0) + 1
        
        activity_patterns['month_comparison'] = monthly_activity
        
        return jsonify({
            'success': True,
            'patterns': activity_patterns
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@data_api.route('/system/engagement-distribution', methods=['GET'])
@login_required
def get_system_engagement_distribution():
    """
    Получает распределение вовлеченности пользователей в системе.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        # Получение всех пользователей
        users = User.query.all()
        engagement_scores = []
        
        # Вычисление баллов вовлеченности для каждого пользователя
        for user in users:
            analytics = data_processor.generate_user_profile_analytics(user.id)
            if 'error' not in analytics:
                engagement_scores.append(analytics['engagement_score'])
        
        # Создание распределения
        distribution = {
            'low_engagement': len([score for score in engagement_scores if score < 3]),  # 0-2.99
            'moderate_engagement': len([score for score in engagement_scores if 3 <= score < 7]),  # 3-6.99
            'high_engagement': len([score for score in engagement_scores if score >= 7]),  # 7-10
            'average_score': round(sum(engagement_scores) / len(engagement_scores), 2) if engagement_scores else 0,
            'total_users': len(users),
            'active_users': len([score for score in engagement_scores if score > 0])
        }
        
        return jsonify({
            'success': True,
            'distribution': distribution
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@data_api.route('/user/<int:user_id>/improvement-areas', methods=['GET'])
@login_required
def get_user_improvement_areas(user_id):
    """
    Получает области для улучшения для пользователя.
    """
    try:
        if not current_user.is_admin and current_user.id != user_id:
            return jsonify({
                'success': False,
                'message': 'Доступ запрещен'
            }), 403
        
        analytics = data_processor.generate_user_profile_analytics(user_id)
        
        if 'error' in analytics:
            return jsonify({
                'success': False,
                'message': analytics['error']
            }), 404
        
        improvement_areas = []
        
        # Анализ тестов
        test_analytics = analytics['test_analytics']
        if test_analytics['total_tests'] == 0:
            improvement_areas.append({
                'area': 'testing',
                'priority': 'high',
                'description': 'Необходимо пройти профессиональные тесты',
                'suggested_actions': ['Пройти тест Холланда', 'Пройти тест Климова']
            })
        elif test_analytics['total_tests'] < 3:
            improvement_areas.append({
                'area': 'testing_depth',
                'priority': 'medium',
                'description': 'Рекомендуется пройти дополнительные тесты для более точных результатов',
                'suggested_actions': ['Пройти тест на профессиональные склонности', 'Пройти тест на интересы']
            })
        
        # Анализ карьерных целей
        career_analytics = analytics['career_analytics']
        if career_analytics['total_goals'] == 0:
            improvement_areas.append({
                'area': 'career_planning',
                'priority': 'high',
                'description': 'Необходимо установить карьерные цели',
                'suggested_actions': ['Создать первую карьерную цель', 'Определить профессиональные приоритеты']
            })
        elif career_analytics['active_goals'] == 0 and career_analytics['total_goals'] > 0:
            improvement_areas.append({
                'area': 'goal_activation',
                'priority': 'medium',
                'description': 'Активируйте существующие карьерные цели',
                'suggested_actions': ['Начать работу над карьерными целями', 'Установить сроки выполнения']
            })
        
        # Анализ образовательных траекторий
        learning_analytics = analytics['learning_analytics']
        if learning_analytics['total_paths'] == 0 and career_analytics['total_goals'] > 0:
            improvement_areas.append({
                'area': 'learning_planning',
                'priority': 'medium',
                'description': 'Создайте образовательные траектории для достижения целей',
                'suggested_actions': ['Создать первую образовательную траекторию', 'Выбрать подходящие курсы']
            })
        elif learning_analytics['active_paths'] == 0 and learning_analytics['total_paths'] > 0:
            improvement_areas.append({
                'area': 'learning_activation',
                'priority': 'medium',
                'description': 'Начните обучение по существующим траекториям',
                'suggested_actions': ['Начать выполнение образовательных траекторий', 'Установить график обучения']
            })
        
        return jsonify({
            'success': True,
            'improvement_areas': improvement_areas
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500