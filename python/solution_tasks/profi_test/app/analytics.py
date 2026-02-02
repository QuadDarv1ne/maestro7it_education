from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, TestResult, Notification
from datetime import datetime, timedelta
import json

analytics = Blueprint('analytics', __name__)

@analytics.route('/analytics')
@login_required
def analytics_dashboard():
    """Analytics dashboard"""
    if not current_user.is_admin:
        return jsonify({'error': 'Доступ запрещен'}), 403
    
    # Get time range from request
    days = request.args.get('days', 30, type=int)
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # User statistics
    total_users = User.query.count()
    new_users = User.query.filter(User.created_at >= start_date).count()
    
    # Test statistics
    total_tests = TestResult.query.count()
    recent_tests = TestResult.query.filter(TestResult.created_at >= start_date).count()
    
    # Methodology distribution
    klimov_tests = TestResult.query.filter_by(methodology='klimov').count()
    holland_tests = TestResult.query.filter_by(methodology='holland').count()
    
    # Daily test counts
    daily_tests = db.session.query(
        db.func.date(TestResult.created_at).label('date'),
        db.func.count(TestResult.id).label('count')
    ).filter(TestResult.created_at >= start_date).group_by(
        db.func.date(TestResult.created_at)
    ).order_by('date').all()
    
    # User activity
    active_users = db.session.query(
        TestResult.user_id,
        db.func.count(TestResult.id).label('test_count')
    ).group_by(TestResult.user_id).order_by(db.desc('test_count')).limit(10).all()
    
    # Get user details for active users
    active_users_details = []
    for user_id, test_count in active_users:
        user = User.query.get(user_id)
        if user:
            active_users_details.append({
                'username': user.username,
                'test_count': test_count,
                'is_admin': user.is_admin
            })
    
    stats = {
        'total_users': total_users,
        'new_users': new_users,
        'total_tests': total_tests,
        'recent_tests': recent_tests,
        'klimov_tests': klimov_tests,
        'holland_tests': holland_tests,
        'daily_tests': [{'date': str(row[0]), 'count': row[1]} for row in daily_tests],
        'active_users': active_users_details,
        'time_range': days
    }
    
    return render_template('analytics/dashboard.html', stats=stats)

@analytics.route('/analytics/user/<int:user_id>')
@login_required
def user_analytics(user_id):
    """Detailed user analytics"""
    if not current_user.is_admin and current_user.id != user_id:
        return jsonify({'error': 'Доступ запрещен'}), 403
    
    user = User.query.get_or_404(user_id)
    
    # Get user's test history
    tests = TestResult.query.filter_by(user_id=user_id).order_by(
        TestResult.created_at.desc()
    ).all()
    
    # Calculate statistics
    total_tests = len(tests)
    
    # Methodology usage
    methodology_counts = {}
    for test in tests:
        methodology = test.methodology
        methodology_counts[methodology] = methodology_counts.get(methodology, 0) + 1
    
    # Recent activity (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_tests = TestResult.query.filter(
        TestResult.user_id == user_id,
        TestResult.created_at >= thirty_days_ago
    ).count()
    
    user_stats = {
        'user': user,
        'total_tests': total_tests,
        'methodology_counts': methodology_counts,
        'recent_tests': recent_tests,
        'tests': tests
    }
    
    return render_template('analytics/user_detail.html', stats=user_stats)

@analytics.route('/analytics/api/chart_data')
@login_required
def chart_data():
    """API endpoint for chart data"""
    if not current_user.is_admin:
        return jsonify({'error': 'Доступ запрещен'}), 403
    
    days = request.args.get('days', 30, type=int)
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Daily registrations
    daily_registrations = db.session.query(
        db.func.date(User.created_at).label('date'),
        db.func.count(User.id).label('count')
    ).filter(User.created_at >= start_date).group_by(
        db.func.date(User.created_at)
    ).order_by('date').all()
    
    # Daily tests
    daily_tests = db.session.query(
        db.func.date(TestResult.created_at).label('date'),
        db.func.count(TestResult.id).label('count')
    ).filter(TestResult.created_at >= start_date).group_by(
        db.func.date(TestResult.created_at)
    ).order_by('date').all()
    
    # Methodology distribution
    methodology_stats = db.session.query(
        TestResult.methodology,
        db.func.count(TestResult.id).label('count')
    ).group_by(TestResult.methodology).all()
    
    return jsonify({
        'daily_registrations': [{'date': str(row[0]), 'count': row[1]} for row in daily_registrations],
        'daily_tests': [{'date': str(row[0]), 'count': row[1]} for row in daily_tests],
        'methodology_stats': [{'methodology': row[0], 'count': row[1]} for row in methodology_stats]
    })