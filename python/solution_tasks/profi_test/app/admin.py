from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, TestResult
from datetime import datetime, timedelta
import json

admin = Blueprint('admin', __name__)

@admin.route('/admin')
@login_required
def admin_dashboard():
    """Admin dashboard route"""
    if not current_user.is_admin:
        flash('Доступ запрещен', 'error')
        return redirect(url_for('main.index'))
    
    # Получить статистику
    total_users = User.query.count()
    total_tests = TestResult.query.count()
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    recent_tests = TestResult.query.order_by(TestResult.created_at.desc()).limit(10).all()
    
    # Получить статистику по методологиям
    klimov_tests = TestResult.query.filter_by(methodology='klimov').count()
    holland_tests = TestResult.query.filter_by(methodology='holland').count()
    
    stats = {
        'total_users': total_users,
        'total_tests': total_tests,
        'klimov_tests': klimov_tests,
        'holland_tests': holland_tests,
        'recent_users': recent_users,
        'recent_tests': recent_tests
    }
    
    return render_template('admin/dashboard.html', stats=stats)

@admin.route('/admin/users')
@login_required
def admin_users():
    """Manage users route"""
    if not current_user.is_admin:
        flash('Доступ запрещен', 'error')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    return render_template('admin/users.html', users=users)

@admin.route('/admin/tests')
@login_required
def admin_tests():
    """Manage tests route"""
    if not current_user.is_admin:
        flash('Доступ запрещен', 'error')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    tests = TestResult.query.order_by(TestResult.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    return render_template('admin/tests.html', tests=tests)

@admin.route('/admin/user/<int:user_id>/toggle_admin', methods=['POST'])
@login_required
def toggle_admin(user_id):
    """Toggle user admin status"""
    if not current_user.is_admin:
        return jsonify({'error': 'Доступ запрещен'}), 403
    
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        return jsonify({'error': 'Нельзя изменить свои права'}), 400
    
    user.is_admin = not user.is_admin
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'is_admin': user.is_admin,
        'message': f'Права администратора {"предоставлены" if user.is_admin else "отозваны"}'
    })

@admin.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    """Delete user"""
    if not current_user.is_admin:
        return jsonify({'error': 'Доступ запрещен'}), 403
    
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        return jsonify({'error': 'Нельзя удалить себя'}), 400
    
    username = user.username
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': f'Пользователь {username} удален'
    })

@admin.route('/admin/test/<int:test_id>/delete', methods=['POST'])
@login_required
def delete_test(test_id):
    """Delete test result"""
    if not current_user.is_admin:
        return jsonify({'error': 'Доступ запрещен'}), 403
    
    test = TestResult.query.get_or_404(test_id)
    db.session.delete(test)
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': 'Результат теста удален'
    })

@admin.route('/admin/statistics')
@login_required
def admin_statistics():
    """View detailed statistics"""
    if not current_user.is_admin:
        flash('Доступ запрещен', 'error')
        return redirect(url_for('main.index'))
    
    # Получить данные для графиков
    # Статистика регистраций
    week_ago = datetime.utcnow() - timedelta(days=7)
    month_ago = datetime.utcnow() - timedelta(days=30)
    
    weekly_registrations = User.query.filter(User.created_at >= week_ago).count()
    monthly_registrations = User.query.filter(User.created_at >= month_ago).count()
    
    # Статистика тестов по датам
    daily_tests = db.session.query(
        db.func.date(TestResult.created_at).label('date'),
        db.func.count(TestResult.id).label('count')
    ).group_by(db.func.date(TestResult.created_at)).order_by('date').all()
    
    # Популярность методологий
    methodology_stats = db.session.query(
        TestResult.methodology,
        db.func.count(TestResult.id).label('count')
    ).group_by(TestResult.methodology).all()
    
    stats = {
        'weekly_registrations': weekly_registrations,
        'monthly_registrations': monthly_registrations,
        'daily_tests': [{'date': str(row[0]), 'count': row[1]} for row in daily_tests],
        'methodology_stats': [{'methodology': row[0], 'count': row[1]} for row in methodology_stats]
    }
    
    return render_template('admin/statistics.html', stats=stats)