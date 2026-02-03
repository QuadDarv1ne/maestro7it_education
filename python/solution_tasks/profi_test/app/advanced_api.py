"""
Advanced API endpoints for Profi Test
Provides access to enhanced analytics and ML features
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.advanced_analytics import advanced_analytics_instance
from app.enhanced_ml_recommender import enhanced_ml_recommender_instance
from app import db
from app.models import User, TestResult, CareerGoal, LearningPath
import json

advanced_api = Blueprint('advanced_api', __name__)


@advanced_api.route('/analytics/user-engagement', methods=['GET'])
@login_required
def get_user_engagement():
    """Get user engagement statistics"""
    try:
        stats = advanced_analytics_instance.get_user_engagement_stats()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@advanced_api.route('/analytics/test-statistics', methods=['GET'])
@login_required
def get_test_statistics():
    """Get test completion statistics"""
    try:
        stats = advanced_analytics_instance.get_test_completion_statistics()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@advanced_api.route('/analytics/popular-categories', methods=['GET'])
@login_required
def get_popular_categories():
    """Get popular professional categories"""
    try:
        categories = advanced_analytics_instance.get_popular_categories()
        return jsonify({
            'success': True,
            'data': categories
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@advanced_api.route('/analytics/career-goals', methods=['GET'])
@login_required
def get_career_goals_analytics():
    """Get career goals statistics"""
    try:
        stats = advanced_analytics_instance.get_career_goal_statistics()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@advanced_api.route('/analytics/learning-paths', methods=['GET'])
@login_required
def get_learning_paths_analytics():
    """Get learning paths statistics"""
    try:
        stats = advanced_analytics_instance.get_learning_path_statistics()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@advanced_api.route('/ml/train-model', methods=['POST'])
@login_required
def train_ml_model():
    """Train the ML recommendation model"""
    try:
        if current_user.is_admin:
            success = enhanced_ml_recommender_instance.train_model()
            if success:
                return jsonify({
                    'success': True,
                    'message': 'ML model trained successfully'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Failed to train ML model'
                }), 500
        else:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@advanced_api.route('/ml/recommendations/<int:user_id>', methods=['GET'])
@login_required
def get_ml_recommendations(user_id):
    """Get ML-based recommendations for a user"""
    try:
        if not current_user.is_admin and current_user.id != user_id:
            return jsonify({
                'success': False,
                'message': 'Access denied'
            }), 403
        
        recommendations = enhanced_ml_recommender_instance.generate_personalized_recommendations(user_id)
        return jsonify({
            'success': True,
            'data': recommendations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@advanced_api.route('/ml/similar-users/<int:user_id>', methods=['GET'])
@login_required
def get_similar_users(user_id):
    """Get users similar to the given user"""
    try:
        if not current_user.is_admin and current_user.id != user_id:
            return jsonify({
                'success': False,
                'message': 'Access denied'
            }), 403
        
        similar_users = enhanced_ml_recommender_instance.get_similar_users(user_id)
        return jsonify({
            'success': True,
            'data': similar_users
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@advanced_api.route('/ml/cluster-insights', methods=['GET'])
@login_required
def get_cluster_insights():
    """Get insights about user clusters"""
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        insights = enhanced_ml_recommender_instance.get_cluster_insights()
        return jsonify({
            'success': True,
            'data': insights
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@advanced_api.route('/analytics/comprehensive-report', methods=['GET'])
@login_required
def get_comprehensive_report():
    """Get a comprehensive analytics report"""
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        report = advanced_analytics_instance.generate_comprehensive_report()
        return jsonify({
            'success': True,
            'data': report
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@advanced_api.route('/analytics/export-csv', methods=['POST'])
@login_required
def export_analytics_csv():
    """Export analytics data to CSV"""
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        data = request.get_json()
        filename = data.get('filename') if data else None
        
        exported_file = advanced_analytics_instance.export_to_csv(filename)
        if exported_file:
            return jsonify({
                'success': True,
                'filename': exported_file,
                'message': 'Analytics exported successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to export analytics'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@advanced_api.route('/user/profile-completion/<int:user_id>', methods=['GET'])
@login_required
def get_profile_completion(user_id):
    """Get profile completion percentage for a user"""
    try:
        if not current_user.is_admin and current_user.id != user_id:
            return jsonify({
                'success': False,
                'message': 'Access denied'
            }), 403
        
        user = User.query.get_or_404(user_id)
        
        # Calculate profile completion based on various factors
        completion_score = 0
        max_score = 100
        
        # Check if user has taken tests
        test_results = TestResult.query.filter_by(user_id=user_id).count()
        if test_results > 0:
            completion_score += 25  # 25% for taking tests
        
        # Check if user has career goals
        career_goals = CareerGoal.query.filter_by(user_id=user_id).count()
        if career_goals > 0:
            completion_score += 25  # 25% for having career goals
        
        # Check if user has learning paths
        learning_paths = LearningPath.query.filter_by(user_id=user_id).count()
        if learning_paths > 0:
            completion_score += 25  # 25% for having learning paths
        
        # Check if user has notification preferences
        from app.models import UserPreference
        preferences = db.session.query(UserPreference).filter_by(user_id=user_id).first()
        if preferences:
            completion_score += 15  # 15% for having preferences
            # Additional 10% if vacancy alerts are enabled
            if preferences.vacancy_alerts_enabled:
                completion_score += 10
        
        # Cap at 100%
        completion_score = min(completion_score, max_score)
        
        return jsonify({
            'success': True,
            'data': {
                'user_id': user_id,
                'completion_percentage': completion_score,
                'test_results_count': test_results,
                'career_goals_count': career_goals,
                'learning_paths_count': learning_paths,
                'has_preferences': preferences is not None
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@advanced_api.route('/user/personal-insights/<int:user_id>', methods=['GET'])
@login_required
def get_personal_insights(user_id):
    """Get personalized insights for a user"""
    try:
        if not current_user.is_admin and current_user.id != user_id:
            return jsonify({
                'success': False,
                'message': 'Access denied'
            }), 403
        
        # Get user's test results
        test_results = TestResult.query.filter_by(user_id=user_id).all()
        
        insights = []
        
        if test_results:
            latest_result = test_results[-1]  # Most recent result
            
            # Add insight about test completion
            insights.append({
                'type': 'test_completion',
                'title': 'Тестирование завершено',
                'description': f'Вы успешно прошли тест "{latest_result.methodology}"',
                'priority': 'high'
            })
            
            # Analyze results for insights
            if latest_result.results:
                try:
                    results_dict = json.loads(latest_result.results)
                    
                    if 'dominant_category' in results_dict:
                        insights.append({
                            'type': 'dominant_category',
                            'title': 'Ваша ведущая профессиональная сфера',
                            'description': f'На основе теста выявлено, что вам наиболее подходят профессии в сфере "{results_dict["dominant_category"]}"',
                            'priority': 'high'
                        })
                    
                    if 'scores' in results_dict:
                        # Find top categories
                        sorted_scores = sorted(results_dict['scores'].items(), key=lambda x: x[1], reverse=True)
                        top_categories = sorted_scores[:2]  # Top 2 categories
                        
                        for i, (category, score) in enumerate(top_categories):
                            insights.append({
                                'type': 'category_strength',
                                'title': f'Сильная сторона #{i+1}',
                                'description': f'Вы показали высокие результаты в сфере "{category}" с оценкой {score}',
                                'priority': 'medium' if i == 0 else 'low'
                            })
                
                except json.JSONDecodeError:
                    insights.append({
                        'type': 'error',
                        'title': 'Ошибка анализа результатов',
                        'description': 'Не удалось проанализировать ваши результаты теста',
                        'priority': 'low'
                    })
        
        # Check career goals
        career_goals = CareerGoal.query.filter_by(user_id=user_id).all()
        if not career_goals:
            insights.append({
                'type': 'suggestion',
                'title': 'Создайте карьерные цели',
                'description': 'Установите карьерные цели, чтобы лучше планировать свое профессиональное развитие',
                'priority': 'medium'
            })
        else:
            active_goals = [g for g in career_goals if g.current_status in ['planning', 'in_progress']]
            if active_goals:
                insights.append({
                    'type': 'goals_active',
                    'title': 'Активные карьерные цели',
                    'description': f'У вас есть {len(active_goals)} активных карьерных целей',
                    'priority': 'medium'
                })
        
        # Check learning paths
        learning_paths = LearningPath.query.filter_by(user_id=user_id).all()
        if not learning_paths:
            insights.append({
                'type': 'suggestion',
                'title': 'Создайте образовательные траектории',
                'description': 'Создайте план обучения, чтобы достичь своих карьерных целей',
                'priority': 'medium'
            })
        else:
            in_progress_paths = [lp for lp in learning_paths if lp.status == 'in_progress']
            completed_paths = [lp for lp in learning_paths if lp.status == 'completed']
            
            if completed_paths:
                insights.append({
                    'type': 'achievement',
                    'title': 'Завершенные траектории',
                    'description': f'Поздравляем! Вы завершили {len(completed_paths)} образовательных траекторий',
                    'priority': 'high'
                })
        
        # Sort insights by priority
        priority_order = {'high': 1, 'medium': 2, 'low': 3}
        insights.sort(key=lambda x: priority_order.get(x['priority'], 999))
        
        return jsonify({
            'success': True,
            'data': {
                'user_id': user_id,
                'insights': insights,
                'total_insights': len(insights)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500