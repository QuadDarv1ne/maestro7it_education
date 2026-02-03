# -*- coding: utf-8 -*-
"""
Модуль расширенной системы рейтингов и отзывов для ПрофиТест
Предоставляет продвинутые возможности управления рейтингами и отзывами
"""
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Any, Tuple
import logging
from dataclasses import dataclass, field
from collections import defaultdict
import statistics
from decimal import Decimal, ROUND_HALF_UP


class RatingType(Enum):
    """Типы рейтингов"""
    STAR_RATING = 'star'  # 1-5 звезд
    LIKE_DISLIKE = 'like_dislike'  # нравится/не нравится
    THUMBS = 'thumbs'  # большой палец вверх/вниз
    PERCENTAGE = 'percentage'  # 0-100%
    POINTS = 'points'  # произвольные баллы


class ReviewStatus(Enum):
    """Статусы отзывов"""
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    FLAGGED = 'flagged'
    DELETED = 'deleted'


class RatingDimension(Enum):
    """Измерения рейтинга"""
    OVERALL = 'overall'  # Общий рейтинг
    QUALITY = 'quality'  # Качество
    USABILITY = 'usability'  # Удобство использования
    SUPPORT = 'support'  # Поддержка
    VALUE = 'value'  # Соотношение цена/качество
    ACCURACY = 'accuracy'  # Точность


@dataclass
class Rating:
    """Класс рейтинга"""
    id: str
    target_id: str  # ID объекта, который оценивается
    target_type: str  # тип объекта (test, course, user и т.д.)
    user_id: int
    rating_type: RatingType
    value: float
    dimension: RatingDimension = RatingDimension.OVERALL
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    comment: Optional[str] = None
    is_anonymous: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Review:
    """Класс отзыва"""
    id: str
    target_id: str
    target_type: str
    user_id: int
    title: str
    content: str
    status: ReviewStatus
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    published_at: Optional[datetime] = None
    helpful_count: int = 0
    not_helpful_count: int = 0
    reports: int = 0
    is_verified: bool = False
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class RatingAggregator:
    """Агрегатор рейтингов"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.rating_weights: Dict[RatingDimension, float] = {
            RatingDimension.OVERALL: 0.4,
            RatingDimension.QUALITY: 0.25,
            RatingDimension.USABILITY: 0.15,
            RatingDimension.SUPPORT: 0.1,
            RatingDimension.VALUE: 0.1
        }
    
    def calculate_average_rating(self, ratings: List[Rating]) -> float:
        """
        Рассчитывает средний рейтинг.
        
        Args:
            ratings: Список рейтингов
            
        Returns:
            float: Средний рейтинг
        """
        if not ratings:
            return 0.0
        
        values = [r.value for r in ratings]
        return float(Decimal(str(statistics.mean(values))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
    
    def calculate_weighted_rating(self, ratings: List[Rating]) -> float:
        """
        Рассчитывает взвешенный рейтинг по измерениям.
        
        Args:
            ratings: Список рейтингов
            
        Returns:
            float: Взвешенный рейтинг
        """
        if not ratings:
            return 0.0
        
        # Группируем рейтинги по измерениям
        dimension_ratings = defaultdict(list)
        for rating in ratings:
            dimension_ratings[rating.dimension].append(rating.value)
        
        # Рассчитываем средние по измерениям
        weighted_sum = 0.0
        total_weight = 0.0
        
        for dimension, values in dimension_ratings.items():
            if values:
                avg_value = statistics.mean(values)
                weight = self.rating_weights.get(dimension, 0.1)
                weighted_sum += avg_value * weight
                total_weight += weight
        
        if total_weight == 0:
            return 0.0
            
        return float(Decimal(str(weighted_sum / total_weight)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
    
    def calculate_rating_distribution(self, ratings: List[Rating]) -> Dict[str, int]:
        """
        Рассчитывает распределение рейтингов.
        
        Args:
            ratings: Список рейтингов
            
        Returns:
            dict: Распределение рейтингов
        """
        distribution = defaultdict(int)
        
        for rating in ratings:
            # Для звездного рейтинга группируем по целым числам
            if rating.rating_type == RatingType.STAR_RATING:
                star_value = int(round(rating.value))
                distribution[f"{star_value}_stars"] += 1
            else:
                # Для других типов создаем диапазоны
                if rating.value >= 90:
                    distribution["90-100"] += 1
                elif rating.value >= 80:
                    distribution["80-89"] += 1
                elif rating.value >= 70:
                    distribution["70-79"] += 1
                elif rating.value >= 60:
                    distribution["60-69"] += 1
                else:
                    distribution["0-59"] += 1
        
        return dict(distribution)
    
    def calculate_rating_trend(self, ratings: List[Rating], 
                             period_days: int = 30) -> Dict[str, Any]:
        """
        Рассчитывает тренд рейтинга за период.
        
        Args:
            ratings: Список рейтингов
            period_days: Период в днях
            
        Returns:
            dict: Информация о тренде
        """
        if not ratings:
            return {'trend': 'no_data', 'change': 0.0, 'period_ratings': 0}
        
        cutoff_date = datetime.now() - timedelta(days=period_days)
        recent_ratings = [r for r in ratings if r.created_at >= cutoff_date]
        older_ratings = [r for r in ratings if r.created_at < cutoff_date]
        
        if not recent_ratings or not older_ratings:
            return {'trend': 'insufficient_data', 'change': 0.0, 'period_ratings': len(recent_ratings)}
        
        recent_avg = self.calculate_average_rating(recent_ratings)
        older_avg = self.calculate_average_rating(older_ratings)
        
        change = recent_avg - older_avg
        trend = 'improving' if change > 0 else 'declining' if change < 0 else 'stable'
        
        return {
            'trend': trend,
            'change': round(change, 2),
            'recent_average': round(recent_avg, 2),
            'older_average': round(older_avg, 2),
            'period_ratings': len(recent_ratings),
            'total_ratings': len(ratings)
        }


class AdvancedRatingManager:
    """
    Расширенный менеджер рейтингов и отзывов для системы ПрофиТест.
    Обеспечивает управление рейтингами, отзывами и аналитику.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ratings: Dict[str, Rating] = {}
        self.reviews: Dict[str, Review] = {}
        self.target_ratings: Dict[str, Set[str]] = defaultdict(set)  # target_id -> rating_ids
        self.target_reviews: Dict[str, Set[str]] = defaultdict(set)  # target_id -> review_ids
        self.user_ratings: Dict[int, Set[str]] = defaultdict(set)   # user_id -> rating_ids
        self.user_reviews: Dict[int, Set[str]] = defaultdict(set)   # user_id -> review_ids
        
        self.aggregator = RatingAggregator()
        self.trusted_users: Set[int] = set()
        
        # Инициализация системных рейтингов
        self._create_system_ratings()
    
    def _create_system_ratings(self):
        """Создает системные рейтинги по умолчанию"""
        pass  # Пока пусто, можно добавить примеры позже
    
    def add_rating(self, target_id: str, target_type: str, user_id: int,
                   rating_type: RatingType, value: float, 
                   dimension: RatingDimension = RatingDimension.OVERALL,
                   comment: str = None, is_anonymous: bool = False,
                   metadata: Dict[str, Any] = None) -> Optional[str]:
        """
        Добавляет новый рейтинг.
        
        Args:
            target_id: ID объекта
            target_type: Тип объекта
            user_id: ID пользователя
            rating_type: Тип рейтинга
            value: Значение рейтинга
            dimension: Измерение рейтинга
            comment: Комментарий
            is_anonymous: Анонимный рейтинг
            metadata: Метаданные
            
        Returns:
            str: ID рейтинга или None
        """
        try:
            import uuid
            rating_id = str(uuid.uuid4())
            
            # Валидация значения рейтинга
            if not self._validate_rating_value(rating_type, value):
                self.logger.warning(f"Некорректное значение рейтинга: {value} для типа {rating_type}")
                return None
            
            rating = Rating(
                id=rating_id,
                target_id=target_id,
                target_type=target_type,
                user_id=user_id,
                rating_type=rating_type,
                value=value,
                dimension=dimension,
                comment=comment,
                is_anonymous=is_anonymous,
                metadata=metadata or {}
            )
            
            # Добавляем рейтинг
            self.ratings[rating_id] = rating
            self.target_ratings[target_id].add(rating_id)
            self.user_ratings[user_id].add(rating_id)
            
            self.logger.info(f"Рейтинг {rating_id} добавлен для {target_type} {target_id}")
            return rating_id
            
        except Exception as e:
            self.logger.error(f"Ошибка при добавлении рейтинга: {str(e)}")
            return None
    
    def _validate_rating_value(self, rating_type: RatingType, value: float) -> bool:
        """
        Проверяет корректность значения рейтинга.
        
        Args:
            rating_type: Тип рейтинга
            value: Значение
            
        Returns:
            bool: Корректность значения
        """
        if rating_type == RatingType.STAR_RATING:
            return 1.0 <= value <= 5.0
        elif rating_type == RatingType.PERCENTAGE:
            return 0.0 <= value <= 100.0
        elif rating_type == RatingType.LIKE_DISLIKE:
            return value in [0.0, 1.0]  # 0 - dislike, 1 - like
        elif rating_type == RatingType.THUMBS:
            return value in [0.0, 1.0]  # 0 - down, 1 - up
        else:  # POINTS
            return value >= 0.0
    
    def get_ratings_for_target(self, target_id: str) -> List[Rating]:
        """
        Получает все рейтинги для объекта.
        
        Args:
            target_id: ID объекта
            
        Returns:
            list: Список рейтингов
        """
        rating_ids = self.target_ratings.get(target_id, set())
        return [self.ratings[rid] for rid in rating_ids if rid in self.ratings]
    
    def get_user_ratings(self, user_id: int) -> List[Rating]:
        """
        Получает все рейтинги пользователя.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            list: Список рейтингов
        """
        rating_ids = self.user_ratings.get(user_id, set())
        return [self.ratings[rid] for rid in rating_ids if rid in self.ratings]
    
    def calculate_target_rating(self, target_id: str, 
                              method: str = 'average') -> Dict[str, Any]:
        """
        Рассчитывает рейтинг для объекта.
        
        Args:
            target_id: ID объекта
            method: Метод расчета ('average', 'weighted', 'bayesian')
            
        Returns:
            dict: Информация о рейтинге
        """
        ratings = self.get_ratings_for_target(target_id)
        if not ratings:
            return {
                'rating': 0.0,
                'count': 0,
                'distribution': {},
                'trend': {}
            }
        
        if method == 'average':
            rating_value = self.aggregator.calculate_average_rating(ratings)
        elif method == 'weighted':
            rating_value = self.aggregator.calculate_weighted_rating(ratings)
        else:  # bayesian
            rating_value = self._calculate_bayesian_average(ratings)
        
        distribution = self.aggregator.calculate_rating_distribution(ratings)
        trend = self.aggregator.calculate_rating_trend(ratings)
        
        return {
            'rating': round(rating_value, 2),
            'count': len(ratings),
            'distribution': distribution,
            'trend': trend,
            'method': method
        }
    
    def _calculate_bayesian_average(self, ratings: List[Rating]) -> float:
        """
        Рассчитывает байесовский средний рейтинг.
        
        Args:
            ratings: Список рейтингов
            
        Returns:
            float: Байесовский средний
        """
        if not ratings:
            return 0.0
        
        # Параметры для байесовского среднего
        global_avg = 3.0  # Глобальное среднее (предположение)
        min_ratings = 5   # Минимальное количество рейтингов
        
        values = [r.value for r in ratings]
        avg = statistics.mean(values)
        count = len(values)
        
        # Байесовская формула: (C * m + R * v) / (C + R)
        # где C = min_ratings, m = global_avg, R = count, v = avg
        bayesian_avg = (min_ratings * global_avg + count * avg) / (min_ratings + count)
        return round(bayesian_avg, 2)
    
    def add_review(self, target_id: str, target_type: str, user_id: int,
                   title: str, content: str, is_verified: bool = False,
                   tags: List[str] = None, metadata: Dict[str, Any] = None) -> Optional[str]:
        """
        Добавляет новый отзыв.
        
        Args:
            target_id: ID объекта
            target_type: Тип объекта
            user_id: ID пользователя
            title: Заголовок отзыва
            content: Содержание отзыва
            is_verified: Проверенный отзыв
            tags: Теги
            metadata: Метаданные
            
        Returns:
            str: ID отзыва или None
        """
        try:
            import uuid
            review_id = str(uuid.uuid4())
            
            review = Review(
                id=review_id,
                target_id=target_id,
                target_type=target_type,
                user_id=user_id,
                title=title,
                content=content,
                status=ReviewStatus.PENDING,
                is_verified=is_verified,
                tags=tags or [],
                metadata=metadata or {}
            )
            
            # Добавляем отзыв
            self.reviews[review_id] = review
            self.target_reviews[target_id].add(review_id)
            self.user_reviews[user_id].add(review_id)
            
            self.logger.info(f"Отзыв {review_id} добавлен для {target_type} {target_id}")
            return review_id
            
        except Exception as e:
            self.logger.error(f"Ошибка при добавлении отзыва: {str(e)}")
            return None
    
    def get_reviews_for_target(self, target_id: str, 
                             status: ReviewStatus = None) -> List[Review]:
        """
        Получает отзывы для объекта.
        
        Args:
            target_id: ID объекта
            status: Фильтр по статусу
            
        Returns:
            list: Список отзывов
        """
        review_ids = self.target_reviews.get(target_id, set())
        reviews = [self.reviews[rid] for rid in review_ids if rid in self.reviews]
        
        if status:
            reviews = [r for r in reviews if r.status == status]
        
        # Сортировка по полезности и дате
        reviews.sort(key=lambda x: (x.helpful_count - x.not_helpful_count, x.created_at), reverse=True)
        return reviews
    
    def mark_review_helpful(self, review_id: str, user_id: int, helpful: bool) -> bool:
        """
        Помечает отзыв как полезный/неполезный.
        
        Args:
            review_id: ID отзыва
            user_id: ID пользователя
            helpful: Полезен или нет
            
        Returns:
            bool: Успешность операции
        """
        try:
            review = self.reviews.get(review_id)
            if not review:
                return False
            
            if helpful:
                review.helpful_count += 1
            else:
                review.not_helpful_count += 1
            
            self.logger.info(f"Отзыв {review_id} помечен как {'полезный' if helpful else 'неполезный'} пользователем {user_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при пометке отзыва: {str(e)}")
            return False
    
    def report_review(self, review_id: str, user_id: int, reason: str) -> bool:
        """
        Отмечает отзыв как неприемлемый.
        
        Args:
            review_id: ID отзыва
            user_id: ID пользователя
            reason: Причина жалобы
            
        Returns:
            bool: Успешность операции
        """
        try:
            review = self.reviews.get(review_id)
            if not review:
                return False
            
            review.reports += 1
            
            # Автоматически флагуем при большом количестве жалоб
            if review.reports >= 3:
                review.status = ReviewStatus.FLAGGED
                self.logger.info(f"Отзыв {review_id} автоматически помечен как подозрительный")
            
            self.logger.info(f"Жалоба на отзыв {review_id} от пользователя {user_id}: {reason}")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при подаче жалобы: {str(e)}")
            return False
    
    def get_top_rated_targets(self, target_type: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Получает объекты с наивысшими рейтингами.
        
        Args:
            target_type: Тип объектов
            limit: Максимальное количество
            
        Returns:
            list: Список объектов с рейтингами
        """
        # Находим все объекты указанного типа
        target_ids = set()
        for rating in self.ratings.values():
            if rating.target_type == target_type:
                target_ids.add(rating.target_id)
        
        # Рассчитываем рейтинги для каждого объекта
        rated_targets = []
        for target_id in target_ids:
            rating_info = self.calculate_target_rating(target_id)
            if rating_info['count'] > 0:  # Только объекты с рейтингами
                rated_targets.append({
                    'target_id': target_id,
                    'rating': rating_info['rating'],
                    'count': rating_info['count'],
                    'trend': rating_info['trend']
                })
        
        # Сортировка по рейтингу и количеству отзывов
        rated_targets.sort(key=lambda x: (x['rating'], x['count']), reverse=True)
        return rated_targets[:limit]
    
    def get_user_contribution_stats(self, user_id: int) -> Dict[str, Any]:
        """
        Получает статистику вклада пользователя.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            dict: Статистика вклада
        """
        user_ratings = self.get_user_ratings(user_id)
        user_reviews = self.user_reviews.get(user_id, set())
        user_reviews = [self.reviews[rid] for rid in user_reviews if rid in self.reviews]
        
        # Рассчитываем статистику
        total_ratings = len(user_ratings)
        total_reviews = len(user_reviews)
        
        avg_rating_given = 0.0
        if user_ratings:
            avg_rating_given = statistics.mean([r.value for r in user_ratings])
        
        helpful_votes = sum(r.helpful_count for r in user_reviews)
        not_helpful_votes = sum(r.not_helpful_count for r in user_reviews)
        
        return {
            'user_id': user_id,
            'total_ratings': total_ratings,
            'total_reviews': total_reviews,
            'average_rating_given': round(avg_rating_given, 2),
            'helpful_votes_received': helpful_votes,
            'not_helpful_votes_received': not_helpful_votes,
            'helpfulness_ratio': round(helpful_votes / (helpful_votes + not_helpful_votes) if (helpful_votes + not_helpful_votes) > 0 else 0, 2),
            'verified_reviews': len([r for r in user_reviews if r.is_verified]),
            'approved_reviews': len([r for r in user_reviews if r.status == ReviewStatus.APPROVED])
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Получает статистику по рейтингам и отзывам.
        
        Returns:
            dict: Статистика системы
        """
        total_ratings = len(self.ratings)
        total_reviews = len(self.reviews)
        
        # Статистика по типам рейтингов
        rating_types = defaultdict(int)
        rating_dimensions = defaultdict(int)
        for rating in self.ratings.values():
            rating_types[rating.rating_type.value] += 1
            rating_dimensions[rating.dimension.value] += 1
        
        # Статистика по статусам отзывов
        review_statuses = defaultdict(int)
        for review in self.reviews.values():
            review_statuses[review.status.value] += 1
        
        # Средние значения
        rating_values = [r.value for r in self.ratings.values()]
        avg_rating = statistics.mean(rating_values) if rating_values else 0.0
        
        return {
            'total_ratings': total_ratings,
            'total_reviews': total_reviews,
            'total_targets_rated': len(self.target_ratings),
            'total_users_contributed': len(self.user_ratings),
            'average_rating': round(avg_rating, 2),
            'ratings_by_type': dict(rating_types),
            'ratings_by_dimension': dict(rating_dimensions),
            'reviews_by_status': dict(review_statuses),
            'verified_reviews': len([r for r in self.reviews.values() if r.is_verified]),
            'helpful_reviews': len([r for r in self.reviews.values() if r.helpful_count > r.not_helpful_count]),
            'flagged_content': len([r for r in self.reviews.values() if r.status == ReviewStatus.FLAGGED])
        }


# Глобальный экземпляр менеджера рейтингов
rating_manager = AdvancedRatingManager()