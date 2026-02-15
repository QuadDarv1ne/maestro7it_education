from flask import Blueprint, request, jsonify
from app import db
from app.models.tournament import Tournament
from app.models.user import User
from app.models.rating import TournamentRating
from app.models.favorite import FavoriteTournament
from app.models.notification import Subscription
from app.utils.cache import TournamentCache
from datetime import datetime, date
from sqlalchemy import or_, and_

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/tournaments', methods=['GET'])
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
        
        # Base query
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

@api_bp.route('/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'ChessCalendar API'
    }), 200