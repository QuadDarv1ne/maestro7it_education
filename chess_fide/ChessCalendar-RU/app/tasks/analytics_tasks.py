"""
Celery задачи для аналитики и отчетов
"""
from app.celery_app import celery_app
from app import create_app, db
from app.models.tournament import Tournament
from app.models.user import User
from app.utils.unified_cache import cache
from app.utils.metrics import track_celery_task
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@celery_app.task
@track_celery_task('generate_daily_report')
def generate_daily_report():
    """
    Генерация ежедневного отчета
    """
    app = create_app()
    
    with app.app_context():
        try:
            today = datetime.utcnow().date()
            yesterday = today - timedelta(days=1)
            
            # Статистика за вчера
            new_tournaments = Tournament.query.filter(
                Tournament.created_at >= yesterday,
                Tournament.created_at < today
            ).count()
            
            new_users = User.query.filter(
                User.created_at >= yesterday,
                User.created_at < today
            ).count()
            
            upcoming_tournaments = Tournament.query.filter(
                Tournament.start_date >= today,
                Tournament.start_date < today + timedelta(days=7),
                Tournament.status == 'Scheduled'
            ).count()
            
            report = {
                'date': yesterday.isoformat(),
                'new_tournaments': new_tournaments,
                'new_users': new_users,
                'upcoming_tournaments': upcoming_tournaments,
                'generated_at': datetime.utcnow().isoformat()
            }
            
            # Кэшируем отчет
            cache_manager.set(f'daily_report:{yesterday}', report, timeout=86400 * 7)
            
            logger.info(f"Daily report generated for {yesterday}")
            
            return report
            
        except Exception as e:
            logger.error(f"Daily report generation error: {e}")
            return {'status': 'error', 'message': str(e)}

@celery_app.task
@track_celery_task('update_recommendations_cache')
def update_recommendations_cache():
    """
    Обновление кэша рекомендаций для всех пользователей
    """
    app = create_app()
    
    with app.app_context():
        try:
            from app.utils.recommendations import RecommendationEngine
            
            active_users = User.query.filter_by(is_active=True).all()
            updated_count = 0
            
            for user in active_users:
                try:
                    # Генерируем рекомендации
                    recommendations = RecommendationEngine.get_user_recommendations(user.id)
                    
                    # Кэшируем
                    cache_key = f'recommendations:user:{user.id}'
                    cache_manager.set(cache_key, recommendations, timeout=7200)
                    
                    updated_count += 1
                except Exception as e:
                    logger.error(f"Error updating recommendations for user {user.id}: {e}")
            
            logger.info(f"Updated recommendations cache for {updated_count} users")
            
            return {
                'status': 'success',
                'updated': updated_count,
                'total': len(active_users)
            }
            
        except Exception as e:
            logger.error(f"Recommendations cache update error: {e}")
            return {'status': 'error', 'message': str(e)}

@celery_app.task
def calculate_tournament_statistics(tournament_id):
    """
    Расчет статистики для турнира
    """
    app = create_app()
    
    with app.app_context():
        try:
            from app.models.rating import TournamentRating
            from app.models.favorite import FavoriteTournament
            
            tournament = Tournament.query.get(tournament_id)
            if not tournament:
                return {'status': 'error', 'message': 'Tournament not found'}
            
            # Рейтинги
            ratings = TournamentRating.query.filter_by(tournament_id=tournament_id).all()
            avg_rating = sum(r.rating for r in ratings) / len(ratings) if ratings else 0
            
            # Избранное
            favorites_count = FavoriteTournament.query.filter_by(tournament_id=tournament_id).count()
            
            # Просмотры (если есть модель)
            # views_count = TournamentView.query.filter_by(tournament_id=tournament_id).count()
            
            stats = {
                'tournament_id': tournament_id,
                'ratings_count': len(ratings),
                'average_rating': round(avg_rating, 2),
                'favorites_count': favorites_count,
                'calculated_at': datetime.utcnow().isoformat()
            }
            
            # Кэшируем статистику
            cache_key = f'tournament_stats:{tournament_id}'
            cache_manager.set(cache_key, stats, timeout=3600)
            
            return stats
            
        except Exception as e:
            logger.error(f"Tournament statistics calculation error: {e}")
            return {'status': 'error', 'message': str(e)}

@celery_app.task
def generate_user_activity_report(user_id):
    """
    Генерация отчета об активности пользователя
    """
    app = create_app()
    
    with app.app_context():
        try:
            from app.models.favorite import FavoriteTournament
            from app.models.rating import TournamentRating
            
            user = User.query.get(user_id)
            if not user:
                return {'status': 'error', 'message': 'User not found'}
            
            # Избранные турниры
            favorites = FavoriteTournament.query.filter_by(user_id=user_id).count()
            
            # Оценки
            ratings = TournamentRating.query.filter_by(user_id=user_id).count()
            
            # Последняя активность
            last_login = user.last_login if hasattr(user, 'last_login') else None
            
            report = {
                'user_id': user_id,
                'username': user.username,
                'favorites_count': favorites,
                'ratings_count': ratings,
                'last_login': last_login.isoformat() if last_login else None,
                'account_age_days': (datetime.utcnow() - user.created_at).days,
                'generated_at': datetime.utcnow().isoformat()
            }
            
            return report
            
        except Exception as e:
            logger.error(f"User activity report error: {e}")
            return {'status': 'error', 'message': str(e)}

@celery_app.task
def cleanup_expired_cache():
    """
    Очистка устаревшего кэша
    """
    try:
        # Redis автоматически удаляет истекшие ключи
        # Но можем принудительно очистить определенные паттерны
        
        stats = cache_manager.get_stats()
        logger.info(f"Cache stats: {stats}")
        
        return {
            'status': 'success',
            'stats': stats
        }
        
    except Exception as e:
        logger.error(f"Cache cleanup error: {e}")
        return {'status': 'error', 'message': str(e)}
