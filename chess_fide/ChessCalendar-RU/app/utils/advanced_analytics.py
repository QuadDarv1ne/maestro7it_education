"""
Расширенная система аналитики
Глубокий анализ данных, тренды, прогнозы
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
import math


class AdvancedAnalytics:
    """Расширенная аналитика для бизнес-инсайтов"""
    
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 300  # 5 минут
    
    def analyze_user_retention(
        self,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Анализ удержания пользователей (retention)
        
        Cohort analysis по неделям
        """
        from app.models.user import User
        from sqlalchemy import func, extract
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Группировка пользователей по неделям регистрации
        cohorts = db.session.query(
            func.date_trunc('week', User.created_at).label('cohort_week'),
            func.count(User.id).label('users')
        ).filter(
            User.created_at >= start_date
        ).group_by('cohort_week').all()
        
        retention_data = []
        
        for cohort_week, cohort_size in cohorts:
            # Анализ активности когорты по неделям
            weekly_retention = []
            
            for week in range(4):  # 4 недели
                week_start = cohort_week + timedelta(weeks=week)
                week_end = week_start + timedelta(weeks=1)
                
                active_users = User.query.filter(
                    User.created_at >= cohort_week,
                    User.created_at < cohort_week + timedelta(weeks=1),
                    User.last_login >= week_start,
                    User.last_login < week_end
                ).count()
                
                retention_rate = (active_users / cohort_size * 100) if cohort_size > 0 else 0
                weekly_retention.append({
                    'week': week,
                    'active_users': active_users,
                    'retention_rate': round(retention_rate, 2)
                })
            
            retention_data.append({
                'cohort_week': cohort_week.isoformat(),
                'cohort_size': cohort_size,
                'retention': weekly_retention
            })
        
        return {
            'period_days': days,
            'cohorts': retention_data,
            'generated_at': datetime.utcnow().isoformat()
        }
    
    def analyze_user_engagement(self) -> Dict[str, Any]:
        """
        Анализ вовлеченности пользователей
        
        Метрики:
        - DAU (Daily Active Users)
        - WAU (Weekly Active Users)
        - MAU (Monthly Active Users)
        - Stickiness (DAU/MAU)
        """
        from app.models.user import User
        
        now = datetime.utcnow()
        
        # DAU
        dau = User.query.filter(
            User.last_login >= now - timedelta(days=1)
        ).count()
        
        # WAU
        wau = User.query.filter(
            User.last_login >= now - timedelta(days=7)
        ).count()
        
        # MAU
        mau = User.query.filter(
            User.last_login >= now - timedelta(days=30)
        ).count()
        
        # Stickiness
        stickiness = (dau / mau * 100) if mau > 0 else 0
        
        return {
            'dau': dau,
            'wau': wau,
            'mau': mau,
            'stickiness': round(stickiness, 2),
            'engagement_level': self._classify_engagement(stickiness),
            'timestamp': now.isoformat()
        }
    
    def _classify_engagement(self, stickiness: float) -> str:
        """Классификация уровня вовлеченности"""
        if stickiness >= 20:
            return 'excellent'
        elif stickiness >= 15:
            return 'good'
        elif stickiness >= 10:
            return 'average'
        else:
            return 'poor'
    
    def analyze_tournament_trends(
        self,
        months: int = 6
    ) -> Dict[str, Any]:
        """
        Анализ трендов турниров
        
        Включает:
        - Рост по месяцам
        - Популярные категории
        - Географическое распределение
        - Сезонность
        """
        from app.models.tournament import Tournament
        from sqlalchemy import func, extract
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=months * 30)
        
        # Рост по месяцам
        monthly_growth = db.session.query(
            func.date_trunc('month', Tournament.created_at).label('month'),
            func.count(Tournament.id).label('count')
        ).filter(
            Tournament.created_at >= start_date
        ).group_by('month').order_by('month').all()
        
        # Расчет темпа роста
        growth_rates = []
        for i in range(1, len(monthly_growth)):
            prev_count = monthly_growth[i-1][1]
            curr_count = monthly_growth[i][1]
            growth_rate = ((curr_count - prev_count) / prev_count * 100) if prev_count > 0 else 0
            growth_rates.append(round(growth_rate, 2))
        
        # Популярные категории
        category_distribution = db.session.query(
            Tournament.category,
            func.count(Tournament.id).label('count')
        ).filter(
            Tournament.created_at >= start_date
        ).group_by(Tournament.category).order_by(
            func.count(Tournament.id).desc()
        ).all()
        
        # Географическое распределение
        location_distribution = db.session.query(
            Tournament.location,
            func.count(Tournament.id).label('count')
        ).filter(
            Tournament.created_at >= start_date
        ).group_by(Tournament.location).order_by(
            func.count(Tournament.id).desc()
        ).limit(10).all()
        
        # Сезонность (по месяцам года)
        seasonality = db.session.query(
            extract('month', Tournament.start_date).label('month'),
            func.count(Tournament.id).label('count')
        ).filter(
            Tournament.start_date.isnot(None)
        ).group_by('month').order_by('month').all()
        
        return {
            'period_months': months,
            'monthly_growth': [
                {
                    'month': month.isoformat(),
                    'count': count,
                    'growth_rate': growth_rates[i] if i < len(growth_rates) else None
                }
                for i, (month, count) in enumerate(monthly_growth)
            ],
            'categories': [
                {'category': cat, 'count': count}
                for cat, count in category_distribution
            ],
            'locations': [
                {'location': loc, 'count': count}
                for loc, count in location_distribution
            ],
            'seasonality': [
                {'month': int(month), 'count': count}
                for month, count in seasonality
            ],
            'generated_at': datetime.utcnow().isoformat()
        }
    
    def predict_tournament_popularity(
        self,
        tournament_id: int
    ) -> Dict[str, Any]:
        """
        Предсказание популярности турнира
        
        На основе:
        - Исторических данных похожих турниров
        - Категории и локации
        - Времени года
        - Текущих трендов
        """
        from app.models.tournament import Tournament
        from app.models.favorite import FavoriteTournament
        from app.models.rating import TournamentRating
        from sqlalchemy import func
        
        tournament = Tournament.query.get(tournament_id)
        if not tournament:
            return {'error': 'Tournament not found'}
        
        # Поиск похожих турниров
        similar_tournaments = Tournament.query.filter(
            Tournament.category == tournament.category,
            Tournament.location == tournament.location,
            Tournament.id != tournament_id,
            Tournament.created_at < datetime.utcnow() - timedelta(days=30)
        ).limit(10).all()
        
        if not similar_tournaments:
            return {
                'prediction': 'insufficient_data',
                'confidence': 0,
                'message': 'Недостаточно данных для предсказания'
            }
        
        # Анализ популярности похожих турниров
        popularity_scores = []
        
        for similar in similar_tournaments:
            favorites = FavoriteTournament.query.filter_by(
                tournament_id=similar.id
            ).count()
            
            ratings_data = db.session.query(
                func.count(TournamentRating.id),
                func.avg(TournamentRating.rating)
            ).filter_by(tournament_id=similar.id).first()
            
            ratings_count = ratings_data[0] if ratings_data else 0
            avg_rating = float(ratings_data[1]) if ratings_data and ratings_data[1] else 0
            
            score = favorites * 2 + ratings_count * 1.5 + avg_rating * 10
            popularity_scores.append(score)
        
        # Предсказание
        avg_popularity = sum(popularity_scores) / len(popularity_scores)
        std_dev = math.sqrt(sum((x - avg_popularity) ** 2 for x in popularity_scores) / len(popularity_scores))
        
        # Классификация
        if avg_popularity >= 50:
            prediction = 'high'
            confidence = 0.8
        elif avg_popularity >= 25:
            prediction = 'medium'
            confidence = 0.7
        else:
            prediction = 'low'
            confidence = 0.6
        
        return {
            'tournament_id': tournament_id,
            'prediction': prediction,
            'expected_score': round(avg_popularity, 2),
            'confidence': confidence,
            'similar_tournaments_analyzed': len(similar_tournaments),
            'factors': {
                'category': tournament.category,
                'location': tournament.location,
                'month': tournament.start_date.month if tournament.start_date else None
            }
        }
    
    def analyze_conversion_funnel(self) -> Dict[str, Any]:
        """
        Анализ воронки конверсии
        
        Этапы:
        1. Посетители (все пользователи)
        2. Регистрация
        3. Первое взаимодействие (избранное/рейтинг)
        4. Активные пользователи (>3 взаимодействий)
        5. Лояльные пользователи (>10 взаимодействий)
        """
        from app.models.user import User
        from app.models.favorite import FavoriteTournament
        from app.models.rating import TournamentRating
        from sqlalchemy import func
        
        # Всего пользователей
        total_users = User.query.count()
        
        # Пользователи с хотя бы одним взаимодействием
        users_with_interaction = db.session.query(
            func.count(func.distinct(FavoriteTournament.user_id))
        ).scalar() or 0
        
        # Активные пользователи (>3 взаимодействий)
        active_users = db.session.query(
            FavoriteTournament.user_id
        ).group_by(FavoriteTournament.user_id).having(
            func.count(FavoriteTournament.id) > 3
        ).count()
        
        # Лояльные пользователи (>10 взаимодействий)
        loyal_users = db.session.query(
            FavoriteTournament.user_id
        ).group_by(FavoriteTournament.user_id).having(
            func.count(FavoriteTournament.id) > 10
        ).count()
        
        # Расчет конверсий
        funnel = [
            {
                'stage': 'Registered Users',
                'count': total_users,
                'conversion_rate': 100.0
            },
            {
                'stage': 'First Interaction',
                'count': users_with_interaction,
                'conversion_rate': round((users_with_interaction / total_users * 100), 2) if total_users > 0 else 0
            },
            {
                'stage': 'Active Users',
                'count': active_users,
                'conversion_rate': round((active_users / total_users * 100), 2) if total_users > 0 else 0
            },
            {
                'stage': 'Loyal Users',
                'count': loyal_users,
                'conversion_rate': round((loyal_users / total_users * 100), 2) if total_users > 0 else 0
            }
        ]
        
        return {
            'funnel': funnel,
            'drop_off_analysis': self._analyze_drop_off(funnel),
            'generated_at': datetime.utcnow().isoformat()
        }
    
    def _analyze_drop_off(self, funnel: List[Dict]) -> List[Dict]:
        """Анализ отвала пользователей между этапами"""
        drop_offs = []
        
        for i in range(1, len(funnel)):
            prev_stage = funnel[i-1]
            curr_stage = funnel[i]
            
            drop_off_count = prev_stage['count'] - curr_stage['count']
            drop_off_rate = (drop_off_count / prev_stage['count'] * 100) if prev_stage['count'] > 0 else 0
            
            drop_offs.append({
                'from_stage': prev_stage['stage'],
                'to_stage': curr_stage['stage'],
                'drop_off_count': drop_off_count,
                'drop_off_rate': round(drop_off_rate, 2)
            })
        
        return drop_offs
    
    def generate_executive_summary(self) -> Dict[str, Any]:
        """
        Генерация executive summary для руководства
        
        Ключевые метрики и инсайты
        """
        engagement = self.analyze_user_engagement()
        trends = self.analyze_tournament_trends(months=3)
        funnel = self.analyze_conversion_funnel()
        
        # Ключевые метрики
        key_metrics = {
            'mau': engagement['mau'],
            'stickiness': engagement['stickiness'],
            'engagement_level': engagement['engagement_level'],
            'total_tournaments': sum(item['count'] for item in trends['monthly_growth']),
            'avg_monthly_growth': round(
                sum(item['growth_rate'] for item in trends['monthly_growth'] if item['growth_rate'])
                / len([item for item in trends['monthly_growth'] if item['growth_rate']]),
                2
            ) if any(item['growth_rate'] for item in trends['monthly_growth']) else 0
        }
        
        # Инсайты
        insights = []
        
        if key_metrics['stickiness'] < 10:
            insights.append({
                'type': 'warning',
                'message': 'Низкая вовлеченность пользователей. Рекомендуется улучшить UX и контент.'
            })
        
        if key_metrics['avg_monthly_growth'] < 0:
            insights.append({
                'type': 'alert',
                'message': 'Отрицательный рост турниров. Требуется анализ причин.'
            })
        elif key_metrics['avg_monthly_growth'] > 20:
            insights.append({
                'type': 'success',
                'message': 'Отличный рост турниров! Продолжайте в том же духе.'
            })
        
        # Анализ воронки
        first_interaction_rate = funnel['funnel'][1]['conversion_rate']
        if first_interaction_rate < 30:
            insights.append({
                'type': 'warning',
                'message': f'Только {first_interaction_rate}% пользователей взаимодействуют с турнирами. Улучшите onboarding.'
            })
        
        return {
            'key_metrics': key_metrics,
            'insights': insights,
            'recommendations': self._generate_recommendations(key_metrics, insights),
            'generated_at': datetime.utcnow().isoformat()
        }
    
    def _generate_recommendations(
        self,
        metrics: Dict[str, Any],
        insights: List[Dict]
    ) -> List[str]:
        """Генерация рекомендаций на основе метрик"""
        recommendations = []
        
        if metrics['stickiness'] < 15:
            recommendations.append("Внедрить программу лояльности для увеличения retention")
            recommendations.append("Добавить персонализированные уведомления")
        
        if metrics['avg_monthly_growth'] < 5:
            recommendations.append("Усилить маркетинговые активности")
            recommendations.append("Партнерство с шахматными организациями")
        
        if len([i for i in insights if i['type'] == 'warning']) > 2:
            recommendations.append("Провести пользовательское исследование (UX research)")
        
        return recommendations


# Глобальный экземпляр
advanced_analytics = AdvancedAnalytics()


# Импорт db
from app import db
