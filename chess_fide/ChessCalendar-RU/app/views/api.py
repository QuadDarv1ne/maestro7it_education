from flask import Blueprint, request, jsonify, session
from app import db, csrf
from app.models.tournament import Tournament
from app.models.user import User
from app.models.rating import TournamentRating
from app.models.notification import Subscription
from app.repositories import TournamentRepository, FavoriteRepository
from app.utils.unified_cache import TournamentCache
from app.utils.performance_monitor import track_performance
from datetime import datetime, date, timedelta
from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload
import logging

logger = logging.getLogger(__name__)

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
        
        # Use optimized query to avoid loading all ratings upfront
        query = Tournament.query
        
        # Apply filters
        if category:
            query = query.filter(Tournament.category == category)
        if status:
            query = query.filter(Tournament.status == status)
        if location:
            query = query.filter(Tournament.location.contains(location))
        if search_query:
            search_filter = or_(
                Tournament.name.ilike(f'%{search_query}%'),
                Tournament.location.ilike(f'%{search_query}%'),
                Tournament.description.ilike(f'%{search_query}%'),
                Tournament.organizer.ilike(f'%{search_query}%')
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
        
        # Use optimized pagination from our utility
        from app.utils.db_optimization import PaginationHelper
        pagination_result = PaginationHelper.paginate(query, page, per_page)
        
        # Prepare response
        result = {
            'tournaments': [t.to_dict() for t in pagination_result['items']],
            'pagination': {
                'page': pagination_result['page'],
                'pages': pagination_result['pages'],
                'per_page': pagination_result['per_page'],
                'total': pagination_result['total'],
                'has_next': pagination_result['has_next'],
                'has_prev': pagination_result['has_prev']
            },
            'filters_applied': {
                'category': category,
                'status': status,
                'location': location,
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
        
        # Get tournament objects efficiently with a single query
        tournament_ids = [ic.tournament_id for ic in interaction_counts]
        if tournament_ids:
            tournaments = Tournament.query.filter(
                Tournament.id.in_(tournament_ids),
                Tournament.status != 'Completed'  # Only show non-completed tournaments
            ).all()
            
            # Sort tournaments to match the interaction count order
            tournament_dict = {t.id: t for t in tournaments}
            sorted_tournaments = [tournament_dict[tid] for tid in tournament_ids if tid in tournament_dict]
        else:
            sorted_tournaments = []
        
        return jsonify({
            'tournaments': [t.to_dict() for t in sorted_tournaments],
            'count': len(sorted_tournaments)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tournaments/categories', methods=['GET'])
def get_categories():
    """Get all tournament categories"""
    try:
        categories = TournamentCache.get_categories_list()
        return jsonify({
            'categories': categories if categories else [],
            'total': len(categories) if categories else 0
        }), 200
    
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        return jsonify({
            'categories': [],
            'total': 0,
            'error': 'Failed to load categories'
        }), 500

@api_bp.route('/tournaments/locations', methods=['GET'])
def get_locations():
    """Get all tournament locations"""
    try:
        locations = TournamentCache.get_locations_list()
        return jsonify({
            'locations': locations if locations else [],
            'total': len(locations) if locations else 0
        }), 200
    
    except Exception as e:
        logger.error(f"Error getting locations: {e}")
        return jsonify({
            'locations': [],
            'total': 0,
            'error': 'Failed to load locations'
        }), 500

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
def rate_tournament(tournament_id):
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
def add_favorite(tournament_id):
    """Add tournament to favorites"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
        
        tournament = TournamentRepository.get_by_id(tournament_id)
        if not tournament:
            return jsonify({'error': 'Tournament not found'}), 404
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if already favorited and add
        favorite = FavoriteRepository.add_favorite(user_id, tournament_id)
        
        if not favorite:
            return jsonify({'error': 'Failed to add to favorites'}), 500
        
        # Check if it was already in favorites
        if favorite.created_at < datetime.utcnow() - timedelta(seconds=1):
            return jsonify({'error': 'Tournament already in favorites'}), 409
        
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
def remove_favorite(tournament_id):
    """Remove tournament from favorites"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
        
        # Remove favorite using repository
        success = FavoriteRepository.remove_favorite(user_id, tournament_id)
        
        if not success:
            return jsonify({'error': 'Favorite not found'}), 404
        
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
        
        favorites = FavoriteRepository.get_user_favorites(user_id)
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

@api_bp.route('/tournaments/<int:tournament_id>/unfavorite', methods=['POST'])
def unfavorite_tournament(tournament_id):
    """Remove tournament from favorites (POST version for consistency)"""
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id') or session.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 401
        
        success = FavoriteRepository.remove_favorite(user_id, tournament_id)
        
        if not success:
            return jsonify({'error': 'Favorite not found'}), 404
        
        return jsonify({
            'success': True,
            'message': 'Tournament removed from favorites',
            'is_favorite': False
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tournaments/<int:tournament_id>/toggle-favorite', methods=['POST'])
def toggle_favorite(tournament_id):
    """Toggle tournament favorite status"""
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id') or session.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 401
        
        # Check if tournament exists
        tournament = TournamentRepository.get_by_id(tournament_id)
        if not tournament:
            return jsonify({'error': 'Tournament not found'}), 404
        
        # Toggle favorite using repository
        is_favorite, message = FavoriteRepository.toggle_favorite(user_id, tournament_id)
        
        return jsonify({
            'success': True,
            'is_favorite': is_favorite,
            'message': message
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
    """Search tournaments with advanced filtering"""
    try:
        # Get all search parameters
        query = request.args.get('q', '').strip()
        category = request.args.get('category', '')
        location = request.args.get('location', '')
        status = request.args.get('status', '')
        start_date = request.args.get('start_date', '')
        end_date = request.args.get('end_date', '')
        min_rating = request.args.get('min_rating', type=float)
        max_rating = request.args.get('max_rating', type=float)
        sort_by = request.args.get('sort_by', 'start_date')  # start_date, rating, name
        sort_order = request.args.get('sort_order', 'asc')  # asc, desc
        limit = min(request.args.get('limit', 20, type=int), 100)  # Max 100 results
        
        # Build query
        search_query = Tournament.query
        
        # Apply search term if provided
        if query and len(query) >= 2:
            search_query = search_query.filter(
                db.or_(
                    Tournament.name.ilike(f'%{query}%'),
                    Tournament.location.ilike(f'%{query}%'),
                    Tournament.description.ilike(f'%{query}%')
                )
            )
        
        # Apply filters
        if category:
            search_query = search_query.filter(Tournament.category == category)
        
        if location:
            search_query = search_query.filter(Tournament.location.ilike(f'%{location}%'))
        
        if status:
            search_query = search_query.filter(Tournament.status == status)
        
        if start_date:
            from datetime import datetime
            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
                search_query = search_query.filter(Tournament.start_date >= start_dt)
            except ValueError:
                pass  # Invalid date format, ignore filter
        
        if end_date:
            from datetime import datetime
            try:
                end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
                search_query = search_query.filter(Tournament.end_date <= end_dt)
            except ValueError:
                pass  # Invalid date format, ignore filter
        
        if min_rating is not None or max_rating is not None:
            # Note: average_rating is calculated dynamically in to_dict, so we can't filter on it directly
            # We would need to join with ratings table to filter on actual rating values
            # For now, we'll skip rating filters since they can't be applied efficiently without joins
            pass
        
        # Apply sorting
        if sort_by == 'rating':
            order_column = Tournament.average_rating  # This will use the property
        elif sort_by == 'name':
            order_column = Tournament.name
        else:  # default to start_date
            order_column = Tournament.start_date
        
        if sort_order == 'desc':
            search_query = search_query.order_by(order_column.desc())
        else:
            search_query = search_query.order_by(order_column.asc())
        
        # Execute query with limit
        tournaments = search_query.limit(limit).all()
        
        return jsonify([{
            'id': t.id,
            'name': t.name,
            'location': t.location,
            'start_date': t.start_date.isoformat() if t.start_date else None,
            'end_date': t.end_date.isoformat() if t.end_date else None,
            'category': t.category,
            'status': t.status,
            'rating': t.get_average_rating(),  # Use method to get actual rating
            'description': t.description[:100] + '...' if t.description and len(t.description) > 100 else t.description
        } for t in tournaments]), 200
        
    except Exception as e:
        from app.utils.logger import logger
        logger.error(f"Advanced search error: {str(e)}")
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


@api_bp.route('/tournaments/popular', methods=['GET'])
@track_performance()
def get_popular_tournaments():
    """Get popular tournaments based on user interactions"""
    try:
        from app.utils.recommendations import RecommendationEngine
        
        limit = request.args.get('limit', 10, type=int)
        limit = min(max(limit, 1), 50)
        
        popular_tournaments = RecommendationEngine.get_popular_tournaments(limit=limit)
        
        return jsonify({
            'tournaments': [t.to_dict() for t in popular_tournaments],
            'count': len(popular_tournaments)
        }), 200
        
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Popular tournaments error: {str(e)}")
        return jsonify({'error': 'Failed to get popular tournaments'}), 500


@api_bp.route('/tournaments/nearby', methods=['GET'])
@track_performance()
def get_nearby_tournaments():
    """Get tournaments near a specific location"""
    try:
        latitude = request.args.get('lat', type=float)
        longitude = request.args.get('lon', type=float)
        radius = request.args.get('radius', 100, type=int)  # in km
        limit = request.args.get('limit', 10, type=int)
        
        if latitude is None or longitude is None:
            return jsonify({'error': 'Latitude and longitude are required'}), 400
        
        # This would require geocoding functionality which isn't fully implemented
        # For now, return tournaments that have location info
        tournaments = Tournament.query.filter(
            Tournament.location.isnot(None)
        ).limit(limit).all()
        
        return jsonify({
            'tournaments': [t.to_dict() for t in tournaments],
            'count': len(tournaments)
        }), 200
        
    except Exception as e:
        from app.utils.logger import logger
        logger.error(f"Nearby tournaments error: {str(e)}")
        return jsonify({'error': 'Failed to get nearby tournaments'}), 500


@api_bp.route('/tournaments/<int:tournament_id>/similar', methods=['GET'])
@track_performance()
def get_similar_tournaments(tournament_id):
    """Get tournaments similar to the given tournament"""
    try:
        tournament = Tournament.query.get_or_404(tournament_id)
        
        limit = request.args.get('limit', 10, type=int)
        limit = min(max(limit, 1), 20)
        
        # Find similar tournaments based on category, location, and date proximity
        similar_tournaments = Tournament.query.filter(
            Tournament.id != tournament_id,
            Tournament.category == tournament.category,
            Tournament.start_date.between(
                tournament.start_date.replace(day=1),
                tournament.start_date.replace(day=28) + timedelta(days=7)
            )
        ).limit(limit).all()
        
        return jsonify({
            'tournaments': [t.to_dict() for t in similar_tournaments],
            'count': len(similar_tournaments),
            'reference_tournament': tournament.to_dict()
        }), 200
        
    except Exception as e:
        from app.utils.logger import logger
        logger.error(f"Similar tournaments error: {str(e)}")
        return jsonify({'error': 'Failed to get similar tournaments'}), 500


@api_bp.route('/tournaments/upcoming-by-category', methods=['GET'])
@track_performance()
def get_upcoming_by_category():
    """Get upcoming tournaments grouped by category"""
    try:
        from datetime import datetime
        
        # Get all upcoming tournaments
        upcoming_tournaments = Tournament.query.filter(
            Tournament.start_date >= datetime.now().date(),
            Tournament.status.in_(['Scheduled', 'Registration Open'])
        ).order_by(Tournament.start_date).all()
        
        # Group by category
        grouped_tournaments = {}
        for tournament in upcoming_tournaments:
            category = tournament.category
            if category not in grouped_tournaments:
                grouped_tournaments[category] = []
            grouped_tournaments[category].append(tournament.to_dict())
        
        return jsonify({
            'categories': grouped_tournaments,
            'total_count': len(upcoming_tournaments)
        }), 200
        
    except Exception as e:
        from app.utils.logger import logger
        logger.error(f"Upcoming by category error: {str(e)}")
        return jsonify({'error': 'Failed to get upcoming tournaments by category'}), 500


@api_bp.route('/tournaments/statistics', methods=['GET'])
@track_performance()
def get_tournament_statistics():
    """Get comprehensive tournament statistics"""
    try:
        from app.utils.analytics import analytics_service
        
        # Get comprehensive statistics
        stats = {
            'general': analytics_service.get_tournament_analytics(),
            'by_category': {},
            'by_location': {},
            'by_status': {}
        }
        
        # Get category breakdown
        category_stats = db.session.query(
            Tournament.category,
            db.func.count(Tournament.id)
        ).group_by(Tournament.category).all()
        stats['by_category'] = dict(category_stats)
        
        # Get location breakdown
        location_stats = db.session.query(
            Tournament.location,
            db.func.count(Tournament.id)
        ).group_by(Tournament.location).order_by(
            db.func.count(Tournament.id).desc()
        ).limit(10).all()
        stats['by_location'] = dict(location_stats)
        
        # Get status breakdown
        status_stats = db.session.query(
            Tournament.status,
            db.func.count(Tournament.id)
        ).group_by(Tournament.status).all()
        stats['by_status'] = dict(status_stats)
        
        return jsonify(stats), 200
        
    except Exception as e:
        from app.utils.logger import logger
        logger.error(f"Tournament statistics error: {str(e)}")
        return jsonify({'error': 'Failed to get tournament statistics'}), 500


@api_bp.route('/favorites', methods=['POST'])
def manage_favorites():
    """Manage user favorites (add/remove)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        tournament_id = data.get('tournament_id')
        action = data.get('action')  # 'add' or 'remove'
        user_id = session.get('user_id')  # Get from session if logged in
        
        if not tournament_id:
            return jsonify({'error': 'Tournament ID is required'}), 400
        
        if not action or action not in ['add', 'remove']:
            return jsonify({'error': 'Action must be "add" or "remove"'}), 400
        
        # If user is logged in, sync with database
        if user_id:
            tournament = Tournament.query.get(tournament_id)
            if not tournament:
                return jsonify({'error': 'Tournament not found'}), 404
            
            if action == 'add':
                # Check if already favorited
                existing_favorite = FavoriteTournament.query.filter_by(
                    user_id=user_id,
                    tournament_id=tournament_id
                ).first()
                
                if not existing_favorite:
                    favorite = FavoriteTournament(user_id=user_id, tournament_id=tournament_id)
                    db.session.add(favorite)
                    db.session.commit()
                    
                return jsonify({
                    'success': True,
                    'message': 'Tournament added to favorites',
                    'tournament_id': tournament_id
                }), 200
                
            elif action == 'remove':
                favorite = FavoriteTournament.query.filter_by(
                    user_id=user_id,
                    tournament_id=tournament_id
                ).first()
                
                if favorite:
                    db.session.delete(favorite)
                    db.session.commit()
                
                return jsonify({
                    'success': True,
                    'message': 'Tournament removed from favorites',
                    'tournament_id': tournament_id
                }), 200
        else:
            # User not logged in, just acknowledge the request (client handles localStorage)
            return jsonify({
                'success': True,
                'message': f'Favorite {action}ed (local only)',
                'tournament_id': tournament_id
            }), 200
    
    except Exception as e:
        db.session.rollback()
        from app.utils.logger import logger
        logger.error(f"Favorites management error: {str(e)}")
        return jsonify({'error': 'Failed to manage favorites'}), 500


@api_bp.route('/notifications', methods=['POST'])
def manage_notifications():
    """Manage tournament notifications (enable/disable)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        tournament_id = data.get('tournament_id')
        action = data.get('action')  # 'enable' or 'disable'
        user_id = session.get('user_id')  # Get from session if logged in
        
        if not tournament_id:
            return jsonify({'error': 'Tournament ID is required'}), 400
        
        if not action or action not in ['enable', 'disable']:
            return jsonify({'error': 'Action must be "enable" or "disable"'}), 400
        
        # If user is logged in, sync with database
        if user_id:
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
                
            tournament = Tournament.query.get(tournament_id)
            if not tournament:
                return jsonify({'error': 'Tournament not found'}), 404
            
            if action == 'enable':
                # Check if subscription already exists
                existing_subscription = Subscription.query.filter_by(
                    email=user.email
                ).first()
                
                if not existing_subscription:
                    # Create subscription
                    subscription = Subscription(
                        email=user.email,
                        preferences={
                            'new_tournaments': True,
                            'tournament_updates': True,
                            'reminders': True
                        }
                    )
                    subscription.active = True
                    db.session.add(subscription)
                    db.session.commit()
                else:
                    # Reactivate if exists
                    existing_subscription.active = True
                    db.session.commit()
                
                return jsonify({
                    'success': True,
                    'message': 'Notification enabled for tournament',
                    'tournament_id': tournament_id
                }), 200
                
            elif action == 'disable':
                subscription = Subscription.query.filter_by(
                    email=user.email
                ).first()
                
                if subscription:
                    subscription.active = False
                    db.session.commit()
                
                return jsonify({
                    'success': True,
                    'message': 'Notification disabled for tournament',
                    'tournament_id': tournament_id
                }), 200
        else:
            # User not logged in, just acknowledge the request (client handles localStorage)
            return jsonify({
                'success': True,
                'message': f'Notification {action}d (local only)',
                'tournament_id': tournament_id
            }), 200
    
    except Exception as e:
        db.session.rollback()
        from app.utils.logger import logger
        logger.error(f"Notifications management error: {str(e)}")
        return jsonify({'error': 'Failed to manage notifications'}), 500
