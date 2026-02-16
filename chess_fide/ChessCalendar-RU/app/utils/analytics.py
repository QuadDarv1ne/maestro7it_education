from app import db
from app.models.tournament import Tournament
from app.models.user import User
from app.models.rating import TournamentRating
from app.models.preference import UserInteraction
from app.models.favorite import FavoriteTournament
from app.models.notification import Subscription
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import json
import time


class AnalyticsService:
    """Service for collecting and analyzing application usage data"""

    @staticmethod
    def get_tournament_analytics():
        """Get comprehensive tournament analytics"""
        # Overall tournament statistics
        total_tournaments = Tournament.query.count()
        upcoming_tournaments = Tournament.query.filter(
            Tournament.start_date >= datetime.today().date(),
            Tournament.status != 'Completed'
        ).count()
        completed_tournaments = Tournament.query.filter_by(status='Completed').count()
        
        # Category distribution
        category_counts = db.session.query(
            Tournament.category, 
            db.func.count(Tournament.id)
        ).group_by(Tournament.category).all()
        
        # Status distribution
        status_counts = db.session.query(
            Tournament.status, 
            db.func.count(Tournament.id)
        ).group_by(Tournament.status).all()
        
        # Location distribution (top 10)
        location_counts = db.session.query(
            Tournament.location, 
            db.func.count(Tournament.id)
        ).group_by(Tournament.location).order_by(
            db.func.count(Tournament.id).desc()
        ).limit(10).all()
        
        # Monthly tournament counts for the past year
        one_year_ago = datetime.today() - timedelta(days=365)
        monthly_counts = db.session.query(
            db.func.strftime('%Y-%m', Tournament.start_date),
            db.func.count(Tournament.id)
        ).filter(
            Tournament.start_date >= one_year_ago
        ).group_by(db.func.strftime('%Y-%m', Tournament.start_date)).all()
        
        return {
            'total_tournaments': total_tournaments,
            'upcoming_tournaments': upcoming_tournaments,
            'completed_tournaments': completed_tournaments,
            'categories': dict(category_counts),
            'statuses': dict(status_counts),
            'top_locations': dict(location_counts),
            'monthly_distribution': dict(monthly_counts)
        }

    @staticmethod
    def get_user_analytics():
        """Get comprehensive user analytics"""
        total_users = User.query.count()
        active_users = User.query.filter(User.is_active == True).count()
        admin_users = User.query.filter(User.is_admin == True).count()
        
        # User registration trends
        thirty_days_ago = datetime.today() - timedelta(days=30)
        recent_registrations = db.session.query(
            db.func.date(User.created_at),
            db.func.count(User.id)
        ).filter(
            User.created_at >= thirty_days_ago
        ).group_by(db.func.date(User.created_at)).all()
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'admin_users': admin_users,
            'recent_registrations': dict(recent_registrations)
        }

    @staticmethod
    def get_interaction_analytics():
        """Get user interaction analytics"""
        total_interactions = UserInteraction.query.count()
        
        # Interaction type distribution
        interaction_types = db.session.query(
            UserInteraction.interaction_type,
            db.func.count(UserInteraction.id)
        ).group_by(UserInteraction.interaction_type).all()
        
        # Popular tournaments based on interactions
        popular_tournaments = db.session.query(
            Tournament,
            db.func.count(UserInteraction.id).label('interaction_count')
        ).join(UserInteraction).group_by(Tournament.id).order_by(
            db.func.count(UserInteraction.id).desc()
        ).limit(10).all()
        
        # Recent interactions
        seven_days_ago = datetime.today() - timedelta(days=7)
        recent_interactions = db.session.query(
            UserInteraction
        ).filter(
            UserInteraction.created_at >= seven_days_ago
        ).count()
        
        return {
            'total_interactions': total_interactions,
            'interaction_types': dict(interaction_types),
            'popular_tournaments': [(t[0].name, t[1]) for t in popular_tournaments],
            'recent_interactions': recent_interactions
        }

    @staticmethod
    def get_rating_analytics():
        """Get tournament rating analytics"""
        total_ratings = TournamentRating.query.count()
        
        # Average ratings by tournament
        avg_ratings = db.session.query(
            Tournament.id,
            Tournament.name,
            db.func.avg(TournamentRating.rating).label('avg_rating'),
            db.func.count(TournamentRating.id).label('rating_count')
        ).join(TournamentRating).group_by(Tournament.id).order_by(
            db.func.avg(TournamentRating.rating).desc()
        ).limit(10).all()
        
        # Rating distribution
        rating_distribution = db.session.query(
            TournamentRating.rating,
            db.func.count(TournamentRating.id)
        ).group_by(TournamentRating.rating).all()
        
        # Overall average rating
        overall_avg = db.session.query(
            db.func.avg(TournamentRating.rating)
        ).scalar()
        
        return {
            'total_ratings': total_ratings,
            'overall_average': float(overall_avg) if overall_avg else 0,
            'top_rated': [(t[1], float(t[2]), t[3]) for t in avg_ratings],
            'rating_distribution': dict(rating_distribution)
        }

    @staticmethod
    def get_favorite_analytics():
        """Get favorite tournament analytics"""
        total_favorites = FavoriteTournament.query.count()
        
        # Most favorited tournaments
        most_favorited = db.session.query(
            Tournament.name,
            db.func.count(FavoriteTournament.id).label('favorite_count')
        ).join(FavoriteTournament).group_by(Tournament.id).order_by(
            db.func.count(FavoriteTournament.id).desc()
        ).limit(10).all()
        
        # Favorites by user
        user_favorite_counts = db.session.query(
            User.id,
            User.username,
            db.func.count(FavoriteTournament.id).label('favorites_count')
        ).join(FavoriteTournament).group_by(User.id).order_by(
            db.func.count(FavoriteTournament.id).desc()
        ).limit(10).all()
        
        return {
            'total_favorites': total_favorites,
            'most_favorited': most_favorited,
            'top_users_by_favorites': [(u[1], u[2]) for u in user_favorite_counts]
        }

    @staticmethod
    def get_session_analytics():
        """Get session-based analytics from tracked events"""
        # This would typically come from a dedicated analytics database
        # For now, we'll simulate some session metrics
        try:
            # In a real implementation, this would query stored analytics events
            # Here we're providing placeholder data
            return {
                'active_sessions': 42,  # Simulated value
                'avg_session_duration': 345,  # Seconds
                'bounce_rate': 0.25,  # 25%
                'pages_per_session': 3.2,
                'returning_users_ratio': 0.65  # 65%
            }
        except Exception as e:
            return {
                'active_sessions': 0,
                'avg_session_duration': 0,
                'bounce_rate': 0,
                'pages_per_session': 0,
                'returning_users_ratio': 0
            }

    @staticmethod
    def get_performance_analytics():
        """Get application performance analytics"""
        try:
            # In a real implementation, this would collect data from performance monitoring
            # For now, we'll provide simulated data
            return {
                'avg_response_time': 245,  # milliseconds
                'slow_pages': ['/search', '/calendar'],
                'error_rate': 0.02,  # 2%
                'uptime': 0.999,  # 99.9%
                'peak_load_times': ['18:00', '12:00']
            }
        except Exception as e:
            return {
                'avg_response_time': 0,
                'slow_pages': [],
                'error_rate': 0,
                'uptime': 0,
                'peak_load_times': []
            }

    @staticmethod
    def get_notification_analytics():
        """Get notification subscription and engagement analytics"""
        total_subscriptions = Subscription.query.count()
        
        # Subscription types
        subscription_types = db.session.query(
            Subscription.subscription_type,
            db.func.count(Subscription.id)
        ).group_by(Subscription.subscription_type).all()
        
        # Recently subscribed tournaments
        recent_subscriptions = db.session.query(
            Tournament.name,
            db.func.count(Subscription.id).label('subscription_count')
        ).join(Subscription).group_by(Tournament.id).order_by(
            db.func.count(Subscription.id).desc()
        ).limit(10).all()
        
        return {
            'total_subscriptions': total_subscriptions,
            'subscription_types': dict(subscription_types),
            'most_subscribed_tournaments': [(t[0], t[1]) for t in recent_subscriptions]
        }

    @staticmethod
    def get_comprehensive_report():
        """Generate a comprehensive analytics report"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'timestamp': int(time.time()),
            'tournament_analytics': AnalyticsService.get_tournament_analytics(),
            'user_analytics': AnalyticsService.get_user_analytics(),
            'interaction_analytics': AnalyticsService.get_interaction_analytics(),
            'rating_analytics': AnalyticsService.get_rating_analytics(),
            'favorite_analytics': AnalyticsService.get_favorite_analytics(),
            'session_analytics': AnalyticsService.get_session_analytics(),
            'performance_analytics': AnalyticsService.get_performance_analytics(),
            'notification_analytics': AnalyticsService.get_notification_analytics()
        }
        
        return report

    @staticmethod
    def get_tournament_performance(tournament_id):
        """Get detailed performance analytics for a specific tournament"""
        tournament = Tournament.query.get(tournament_id)
        if not tournament:
            return None
        
        # Get all interactions with this tournament
        interactions = UserInteraction.query.filter_by(
            tournament_id=tournament_id
        ).all()
        
        interaction_summary = defaultdict(list)
        for interaction in interactions:
            interaction_summary[interaction.interaction_type].append({
                'user_id': interaction.user_id,
                'created_at': interaction.created_at.isoformat()
            })
        
        # Get ratings for this tournament
        ratings = TournamentRating.query.filter_by(
            tournament_id=tournament_id
        ).all()
        
        avg_rating = sum(r.rating for r in ratings) / len(ratings) if ratings else 0
        
        # Get favorites
        favorites = FavoriteTournament.query.filter_by(
            tournament_id=tournament_id
        ).count()
        
        return {
            'tournament': tournament.to_dict(),
            'interactions': dict(interaction_summary),
            'total_interactions': len(interactions),
            'total_ratings': len(ratings),
            'average_rating': round(avg_rating, 2),
            'total_favorites': favorites,
            'engagement_score': len(interactions) + len(ratings) * 2 + favorites * 3
        }


# Global instance
analytics_service = AnalyticsService()