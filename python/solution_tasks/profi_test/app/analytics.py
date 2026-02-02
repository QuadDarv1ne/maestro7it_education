import json
from datetime import datetime, timedelta
from collections import defaultdict
import plotly.graph_objs as go
import plotly.utils
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app import db
from app.models import User, TestResult, Notification, Rating, Comment
from app.ml_recommendations import get_user_recommendations

analytics = Blueprint('analytics', __name__)

@analytics.route('/analytics')
@login_required
def dashboard():
    """Analytics dashboard for users"""
    return render_template('analytics/dashboard.html')

@analytics.route('/api/users')
@login_required
def get_users():
    """Get list of users (admin only)"""
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.isoformat() if user.created_at else None
        })
    
    return jsonify({'users': user_list})

@analytics.route('/api/analytics/overview')
@login_required
def overview():
    """Get general analytics overview"""
    # Total users
    total_users = User.query.count()
    
    # Total test results
    total_tests = TestResult.query.count()
    
    # Tests in last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_tests = TestResult.query.filter(TestResult.created_at >= thirty_days_ago).count()
    
    # Most popular methodology
    klimov_count = TestResult.query.filter_by(methodology='klimov').count()
    holland_count = TestResult.query.filter_by(methodology='holland').count()
    
    most_popular = 'Климов' if klimov_count > holland_count else 'Холланд' if holland_count > klimov_count else 'Равное распределение'
    
    # Average tests per user
    avg_tests_per_user = total_tests / total_users if total_users > 0 else 0
    
    return jsonify({
        'total_users': total_users,
        'total_tests': total_tests,
        'recent_tests': recent_tests,
        'most_popular_methodology': most_popular,
        'avg_tests_per_user': round(avg_tests_per_user, 2)
    })

@analytics.route('/api/analytics/methodology-distribution')
@login_required
def methodology_distribution():
    """Get distribution of methodologies used"""
    klimov_count = TestResult.query.filter_by(methodology='klimov').count()
    holland_count = TestResult.query.filter_by(methodology='holland').count()
    
    labels = ['Климов', 'Холланд']
    values = [klimov_count, holland_count]
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title="Распределение по методикам")
    
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify(graph_json)

@analytics.route('/api/analytics/test-trends')
@login_required
def test_trends():
    """Get test completion trends over time"""
    # Get data for last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    results = TestResult.query.filter(TestResult.created_at >= thirty_days_ago).all()
    
    # Group by date
    daily_counts = defaultdict(lambda: {'klimov': 0, 'holland': 0})
    for result in results:
        date = result.created_at.strftime('%Y-%m-%d')
        daily_counts[date][result.methodology] += 1
    
    dates = sorted(daily_counts.keys())
    klimov_data = [daily_counts[date]['klimov'] for date in dates]
    holland_data = [daily_counts[date]['holland'] for date in dates]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=klimov_data, mode='lines+markers', name='Климов'))
    fig.add_trace(go.Scatter(x=dates, y=holland_data, mode='lines+markers', name='Холланд'))
    fig.update_layout(title="Тренды прохождения тестов", xaxis_title="Дата", yaxis_title="Количество")
    
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify(graph_json)

@analytics.route('/api/analytics/dominant-categories')
@login_required
def dominant_categories():
    """Get distribution of dominant categories"""
    results = TestResult.query.all()
    
    category_counts = defaultdict(int)
    for result in results:
        try:
            results_dict = json.loads(result.results) if result.results else {}
            dominant_category = results_dict.get('dominant_category', 'Не определено')
            category_counts[dominant_category] += 1
        except:
            continue
    
    # Filter out 'Не определено' and get top 10
    filtered_counts = {k: v for k, v in category_counts.items() if k != 'Не определено'}
    top_categories = dict(sorted(filtered_counts.items(), key=lambda x: x[1], reverse=True)[:10])
    
    labels = list(top_categories.keys())
    values = list(top_categories.values())
    
    fig = go.Figure(data=[go.Bar(x=labels, y=values)])
    fig.update_layout(title="Топ популярных профессиональных сфер", xaxis_tickangle=-45)
    
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify(graph_json)

@analytics.route('/api/analytics/user-progress/<int:user_id>')
@login_required
def user_progress(user_id):
    """Get progress analytics for a specific user"""
    # Only allow access to own data or if admin
    if current_user.id != user_id and not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    user_results = TestResult.query.filter_by(user_id=user_id).order_by(TestResult.created_at).all()
    
    if not user_results:
        return jsonify({'dates': [], 'scores': {}, 'categories': []})
    
    dates = []
    scores_data = defaultdict(list)
    categories = set()
    
    for result in user_results:
        dates.append(result.created_at.strftime('%Y-%m-%d'))
        try:
            results_dict = json.loads(result.results) if result.results else {}
            scores = results_dict.get('scores', {})
            
            for category, score in scores.items():
                scores_data[category].append(float(score))
                categories.add(category)
        except:
            continue
    
    # Prepare data for chart
    fig = go.Figure()
    for category in categories:
        fig.add_trace(go.Scatter(x=dates, y=scores_data[category], mode='lines+markers', name=category))
    
    fig.update_layout(title=f"Прогресс пользователя {user_id} по категориям", xaxis_title="Дата", yaxis_title="Оценка")
    
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify(graph_json)

@analytics.route('/api/analytics/ml-effectiveness')
@login_required
def ml_effectiveness():
    """Analyze effectiveness of ML recommendations"""
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403
    
    # Get all users who received ML recommendations
    notifications = Notification.query.filter(
        Notification.title.contains('Рекомендация'),
        Notification.created_at >= datetime.utcnow() - timedelta(days=30)
    ).all()
    
    # Analyze engagement with ML notifications
    ml_notifications = [n for n in notifications if 'рекомендация' in n.title.lower() or 'рекомендация' in n.message.lower()]
    
    total_ml_notifs = len(ml_notifications)
    read_count = len([n for n in ml_notifications if n.is_read])
    
    # Calculate engagement rate
    engagement_rate = (read_count / total_ml_notifs * 100) if total_ml_notifs > 0 else 0
    
    # Get most recommended professions
    profession_counts = defaultdict(int)
    for notif in ml_notifications:
        if 'рекомендация:' in notif.title.lower():
            parts = notif.title.split(':')
            if len(parts) > 1:
                prof = parts[1].strip()
                profession_counts[prof] += 1
    
    top_recommendations = dict(sorted(profession_counts.items(), key=lambda x: x[1], reverse=True)[:5])
    
    return jsonify({
        'total_ml_notifications': total_ml_notifs,
        'read_count': read_count,
        'engagement_rate': round(engagement_rate, 2),
        'top_recommendations': top_recommendations
    })

@analytics.route('/api/analytics/comparison/<int:user_id>')
@login_required
def comparison_analysis(user_id):
    """Compare user with similar users"""
    # Only allow access to own data or if admin
    if current_user.id != user_id and not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    # Get user's latest results
    user_latest_result = TestResult.query.filter_by(user_id=user_id).order_by(TestResult.created_at.desc()).first()
    
    if not user_latest_result:
        return jsonify({'message': 'No results found for user'})
    
    try:
        user_results = json.loads(user_latest_result.results) if user_latest_result.results else {}
        user_scores = user_results.get('scores', {})
    except:
        return jsonify({'message': 'Could not parse user results'})
    
    if not user_scores:
        return jsonify({'message': 'No scores found for user'})
    
    # Find similar users based on scores
    all_results = TestResult.query.all()
    similarities = []
    
    for result in all_results:
        if result.user_id == user_id:  # Skip same user
            continue
            
        try:
            result_dict = json.loads(result.results) if result.results else {}
            result_scores = result_dict.get('scores', {})
            
            if result_scores:
                # Calculate similarity (simple approach: common categories)
                common_categories = set(user_scores.keys()) & set(result_scores.keys())
                if common_categories:
                    similarity = 0
                    for cat in common_categories:
                        diff = abs(user_scores[cat] - result_scores[cat])
                        similarity += (1 / (1 + diff))  # Higher similarity for smaller differences
                    
                    similarity /= len(common_categories)  # Average similarity
                    similarities.append((result.user_id, similarity))
        except:
            continue
    
    # Sort by similarity and get top 5
    similarities.sort(key=lambda x: x[1], reverse=True)
    top_similar = similarities[:5]
    
    # Get info about similar users
    similar_users_info = []
    for sim_user_id, sim_score in top_similar:
        user_obj = User.query.get(sim_user_id)
        if user_obj:
            # Get their dominant category
            user_results = TestResult.query.filter_by(user_id=sim_user_id).order_by(TestResult.created_at.desc()).first()
            dom_category = 'Неизвестно'
            if user_results:
                try:
                    res_dict = json.loads(user_results.results) if user_results.results else {}
                    dom_category = res_dict.get('dominant_category', 'Неизвестно')
                except:
                    pass
            
            similar_users_info.append({
                'user_id': sim_user_id,
                'username': user_obj.username,
                'similarity': round(sim_score, 3),
                'dominant_category': dom_category
            })
    
    return jsonify({
        'user_id': user_id,
        'similar_users': similar_users_info,
        'total_compared': len(similarities)
    })