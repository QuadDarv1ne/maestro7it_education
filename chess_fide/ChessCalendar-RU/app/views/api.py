from flask import Blueprint, request, jsonify, session
from app import db, csrf
from app.models.tournament import Tournament
from app.models.user import User
from app.models.rating import TournamentRating
from app.models.favorite import FavoriteTournament
from app.models.notification import Subscription
from app.utils.cache import TournamentCache
from app.utils.performance_monitor import track_performance
from datetime import datetime, date
from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload

api_bp = Blueprint('api', __name__, url_prefix='/api')

# CSRF защита для API (исключаем GET запросы)
@api_bp.before_request
def check_csrf():
    """Check CSRF token for non-GET requests"""
    if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
        # Проверяем токен из заголовка или JSON
        token = request.headers.get('X-CSRF-Token') or request.headers.get('X-CSRFToken')
        if not token:
            token = request.get_json(silent=True).get('_csrf_token') if request.is_json else None
        if not token:
            return jsonify({'error': 'CSRF token missing'}), 403
        
        stored_token = session.get('_csrf_token')
        if not stored_token or token != stored_token:
            return jsonify({'error': 'Invalid CSRF token'}), 403

@api_bp.route('/tournaments', methods=['GET'])
@track_performance()
def get_tournaments():
    """Get list of tournaments with pagination and filtering"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)  # Max 100 per page
        category = request.args.get('category', '')
        status = request.args.get('status', '')
        location = request.args.get('location', '')
        sort_by = request.args.get('sort_by', 'start_date')
        search_query = request.args.get('search', '').strip()
        upcoming_only = request.args.get('upcoming_only', 'false').lower() == 'true'
        
        # Base query with joinedload for ratings
        query = Tournament.query.options(
            joinedload(Tournament.ratings)
        )
        
        # Apply filters
        if category:
            query = query.filter(Tournament.category == category)
        if status:
            query = query.filter(Tournament.status == status)
        if location:
            query = query.filter(Tournament.location.contains(location))
        if search_query:
            search_filter = or_(
                Tournament.name.contains(search_query),
                Tournament.location.contains(search_query),
                Tournament.description.contains(search_query),
                Tournament.organizer.contains(search_query)
            )
            query = query.filter(search_filter)
        if upcoming_only:
            query = query.filter(
                Tournament.start_date >= date.today(),
                Tournament.status.in_(['Scheduled', 'Ongoing'])
            )
        
        # Apply sorting
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
        
        # Paginate
        tournaments = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Prepare response
        result = {
            'tournaments': [t.to_dict() for t in tournaments.items],
            'pagination': {
                'page': page,
                'pages': tournaments.pages,
                'per_page': per_page,
                'total': tournaments.total,
                'has_next': tournaments.has_next,
                'has_prev': tournaments.has_prev
            },
            'filters_applied': {
                'category': category,
                'status': status,                'location': location,
                'search': search_query,
                'upcoming_only': upcoming_only
            }
        }
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tournaments/<int:tournament_id>', methods=['GET'])
@track_performance()
def get_tournament(tournament_id):
    """Get tournament by ID"""
    try:
        tournament = TournamentCache.get_tournament_by_id(tournament_id)
        if not tournament:
            return jsonify({'error': 'Tournament not found'}), 404
        
        return jsonify(tournament.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tournaments/upcoming', methods=['GET'])
def get_upcoming_tournaments():
    """Get upcoming tournaments"""
    try:
        limit = request.args.get('limit', 10, type=int)
        tournaments = TournamentCache.get_upcoming_tournaments(limit=limit)
        
        return jsonify({
            'tournaments': [t.to_dict() for t in tournaments],
            'total': len(tournaments)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tournaments/popular', methods=['GET'])
def get_popular_tournaments():
    """Get popular tournaments"""
    try:
        limit = request.args.get('limit', 10, type=int)
        tournaments = TournamentCache.get_popular_tournaments(limit=limit)
        
        return jsonify({
            'tournaments': [t.to_dict() for t in tournaments],
            'total': len(tournaments)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/metrics/performance', methods=['GET'])
@track_performance()
def get_performance_metrics():
    """Get performance metrics for the application"""
    try:
        from app.utils.performance_monitor import perf_monitor
        
        # Get performance summary
        summary = perf_monitor.get_performance_summary()
        
        # Get slow endpoints
        slow_endpoints = perf_monitor.get_slow_endpoints(threshold=0.5)  # Endpoints taking > 0.5s
        
        # Get recent requests
        recent_requests = perf_monitor.get_recent_requests(minutes=5)
        
        return jsonify({
            'summary': summary,
            'slow_endpoints': slow_endpoints,
            'recent_requests_count': len(recent_requests),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tournaments/trending', methods=['GET'])
def get_trending_tournaments():
    """Get trending tournaments based on recent activity"""
    try:
        from app.models.preference import UserInteraction
        from datetime import datetime, timedelta
        from sqlalchemy import func
        
        # Get tournaments that had interactions in the last 7 days
        week_ago = datetime.utcnow() - timedelta(days=7)
        
        # Count interactions per tournament in the last week
        interaction_counts = db.session.query(
            UserInteraction.tournament_id,
            func.count(UserInteraction.id).label('count')
        ).filter(
            UserInteraction.created_at >= week_ago
        ).group_by(UserInteraction.tournament_id).order_by(
            func.count(UserInteraction.id).desc()
        ).limit(10).all()
        
        # Get tournament objects
        tournament_ids = [ic.tournament_id for ic in interaction_counts]
        tournaments = []
        for tid in tournament_ids:
            tournament = Tournament.query.get(tid)
            if tournament and tournament.status != 'Completed':  # Only show non-completed tournaments
                tournaments.append(tournament)
        
        return jsonify({
            'tournaments': [t.to_dict() for t in tournaments],
            'count': len(tournaments)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tournaments/categories', methods=['GET'])
def get_categories():
    """Get all tournament categories"""
    try:
        categories = TournamentCache.get_categories_list()
        return jsonify({
            'categories': categories,
            'total': len(categories)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tournaments/locations', methods=['GET'])
def get_locations():
    """Get all tournament locations"""
    try:
        locations = TournamentCache.get_locations_list()
        return jsonify({
            'locations': locations,
            'total': len(locations)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tournaments/statuses', methods=['GET'])
def get_statuses():
    """Get all tournament statuses"""
    try:
        statuses = TournamentCache.get_statuses_list()
        return jsonify({
            'statuses': statuses,
            'total': len(statuses)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/users/register', methods=['POST'])
def register_user():
    """Register a new user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return jsonify({'error': 'Username, email, and password are required'}), 400
        
        # Check if user already exists
        existing_user = User.query.filter(
            or_(User.username == username, User.email == email)
        ).first()
        
        if existing_user:
            return jsonify({'error': 'User with this username or email already exists'}), 409
        
        # Validate password
        from app.views.user import validate_password
        is_valid, msg = validate_password(password)
        if not is_valid:
            return jsonify({'error': msg}), 400
        
        # Create new user
        user = User(
            username=username,
            email=email,
            password=password
        )
        
        # Validate user data
        validation_errors = user.validate()
        if validation_errors:
            return jsonify({'error': '; '.join(validation_errors)}), 400
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/users/login', methods=['POST'])
def login_user():
    """Login user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 403
        
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'api_key': user.api_key,
                'is_admin': user.is_admin
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tournaments/<int:tournament_id>/rate', methods=['POST'])
def rate_tournament():
    """Rate a tournament"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user_id = data.get('user_id')
        rating = data.get('rating')
        review = data.get('review', '')
        
        if not user_id or rating is None:
            return jsonify({'error': 'User ID and rating are required'}), 400
        
        if not (1 <= rating <= 5):
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        
        tournament = Tournament.query.get(tournament_id)
        if not tournament:
            return jsonify({'error': 'Tournament not found'}), 404
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if user already rated this tournament
        existing_rating = TournamentRating.query.filter_by(
            user_id=user_id,
            tournament_id=tournament_id
        ).first()
        
        if existing_rating:
            # Update existing rating
            existing_rating.rating = rating
            existing_rating.review = review
            existing_rating.updated_at = datetime.utcnow()
        else:
            # Create new rating
            rating_obj = TournamentRating(
                user_id=user_id,
                tournament_id=tournament_id,
                rating=rating,
                review=review
            )
            # Validate rating data
            validation_errors = rating_obj.validate()
            if validation_errors:
                return jsonify({'error': '; '.join(validation_errors)}), 400
            db.session.add(rating_obj)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Rating submitted successfully',
            'rating': {
                'user_id': user_id,
                'tournament_id': tournament_id,
                'rating': rating,
                'review': review
            }
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tournaments/<int:tournament_id>/favorite', methods=['POST'])
def add_favorite():
    """Add tournament to favorites"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
        
        tournament = Tournament.query.get(tournament_id)
        if not tournament:
            return jsonify({'error': 'Tournament not found'}), 404
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if already favorited
        existing_favorite = FavoriteTournament.query.filter_by(
            user_id=user_id,
            tournament_id=tournament_id
        ).first()
        
        if existing_favorite:
            return jsonify({'error': 'Tournament already in favorites'}), 409
        
        # Create new favorite
        favorite = FavoriteTournament(user_id=user_id, tournament_id=tournament_id)
        db.session.add(favorite)
        db.session.commit()
        
        return jsonify({
            'message': 'Tournament added to favorites',
            'favorite': {
                'user_id': user_id,
                'tournament_id': tournament_id,
                'created_at': favorite.created_at.isoformat()
            }
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tournaments/<int:tournament_id>/favorite', methods=['DELETE'])
def remove_favorite():
    """Remove tournament from favorites"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
        
        # Find and delete favorite
        favorite = FavoriteTournament.query.filter_by(
            user_id=user_id,
            tournament_id=tournament_id
        ).first()
        
        if not favorite:
            return jsonify({'error': 'Favorite not found'}), 404
        
        db.session.delete(favorite)
        db.session.commit()
        
        return jsonify({
            'message': 'Tournament removed from favorites'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    """Get user's favorite tournaments"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        favorites = FavoriteTournament.query.filter_by(user_id=user_id).all()
        favorite_tournaments = []
        
        for fav in favorites:
            tournament = TournamentCache.get_tournament_by_id(fav.tournament_id)
            if tournament:
                favorite_tournaments.append({
                    'tournament': tournament.to_dict(),
                    'added_at': fav.created_at.isoformat()
                })
        
        return jsonify({
            'favorites': favorite_tournaments,
            'total': len(favorite_tournaments)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/notifications/subscribe', methods=['POST'])
def subscribe_to_notifications():
    """Subscribe to notifications"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email')
        preferences = data.get('preferences', {})
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        # Check if subscription already exists
        existing_subscription = Subscription.query.filter_by(email=email).first()
        
        if existing_subscription:
            # Update preferences
            existing_subscription.preferences = preferences
            existing_subscription.active = True
        else:
            # Create new subscription
            subscription = Subscription(email=email, preferences=preferences)
            db.session.add(subscription)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Successfully subscribed to notifications',
            'email': email
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/users/<int:user_id>/preferences', methods=['GET'])
def get_user_preferences(user_id):
    """Get user preferences"""
    try:
        from app.models.preference import UserPreference
        user_pref = UserPreference.query.filter_by(user_id=user_id).first()
        
        if not user_pref:
            # Create default preferences if not exist
            user_pref = UserPreference(user_id=user_id)
            db.session.add(user_pref)
            db.session.commit()
        
        return jsonify(user_pref.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/users/<int:user_id>/preferences', methods=['POST'])
def update_user_preferences(user_id):
    """Update user preferences"""
    try:
        from app.models.preference import UserPreference
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user_pref = UserPreference.query.filter_by(user_id=user_id).first()
        
        if not user_pref:
            user_pref = UserPreference(user_id=user_id)
            db.session.add(user_pref)
        
        # Update preferences if provided
        if 'category_preference' in data:
            user_pref.category_preference = data['category_preference']
        if 'location_preference' in data:
            user_pref.location_preference = data['location_preference']
        if 'difficulty_preference' in data:
            user_pref.difficulty_preference = data['difficulty_preference']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Preferences updated successfully',
            'preferences': user_pref.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/users/<int:user_id>/interactions', methods=['POST'])
def record_user_interaction(user_id):
    """Record user interaction with a tournament"""
    try:
        from app.models.preference import UserInteraction
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        tournament_id = data.get('tournament_id')
        interaction_type = data.get('interaction_type', 'view')
        interaction_value = data.get('interaction_value', 1)
        
        if not tournament_id:
            return jsonify({'error': 'Tournament ID is required'}), 400
        
        # Check if user and tournament exist
        user = User.query.get(user_id)
        tournament = Tournament.query.get(tournament_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        if not tournament:
            return jsonify({'error': 'Tournament not found'}), 404
        
        # Create interaction record
        interaction = UserInteraction(
            user_id=user_id,
            tournament_id=tournament_id,
            interaction_type=interaction_type,
            interaction_value=interaction_value
        )
        
        db.session.add(interaction)
        db.session.commit()
        
        return jsonify({
            'message': 'Interaction recorded successfully',
            'interaction': interaction.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'ChessCalendar API'
    }), 200

@api_bp.route('/users/<int:user_id>/recommendations/collaborative', methods=['GET'])
def get_collaborative_recommendations(user_id):
    """Get collaborative filtering recommendations for a user"""
    try:
        from app.utils.recommendations import RecommendationEngine
        
        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        limit = request.args.get('limit', 10, type=int)
        limit = min(max(limit, 1), 50)  # Between 1 and 50
        
        recommended_tournaments = RecommendationEngine.get_collaborative_recommendations(user_id, limit)
        
        return jsonify({
            'recommendations': [t.to_dict() for t in recommended_tournaments],
            'count': len(recommended_tournaments)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/analytics', methods=['POST'])
def track_analytics():
    """Track analytics events from frontend"""
    try:
        data = request.get_json()
        
        if not data or 'events' not in data:
            return jsonify({'error': 'No events provided'}), 400
        
        events = data.get('events', [])
        session_id = data.get('session_id')
        
        # Log analytics events (in production, save to database or analytics service)
        from app.utils.logger import logger
        
        for event in events:
            logger.info(f"Analytics: {event.get('event')} - Session: {session_id}", extra={
                'event_type': event.get('event'),
                'session_id': session_id,
                'event_data': event
            })
        
        # In production, you might want to:
        # 1. Save to a dedicated analytics database
        # 2. Send to analytics service (Google Analytics, Mixpanel, etc.)
        # 3. Process for real-time dashboards
        
        return jsonify({
            'success': True,
            'events_received': len(events)
        }), 200
        
    except Exception as e:
        from app.utils.logger import logger
        logger.error(f"Analytics tracking error: {str(e)}")
        return jsonify({'error': 'Failed to track analytics'}), 500


@api_bp.route('/tournaments/search', methods=['GET'])
def search_tournaments():
    """Search tournaments by query"""
    try:
        query = request.args.get('q', '').strip()
        
        if not query or len(query) < 2:
            return jsonify([]), 200
        
        # Search in name, location, and description
        tournaments = Tournament.query.filter(
            db.or_(
                Tournament.name.ilike(f'%{query}%'),
                Tournament.location.ilike(f'%{query}%'),
                Tournament.description.ilike(f'%{query}%')
            )
        ).order_by(Tournament.start_date.desc()).limit(20).all()
        
        return jsonify([{
            'id': t.id,
            'name': t.name,
            'location': t.location,
            'start_date': t.start_date.isoformat() if t.start_date else None,
            'end_date': t.end_date.isoformat() if t.end_date else None,
            'category': t.category,
            'rating': t.average_rating
        } for t in tournaments]), 200
        
    except Exception as e:
        from app.utils.logger import logger
        logger.error(f"Search error: {str(e)}")
        return jsonify({'error': 'Search failed'}), 500


@api_bp.route('/tournaments/<int:tournament_id>/export/ical', methods=['GET'])
def export_tournament_ical(tournament_id):
    """Export single tournament to iCal format"""
    try:
        from app.utils.ical_export import ICalExporter, create_ical_response
        
        tournament = Tournament.query.get(tournament_id)
        if not tournament:
            return jsonify({'error': 'Tournament not found'}), 404
        
        ical_content = ICalExporter.export_tournament(tournament)
        filename = f"tournament_{tournament_id}.ics"
        
        return create_ical_response(ical_content, filename)
        
    except Exception as e:
        from app.utils.logger import logger
        logger.error(f"iCal export error: {str(e)}")
        return jsonify({'error': 'Export failed'}), 500


@api_bp.route('/tournaments/export/ical', methods=['GET'])
def export_tournaments_ical():
    """Export multiple tournaments to iCal format"""
    try:
        from app.utils.ical_export import ICalExporter, create_ical_response
        
        # Get filter parameters
        category = request.args.get('category')
        location = request.args.get('location')
        days = request.args.get('days', 30, type=int)
        
        # Build query
        query = Tournament.query
        
        if category:
            query = query.filter_by(category=category)
        
        if location:
            query = query.filter(Tournament.location.ilike(f'%{location}%'))
        
        # Date range
        from datetime import datetime, timedelta
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=days)
        
        query = query.filter(
            Tournament.start_date >= start_date,
            Tournament.start_date <= end_date
        )
        
        tournaments = query.order_by(Tournament.start_date).all()
        
        ical_content = ICalExporter.export_tournaments(tournaments)
        filename = "tournaments.ics"
        
        return create_ical_response(ical_content, filename)
        
    except Exception as e:
        from app.utils.logger import logger
        logger.error(f"iCal export error: {str(e)}")
        return jsonify({'error': 'Export failed'}), 500


@api_bp.route('/users/<int:user_id>/favorites/export/ical', methods=['GET'])
def export_user_favorites_ical(user_id):
    """Export user's favorite tournaments to iCal"""
    try:
        from app.utils.ical_export import ICalExporter, create_ical_response
        
        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        ical_content = ICalExporter.export_user_favorites(user_id)
        filename = f"favorites_{user_id}.ics"
        
        return create_ical_response(ical_content, filename)
        
    except Exception as e:
        from app.utils.logger import logger
        logger.error(f"iCal export error: {str(e)}")
        return jsonify({'error': 'Export failed'}), 500


@api_bp.route('/users/<int:user_id>/achievements', methods=['GET'])
def get_user_achievements(user_id):
    """Get user achievements"""
    try:
        from app.utils.achievements import AchievementSystem
        
        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        achievements = AchievementSystem.get_user_achievements(user_id)
        stats = AchievementSystem.get_user_stats(user_id)
        
        return jsonify({
            'achievements': [a.to_dict() for a in achievements],
            'stats': stats
        }), 200
        
    except Exception as e:
        from app.utils.logger import logger
        logger.error(f"Achievements error: {str(e)}")
        return jsonify({'error': 'Failed to get achievements'}), 500


@api_bp.route('/achievements/leaderboard', methods=['GET'])
def get_achievements_leaderboard():
    """Get achievements leaderboard"""
    try:
        from app.utils.achievements import AchievementSystem
        
        limit = request.args.get('limit', 10, type=int)
        limit = min(max(limit, 1), 100)
        
        leaderboard = AchievementSystem.get_leaderboard(limit)
        
        return jsonify({
            'leaderboard': leaderboard,
            'count': len(leaderboard)
        }), 200
        
    except Exception as e:
        from app.utils.logger import logger
        logger.error(f"Leaderboard error: {str(e)}")
        return jsonify({'error': 'Failed to get leaderboard'}), 500
