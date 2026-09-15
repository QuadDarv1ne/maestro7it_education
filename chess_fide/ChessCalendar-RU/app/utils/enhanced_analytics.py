"""
Расширенная аналитика для шахматного календаря
"""
from app import db
from app.models.tournament import Tournament
from app.models.user import User
from app.models.favorite import FavoriteTournament
from app.models.comment import TournamentComment
from app.models.tag import Tag, TagTournament
from datetime import datetime, date, timedelta
from sqlalchemy import func, extract
import logging

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Сервис аналитики"""
    
    @staticmethod
    def get_overview():
        """Получить общую статистику"""
        try:
            total_tournaments = Tournament.query.count()
            total_users = User.query.count()
            total_favorites = FavoriteTournament.query.count()
            total_comments = TournamentComment.query.count()
            
            # Турниры по статусу
            tournaments_by_status = db.session.query(
                Tournament.status, func.count(Tournament.id)
            ).group_by(Tournament.status).all()
            
            # Топ категорий
            tournaments_by_category = db.session.query(
                Tournament.category, func.count(Tournament.id)
            ).group_by(Tournament.category).order_by(
                func.count(Tournament.id).desc()
            ).limit(10).all()
            
            # Топ локаций
            tournaments_by_location = db.session.query(
                Tournament.location, func.count(Tournament.id)
            ).group_by(Tournament.location).order_by(
                func.count(Tournament.id).desc()
            ).limit(10).all()
            
            return {
                'total_tournaments': total_tournaments,
                'total_users': total_users,
                'total_favorites': total_favorites,
                'total_comments': total_comments,
                'tournaments_by_status': dict(tournaments_by_status),
                'tournaments_by_category': dict(tournaments_by_category),
                'tournaments_by_location': dict(tournaments_by_location)
            }
        except Exception as e:
            logger.error(f"Get overview error: {str(e)}")
            return {}
    
    @staticmethod
    def get_trends(period_days=30):
        """Получить тренды по турнирам"""
        try:
            start_date = date.today() - timedelta(days=period_days)
            
            # Новые турниры по дням
            daily_tournaments = db.session.query(
                extract('date', Tournament.created_at).label('day'),
                func.count(Tournament.id)
            ).filter(
                Tournament.created_at >= start_date
            ).group_by(
                extract('date', Tournament.created_at)
            ).order_by(
                extract('date', Tournament.created_at)
            ).all()
            
            trends = {str(row.day): row.count for row in daily_tournaments}
            
            return {
                'period_days': period_days,
                'daily_tournaments': trends
            }
        except Exception as e:
            logger.error(f"Get trends error: {str(e)}")
            return {}
    
    @staticmethod
    def get_popular_tournaments(limit=10, period_days=30):
        """Получить популярные турниры"""
        try:
            start_date = date.today() - timedelta(days=period_days)
            
            # По количеству просмотров
            popular_by_views = Tournament.query.filter(
                Tournament.created_at >= start_date
            ).order_by(
                Tournament.view_count.desc()
            ).limit(limit).all()
            
            # По количеству избранных
            popular_by_favorites = db.session.query(
                Tournament, func.count(FavoriteTournament.id).label('fav_count')
            ).join(
                FavoriteTournament, Tournament.id == FavoriteTournament.tournament_id
            ).filter(
                FavoriteTournament.created_at >= start_date
            ).group_by(
                Tournament.id
            ).order_by(
                func.count(FavoriteTournament.id).desc()
            ).limit(limit).all()
            
            # По количеству комментариев
            popular_by_comments = db.session.query(
                Tournament, func.count(TournamentComment.id).label('comment_count')
            ).join(
                TournamentComment, Tournament.id == TournamentComment.tournament_id
            ).filter(
                TournamentComment.created_at >= start_date
            ).group_by(
                Tournament.id
            ).order_by(
                func.count(TournamentComment.id).desc()
            ).limit(limit).all()
            
            return {
                'by_views': [t[0].to_dict() for t in popular_by_views],
                'by_favorites': [t[0].to_dict() for t in popular_by_favorites],
                'by_comments': [t[0].to_dict() for t in popular_by_comments]
            }
        except Exception as e:
            logger.error(f"Get popular tournaments error: {str(e)}")
            return {}
    
    @staticmethod
    def get_user_activity(limit=20):
        """Получить активность пользователей"""
        try:
            # Топ пользователей по действиям (избранное + комментарии)
            user_activity = db.session.query(
                User.id,
                User.username,
                func.count(FavoriteTournament.id).label('favorites'),
                func.count(TournamentComment.id).label('comments')
            ).outerjoin(
                FavoriteTournament, User.id == FavoriteTournament.user_id
            ).outerjoin(
                TournamentComment, User.id == TournamentComment.user_id
            ).group_by(
                User.id, User.username
            ).order_by(
                func.count(FavoriteTournament.id).desc(),
                func.count(TournamentComment.id).desc()
            ).limit(limit).all()
            
            return [
                {
                    'user_id': row.id,
                    'username': row.username,
                    'favorites': row.favorites or 0,
                    'comments': row.comments or 0
                }
                for row in user_activity
            ]
        except Exception as e:
            logger.error(f"Get user activity error: {str(e)}")
            return []
    
    @staticmethod
    def get_tag_statistics():
        """Получить статистику по тегам"""
        try:
            popular_tags = Tag.query.order_by(
                Tag.usage_count.desc()
            ).limit(20).all()
            
            return [tag.to_dict() for tag in popular_tags]
        except Exception as e:
            logger.error(f"Get tag statistics error: {str(e)}")
            return []
    
    @staticmethod
    def get_monthly_report(year=None):
        """Получить ежемесячный отчёт"""
        if year is None:
            year = date.today().year
        
        try:
            monthly_data = db.session.query(
                extract('month', Tournament.created_at).label('month'),
                func.count(Tournament.id).label('count')
            ).filter(
                extract('year', Tournament.created_at) == year
            ).group_by(
                extract('month', Tournament.created_at)
            ).order_by(
                extract('month', Tournament.created_at)
            ).all()
            
            monthly_report = {
                str(row.month): row.count
                for row in monthly_data
            }
            
            total = sum(monthly_report.values())
            
            return {
                'year': year,
                'monthly': monthly_report,
                'total': total,
                'average_per_month': total / 12 if total > 0 else 0
            }
        except Exception as e:
            logger.error(f"Get monthly report error: {str(e)}")
            return {}
