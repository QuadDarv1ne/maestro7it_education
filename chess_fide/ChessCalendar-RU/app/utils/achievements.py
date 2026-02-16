"""
User achievements and gamification system
"""

from datetime import datetime, timedelta
from typing import List, Dict
from app.models.user import User
from app.models.favorite import Favorite
from app.models.rating import Rating
from app.models.tournament_subscription import TournamentSubscription


class Achievement:
    """Base achievement class"""
    
    def __init__(self, id: str, name: str, description: str, icon: str, 
                 points: int = 10, tier: str = 'bronze'):
        self.id = id
        self.name = name
        self.description = description
        self.icon = icon
        self.points = points
        self.tier = tier  # bronze, silver, gold, platinum
        self.unlocked = False
        self.unlocked_at = None
        self.progress = 0
        self.progress_max = 100
    
    def check(self, user_id: int) -> bool:
        """Check if achievement is unlocked"""
        raise NotImplementedError
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'points': self.points,
            'tier': self.tier,
            'unlocked': self.unlocked,
            'unlocked_at': self.unlocked_at.isoformat() if self.unlocked_at else None,
            'progress': self.progress,
            'progress_max': self.progress_max
        }


class FirstFavoriteAchievement(Achievement):
    """First favorite tournament"""
    
    def __init__(self):
        super().__init__(
            id='first_favorite',
            name='Первое избранное',
            description='Добавьте первый турнир в избранное',
            icon='bi-heart-fill',
            points=5,
            tier='bronze'
        )
        self.progress_max = 1
    
    def check(self, user_id: int) -> bool:
        count = Favorite.query.filter_by(user_id=user_id).count()
        self.progress = min(count, self.progress_max)
        
        if count >= 1:
            self.unlocked = True
            return True
        return False


class FavoriteCollectorAchievement(Achievement):
    """Collect many favorites"""
    
    def __init__(self):
        super().__init__(
            id='favorite_collector',
            name='Коллекционер',
            description='Добавьте 10 турниров в избранное',
            icon='bi-collection-fill',
            points=20,
            tier='silver'
        )
        self.progress_max = 10
    
    def check(self, user_id: int) -> bool:
        count = Favorite.query.filter_by(user_id=user_id).count()
        self.progress = min(count, self.progress_max)
        
        if count >= 10:
            self.unlocked = True
            return True
        return False


class FirstRatingAchievement(Achievement):
    """First tournament rating"""
    
    def __init__(self):
        super().__init__(
            id='first_rating',
            name='Первая оценка',
            description='Оцените первый турнир',
            icon='bi-star-fill',
            points=5,
            tier='bronze'
        )
        self.progress_max = 1
    
    def check(self, user_id: int) -> bool:
        count = Rating.query.filter_by(user_id=user_id).count()
        self.progress = min(count, self.progress_max)
        
        if count >= 1:
            self.unlocked = True
            return True
        return False


class CriticAchievement(Achievement):
    """Rate many tournaments"""
    
    def __init__(self):
        super().__init__(
            id='critic',
            name='Критик',
            description='Оцените 20 турниров',
            icon='bi-chat-quote-fill',
            points=30,
            tier='gold'
        )
        self.progress_max = 20
    
    def check(self, user_id: int) -> bool:
        count = Rating.query.filter_by(user_id=user_id).count()
        self.progress = min(count, self.progress_max)
        
        if count >= 20:
            self.unlocked = True
            return True
        return False


class EarlyBirdAchievement(Achievement):
    """Subscribe to notifications"""
    
    def __init__(self):
        super().__init__(
            id='early_bird',
            name='Ранняя пташка',
            description='Подпишитесь на уведомления о турнире',
            icon='bi-bell-fill',
            points=10,
            tier='bronze'
        )
        self.progress_max = 1
    
    def check(self, user_id: int) -> bool:
        count = TournamentSubscription.query.filter_by(user_id=user_id).count()
        self.progress = min(count, self.progress_max)
        
        if count >= 1:
            self.unlocked = True
            return True
        return False


class ActiveUserAchievement(Achievement):
    """Active for 7 days"""
    
    def __init__(self):
        super().__init__(
            id='active_user',
            name='Активный пользователь',
            description='Используйте приложение 7 дней подряд',
            icon='bi-fire',
            points=25,
            tier='silver'
        )
        self.progress_max = 7
    
    def check(self, user_id: int) -> bool:
        # This would require tracking daily logins
        # For now, just check account age
        user = User.query.get(user_id)
        if user and user.created_at:
            days = (datetime.now() - user.created_at).days
            self.progress = min(days, self.progress_max)
            
            if days >= 7:
                self.unlocked = True
                return True
        return False


class VeteranAchievement(Achievement):
    """Account older than 30 days"""
    
    def __init__(self):
        super().__init__(
            id='veteran',
            name='Ветеран',
            description='Зарегистрированы более 30 дней',
            icon='bi-award-fill',
            points=50,
            tier='gold'
        )
        self.progress_max = 30
    
    def check(self, user_id: int) -> bool:
        user = User.query.get(user_id)
        if user and user.created_at:
            days = (datetime.now() - user.created_at).days
            self.progress = min(days, self.progress_max)
            
            if days >= 30:
                self.unlocked = True
                return True
        return False


class SocialButterflyAchievement(Achievement):
    """Share tournaments"""
    
    def __init__(self):
        super().__init__(
            id='social_butterfly',
            name='Социальная бабочка',
            description='Поделитесь турниром в соцсетях',
            icon='bi-share-fill',
            points=15,
            tier='bronze'
        )
        self.progress_max = 1
    
    def check(self, user_id: int) -> bool:
        # This would require tracking shares
        # For now, always return False
        return False


class PerfectionistAchievement(Achievement):
    """Give only 5-star ratings"""
    
    def __init__(self):
        super().__init__(
            id='perfectionist',
            name='Перфекционист',
            description='Поставьте 5 звезд 5 турнирам',
            icon='bi-stars',
            points=20,
            tier='silver'
        )
        self.progress_max = 5
    
    def check(self, user_id: int) -> bool:
        count = Rating.query.filter_by(user_id=user_id, rating=5).count()
        self.progress = min(count, self.progress_max)
        
        if count >= 5:
            self.unlocked = True
            return True
        return False


class AchievementSystem:
    """Manage user achievements"""
    
    # All available achievements
    ACHIEVEMENTS = [
        FirstFavoriteAchievement,
        FavoriteCollectorAchievement,
        FirstRatingAchievement,
        CriticAchievement,
        EarlyBirdAchievement,
        ActiveUserAchievement,
        VeteranAchievement,
        SocialButterflyAchievement,
        PerfectionistAchievement
    ]
    
    @staticmethod
    def get_user_achievements(user_id: int) -> List[Achievement]:
        """Get all achievements for a user"""
        achievements = []
        
        for achievement_class in AchievementSystem.ACHIEVEMENTS:
            achievement = achievement_class()
            achievement.check(user_id)
            achievements.append(achievement)
        
        return achievements
    
    @staticmethod
    def get_user_stats(user_id: int) -> Dict:
        """Get user achievement statistics"""
        achievements = AchievementSystem.get_user_achievements(user_id)
        
        unlocked = [a for a in achievements if a.unlocked]
        total_points = sum(a.points for a in unlocked)
        
        # Calculate level based on points
        level = 1 + (total_points // 50)
        points_to_next_level = 50 - (total_points % 50)
        
        # Tier counts
        tier_counts = {
            'bronze': len([a for a in unlocked if a.tier == 'bronze']),
            'silver': len([a for a in unlocked if a.tier == 'silver']),
            'gold': len([a for a in unlocked if a.tier == 'gold']),
            'platinum': len([a for a in unlocked if a.tier == 'platinum'])
        }
        
        return {
            'total_achievements': len(achievements),
            'unlocked_achievements': len(unlocked),
            'locked_achievements': len(achievements) - len(unlocked),
            'total_points': total_points,
            'level': level,
            'points_to_next_level': points_to_next_level,
            'completion_percentage': round((len(unlocked) / len(achievements)) * 100, 1),
            'tier_counts': tier_counts
        }
    
    @staticmethod
    def check_new_achievements(user_id: int) -> List[Achievement]:
        """Check for newly unlocked achievements"""
        # This would require storing unlocked achievements in database
        # For now, just return all unlocked achievements
        achievements = AchievementSystem.get_user_achievements(user_id)
        return [a for a in achievements if a.unlocked]
    
    @staticmethod
    def get_leaderboard(limit: int = 10) -> List[Dict]:
        """Get top users by achievement points"""
        users = User.query.all()
        
        leaderboard = []
        for user in users:
            stats = AchievementSystem.get_user_stats(user.id)
            leaderboard.append({
                'user_id': user.id,
                'username': user.username,
                'total_points': stats['total_points'],
                'level': stats['level'],
                'unlocked_achievements': stats['unlocked_achievements']
            })
        
        # Sort by points
        leaderboard.sort(key=lambda x: x['total_points'], reverse=True)
        
        return leaderboard[:limit]
