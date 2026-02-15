from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from app import db
from app.models.tournament import Tournament
from app.models.user import User
from app.utils.notifications import notification_service
from app.utils.cache import cache_service, TournamentCache
from app.utils.monitoring import health_checker, performance_monitor
from datetime import datetime
import json

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Функция для проверки аутентификации администратора
@admin_bp.before_request
def admin_required():
    """Проверка прав администратора"""
    # Проверяем, авторизован ли пользователь
    if 'user_id' not in session:
        return redirect(url_for('admin.login'))
    
    # Проверяем, является ли пользователь администратором
    user = User.query.get(session['user_id'])
    if not user or not user.is_admin:
        return redirect(url_for('admin.login'))

@admin_bp.route('/')
def dashboard():
    """Админ-панель"""
    # Статистика
    total_tournaments = Tournament.query.count()
    recent_tournaments = Tournament.query.order_by(Tournament.created_at.desc()).limit(5).all()
    
    # Статистика кэша
    cache_stats = cache_service.get_stats()
    
    # Статистика уведомлений
    notification_stats = notification_service.get_subscriber_stats()
    
    # Статус здоровья системы
    health_status = health_checker.get_health_status()
    health_details = health_checker.run_health_checks()
    
    # Метрики производительности
    performance_metrics = performance_monitor.get_metrics_summary()
    
    return render_template('admin/dashboard.html',
                         total_tournaments=total_tournaments,
                         recent_tournaments=recent_tournaments,
                         cache_stats=cache_stats,
                         notification_stats=notification_stats,
                         health_status=health_status,
                         health_details=health_details,
                         performance_metrics=performance_metrics)

@admin_bp.route('/tournaments')
def tournaments():
    """Управление турнирами"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    tournaments = Tournament.query.order_by(Tournament.start_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin/tournaments.html', tournaments=tournaments)

@admin_bp.route('/tournaments/add', methods=['GET', 'POST'])
def add_tournament():
    """Добавить турнир вручную"""
    if request.method == 'POST':
        try:
            tournament = Tournament(
                name=request.form['name'],
                start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d').date(),
                end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d').date(),
                location=request.form['location'],
                category=request.form['category'],
                status=request.form.get('status', 'Scheduled'),
                fide_id=request.form.get('fide_id'),
                source_url=request.form.get('source_url')
            )
            
            db.session.add(tournament)
            db.session.commit()
            
            # Инвалидируем кэш
            TournamentCache.invalidate_tournaments_cache()
            
            # Отправляем уведомления
            notification_service.send_new_tournament_notification(tournament)
            
            flash('Турнир успешно добавлен', 'success')
            return redirect(url_for('admin.tournaments'))
            
        except Exception as e:
            flash(f'Ошибка при добавлении турнира: {e}', 'error')
    
    return render_template('admin/add_tournament.html')

@admin_bp.route('/tournaments/<int:id>/edit', methods=['GET', 'POST'])
def edit_tournament(id):
    """Редактировать турнир"""
    tournament = Tournament.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Сохраняем старые значения для уведомлений
            old_values = {
                'name': tournament.name,
                'start_date': tournament.start_date,
                'end_date': tournament.end_date,
                'location': tournament.location,
                'category': tournament.category,
                'status': tournament.status
            }
            
            # Обновляем значения
            tournament.name = request.form['name']
            tournament.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
            tournament.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
            tournament.location = request.form['location']
            tournament.category = request.form['category']
            tournament.status = request.form.get('status', 'Scheduled')
            tournament.fide_id = request.form.get('fide_id')
            tournament.source_url = request.form.get('source_url')
            tournament.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            # Инвалидируем кэш
            TournamentCache.invalidate_tournaments_cache()
            
            # Подготавливаем изменения для уведомлений
            changes = {}
            for field, old_val in old_values.items():
                new_val = getattr(tournament, field)
                if old_val != new_val:
                    changes[field] = (str(old_val), str(new_val))
            
            # Отправляем уведомления об изменениях
            if changes:
                notification_service.send_tournament_update_notification(tournament, changes)
            
            flash('Турнир успешно обновлен', 'success')
            return redirect(url_for('admin.tournaments'))
            
        except Exception as e:
            flash(f'Ошибка при обновлении турнира: {e}', 'error')
    
    return render_template('admin/edit_tournament.html', tournament=tournament)

@admin_bp.route('/tournaments/<int:id>/delete', methods=['POST'])
def delete_tournament(id):
    """Удалить турнир"""
    try:
        tournament = Tournament.query.get_or_404(id)
        db.session.delete(tournament)
        db.session.commit()
        
        # Инвалидируем кэш
        TournamentCache.invalidate_tournaments_cache()
        
        flash('Турнир успешно удален', 'success')
    except Exception as e:
        flash(f'Ошибка при удалении турнира: {e}', 'error')
    
    return redirect(url_for('admin.tournaments'))

@admin_bp.route('/cache')
def cache_management():
    """Управление кэшем"""
    cache_stats = cache_service.get_stats()
    return render_template('admin/cache.html', cache_stats=cache_stats)

@admin_bp.route('/cache/clear', methods=['POST'])
def clear_cache():
    """Очистить кэш"""
    try:
        cache_service.clear()
        TournamentCache.invalidate_tournaments_cache()
        flash('Кэш успешно очищен', 'success')
    except Exception as e:
        flash(f'Ошибка при очистке кэша: {e}', 'error')
    
    return redirect(url_for('admin.cache_management'))

@admin_bp.route('/notifications')
def notifications():
    """Управление уведомлениями"""
    from app.models.notification import Subscription
    subscribers = Subscription.query.all()
    stats = notification_service.get_subscriber_stats()
    return render_template('admin/notifications.html', subscribers=subscribers, stats=stats)

@admin_bp.route('/notifications/add_subscriber', methods=['POST'])
def add_subscriber():
    """Добавить подписчика"""
    try:
        email = request.form['email']
        preferences = {
            'new_tournaments': request.form.get('new_tournaments') == 'on',
            'updates': request.form.get('updates') == 'on',
            'daily_summary': request.form.get('daily_summary') == 'on'
        }
        
        notification_service.add_subscriber(email, preferences)
        flash(f'Подписчик {email} успешно добавлен', 'success')
    except Exception as e:
        flash(f'Ошибка при добавлении подписчика: {e}', 'error')
    
    return redirect(url_for('admin.notifications'))

@admin_bp.route('/notifications/remove_subscriber', methods=['POST'])
def remove_subscriber():
    """Удалить подписчика"""
    try:
        email = request.form['email']
        
        # Удаляем подписчика из базы данных
        from app.models.notification import Subscription
        subscription = Subscription.query.filter_by(email=email).first()
        if subscription:
            db.session.delete(subscription)
            db.session.commit()
            flash(f'Подписчик {email} успешно удален', 'success')
        else:
            flash(f'Подписчик {email} не найден', 'error')
    except Exception as e:
        flash(f'Ошибка при удалении подписчика: {e}', 'error')
    
    return redirect(url_for('admin.notifications'))

@admin_bp.route('/health')
def health_check():
    """Проверка состояния системы"""
    health_status = health_checker.get_health_status()
    health_details = health_checker.run_health_checks()
    
    return render_template('admin/health.html', 
                         health_status=health_status, 
                         health_details=health_details)

@admin_bp.route('/api/health')
def api_health():
    """API для проверки состояния"""
    return jsonify(health_checker.run_health_checks())

@admin_bp.route('/api/metrics')
def api_metrics():
    """API для получения метрик производительности"""
    return jsonify(performance_monitor.get_metrics_summary())

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Страница входа для администратора"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_admin:
            session['user_id'] = user.id
            session['username'] = user.username
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Перенаправляем на главную страницу админки
            next_url = request.args.get('next')
            return redirect(next_url or url_for('admin.dashboard'))
        else:
            flash('Неправильное имя пользователя или пароль', 'error')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    """Выход из аккаунта администратора"""
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('main.index'))

@admin_bp.route('/settings')
def settings():
    """Настройки приложения"""
    import sys
    from flask import __version__ as flask_version
    from app.models.user import User
    from app.models.tournament import Tournament
    
    def python_version():
        return f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'
    
    def flask_version_func():
        return flask_version
    
    def total_users():
        return User.query.count()
    
    def total_tournaments():
        return Tournament.query.count()
    
    return render_template('admin/settings.html',
                         python_version=python_version,
                         flask_version=flask_version_func,
                         total_users=total_users,
                         total_tournaments=total_tournaments)