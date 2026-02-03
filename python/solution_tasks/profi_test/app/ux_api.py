"""
User Experience API endpoints for Profi Test
Provides access to UX enhancement features
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.user_experience import ux_manager
from app.advanced_analytics import advanced_analytics_instance
from app.enhanced_ml_recommender import enhanced_ml_recommender_instance
from app import db
from app.models import User, TestResult, CareerGoal, LearningPath
import json

ux_api = Blueprint('ux_api', __name__)


@ux_api.route('/dashboard/widgets', methods=['GET'])
@login_required
def get_dashboard_widgets():
    """Get personalized dashboard widgets for the user"""
    try:
        widgets = ux_manager.get_personalized_dashboard_widgets(current_user)
        return jsonify({
            'success': True,
            'widgets': widgets
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@ux_api.route('/user/progress', methods=['GET'])
@login_required
def get_user_progress():
    """Get user's progress through the platform"""
    try:
        progress = ux_manager.get_user_progress(current_user)
        return jsonify({
            'success': True,
            'progress': progress
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@ux_api.route('/welcome-message', methods=['GET'])
@login_required
def get_welcome_message():
    """Get personalized welcome message"""
    try:
        message = ux_manager.get_welcome_message(current_user)
        return jsonify({
            'success': True,
            'message': message
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@ux_api.route('/smart-notifications', methods=['GET'])
@login_required
def get_smart_notifications():
    """Get smart notifications based on user behavior"""
    try:
        notifications = ux_manager.get_smart_notifications(current_user)
        return jsonify({
            'success': True,
            'notifications': notifications
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@ux_api.route('/adaptive-learning-path', methods=['POST'])
@login_required
def get_adaptive_learning_path():
    """Get adaptive learning path based on test results"""
    try:
        data = request.get_json()
        test_result_id = data.get('test_result_id')
        
        if not test_result_id:
            return jsonify({
                'success': False,
                'message': 'Test result ID is required'
            }), 400
        
        test_result = TestResult.query.get_or_404(test_result_id)
        
        if test_result.user_id != current_user.id and not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Access denied'
            }), 403
        
        learning_modules = ux_manager.get_adaptive_learning_path(current_user, test_result)
        return jsonify({
            'success': True,
            'learning_modules': learning_modules
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@ux_api.route('/user-insights', methods=['GET'])
@login_required
def get_user_insights():
    """Get personalized insights and tips for the user"""
    try:
        insights = ux_manager.get_user_insights_and_tips(current_user)
        return jsonify({
            'success': True,
            'insights': insights
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@ux_api.route('/onboarding-status', methods=['GET'])
@login_required
def get_onboarding_status():
    """Get user's onboarding status and next steps"""
    try:
        progress = ux_manager.get_user_progress(current_user)
        
        # Determine next steps based on what's not completed
        next_steps = []
        
        if 'first_test_taken' not in progress['completed_steps']:
            next_steps.append({
                'step': 'take_first_test',
                'title': 'Пройти первый тест',
                'description': 'Пройдите профессиональный тест, чтобы получить персональные рекомендации',
                'action_url': '/test/holland_test',
                'priority': 'high'
            })
        elif 'career_goal_set' not in progress['completed_steps']:
            next_steps.append({
                'step': 'set_career_goal',
                'title': 'Установить карьерную цель',
                'description': 'Создайте свою первую карьерную цель для планирования развития',
                'action_url': '/career-goals/create',
                'priority': 'high'
            })
        elif 'learning_path_created' not in progress['completed_steps']:
            next_steps.append({
                'step': 'create_learning_path',
                'title': 'Создать образовательную траекторию',
                'description': 'Создайте план обучения, который поможет достичь ваших целей',
                'action_url': '/learning-paths/create',
                'priority': 'medium'
            })
        elif 'portfolio_project_added' not in progress['completed_steps']:
            next_steps.append({
                'step': 'add_portfolio_project',
                'title': 'Добавить проект в портфолио',
                'description': 'Добавьте свой первый проект в портфолио',
                'action_url': '/portfolio/create',
                'priority': 'medium'
            })
        
        return jsonify({
            'success': True,
            'progress': progress,
            'next_steps': next_steps
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@ux_api.route('/recommended-content', methods=['GET'])
@login_required
def get_recommended_content():
    """Get content recommendations based on user's profile and behavior"""
    try:
        recommendations = []
        
        # Get user's test results
        test_results = TestResult.query.filter_by(user_id=current_user.id).all()
        
        if not test_results:
            # If no test results, recommend taking a test
            recommendations.append({
                'type': 'test_recommendation',
                'title': 'Пройдите профессиональный тест',
                'description': 'Начните с прохождения теста Холланда для определения ваших профессиональных интересов',
                'priority': 'high',
                'action_url': '/test/holland_test',
                'category': 'assessment'
            })
        else:
            # Get ML-based recommendations
            ml_recommendations = enhanced_ml_recommender_instance.generate_personalized_recommendations(current_user.id)
            
            # Add top ML recommendations
            for rec in ml_recommendations[:3]:
                recommendations.append({
                    'type': 'ml_recommendation',
                    'title': 'Персональная рекомендация',
                    'description': rec['content'],
                    'confidence': rec.get('confidence', 0),
                    'category': rec.get('type', 'general'),
                    'priority': 'high' if rec.get('confidence', 0) > 0.7 else 'medium'
                })
        
        # Check for career goals
        career_goals = CareerGoal.query.filter_by(user_id=current_user.id).all()
        if not career_goals:
            recommendations.append({
                'type': 'goal_setting',
                'title': 'Создайте карьерные цели',
                'description': 'Определите, чего вы хотите достичь в своей карьере',
                'priority': 'high',
                'action_url': '/career-goals/create',
                'category': 'planning'
            })
        
        # Check for learning paths
        learning_paths = LearningPath.query.filter_by(user_id=current_user.id).all()
        if not learning_paths and career_goals:
            recommendations.append({
                'type': 'learning_path',
                'title': 'Создайте образовательный план',
                'description': 'Спланируйте пути получения необходимых навыков',
                'priority': 'medium',
                'action_url': '/learning-paths/create',
                'category': 'development'
            })
        
        # Add system-wide analytics insights
        if current_user.is_admin:
            analytics_summary = advanced_analytics_instance.get_popular_categories()
            if analytics_summary['klimov_popular']:
                top_category = analytics_summary['klimov_popular'][0] if analytics_summary['klimov_popular'] else None
                if top_category:
                    recommendations.append({
                        'type': 'trend_insight',
                        'title': f'Популярная профессиональная сфера: {top_category[0]}',
                        'description': f'Эта сфера популярна среди пользователей: средняя оценка {round(top_category[1], 2)}',
                        'priority': 'low',
                        'category': 'trends'
                    })
        
        # Sort recommendations by priority
        priority_order = {'high': 1, 'medium': 2, 'low': 3}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 999))
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@ux_api.route('/user-preferences', methods=['GET', 'POST'])
@login_required
def manage_user_preferences():
    """Get or update user preferences for UX personalization"""
    try:
        from app.models import UserPreference
        
        if request.method == 'GET':
            # Get user preferences
            preferences = UserPreference.query.filter_by(user_id=current_user.id).first()
            
            if not preferences:
                # Create default preferences
                preferences = UserPreference(
                    user_id=current_user.id,
                    vacancy_alerts_enabled=True,
                    preferred_professions=json.dumps([])
                )
                db.session.add(preferences)
                db.session.commit()
            
            return jsonify({
                'success': True,
                'preferences': {
                    'vacancy_alerts_enabled': preferences.vacancy_alerts_enabled,
                    'preferred_professions': json.loads(preferences.preferred_professions) if preferences.preferred_professions else [],
                    'email_notifications': preferences.email_notifications
                }
            })
        
        elif request.method == 'POST':
            # Update user preferences
            data = request.get_json()
            
            preferences = UserPreference.query.filter_by(user_id=current_user.id).first()
            if not preferences:
                preferences = UserPreference(user_id=current_user.id)
                db.session.add(preferences)
            
            if 'vacancy_alerts_enabled' in data:
                preferences.vacancy_alerts_enabled = data['vacancy_alerts_enabled']
            
            if 'preferred_professions' in data:
                preferences.preferred_professions = json.dumps(data['preferred_professions'])
            
            if 'email_notifications' in data:
                preferences.email_notifications = data['email_notifications']
            
            preferences.updated_at = datetime.utcnow()
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Preferences updated successfully'
            })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@ux_api.route('/gamification-rewards', methods=['GET'])
@login_required
def get_gamification_rewards():
    """Get gamification rewards based on user achievements"""
    try:
        # Calculate user achievements
        test_count = TestResult.query.filter_by(user_id=current_user.id).count()
        goal_count = CareerGoal.query.filter_by(user_id=current_user.id).count()
        path_count = LearningPath.query.filter_by(user_id=current_user.id).count()
        
        rewards = []
        
        # Test completion badges
        if test_count >= 1:
            rewards.append({
                'type': 'badge',
                'name': 'First Steps',
                'description': 'Пройден первый тест',
                'earned': True,
                'icon': 'fa-clipboard-list'
            })
        
        if test_count >= 3:
            rewards.append({
                'type': 'badge',
                'name': 'Explorer',
                'description': 'Пройдено 3 и более тестов',
                'earned': True,
                'icon': 'fa-compass'
            })
        
        # Goal setting badges
        if goal_count >= 1:
            rewards.append({
                'type': 'badge',
                'name': 'Goal Setter',
                'description': 'Создана первая карьерная цель',
                'earned': True,
                'icon': 'fa-bullseye'
            })
        
        # Learning path badges
        if path_count >= 1:
            rewards.append({
                'type': 'badge',
                'name': 'Learner',
                'description': 'Создан первый план обучения',
                'earned': True,
                'icon': 'fa-graduation-cap'
            })
        
        # Achievement levels
        total_activities = test_count + goal_count + path_count
        level = min(5, max(1, total_activities // 2 + 1))  # Level 1-5 based on activities
        
        rewards.append({
            'type': 'level',
            'name': f'Level {level}',
            'description': f'Достигнут уровень {level} активности',
            'level': level,
            'icon': 'fa-star'
        })
        
        return jsonify({
            'success': True,
            'rewards': rewards,
            'total_activities': total_activities,
            'current_level': level
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


# Helper function to import datetime
from datetime import datetime