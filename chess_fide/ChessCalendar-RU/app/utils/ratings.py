from app import db
from app.models.user import User
from app.models.tournament import Tournament
from app.models.rating import TournamentRating
from datetime import datetime


class RatingService:
    """Service for handling tournament ratings"""
    
    @staticmethod
    def rate_tournament(user_id, tournament_id, rating, review=None):
        """Rate a tournament or update existing rating"""
        # Validate rating value
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        
        # Check if tournament exists
        tournament = Tournament.query.get(tournament_id)
        if not tournament:
            raise ValueError("Tournament not found")
        
        # Check if user has already rated this tournament
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
            new_rating = TournamentRating(
                user_id=user_id,
                tournament_id=tournament_id,
                rating=rating,
                review=review
            )
            db.session.add(new_rating)
        
        db.session.commit()
        return True
    
    @staticmethod
    def get_user_rating(user_id, tournament_id):
        """Get user's rating for a tournament"""
        rating = TournamentRating.query.filter_by(
            user_id=user_id,
            tournament_id=tournament_id
        ).first()
        
        if rating:
            return {
                'rating': rating.rating,
                'review': rating.review or '',
                'created_at': rating.created_at,
                'updated_at': rating.updated_at
            }
        else:
            return {
                'rating': 0,
                'review': '',
                'created_at': None,
                'updated_at': None
            }
    
    @staticmethod
    def get_tournament_average_rating(tournament_id):
        """Get average rating for a tournament"""
        ratings = TournamentRating.query.filter_by(
            tournament_id=tournament_id
        ).all()
        
        if not ratings:
            return {
                'average_rating': 0,
                'total_ratings': 0,
                'ratings': []
            }
        
        avg_rating = sum(r.rating for r in ratings) / len(ratings)
        
        return {
            'average_rating': round(avg_rating, 2),
            'total_ratings': len(ratings),
            'ratings': [r.to_dict() for r in ratings]
        }
    
    @staticmethod
    def get_user_ratings(user_id):
        """Get all ratings by a user"""
        ratings = TournamentRating.query.filter_by(user_id=user_id).all()
        return [r.to_dict() for r in ratings]