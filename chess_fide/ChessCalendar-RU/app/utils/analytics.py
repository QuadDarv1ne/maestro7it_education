from datetime import datetime, timedelta
from collections import defaultdict
from app import db
from app.models.user import User
from app.models.tournament import Tournament
from app.models.forum import ForumThread, ForumPost
from app.models.rating import TournamentRating
from app.models.notification import Notification
from app.models.report import Report


class AnalyticsService:
    """Service for analytics and reporting"""
    
    @staticmethod
    def get_platform_overview():
        """Get overall platform statistics"""
        stats = {
            'total_users': User.query.count(),
            'total_tournaments': Tournament.query.count(),
            'total_forum_threads': ForumThread.query.count(),
            'total_forum_posts': ForumPost.query.count(),
            'total_ratings': TournamentRating.query.count(),
            'total_notifications': Notification.query.count(),
            'total_reports': Report.query.count(),
            'active_users_30_days': AnalyticsService.get_active_users_count(30),
            'new_users_30_days': AnalyticsService.get_new_users_count(30)
        }
        return stats
    
    @staticmethod
    def get_active_users_count(days=30):
        """Get count of users who were active in the last N days"""
        from datetime import datetime, timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Assuming we track user activity through last_login or similar field
        # In a real app, you'd have more sophisticated activity tracking
        active_users = User.query.filter(User.last_login >= cutoff_date).count()
        return active_users
    
    @staticmethod
    def get_new_users_count(days=30):
        """Get count of new users registered in the last N days"""
        from datetime import datetime, timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        new_users = User.query.filter(User.created_at >= cutoff_date).count()
        return new_users
    
    @staticmethod
    def get_user_activity_data(days=30):
        """Get user activity data for the last N days"""
        from datetime import datetime, timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Get daily user activity counts
        user_activities = db.session.query(
            db.func.date(User.created_at).label('date'),
            db.func.count(User.id).label('count')
        ).filter(
            User.created_at >= cutoff_date
        ).group_by(db.func.date(User.created_at)).all()
        
        # Create a dictionary with dates and counts
        activity_data = {}
        current_date = cutoff_date.date()
        end_date = datetime.utcnow().date()
        
        # Initialize all dates with 0
        while current_date <= end_date:
            activity_data[current_date.strftime('%Y-%m-%d')] = 0
            current_date += timedelta(days=1)
        
        # Fill in actual counts
        for activity in user_activities:
            activity_data[activity.date.strftime('%Y-%m-%d')] = activity.count
        
        # Convert to sorted list of tuples
        sorted_data = sorted(activity_data.items())
        return sorted_data
    
    @staticmethod
    def get_forum_activity_data(days=30):
        """Get forum activity data for the last N days"""
        from datetime import datetime, timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Get daily forum post counts
        post_activities = db.session.query(
            db.func.date(ForumPost.created_at).label('date'),
            db.func.count(ForumPost.id).label('count')
        ).filter(
            ForumPost.created_at >= cutoff_date
        ).group_by(db.func.date(ForumPost.created_at)).all()
        
        # Create a dictionary with dates and counts
        activity_data = {}
        current_date = cutoff_date.date()
        end_date = datetime.utcnow().date()
        
        # Initialize all dates with 0
        while current_date <= end_date:
            activity_data[current_date.strftime('%Y-%m-%d')] = 0
            current_date += timedelta(days=1)
        
        # Fill in actual counts
        for activity in post_activities:
            activity_data[activity.date.strftime('%Y-%m-%d')] = activity.count
        
        # Convert to sorted list of tuples
        sorted_data = sorted(activity_data.items())
        return sorted_data
    
    @staticmethod
    def get_top_rated_tournaments(limit=10):
        """Get top-rated tournaments"""
        # This requires a more complex query to calculate average ratings
        from sqlalchemy import func
        
        # Subquery to calculate average rating per tournament
        avg_ratings = db.session.query(
            TournamentRating.tournament_id,
            func.avg(TournamentRating.rating).label('avg_rating'),
            func.count(TournamentRating.id).label('rating_count')
        ).group_by(TournamentRating.tournament_id).subquery()
        
        # Join with tournaments to get details
        top_tournaments = db.session.query(
            Tournament,
            avg_ratings.c.avg_rating,
            avg_ratings.c.rating_count
        ).join(avg_ratings, Tournament.id == avg_ratings.c.tournament_id)\
         .order_by(avg_ratings.c.avg_rating.desc(), avg_ratings.c.rating_count.desc())\
         .limit(limit).all()
        
        result = []
        for tournament, avg_rating, rating_count in top_tournaments:
            result.append({
                'id': tournament.id,
                'name': tournament.name,
                'location': tournament.location,
                'avg_rating': round(float(avg_rating), 2),
                'rating_count': rating_count
            })
        
        return result
    
    @staticmethod
    def get_most_active_users(limit=10):
        """Get most active users based on forum participation"""
        # Count posts and threads per user
        user_activity = db.session.query(
            User.id,
            User.username,
            db.func.count(ForumPost.id).label('post_count'),
            db.func.count(ForumThread.id).label('thread_count')
        ).outerjoin(ForumPost, User.id == ForumPost.author_id)\
         .outerjoin(ForumThread, User.id == ForumThread.author_id)\
         .group_by(User.id, User.username)\
         .order_by(db.func.coalesce(db.func.count(ForumPost.id), 0) + 
                  db.func.coalesce(db.func.count(ForumThread.id), 0).desc())\
         .limit(limit).all()
        
        result = []
        for user in user_activity:
            result.append({
                'id': user.id,
                'username': user.username,
                'post_count': user.post_count or 0,
                'thread_count': user.thread_count or 0,
                'total_activity': (user.post_count or 0) + (user.thread_count or 0)
            })
        
        return result
    
    @staticmethod
    def get_recent_reports(limit=10):
        """Get recent reports"""
        recent_reports = Report.query.order_by(Report.created_at.desc()).limit(limit).all()
        
        result = []
        for report in recent_reports:
            result.append({
                'id': report.id,
                'reported_type': report.reported_type,
                'reported_id': report.reported_id,
                'reason': report.reason,
                'reporter_username': report.reporter.username if report.reporter else 'Unknown',
                'created_at': report.created_at,
                'is_resolved': report.is_resolved
            })
        
        return result
    
    @staticmethod
    def get_tournament_engagement():
        """Get tournament engagement metrics"""
        # Count favorites, ratings, and forum activity per tournament
        engagement_data = db.session.query(
            Tournament.id,
            Tournament.name,
            db.func.count(FavoriteTournament.id).label('favorites_count'),
            db.func.avg(TournamentRating.rating).label('avg_rating'),
            db.func.count(TournamentRating.id).label('rating_count'),
            db.func.count(ForumThread.id).label('discussion_count')
        ).outerjoin('favorites')\
         .outerjoin('ratings')\
         .outerjoin('forum_threads')\
         .group_by(Tournament.id, Tournament.name)\
         .order_by(db.func.coalesce(db.func.count(FavoriteTournament.id), 0).desc())\
         .limit(10).all()
        
        result = []
        for item in engagement_data:
            result.append({
                'id': item.id,
                'name': item.name,
                'favorites_count': item.favorites_count or 0,
                'avg_rating': float(item.avg_rating) if item.avg_rating else 0,
                'rating_count': item.rating_count or 0,
                'discussion_count': item.discussion_count or 0
            })
        
        return result
    
    @staticmethod
    def get_growth_metrics():
        """Get growth metrics for the platform"""
        from datetime import datetime, timedelta
        
        # Calculate weekly growth for the past 12 weeks
        weeks_data = []
        for i in range(12):
            end_date = datetime.utcnow() - timedelta(weeks=i)
            start_date = end_date - timedelta(weeks=1)
            
            new_users = User.query.filter(
                User.created_at >= start_date,
                User.created_at < end_date
            ).count()
            
            new_tournaments = Tournament.query.filter(
                Tournament.created_at >= start_date,
                Tournament.created_at < end_date
            ).count()
            
            weeks_data.append({
                'week': start_date.strftime('%Y-W%U'),
                'new_users': new_users,
                'new_tournaments': new_tournaments
            })
        
        # Reverse to show oldest first
        weeks_data.reverse()
        return weeks_data