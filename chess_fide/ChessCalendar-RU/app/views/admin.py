from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from app import db
from app.models.tournament import Tournament
from app.models.user import User
from app.repositories import TournamentRepository, FavoriteRepository
from app.utils.analytics import analytics_service
from app.utils.notifications import notification_service
from app.utils.unified_cache import cache, TournamentCache
from app.utils.unified_monitoring import health_checker, performance_monitor
from datetime import datetime
import json
import csv
from io import StringIO

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
    # Статистика через репозиторий
    stats = TournamentRepository.get_statistics()
    total_tournaments = stats['total']
    recent_tournaments = TournamentRepository.get_all(limit=5)
    
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
            tournament_data = {
                'name': request.form['name'],
                'start_date': datetime.strptime(request.form['start_date'], '%Y-%m-%d').date(),
                'end_date': datetime.strptime(request.form['end_date'], '%Y-%m-%d').date(),
                'location': request.form['location'],
                'category': request.form['category'],
                'status': request.form.get('status', 'Scheduled'),
                'description': request.form.get('description'),
                'prize_fund': request.form.get('prize_fund'),
                'organizer': request.form.get('organizer'),
                'fide_id': request.form.get('fide_id'),
                'source_url': request.form.get('source_url')
            }
            
            # Создаем турнир через репозиторий
            tournament = TournamentRepository.create(tournament_data)
            
            # Инвалидируем кэш
            TournamentCache.invalidate_tournaments_cache()
            
            # Отправляем уведомления
            notification_service.send_new_tournament_notification(tournament)
            
            flash('Турнир успешно добавлен', 'success')
            return redirect(url_for('admin.tournaments'))
            
        except ValueError as e:
            flash(f'Ошибка валидации данных турнира: {str(e)}', 'error')
        except Exception as e:
            flash(f'Ошибка при добавлении турнира: {str(e)}', 'error')
    
    return render_template('admin/add_tournament.html')

@admin_bp.route('/tournaments/<int:id>/edit', methods=['GET', 'POST'])
def edit_tournament(id):
    """Редактировать турнир"""
    tournament = TournamentRepository.get_by_id(id)
    if not tournament:
        flash('Турнир не найден', 'error')
        return redirect(url_for('admin.tournaments'))
    
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
            
            # Обновляем через репозиторий
            update_data = {
                'name': request.form['name'],
                'start_date': datetime.strptime(request.form['start_date'], '%Y-%m-%d').date(),
                'end_date': datetime.strptime(request.form['end_date'], '%Y-%m-%d').date(),
                'location': request.form['location'],
                'category': request.form['category'],
                'status': request.form.get('status', 'Scheduled'),
                'description': request.form.get('description'),
                'prize_fund': request.form.get('prize_fund'),
                'organizer': request.form.get('organizer'),
                'fide_id': request.form.get('fide_id'),
                'source_url': request.form.get('source_url')
            }
            
            tournament = TournamentRepository.update(tournament, update_data)
            
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
            
        except ValueError as e:
            flash(f'Ошибка валидации данных турнира: {str(e)}', 'error')
        except Exception as e:
            flash(f'Ошибка при обновлении турнира: {str(e)}', 'error')
    
    return render_template('admin/edit_tournament.html', tournament=tournament)

@admin_bp.route('/tournaments/<int:id>/delete', methods=['POST'])
def delete_tournament(id):
    """Удалить турнир"""
    try:
        tournament = TournamentRepository.get_by_id(id)
        if not tournament:
            flash('Турнир не найден', 'error')
            return redirect(url_for('admin.tournaments'))
        
        TournamentRepository.delete(tournament)
        
        # Инвалидируем кэш
        TournamentCache.invalidate_tournaments_cache()
        
        flash('Турнир успешно удален', 'success')
    except Exception as e:
        flash(f'Ошибка при удалении турнира: {str(e)}', 'error')
    
    return redirect(url_for('admin.tournaments'))

@admin_bp.route('/tournaments/import', methods=['GET', 'POST'])
def import_tournaments():
    """Импорт турниров из файла"""
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                flash('Файл не выбран', 'error')
                return redirect(request.url)
            
            file = request.files['file']
            if file.filename == '':
                flash('Файл не выбран', 'error')
                return redirect(request.url)
            
            file_type = request.form.get('file_type', 'csv')
            
            if file_type == 'csv':
                imported_count = _import_csv_tournaments(file)
            elif file_type == 'json':
                imported_count = _import_json_tournaments(file)
            else:
                flash('Неподдерживаемый тип файла', 'error')
                return redirect(request.url)
            
            flash(f'Успешно импортировано {imported_count} турниров', 'success')
            return redirect(url_for('admin.tournaments'))
            
        except Exception as e:
            flash(f'Ошибка при импорте: {e}', 'error')
            return redirect(request.url)
    
    return render_template('admin/import_tournaments.html')

def _import_csv_tournaments(file):
    """Импорт турниров из CSV файла"""
    content = file.read().decode('utf-8')
    csv_reader = csv.DictReader(StringIO(content))
    
    imported_count = 0
    for row in csv_reader:
        try:
            # Проверяем, существует ли уже турнир с таким FIDE ID
            fide_id = row.get('fide_id') or row.get('FIDE ID')
            if fide_id:
                existing = TournamentRepository.get_by_fide_id(fide_id)
                if existing:
                    continue  # Пропускаем дубликаты
            
            # Создаем новый турнир через репозиторий
            tournament_data = {
                'name': row.get('name') or row.get('Название'),
                'start_date': datetime.strptime(row.get('start_date') or row.get('start_date'), '%Y-%m-%d').date(),
                'end_date': datetime.strptime(row.get('end_date') or row.get('end_date'), '%Y-%m-%d').date(),
                'location': row.get('location') or row.get('Место'),
                'category': row.get('category') or row.get('Категория') or 'National',
                'status': row.get('status') or row.get('Статус') or 'Scheduled',
                'description': row.get('description') or row.get('Описание'),
                'prize_fund': row.get('prize_fund') or row.get('Призовой фонд'),
                'organizer': row.get('organizer') or row.get('Организатор'),
                'fide_id': fide_id,
                'source_url': row.get('source_url') or row.get('source_url')
            }
            
            TournamentRepository.create(tournament_data)
            imported_count += 1
            
        except Exception:
            # Пропускаем строки с ошибками
            continue
    
    TournamentCache.invalidate_tournaments_cache()
    return imported_count

def _import_json_tournaments(file):
    """Импорт турниров из JSON файла"""
    content = file.read().decode('utf-8')
    data = json.loads(content)
    
    imported_count = 0
    tournaments_data = data if isinstance(data, list) else data.get('tournaments', [])
    
    for item in tournaments_data:
        try:
            # Проверяем, существует ли уже турнир с таким FIDE ID
            fide_id = item.get('fide_id')
            if fide_id:
                existing = TournamentRepository.get_by_fide_id(fide_id)
                if existing:
                    continue  # Пропускаем дубликаты
            
            # Создаем новый турнир через репозиторий
            tournament_data = {
                'name': item.get('name'),
                'start_date': datetime.strptime(item.get('start_date'), '%Y-%m-%d').date(),
                'end_date': datetime.strptime(item.get('end_date'), '%Y-%m-%d').date(),
                'location': item.get('location'),
                'category': item.get('category', 'National'),
                'status': item.get('status', 'Scheduled'),
                'description': item.get('description'),
                'prize_fund': item.get('prize_fund'),
                'organizer': item.get('organizer'),
                'fide_id': fide_id,
                'source_url': item.get('source_url')
            }
            
            TournamentRepository.create(tournament_data)
            imported_count += 1
            
        except Exception:
            # Пропускаем записи с ошибками
            continue
    
    TournamentCache.invalidate_tournaments_cache()
    return imported_count

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

@admin_bp.route('/tournaments/export')
def export_tournaments():
    """Экспорт всех турниров"""
    try:
        tournaments = TournamentRepository.get_all()
        data = [t.to_dict() for t in tournaments]
        
        return jsonify(data), 200, {
            'Content-Disposition': 'attachment; filename=all_tournaments.json'
        }
    except Exception as e:
        flash(f'Ошибка при экспорте: {str(e)}', 'error')
        return redirect(url_for('admin.tournaments'))

@admin_bp.route('/tournaments/bulk-delete', methods=['POST'])
def bulk_delete_tournaments():
    """Массовое удаление турниров"""
    try:
        data = request.get_json()
        tournament_ids = data.get('tournament_ids', [])
        
        if not tournament_ids:
            return jsonify({'status': 'error', 'message': 'No tournaments selected'}), 400
        
        deleted_count = 0
        for tournament_id in tournament_ids:
            try:
                tournament = TournamentRepository.get_by_id(tournament_id)
                if tournament:
                    TournamentRepository.delete(tournament)
                    deleted_count += 1
            except Exception:
                continue
        
        TournamentCache.invalidate_tournaments_cache()
        
        return jsonify({
            'status': 'success', 
            'message': f'Удалено {deleted_count} турниров'
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@admin_bp.route('/tournaments/bulk-update-status', methods=['POST'])
def bulk_update_status():
    """Массовое обновление статуса турниров"""
    try:
        data = request.get_json()
        tournament_ids = data.get('tournament_ids', [])
        new_status = data.get('status')
        
        if not tournament_ids or not new_status:
            return jsonify({'status': 'error', 'message': 'Missing data'}), 400
        
        updated_count = 0
        for tournament_id in tournament_ids:
            try:
                tournament = TournamentRepository.get_by_id(tournament_id)
                if tournament:
                    TournamentRepository.update(tournament, {'status': new_status})
                    updated_count += 1
            except Exception:
                continue
        
        TournamentCache.invalidate_tournaments_cache()
        
        return jsonify({
            'status': 'success', 
            'message': f'Обновлено {updated_count} турниров'
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

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

@admin_bp.route('/statistics')
def statistics():
    """Статистика турниров"""
    from datetime import date, timedelta
    from collections import Counter
    
    # Общая статистика
    total_tournaments = Tournament.query.count()
    scheduled_tournaments = Tournament.query.filter_by(status='Scheduled').count()
    ongoing_tournaments = Tournament.query.filter_by(status='Ongoing').count()
    completed_tournaments = Tournament.query.filter_by(status='Completed').count()
    
    # Статистика по категориям
    category_stats = dict(Counter([t.category for t in Tournament.query.all()]))
    
    # Статистика по статусам
    status_stats = dict(Counter([t.status for t in Tournament.query.all()]))
    
    # Турниры в ближайшие 30 дней
    today = date.today()
    next_month = today + timedelta(days=30)
    upcoming_tournaments = Tournament.query.filter(
        Tournament.start_date >= today,
        Tournament.start_date <= next_month
    ).count()
    
    # Турниры по месяцам
    monthly_stats = {}
    for i in range(1, 13):
        month_count = Tournament.query.filter(
            db.extract('month', Tournament.start_date) == i
        ).count()
        if month_count > 0:
            monthly_stats[f'Месяц {i}'] = month_count
    
    # Топ локаций
    location_stats = dict(Counter([t.location for t in Tournament.query.all()]))
    top_locations = dict(sorted(location_stats.items(), key=lambda x: x[1], reverse=True)[:10])
    
    return render_template('admin/statistics.html',
                         total_tournaments=total_tournaments,
                         scheduled_tournaments=scheduled_tournaments,
                         ongoing_tournaments=ongoing_tournaments,
                         completed_tournaments=completed_tournaments,
                         category_stats=category_stats,
                         status_stats=status_stats,
                         upcoming_tournaments=upcoming_tournaments,
                         monthly_stats=monthly_stats,
                         top_locations=top_locations)

@admin_bp.route('/analytics')
def analytics():
    """Comprehensive analytics dashboard"""
    # Get comprehensive analytics report
    analytics_report = analytics_service.get_comprehensive_report()
    
    return render_template('admin/analytics.html', analytics_report=analytics_report)


@admin_bp.route('/analytics/tournament/<int:tournament_id>')
def tournament_analytics(tournament_id):
    """Analytics for a specific tournament"""
    tournament_data = analytics_service.get_tournament_performance(tournament_id)
    
    if not tournament_data:
        flash('Турнир не найден', 'error')
        return redirect(url_for('admin.statistics'))
    
    return render_template('admin/tournament_analytics.html', 
                         tournament_data=tournament_data)
