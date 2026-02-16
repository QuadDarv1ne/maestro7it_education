"""
Система рекомендаций на основе Machine Learning
Улучшенные рекомендации турниров для пользователей
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, Counter
import math


class MLRecommendationEngine:
    """ML-движок для рекомендаций турниров"""
    
    def __init__(self):
        self.user_profiles = {}
        self.tournament_features = {}
        self.similarity_cache = {}
    
    def build_user_profile(self, user_id: int) -> Dict[str, Any]:
        """
        Построение профиля пользователя на основе его активности
        
        Включает:
        - Предпочтения по категориям
        - Предпочтения по локациям
        - Временные паттерны
        - Уровень активности
        """
        from app.models.favorite import FavoriteTournament
        from app.models.rating import TournamentRating
        from app.models.tournament import Tournament
        
        # Избранные турниры
        favorites = FavoriteTournament.query.filter_by(user_id=user_id).all()
        favorite_tournaments = [
            Tournament.query.get(fav.tournament_id)
            for fav in favorites
        ]
        favorite_tournaments = [t for t in favorite_tournaments if t]
        
        # Оцененные турниры
        ratings = TournamentRating.query.filter_by(user_id=user_id).all()
        rated_tournaments = [
            (Tournament.query.get(rating.tournament_id), rating.rating)
            for rating in ratings
        ]
        rated_tournaments = [(t, r) for t, r in rated_tournaments if t]
        
        # Анализ предпочтений по категориям
        category_scores = defaultdict(float)
        for tournament in favorite_tournaments:
            category_scores[tournament.category] += 1.0
        
        for tournament, rating in rated_tournaments:
            # Вес от 0 до 1 на основе рейтинга (1-5)
            weight = (rating - 1) / 4.0
            category_scores[tournament.category] += weight
        
        # Нормализация
        total_score = sum(category_scores.values())
        if total_score > 0:
            category_preferences = {
                cat: score / total_score
                for cat, score in category_scores.items()
            }
        else:
            category_preferences = {}
        
        # Анализ предпочтений по локациям
        location_scores = defaultdict(float)
        for tournament in favorite_tournaments:
            location_scores[tournament.location] += 1.0
        
        for tournament, rating in rated_tournaments:
            weight = (rating - 1) / 4.0
            location_scores[tournament.location] += weight
        
        total_location_score = sum(location_scores.values())
        if total_location_score > 0:
            location_preferences = {
                loc: score / total_location_score
                for loc, score in location_scores.items()
            }
        else:
            location_preferences = {}
        
        # Временные паттерны (предпочитаемые месяцы)
        month_preferences = defaultdict(int)
        for tournament in favorite_tournaments:
            if tournament.start_date:
                month_preferences[tournament.start_date.month] += 1
        
        profile = {
            'user_id': user_id,
            'category_preferences': category_preferences,
            'location_preferences': location_preferences,
            'month_preferences': dict(month_preferences),
            'total_favorites': len(favorites),
            'total_ratings': len(ratings),
            'avg_rating': sum(r for _, r in rated_tournaments) / len(rated_tournaments) if rated_tournaments else 0,
            'activity_level': self._calculate_activity_level(len(favorites), len(ratings))
        }
        
        self.user_profiles[user_id] = profile
        return profile
    
    def _calculate_activity_level(self, favorites: int, ratings: int) -> str:
        """Определение уровня активности пользователя"""
        total_activity = favorites + ratings
        
        if total_activity >= 20:
            return 'high'
        elif total_activity >= 10:
            return 'medium'
        elif total_activity >= 3:
            return 'low'
        else:
            return 'new'
    
    def extract_tournament_features(self, tournament) -> Dict[str, Any]:
        """
        Извлечение признаков турнира для ML
        
        Признаки:
        - Категория
        - Локация
        - Месяц проведения
        - Популярность (избранное, рейтинги)
        - Статус
        """
        from app.models.favorite import FavoriteTournament
        from app.models.rating import TournamentRating
        from sqlalchemy import func
        
        # Популярность
        favorites_count = FavoriteTournament.query.filter_by(
            tournament_id=tournament.id
        ).count()
        
        ratings_data = db.session.query(
            func.count(TournamentRating.id),
            func.avg(TournamentRating.rating)
        ).filter_by(tournament_id=tournament.id).first()
        
        ratings_count = ratings_data[0] if ratings_data else 0
        avg_rating = float(ratings_data[1]) if ratings_data and ratings_data[1] else 0
        
        features = {
            'tournament_id': tournament.id,
            'category': tournament.category,
            'location': tournament.location,
            'month': tournament.start_date.month if tournament.start_date else None,
            'favorites_count': favorites_count,
            'ratings_count': ratings_count,
            'avg_rating': avg_rating,
            'popularity_score': self._calculate_popularity_score(
                favorites_count, ratings_count, avg_rating
            ),
            'status': tournament.status
        }
        
        self.tournament_features[tournament.id] = features
        return features
    
    def _calculate_popularity_score(
        self,
        favorites: int,
        ratings: int,
        avg_rating: float
    ) -> float:
        """Расчет общего показателя популярности"""
        # Взвешенная формула
        score = (
            favorites * 2.0 +  # Избранное весит больше
            ratings * 1.5 +
            avg_rating * 10.0  # Рейтинг нормализован к 50
        )
        return score
    
    def calculate_recommendation_score(
        self,
        user_profile: Dict[str, Any],
        tournament_features: Dict[str, Any]
    ) -> float:
        """
        Расчет скора рекомендации для пары пользователь-турнир
        
        Использует:
        - Совпадение категорий
        - Совпадение локаций
        - Популярность турнира
        - Временные предпочтения
        """
        score = 0.0
        
        # Совпадение категории (вес 40%)
        category = tournament_features['category']
        if category in user_profile['category_preferences']:
            score += user_profile['category_preferences'][category] * 40.0
        
        # Совпадение локации (вес 30%)
        location = tournament_features['location']
        if location in user_profile['location_preferences']:
            score += user_profile['location_preferences'][location] * 30.0
        
        # Популярность турнира (вес 20%)
        popularity = tournament_features['popularity_score']
        # Нормализация популярности (логарифмическая шкала)
        normalized_popularity = math.log(popularity + 1) / math.log(100)
        score += min(normalized_popularity, 1.0) * 20.0
        
        # Временные предпочтения (вес 10%)
        month = tournament_features['month']
        if month and month in user_profile['month_preferences']:
            month_score = user_profile['month_preferences'][month]
            max_month_score = max(user_profile['month_preferences'].values()) if user_profile['month_preferences'] else 1
            score += (month_score / max_month_score) * 10.0
        
        return score
    
    def get_recommendations(
        self,
        user_id: int,
        limit: int = 10,
        exclude_favorites: bool = True
    ) -> List[Tuple[Any, float]]:
        """
        Получить рекомендации для пользователя
        
        Args:
            user_id: ID пользователя
            limit: Количество рекомендаций
            exclude_favorites: Исключить уже избранные турниры
        
        Returns:
            Список кортежей (турнир, скор)
        """
        from app.models.tournament import Tournament
        from app.models.favorite import FavoriteTournament
        
        # Построение профиля пользователя
        user_profile = self.build_user_profile(user_id)
        
        # Получение активных турниров
        tournaments = Tournament.query.filter(
            Tournament.start_date >= datetime.utcnow().date(),
            Tournament.status != 'Completed'
        ).all()
        
        # Исключение избранных
        if exclude_favorites:
            favorite_ids = {
                fav.tournament_id
                for fav in FavoriteTournament.query.filter_by(user_id=user_id).all()
            }
            tournaments = [t for t in tournaments if t.id not in favorite_ids]
        
        # Расчет скоров
        recommendations = []
        for tournament in tournaments:
            features = self.extract_tournament_features(tournament)
            score = self.calculate_recommendation_score(user_profile, features)
            recommendations.append((tournament, score))
        
        # Сортировка по скору
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return recommendations[:limit]
    
    def get_similar_tournaments(
        self,
        tournament_id: int,
        limit: int = 5
    ) -> List[Tuple[Any, float]]:
        """
        Найти похожие турниры
        
        Использует косинусное сходство признаков
        """
        from app.models.tournament import Tournament
        
        target_tournament = Tournament.query.get(tournament_id)
        if not target_tournament:
            return []
        
        target_features = self.extract_tournament_features(target_tournament)
        
        # Получение всех турниров
        all_tournaments = Tournament.query.filter(
            Tournament.id != tournament_id,
            Tournament.start_date >= datetime.utcnow().date()
        ).all()
        
        similarities = []
        for tournament in all_tournaments:
            features = self.extract_tournament_features(tournament)
            similarity = self._calculate_similarity(target_features, features)
            similarities.append((tournament, similarity))
        
        # Сортировка по сходству
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:limit]
    
    def _calculate_similarity(
        self,
        features1: Dict[str, Any],
        features2: Dict[str, Any]
    ) -> float:
        """
        Расчет сходства между двумя турнирами
        
        Использует взвешенное сходство признаков
        """
        similarity = 0.0
        
        # Категория (вес 50%)
        if features1['category'] == features2['category']:
            similarity += 50.0
        
        # Локация (вес 30%)
        if features1['location'] == features2['location']:
            similarity += 30.0
        
        # Месяц (вес 10%)
        if features1['month'] == features2['month']:
            similarity += 10.0
        
        # Популярность (вес 10%)
        pop1 = features1['popularity_score']
        pop2 = features2['popularity_score']
        if pop1 > 0 and pop2 > 0:
            pop_similarity = 1 - abs(pop1 - pop2) / max(pop1, pop2)
            similarity += pop_similarity * 10.0
        
        return similarity / 100.0  # Нормализация к [0, 1]
    
    def get_trending_tournaments(self, days: int = 7, limit: int = 10) -> List[Tuple[Any, float]]:
        """
        Получить трендовые турниры
        
        Основано на росте популярности за последние дни
        """
        from app.models.tournament import Tournament
        from app.models.favorite import FavoriteTournament
        from app.models.rating import TournamentRating
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Получение активных турниров
        tournaments = Tournament.query.filter(
            Tournament.start_date >= datetime.utcnow().date()
        ).all()
        
        trending = []
        for tournament in tournaments:
            # Активность за период
            recent_favorites = FavoriteTournament.query.filter(
                FavoriteTournament.tournament_id == tournament.id,
                FavoriteTournament.created_at >= cutoff_date
            ).count()
            
            recent_ratings = TournamentRating.query.filter(
                TournamentRating.tournament_id == tournament.id,
                TournamentRating.created_at >= cutoff_date
            ).count()
            
            # Расчет трендового скора
            trend_score = recent_favorites * 2.0 + recent_ratings * 1.5
            
            if trend_score > 0:
                trending.append((tournament, trend_score))
        
        # Сортировка по трендовому скору
        trending.sort(key=lambda x: x[1], reverse=True)
        
        return trending[:limit]
    
    def explain_recommendation(
        self,
        user_id: int,
        tournament_id: int
    ) -> Dict[str, Any]:
        """
        Объяснение, почему турнир рекомендован пользователю
        
        Для прозрачности рекомендаций
        """
        from app.models.tournament import Tournament
        
        tournament = Tournament.query.get(tournament_id)
        if not tournament:
            return {'error': 'Tournament not found'}
        
        user_profile = self.build_user_profile(user_id)
        tournament_features = self.extract_tournament_features(tournament)
        
        reasons = []
        
        # Категория
        category = tournament_features['category']
        if category in user_profile['category_preferences']:
            pref = user_profile['category_preferences'][category]
            reasons.append({
                'factor': 'category',
                'value': category,
                'score': pref * 40,
                'explanation': f"Вы часто интересуетесь турнирами категории '{category}'"
            })
        
        # Локация
        location = tournament_features['location']
        if location in user_profile['location_preferences']:
            pref = user_profile['location_preferences'][location]
            reasons.append({
                'factor': 'location',
                'value': location,
                'score': pref * 30,
                'explanation': f"Вы предпочитаете турниры в '{location}'"
            })
        
        # Популярность
        if tournament_features['popularity_score'] > 10:
            reasons.append({
                'factor': 'popularity',
                'value': tournament_features['popularity_score'],
                'score': 20,
                'explanation': "Этот турнир популярен среди других пользователей"
            })
        
        total_score = self.calculate_recommendation_score(user_profile, tournament_features)
        
        return {
            'tournament_id': tournament_id,
            'tournament_name': tournament.name,
            'total_score': round(total_score, 2),
            'reasons': reasons,
            'user_activity_level': user_profile['activity_level']
        }


# Глобальный экземпляр
ml_recommendation_engine = MLRecommendationEngine()


# Импорт db
from app import db
