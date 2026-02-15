from flask import Blueprint, render_template, jsonify, request
from app import db
from app.models.tournament import Tournament
from app.utils.fide_parser import FIDEParses
from app.utils.cfr_parser import CFRParser
from app.utils.updater import updater
from datetime import datetime, date

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Главная страница с календарем турниров"""
    # Получаем параметры фильтрации
    category = request.args.get('category', '')
    status = request.args.get('status', '')
    location = request.args.get('location', '')
    sort_by = request.args.get('sort_by', 'start_date')
    
    # Базовый запрос
    query = Tournament.query
    
    # Применяем фильтры
    if category:
        query = query.filter(Tournament.category == category)
    if status:
        query = query.filter(Tournament.status == status)
    if location:
        query = query.filter(Tournament.location.contains(location))
    
    # Применяем сортировку
    if sort_by == 'name':
        query = query.order_by(Tournament.name)
    elif sort_by == 'location':
        query = query.order_by(Tournament.location)
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
                             'sort_by': sort_by
                         })

@main_bp.route('/tournament/<int:tournament_id>')
def tournament_detail(tournament_id):
    """Страница деталей турнира"""
    tournament = Tournament.query.get_or_404(tournament_id)
    return render_template('tournament_detail.html', tournament=tournament)

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
                Tournament.location.contains(query)
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
                    'Место', 'Категория', 'Статус', 'FIDE ID'])
    
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
    from app.models.notification import Subscription
    
    try:
        email = request.form.get('email')
        if not email:
            return jsonify({'status': 'error', 'message': 'Email required'}), 400
        
        # Проверяем существующую подписку
        existing = Subscription.query.filter_by(email=email).first()
        if existing:
            existing.active = True
            existing.updated_at = datetime.utcnow()
        else:
            # Создаем новую подписку
            preferences = {
                'new_tournaments': request.form.get('new_tournaments') == 'on',
                'tournament_updates': request.form.get('tournament_updates') == 'on',
                'reminders': request.form.get('reminders') == 'on'
            }
            subscription = Subscription(email=email, preferences=preferences)
            db.session.add(subscription)
        
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Subscribed successfully'}), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@main_bp.route('/notifications/unsubscribe')
def unsubscribe_notifications():
    """Отписка от уведомлений"""
    from app.models.notification import Subscription
    
    try:
        email = request.args.get('email')
        if not email:
            return jsonify({'status': 'error', 'message': 'Email required'}), 400
        
        subscription = Subscription.query.filter_by(email=email).first()
        if subscription:
            subscription.active = False
            subscription.updated_at = datetime.utcnow()
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Unsubscribed successfully'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Subscription not found'}), 404
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@main_bp.route('/sw.js')
def service_worker():
    """Serve the service worker file"""
    from flask import send_from_directory
    return send_from_directory('static', 'sw.js', mimetype='application/javascript')

@main_bp.route('/about')
def about():
    """Страница о проекте"""
    return render_template('about.html')