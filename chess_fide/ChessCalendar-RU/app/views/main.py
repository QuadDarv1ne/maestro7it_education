from flask import render_template, request, jsonify, session, redirect, url_for
from app import db
from app.models.tournament import Tournament
from app.models.user import User
from app.models.rating import TournamentRating
from app.models.favorite import FavoriteTournament
from app.models.report import Report
from app.models.audit_log import AuditLog
from app.utils.cache import TournamentCache
from app.utils.performance_monitor import track_performance
from app.utils.validators import validate_tournament_data
from app.utils.security import log_security_event, SecurityLevel
from app.utils.notifications import create_notification
from app.utils.analytics import log_user_action
from app.utils.recommendations import RecommendationEngine
from app.utils.achievements import AchievementSystem
from app.utils.http_cache import set_cache_headers
from datetime import datetime, timedelta
import bleach
import logging

logger = logging.getLogger(__name__)

def register_main_routes(app):
    @app.route('/')
    @track_performance()
    def index():
        """Главная страница с турнирами"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', 12, type=int), 50)
            category = request.args.get('category', '')
            status = request.args.get('status', '')
            location = request.args.get('location', '')
            search_query = request.args.get('search', '').strip()
            
            # Получаем турниры с фильтрацией
            tournaments = Tournament.query
            
            if category:
                tournaments = tournaments.filter(Tournament.category == category)
            if status:
                tournaments = tournaments.filter(Tournament.status == status)
            if location:
                tournaments = tournaments.filter(Tournament.location.contains(location))
            if search_query:
                tournaments = tournaments.filter(
                    db.or_(
                        Tournament.name.contains(search_query),
                        Tournament.location.contains(search_query),
                        Tournament.description.contains(search_query)
                    )
                )
            
            tournaments = tournaments.order_by(Tournament.start_date.desc()).paginate(
                page=page, per_page=per_page, error_out=False
            )
            
            # Статистика для отображения
            stats = {
                'total_tournaments': TournamentCache.get_tournaments_stats()['total'],
                'categories': TournamentCache.get_categories_list()[:5],  # Топ-5 категорий
                'locations': TournamentCache.get_locations_list()[:5]     # Топ-5 локаций
            }
            
            # Логирование просмотра главной страницы
            if 'user_id' in session:
                log_user_action(session['user_id'], 'view_homepage', {})
            
            return render_template('index.html', 
                                 tournaments=tournaments, 
                                 stats=stats,
                                 current_filters={
                                     'category': category,
                                     'status': status,
                                     'location': location,
                                     'search': search_query
                                 }), set_cache_headers(300)  # Кэшируем на 5 минут
            
        except Exception as e:
            logger.error(f"Error in index route: {str(e)}")
            return render_template('error/500.html'), 500

    @app.route('/offline')
    def offline():
        """Оффлайн страница для PWA"""
        return render_template('offline.html')

    @app.route('/calendar')
    @track_performance()
    def calendar():
        """Календарь турниров"""
        try:
            # Получаем турниры для календаря
            start_date = request.args.get('start_date', '')
            end_date = request.args.get('end_date', '')
            
            tournaments = Tournament.query
            if start_date:
                tournaments = tournaments.filter(Tournament.start_date >= start_date)
            if end_date:
                tournaments = tournaments.filter(Tournament.end_date <= end_date)
            
            tournaments = tournaments.order_by(Tournament.start_date).all()
            
            # Подготовка данных для календаря
            calendar_data = []
            for tournament in tournaments:
                calendar_data.append({
                    'id': tournament.id,
                    'title': tournament.name,
                    'start': tournament.start_date.isoformat() if tournament.start_date else None,
                    'end': tournament.end_date.isoformat() if tournament.end_date else None,
                    'category': tournament.category,
                    'location': tournament.location,
                    'status': tournament.status
                })
            
            return render_template('calendar.html', calendar_data=calendar_data)
            
        except Exception as e:
            logger.error(f"Error in calendar route: {str(e)}")
            return render_template('error/500.html'), 500

    @app.route('/tournament/<int:tournament_id>')
    @track_performance()
    def tournament_detail(tournament_id):
        """Детали турнира"""
        try:
            tournament = TournamentCache.get_tournament_by_id(tournament_id)
            if not tournament:
                return render_template('error/404.html'), 404
            
            # Получаем рейтинги для этого турнира
            ratings = TournamentRating.query.filter_by(tournament_id=tournament_id).all()
            avg_rating = sum(r.rating for r in ratings) / len(ratings) if ratings else 0
            
            # Проверяем, является ли турнир избранным для текущего пользователя
            is_favorite = False
            if 'user_id' in session:
                user_id = session['user_id']
                favorite = FavoriteTournament.query.filter_by(
                    user_id=user_id, 
                    tournament_id=tournament_id
                ).first()
                is_favorite = favorite is not None
            
            # Логируем просмотр турнира
            if 'user_id' in session:
                log_user_action(session['user_id'], 'view_tournament', {
                    'tournament_id': tournament_id,
                    'tournament_name': tournament.name
                })
            
            return render_template('tournament_detail.html',
                                 tournament=tournament,
                                 ratings=ratings,
                                 avg_rating=avg_rating,
                                 is_favorite=is_favorite)
            
        except Exception as e:
            logger.error(f"Error in tournament_detail route: {str(e)}")
            return render_template('error/500.html'), 500

    @app.route('/add_tournament', methods=['GET', 'POST'])
    @track_performance()
    def add_tournament():
        """Добавить турнир"""
        if 'user_id' not in session:
            return redirect(url_for('user.login'))
        
        if request.method == 'POST':
            try:
                # Валидация и очистка данных
                name = bleach.clean(request.form.get('name', '').strip())
                start_date_str = request.form.get('start_date')
                end_date_str = request.form.get('end_date')
                location = bleach.clean(request.form.get('location', '').strip())
                category = bleach.clean(request.form.get('category', '').strip())
                description = bleach.clean(request.form.get('description', '').strip())
                prize_fund = bleach.clean(request.form.get('prize_fund', '').strip())
                organizer = bleach.clean(request.form.get('organizer', '').strip())
                
                # Преобразование дат
                from datetime import datetime
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
                
                # Создание нового турнира
                tournament = Tournament(
                    name=name,
                    start_date=start_date,
                    end_date=end_date,
                    location=location,
                    category=category,
                    description=description,
                    prize_fund=prize_fund,
                    organizer=organizer,
                    fide_id=request.form.get('fide_id', ''),
                    source_url=request.form.get('source_url', '')
                )
                
                # Валидация данных турнира
                errors = tournament.validate()
                if errors:
                    return render_template('rating_form.html', errors=errors, tournament=tournament), 400
                
                # Сохранение в базу данных
                db.session.add(tournament)
                db.session.commit()
                
                # Логирование аудита
                AuditLog.log_activity(
                    user_id=session['user_id'],
                    action='create_tournament',
                    details=f'Tournament {tournament.name} created with ID {tournament.id}'
                )
                
                # Инвалидация кэша
                from app.utils.cache_manager import TournamentCacheManager
                TournamentCacheManager.invalidate_tournament_cache(tournament.id)
                
                # Создание уведомления для администраторов
                create_notification(
                    user_id=None,  # Для всех администраторов
                    title='Новый турнир',
                    message=f'Добавлен новый турнир: {tournament.name}',
                    notification_type='info'
                )
                
                return redirect(url_for('main.tournament_detail', tournament_id=tournament.id))
                
            except ValueError as ve:
                return render_template('rating_form.html', 
                                     errors=['Неверный формат даты']), 400
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error adding tournament: {str(e)}")
                return render_template('error/500.html'), 500
        
        return render_template('rating_form.html')

    @app.route('/report_tournament/<int:tournament_id>', methods=['GET', 'POST'])
    def report_tournament(tournament_id):
        """Пожаловаться на турнир"""
        if 'user_id' not in session:
            return redirect(url_for('user.login'))
        
        tournament = Tournament.query.get_or_404(tournament_id)
        
        if request.method == 'POST':
            reason = request.form.get('reason')
            description = request.form.get('description', '')
            
            # Создаем жалобу
            report = Report(
                tournament_id=tournament_id,
                user_id=session['user_id'],
                reason=reason,
                description=description
            )
            
            db.session.add(report)
            db.session.commit()
            
            # Логируем жалобу
            log_security_event(
                user_id=session['user_id'],
                level=SecurityLevel.MEDIUM,
                event_type='tournament_report',
                details=f'Reported tournament {tournament_id} for reason: {reason}'
            )
            
            return jsonify({'success': True, 'message': 'Жалоба успешно отправлена'})
        
        return render_template('report_modal.html', tournament=tournament)

    @app.route('/search')
    @track_performance()
    def search():
        """Поиск турниров"""
        query = request.args.get('q', '').strip()
        category = request.args.get('category', '')
        location = request.args.get('location', '')
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 12, type=int), 50)
        
        tournaments = Tournament.query
        
        if query:
            tournaments = tournaments.filter(
                db.or_(
                    Tournament.name.contains(query),
                    Tournament.location.contains(query),
                    Tournament.description.contains(query)
                )
            )
        
        if category:
            tournaments = tournaments.filter(Tournament.category == category)
        
        if location:
            tournaments = tournaments.filter(Tournament.location.contains(location))
        
        tournaments = tournaments.order_by(Tournament.start_date.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return render_template('index.html', tournaments=tournaments, search_query=query)

    @app.route('/export/csv')
    def export_csv():
        """Экспорт турниров в CSV"""
        from io import StringIO
        import csv
        from flask import Response
        
        tournaments = Tournament.query.limit(1000).all()  # Ограничение для производительности
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Заголовки
        writer.writerow(['ID', 'Name', 'Start Date', 'End Date', 'Location', 'Category', 'Status'])
        
        # Данные
        for t in tournaments:
            writer.writerow([
                t.id, t.name, t.start_date, t.end_date, 
                t.location, t.category, t.status
            ])
        
        output.seek(0)
        
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=tournaments.csv'}
        )

    @app.route('/export/json')
    def export_json():
        """Экспорт турниров в JSON"""
        tournaments = Tournament.query.limit(1000).all()
        
        data = []
        for t in tournaments:
            data.append({
                'id': t.id,
                'name': t.name,
                'start_date': t.start_date.isoformat() if t.start_date else None,
                'end_date': t.end_date.isoformat() if t.end_date else None,
                'location': t.location,
                'category': t.category,
                'status': t.status,
                'description': t.description,
                'prize_fund': t.prize_fund,
                'organizer': t.organizer
            })
        
        from flask import jsonify
        return jsonify({
            'tournaments': data,
            'count': len(data),
            'exported_at': datetime.utcnow().isoformat()
        })

    @app.route('/widget')
    def widget():
        """Виджет для встраивания на другие сайты"""
        # Простой виджет с последними турнирами
        recent_tournaments = Tournament.query.order_by(
            Tournament.start_date.desc()
        ).limit(5).all()
        
        return render_template('widget_docs.html', tournaments=recent_tournaments)

    @app.route('/widget/documentation')
    def widget_docs():
        """Документация по виджету"""
        return render_template('widget_documentation.html')

    @app.route('/statistics')
    def statistics_dashboard():
        """Страница статистики"""
        try:
            from app.utils.analytics import analytics_service
            
            # Получаем аналитику
            stats = analytics_service.get_tournament_analytics()
            
            # Добавляем дополнительные метрики
            stats['user_engagement'] = {
                'total_users': User.query.count(),
                'active_users_monthly': User.query.filter(
                    User.last_login >= datetime.utcnow() - timedelta(days=30)
                ).count(),
                'total_ratings': TournamentRating.query.count(),
                'total_favorites': FavoriteTournament.query.count()
            }
            
            return render_template('statistics_dashboard.html', stats=stats)
            
        except Exception as e:
            logger.error(f"Error in statistics dashboard: {str(e)}")
            return render_template('error/500.html'), 500

    @app.route('/achievements')
    def achievements():
        """Страница достижений пользователей"""
        if 'user_id' not in session:
            return redirect(url_for('user.login'))
        
        try:
            from app.utils.achievements import AchievementSystem
            
            user_id = session['user_id']
            user_achievements = AchievementSystem.get_user_achievements(user_id)
            user_stats = AchievementSystem.get_user_stats(user_id)
            
            # Получаем топ пользователей по достижениям
            leaderboard = AchievementSystem.get_leaderboard(10)
            
            return render_template('user/achievements.html',
                                 user_achievements=user_achievements,
                                 user_stats=user_stats,
                                 leaderboard=leaderboard)
                                 
        except Exception as e:
            logger.error(f"Error in achievements route: {str(e)}")
            return render_template('error/500.html'), 500

    @app.route('/recommendations')
    def recommendations():
        """Рекомендации турниров для пользователя"""
        if 'user_id' not in session:
            return redirect(url_for('user.login'))
        
        try:
            user_id = session['user_id']
            engine = RecommendationEngine()
            
            # Получаем рекомендации разными методами
            collaborative_recs = engine.get_collaborative_recommendations(user_id, limit=5)
            content_based_recs = engine.get_content_based_recommendations(user_id, limit=5)
            popularity_recs = engine.get_popular_tournaments(limit=5)
            
            # Объединяем и убираем дубликаты
            all_recs = list(set(collaborative_recs + content_based_recs + popularity_recs))
            
            return render_template('recommendations.html',
                                 recommendations=all_recs[:10],  # Ограничиваем до 10
                                 collaborative=collaborative_recs,
                                 content_based=content_based_recs,
                                 popular=popularity_recs)
                                 
        except Exception as e:
            logger.error(f"Error in recommendations route: {str(e)}")
            return render_template('error/500.html'), 500

    @app.route('/tournament-map')
    def tournament_map():
        """Карта турниров"""
        try:
            # Получаем турниры с геоданными (упрощенная версия)
            tournaments = Tournament.query.filter(
                Tournament.location.isnot(None)
            ).limit(100).all()
            
            # Форматируем данные для карты (в реальной реализации здесь будет геокодирование)
            map_data = []
            for t in tournaments:
                # В реальной реализации здесь будет геокодирование адреса в координаты
                map_data.append({
                    'id': t.id,
                    'name': t.name,
                    'location': t.location,
                    'start_date': t.start_date.isoformat() if t.start_date else None,
                    'end_date': t.end_date.isoformat() if t.end_date else None,
                    'category': t.category
                })
            
            return render_template('tournament_map.html', tournaments=map_data)
            
        except Exception as e:
            logger.error(f"Error in tournament_map route: {str(e)}")
            return render_template('error/500.html'), 500

    @app.route('/notifications')
    def notifications():
        """Страница уведомлений"""
        if 'user_id' not in session:
            return redirect(url_for('user.login'))
        
        try:
            from app.models.notification import Notification
            user_id = session['user_id']
            
            # Получаем уведомления пользователя
            notifications = Notification.query.filter_by(
                user_id=user_id
            ).order_by(Notification.created_at.desc()).limit(50).all()
            
            # Помечаем как прочитанные
            unread_count = Notification.query.filter_by(
                user_id=user_id, 
                is_read=False
            ).count()
            
            if unread_count > 0:
                Notification.query.filter_by(
                    user_id=user_id, 
                    is_read=False
                ).update({Notification.is_read: True})
                db.session.commit()
            
            return render_template('notifications.html',
                                 notifications=notifications,
                                 unread_count=unread_count)
                                 
        except Exception as e:
            logger.error(f"Error in notifications route: {str(e)}")
            return render_template('error/500.html'), 500