from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app import db
from app.models.tournament import Tournament
from app.models.user import User
from app.models.tournament_subscription import TournamentSubscription
from app.utils.fide_parser import FIDEParses
from app.utils.cfr_parser import CFRParser
from app.utils.updater import updater
from datetime import datetime, date
import re

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Главная страница с календарем турниров"""
    # Получаем параметры фильтрации
    category = request.args.get('category', '')
    status = request.args.get('status', '')
    location = request.args.get('location', '')
    sort_by = request.args.get('sort_by', 'start_date')
    search_query = request.args.get('search', '').strip()
    
    # Базовый запрос
    query = Tournament.query
    
    # Применяем фильтры
    if category:
        query = query.filter(Tournament.category == category)
    if status:
        query = query.filter(Tournament.status == status)
    if location:
        query = query.filter(Tournament.location.contains(location))
    
    # Применяем глобальный поиск если есть
    if search_query:
        search_filter = db.or_(
            Tournament.name.contains(search_query),
            Tournament.location.contains(search_query),
            Tournament.description.contains(search_query),
            Tournament.organizer.contains(search_query)
        )
        query = query.filter(search_filter)
    
    # Применяем сортировку
    if sort_by == 'name':
        query = query.order_by(Tournament.name)
    elif sort_by == 'location':
        query = query.order_by(Tournament.location)
    elif sort_by == 'category':
        query = query.order_by(Tournament.category)
    elif sort_by == 'status':
        query = query.order_by(Tournament.status)
    else:  # start_date
        query = query.order_by(Tournament.start_date)
    
    tournaments = query.all()
    
    # Получаем уникальные значения для фильтров
    categories = db.session.query(Tournament.category).distinct().all()
    statuses = db.session.query(Tournament.status).distinct().all()
    locations = db.session.query(Tournament.location).distinct().all()
    
    return render_template('index.html', 
                         tournaments=tournaments,
                         categories=[c[0] for c in categories],
                         statuses=[s[0] for s in statuses],
                         locations=[l[0] for l in locations],
                         filters={
                             'category': category,
                             'status': status,
                             'location': location,
                             'sort_by': sort_by,
                             'search': search_query
                         })

@main_bp.route('/tournament/<int:tournament_id>')
def tournament_detail(tournament_id):
    """Страница деталей турнира"""
    tournament = Tournament.query.get_or_404(tournament_id)
    
    # Get user subscription status if logged in
    is_subscribed = False
    if 'user_id' in session:
        is_subscribed = TournamentSubscription.is_subscribed(session['user_id'], tournament_id)
        from app.utils.recommendations import RecommendationEngine
        user_id = session['user_id']
        RecommendationEngine.record_interaction(user_id, tournament_id, 'view', 1)
    
    return render_template('tournament_detail.html', 
                         tournament=tournament, 
                         is_subscribed=is_subscribed)

@main_bp.route('/api/tournaments')
def api_tournaments():
    """API для получения турниров"""
    tournaments = Tournament.query.all()
    return jsonify([t.to_dict() for t in tournaments])

@main_bp.route('/api/tournaments/<int:tournament_id>')
def api_tournament_detail(tournament_id):
    """API для получения деталей турнира"""
    tournament = Tournament.query.get_or_404(tournament_id)
    return jsonify(tournament.to_dict())

@main_bp.route('/api/tournaments/search')
def api_tournament_search():
    """API для поиска турниров"""
    query = request.args.get('q', '').strip()
    category = request.args.get('category', '')
    status = request.args.get('status', '')
    location = request.args.get('location', '')
    
    if not query and not category and not status and not location:
        return jsonify([])
    
    # Start with base query
    db_query = Tournament.query
    
    # Apply filters
    if query:
        db_query = db_query.filter(
            db.or_(
                Tournament.name.contains(query),
                Tournament.location.contains(query),
                Tournament.description.contains(query),
                Tournament.organizer.contains(query)
            )
        )
    
    if category:
        db_query = db_query.filter(Tournament.category == category)
    
    if status:
        db_query = db_query.filter(Tournament.status == status)
    
    if location:
        db_query = db_query.filter(Tournament.location.contains(location))
    
    tournaments = db_query.all()
    return jsonify([t.to_dict() for t in tournaments])

@main_bp.route('/update')
def update_tournaments():
    """Ручное обновление турниров из источников"""
    try:
        updater.update_all_sources()
        return jsonify({
            'status': 'success',
            'message': 'Данные успешно обновлены'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@main_bp.route('/export/csv')
def export_csv():
    """Экспорт турниров в CSV"""
    import csv
    from io import StringIO
    
    tournaments = Tournament.query.all()
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Заголовки
    writer.writerow(['ID', 'Название', 'Дата начала', 'Дата окончания', 
                    'Место', 'Категория', 'Статус', 'Описание', 'Призовой фонд', 'Организатор', 'FIDE ID'])
    
    # Данные
    for t in tournaments:
        writer.writerow([
            t.id,
            t.name,
            t.start_date,
            t.end_date,
            t.location,
            t.category,
            t.status,
            t.description,
            t.prize_fund,
            t.organizer,
            t.fide_id
        ])
    
    output.seek(0)
    return output.getvalue(), 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename=tournaments.csv'
    }

@main_bp.route('/export/json')
def export_json():
    """Экспорт турниров в JSON"""
    tournaments = Tournament.query.all()
    data = [t.to_dict() for t in tournaments]
    
    return jsonify(data), 200, {
        'Content-Disposition': 'attachment; filename=tournaments.json'
    }

@main_bp.route('/notifications')
def notifications():
    """Страница уведомлений пользователя"""
    from app.models.notification import Notification
    from app.models.notification import Subscription
    
    # Получаем непрочитанные уведомления (или последние 20)
    user_notifications = Notification.query.order_by(Notification.created_at.desc()).limit(20).all()
    
    # Проверяем подписку пользователя
    user_email = request.args.get('email', '')
    user_subscription = None
    if user_email:
        user_subscription = Subscription.query.filter_by(email=user_email, active=True).first()
    
    return render_template('notifications.html', 
                         notifications=user_notifications,
                         subscription=user_subscription,
                         user_email=user_email)

@main_bp.route('/notifications/subscribe', methods=['POST'])
def subscribe_notifications():
    """Подписка на уведомления"""
    from app.utils.notifications import notification_service
    
    try:
        email = request.form['email']
        preferences = {
            'new_tournaments': request.form.get('new_tournaments') == 'on',
            'updates': request.form.get('updates') == 'on',
            'daily_summary': request.form.get('daily_summary') == 'on'
        }
        
        notification_service.add_subscriber(email, preferences)
        flash(f'Подписка на уведомления для {email} успешно оформлена', 'success')
    except Exception as e:
        flash(f'Ошибка при оформлении подписки: {e}', 'error')
    
    return redirect(url_for('main.notifications'))

@main_bp.route('/notifications/unsubscribe', methods=['POST'])
def unsubscribe_notifications():
    """Отмена подписки на уведомления"""
    from app.utils.notifications import notification_service
    
    try:
        email = request.form['email']
        
        notification_service.remove_subscriber(email)
        flash(f'Подписка для {email} успешно отменена', 'success')
    except Exception as e:
        flash(f'Ошибка при отмене подписки: {e}', 'error')
    
    return redirect(url_for('main.notifications'))

@main_bp.route('/calendar')
def calendar():
    """Календарь турниров"""
    from datetime import date, timedelta
    import calendar
    
    # Получаем текущий месяц или указанный
    year = request.args.get('year', date.today().year, type=int)
    month = request.args.get('month', date.today().month, type=int)
    
    # Получаем турниры для указанного месяца
    tournaments = Tournament.query.filter(
        db.and_(
            db.extract('year', Tournament.start_date) == year,
            db.extract('month', Tournament.start_date) == month
        )
    ).all()
    
    # Создаем структуру календаря
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    
    # Группируем турниры по дням
    tournaments_by_day = {}
    for t in tournaments:
        day = t.start_date.day
        if day not in tournaments_by_day:
            tournaments_by_day[day] = []
        tournaments_by_day[day].append(t)
    
    # Получаем информацию о предыдущем и следующем месяце
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    
    today = date.today()
    
    # Создаем структуру для шаблона
    months_data = []
    for week in cal:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append(None)
            else:
                day_tournaments = tournaments_by_day.get(day, [])
                is_today = (year == today.year and month == today.month and day == today.day)
                week_data.append({
                    'day': day,
                    'tournaments': day_tournaments,
                    'is_today': is_today
                })
        months_data.append(week_data)
    
    return render_template('calendar.html', 
                         months_data=months_data, 
                         month_name=month_name, 
                         year=year,
                         current_month=month,
                         prev_month=prev_month,
                         prev_year=prev_year,
                         next_month=next_month,
                         next_year=next_year,
                         today=today)

@main_bp.route('/recommendations')
def recommendations():
    """Show tournament recommendations for the user"""
    if 'user_id' not in session:
        flash('Пожалуйста, войдите в систему для получения персональных рекомендаций', 'info')
        return redirect(url_for('main.index'))
    
    from app.utils.recommendations import RecommendationEngine
    user_id = session['user_id']
    recommended_tournaments = RecommendationEngine.get_user_recommendations(user_id)
    
    return render_template('recommendations.html', 
                           recommended_tournaments=recommended_tournaments)

@main_bp.route('/tournament/<int:tournament_id>/subscribe', methods=['POST'])
def toggle_tournament_subscription(tournament_id):
    """Toggle subscription to a specific tournament"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Необходимо войти в систему'})
    
    user_id = session['user_id']
    tournament = Tournament.query.get_or_404(tournament_id)
    
    # Check if already subscribed
    is_subscribed = TournamentSubscription.is_subscribed(user_id, tournament_id)
    
    if is_subscribed:
        # Unsubscribe
        success = TournamentSubscription.unsubscribe(user_id, tournament_id)
        if success:
            return jsonify({'success': True, 'subscribed': False, 'message': 'Отписка прошла успешно'})
        else:
            return jsonify({'success': False, 'message': 'Ошибка при отписке'})
    else:
        # Subscribe
        success = TournamentSubscription.subscribe(user_id, tournament_id)
        if success:
            return jsonify({'success': True, 'subscribed': True, 'message': 'Подписка оформлена успешно'})
        else:
            return jsonify({'success': False, 'message': 'Ошибка при подписке'})


@main_bp.route('/api/recommendations/user/<int:user_id>')
def api_user_recommendations(user_id):
    """API endpoint for getting user recommendations"""
    from app.utils.recommendations import RecommendationEngine
    from app.models.user import User
    
    # Check if user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    try:
        recommended_tournaments = RecommendationEngine.get_user_recommendations(user_id)
        return jsonify([t.to_dict() for t in recommended_tournaments])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main_bp.route('/api/analytics/report')
def api_analytics_report():
    """API endpoint for getting comprehensive analytics report"""
    from app.utils.analytics import analytics_service
    
    try:
        analytics_report = analytics_service.get_comprehensive_report()
        return jsonify(analytics_report)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main_bp.route('/api/analytics/tournament/<int:tournament_id>')
def api_tournament_analytics(tournament_id):
    """API endpoint for getting tournament-specific analytics"""
    from app.utils.analytics import analytics_service
    from app.models.tournament import Tournament
    
    # Check if tournament exists
    tournament = Tournament.query.get(tournament_id)
    if not tournament:
        return jsonify({'error': 'Tournament not found'}), 404
    
    try:
        tournament_analytics = analytics_service.get_tournament_performance(tournament_id)
        return jsonify(tournament_analytics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main_bp.route('/health')
def health_check():
    """Health check endpoint for the application"""
    from app.utils.monitoring import health_checker
    
    try:
        health_status = health_checker.get_health_status()
        health_details = health_checker.run_health_checks()
        
        return jsonify({
            'status': 'ok',
            'health_status': health_status,
            'timestamp': datetime.now().isoformat(),
            'checks': health_details
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@main_bp.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('error/404.html'), 404


@main_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    from app.utils.logging_config import get_logger
    logger = get_logger('app.errors')
    logger.error(f'Server Error: {error}', exc_info=True)
    return render_template('error/500.html'), 500