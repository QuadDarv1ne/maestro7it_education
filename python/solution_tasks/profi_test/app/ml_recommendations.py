# -*- coding: utf-8 -*-
"""
Модуль расширенной системы рекомендаций на основе машинного обучения для ПрофиТест
Предоставляет продвинутые возможности персонализированных рекомендаций
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Set, Any, Tuple
import logging
from dataclasses import dataclass, field
from collections import defaultdict
import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import random


class RecommendationType(Enum):
    """Типы рекомендаций"""
    CONTENT_BASED = 'content_based'
    COLLABORATIVE = 'collaborative'
    HYBRID = 'hybrid'
    CONTEXTUAL = 'contextual'
    TRENDING = 'trending'
    PERSONALIZED = 'personalized'


class RecommendationContext(Enum):
    """Контекст рекомендаций"""
    USER_PROFILE = 'user_profile'
    BEHAVIOR = 'behavior'
    TIME = 'time'
    LOCATION = 'location'
    DEVICE = 'device'
    SEASONAL = 'seasonal'


@dataclass
class UserPreference:
    """Предпочтения пользователя"""
    user_id: int
    interests: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    career_goals: List[str] = field(default_factory=list)
    preferred_content_types: List[str] = field(default_factory=list)
    interaction_history: List[Dict[str, Any]] = field(default_factory=list)
    preference_scores: Dict[str, float] = field(default_factory=dict)
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class Recommendation:
    """Класс рекомендации"""
    id: str
    target_id: str
    target_type: str
    score: float
    recommendation_type: RecommendationType
    context: List[RecommendationContext]
    created_at: datetime = field(default_factory=datetime.now)
    explanation: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    expires_at: Optional[datetime] = None


class MLRecommendationEngine:
    """
    Движок рекомендаций на основе машинного обучения для системы ПрофиТест.
    Обеспечивает персонализированные рекомендации с использованием различных алгоритмов.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.recommendations: Dict[str, Recommendation] = {}
        self.user_preferences: Dict[int, UserPreference] = {}
        self.content_features: Dict[str, Dict[str, Any]] = {}
        self.user_item_matrix: pd.DataFrame = None
        self.content_similarity_matrix: np.ndarray = None
        self.user_clusters: Dict[int, int] = {}
        
        # Модели машинного обучения
        self.tfidf_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.scaler = StandardScaler()
        self.kmeans_model = None
        
        # Настройки рекомендаций
        self.recommendation_config = {
            'max_recommendations': 20,
            'min_similarity_threshold': 0.3,
            'diversity_factor': 0.7,
            'freshness_boost': 0.1,
            'popularity_weight': 0.2
        }
        
        # Инициализация системных рекомендаций
        self._initialize_system_data()
    
    def _initialize_system_data(self):
        """Инициализирует системные данные для рекомендаций"""
        # Создаем тестовые данные пользователей
        self._create_sample_users()
        # Создаем тестовые данные контента
        self._create_sample_content()
        # Обучаем модели
        self._train_models()
    
    def _create_sample_users(self):
        """Создает тестовые данные пользователей"""
        sample_users = [
            {
                'user_id': 1,
                'interests': ['психология', 'карьера', 'саморазвитие'],
                'skills': ['анализ', 'коммуникация', 'планирование'],
                'career_goals': ['менеджмент', 'HR', 'бизнес-аналитика'],
                'preferred_content_types': ['test', 'article', 'video']
            },
            {
                'user_id': 2,
                'interests': ['технологии', 'программирование', 'data science'],
                'skills': ['Python', 'SQL', 'машинное обучение'],
                'career_goals': ['data scientist', 'разработчик', 'аналитик'],
                'preferred_content_types': ['course', 'test', 'tutorial']
            },
            {
                'user_id': 3,
                'interests': ['дизайн', 'творчество', 'маркетинг'],
                'skills': ['графический дизайн', 'Photoshop', 'брендинг'],
                'career_goals': ['дизайнер', 'арт-директор', 'креативный директор'],
                'preferred_content_types': ['portfolio', 'article', 'video']
            }
        ]
        
        for user_data in sample_users:
            preference = UserPreference(**user_data)
            self.user_preferences[user_data['user_id']] = preference
    
    def _create_sample_content(self):
        """Создает тестовые данные контента"""
        sample_content = [
            {
                'id': 'content_1',
                'type': 'test',
                'title': 'Профориентационный тест Холланда',
                'description': 'Классический тест для определения профессиональных интересов',
                'category': 'psychology',
                'tags': ['психология', 'карьера', 'профориентация', 'Холланд'],
                'difficulty': 'medium',
                'estimated_time': 30,
                'popularity_score': 0.85
            },
            {
                'id': 'content_2',
                'type': 'test',
                'title': 'Тест Климова по профессиональным склонностям',
                'description': 'Тест для определения профессиональных склонностей',
                'category': 'psychology',
                'tags': ['психология', 'карьера', 'профориентация', 'Климов'],
                'difficulty': 'medium',
                'estimated_time': 25,
                'popularity_score': 0.78
            },
            {
                'id': 'content_3',
                'type': 'course',
                'title': 'Основы Python для анализа данных',
                'description': 'Изучите Python с нуля для анализа данных',
                'category': 'programming',
                'tags': ['Python', 'data science', 'программирование', 'анализ данных'],
                'difficulty': 'beginner',
                'estimated_time': 120,
                'popularity_score': 0.92
            },
            {
                'id': 'content_4',
                'type': 'article',
                'title': 'Как выбрать профессию в 2024 году',
                'description': 'Актуальные советы по выбору профессии',
                'category': 'career',
                'tags': ['карьера', 'советы', '2024', 'профессия'],
                'difficulty': 'easy',
                'estimated_time': 15,
                'popularity_score': 0.88
            },
            {
                'id': 'content_5',
                'type': 'video',
                'title': 'Тренды рынка труда 2024',
                'description': 'Анализ текущих трендов на рынке труда',
                'category': 'market',
                'tags': ['рынок труда', 'тренды', '2024', 'аналитика'],
                'difficulty': 'medium',
                'estimated_time': 45,
                'popularity_score': 0.81
            }
        ]
        
        for content in sample_content:
            self.content_features[content['id']] = content
    
    def _train_models(self):
        """Обучает модели машинного обучения"""
        try:
            # Создаем матрицу пользователь-контент
            self._build_user_item_matrix()
            
            # Создаем матрицу схожести контента
            self._build_content_similarity_matrix()
            
            # Кластеризуем пользователей
            self._cluster_users()
            
            self.logger.info("Модели машинного обучения успешно обучены")
        except Exception as e:
            self.logger.error(f"Ошибка при обучении моделей: {str(e)}")
    
    def _build_user_item_matrix(self):
        """Создает матрицу пользователь-контент"""
        # В реальной системе здесь будут реальные данные взаимодействий
        # Пока создаем тестовую матрицу
        user_ids = list(self.user_preferences.keys())
        content_ids = list(self.content_features.keys())
        
        # Создаем случайную матрицу взаимодействий
        interactions = np.random.rand(len(user_ids), len(content_ids))
        self.user_item_matrix = pd.DataFrame(
            interactions, 
            index=user_ids, 
            columns=content_ids
        )
    
    def _build_content_similarity_matrix(self):
        """Создает матрицу схожести контента"""
        try:
            content_ids = list(self.content_features.keys())
            content_texts = []
            
            # Создаем текстовые описания контента
            for content_id in content_ids:
                content = self.content_features[content_id]
                text = f"{content['title']} {content['description']} {' '.join(content['tags'])}"
                content_texts.append(text)
            
            # Векторизуем тексты
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(content_texts)
            
            # Рассчитываем матрицу схожести
            self.content_similarity_matrix = cosine_similarity(tfidf_matrix)
            
        except Exception as e:
            self.logger.error(f"Ошибка при создании матрицы схожести: {str(e)}")
            # Создаем случайную матрицу как запасной вариант
            n_content = len(self.content_features)
            self.content_similarity_matrix = np.random.rand(n_content, n_content)
    
    def _cluster_users(self):
        """Кластеризует пользователей"""
        try:
            if len(self.user_preferences) < 2:
                return
            
            # Создаем признаковое пространство пользователей
            user_features = []
            user_ids = []
            
            for user_id, preference in self.user_preferences.items():
                # Создаем числовые признаки из предпочтений
                feature_vector = [
                    len(preference.interests),
                    len(preference.skills),
                    len(preference.career_goals),
                    len(preference.preferred_content_types),
                    len(preference.interaction_history)
                ]
                user_features.append(feature_vector)
                user_ids.append(user_id)
            
            # Нормализуем признаки
            if user_features:
                user_features_scaled = self.scaler.fit_transform(user_features)
                
                # Кластеризуем
                n_clusters = min(3, len(user_features))
                self.kmeans_model = KMeans(n_clusters=n_clusters, random_state=42)
                cluster_labels = self.kmeans_model.fit_predict(user_features_scaled)
                
                # Сохраняем кластеры
                for user_id, cluster_id in zip(user_ids, cluster_labels):
                    self.user_clusters[user_id] = cluster_id
                
                self.logger.info(f"Пользователи кластеризованы в {n_clusters} кластеров")
            
        except Exception as e:
            self.logger.error(f"Ошибка при кластеризации пользователей: {str(e)}")
    
    def update_user_preference(self, user_id: int, preference_type: str, 
                             values: List[str], weight: float = 1.0) -> bool:
        """
        Обновляет предпочтения пользователя.
        
        Args:
            user_id: ID пользователя
            preference_type: Тип предпочтения (interests, skills, etc.)
            values: Значения предпочтений
            weight: Вес предпочтения
            
        Returns:
            bool: Успешность операции
        """
        try:
            if user_id not in self.user_preferences:
                self.user_preferences[user_id] = UserPreference(user_id=user_id)
            
            preference = self.user_preferences[user_id]
            
            # Обновляем соответствующее поле
            if hasattr(preference, preference_type):
                current_values = getattr(preference, preference_type)
                # Добавляем новые значения
                for value in values:
                    if value not in current_values:
                        current_values.append(value)
                
                # Обновляем веса предпочтений
                for value in values:
                    current_score = preference.preference_scores.get(value, 0)
                    preference.preference_scores[value] = current_score + weight
            
            preference.last_updated = datetime.now()
            
            # Переобучаем модели если нужно
            self._train_models()
            
            self.logger.info(f"Предпочтения пользователя {user_id} обновлены")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при обновлении предпочтений: {str(e)}")
            return False
    
    def get_content_based_recommendations(self, user_id: int, 
                                        limit: int = 10) -> List[Recommendation]:
        """
        Получает рекомендации на основе контента.
        
        Args:
            user_id: ID пользователя
            limit: Максимальное количество рекомендаций
            
        Returns:
            list: Список рекомендаций
        """
        try:
            if user_id not in self.user_preferences:
                return []
            
            user_preference = self.user_preferences[user_id]
            recommendations = []
            
            # Получаем контент, с которым пользователь уже взаимодействовал
            user_interactions = [item['content_id'] for item in user_preference.interaction_history]
            
            # Для каждого контента рассчитываем релевантность
            content_scores = []
            for content_id, content_features in self.content_features.items():
                if content_id in user_interactions:
                    continue  # Пропускаем уже просмотренный контент
                
                # Рассчитываем оценку релевантности
                score = self._calculate_content_relevance(user_preference, content_features)
                
                if score >= self.recommendation_config['min_similarity_threshold']:
                    content_scores.append((content_id, score))
            
            # Сортируем по релевантности
            content_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Создаем объекты рекомендаций
            for i, (content_id, score) in enumerate(content_scores[:limit]):
                import uuid
                recommendation_id = str(uuid.uuid4())
                
                recommendation = Recommendation(
                    id=recommendation_id,
                    target_id=content_id,
                    target_type=self.content_features[content_id]['type'],
                    score=score,
                    recommendation_type=RecommendationType.CONTENT_BASED,
                    context=[RecommendationContext.USER_PROFILE, RecommendationContext.BEHAVIOR],
                    explanation=f"Рекомендовано на основе ваших интересов и предпочтений",
                    metadata={
                        'relevance_factors': ['interests', 'skills', 'content_similarity'],
                        'confidence': round(score, 3)
                    }
                )
                
                self.recommendations[recommendation_id] = recommendation
                recommendations.append(recommendation)
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Ошибка при получении рекомендаций на основе контента: {str(e)}")
            return []
    
    def _calculate_content_relevance(self, user_preference: UserPreference, 
                                   content_features: Dict[str, Any]) -> float:
        """
        Рассчитывает релевантность контента для пользователя.
        
        Args:
            user_preference: Предпочтения пользователя
            content_features: Характеристики контента
            
        Returns:
            float: Оценка релевантности (0-1)
        """
        score = 0.0
        weight_sum = 0.0
        
        # Релевантность по интересам (вес 0.4)
        interests_match = len(set(user_preference.interests) & set(content_features['tags']))
        if user_preference.interests:
            score += (interests_match / len(user_preference.interests)) * 0.4
        weight_sum += 0.4
        
        # Релевантность по навыкам (вес 0.3)
        skills_match = len(set(user_preference.skills) & set(content_features['tags']))
        if user_preference.skills:
            score += (skills_match / len(user_preference.skills)) * 0.3
        weight_sum += 0.3
        
        # Релевантность по целям карьеры (вес 0.2)
        goals_match = len(set(user_preference.career_goals) & set(content_features['tags']))
        if user_preference.career_goals:
            score += (goals_match / len(user_preference.career_goals)) * 0.2
        weight_sum += 0.2
        
        # Релевантность по типу контента (вес 0.1)
        if content_features['type'] in user_preference.preferred_content_types:
            score += 0.1
        weight_sum += 0.1
        
        # Нормализуем оценку
        if weight_sum > 0:
            score = score / weight_sum
        
        # Добавляем компонент свежести
        if 'created_at' in content_features:
            days_old = (datetime.now() - content_features['created_at']).days
            freshness_factor = max(0.5, 1.0 - (days_old / 365) * 0.5)
            score = score * (1 + self.recommendation_config['freshness_boost'] * freshness_factor)
        
        # Добавляем компонент популярности
        popularity = content_features.get('popularity_score', 0.5)
        score = score * (1 + self.recommendation_config['popularity_weight'] * popularity)
        
        return min(1.0, max(0.0, score))
    
    def get_collaborative_recommendations(self, user_id: int, 
                                        limit: int = 10) -> List[Recommendation]:
        """
        Получает коллаборативные рекомендации.
        
        Args:
            user_id: ID пользователя
            limit: Максимальное количество рекомендаций
            
        Returns:
            list: Список рекомендаций
        """
        try:
            if user_id not in self.user_item_matrix.index:
                return []
            
            # Находим похожих пользователей
            user_similarities = self._calculate_user_similarities(user_id)
            
            # Получаем рекомендации от похожих пользователей
            recommendations = []
            user_items = set(self.user_item_matrix.loc[user_id][self.user_item_matrix.loc[user_id] > 0].index)
            
            for similar_user_id, similarity in user_similarities:
                if similar_user_id == user_id:
                    continue
                
                # Получаем контент, который нравится похожему пользователю
                similar_user_items = set(self.user_item_matrix.loc[similar_user_id][self.user_item_matrix.loc[similar_user_id] > 0.5].index)
                
                # Находим новый контент для рекомендации
                new_items = similar_user_items - user_items
                
                for item_id in list(new_items)[:3]:  # Максимум 3 рекомендации от каждого пользователя
                    if len(recommendations) >= limit:
                        break
                    
                    import uuid
                    recommendation_id = str(uuid.uuid4())
                    
                    score = similarity * self.user_item_matrix.loc[similar_user_id, item_id]
                    
                    recommendation = Recommendation(
                        id=recommendation_id,
                        target_id=item_id,
                        target_type=self.content_features.get(item_id, {}).get('type', 'unknown'),
                        score=score,
                        recommendation_type=RecommendationType.COLLABORATIVE,
                        context=[RecommendationContext.BEHAVIOR],
                        explanation=f"Рекомендовано потому что похожим пользователям это понравилось",
                        metadata={
                            'similar_users_count': len(user_similarities),
                            'similarity_score': round(similarity, 3),
                            'confidence': round(score, 3)
                        }
                    )
                    
                    self.recommendations[recommendation_id] = recommendation
                    recommendations.append(recommendation)
            
            return recommendations[:limit]
            
        except Exception as e:
            self.logger.error(f"Ошибка при получении коллаборативных рекомендаций: {str(e)}")
            return []
    
    def _calculate_user_similarities(self, target_user_id: int) -> List[Tuple[int, float]]:
        """
        Рассчитывает схожесть пользователей.
        
        Args:
            target_user_id: ID целевого пользователя
            
        Returns:
            list: Список (user_id, similarity_score)
        """
        try:
            if self.user_item_matrix is None or target_user_id not in self.user_item_matrix.index:
                return []
            
            target_user_vector = self.user_item_matrix.loc[target_user_id].values
            similarities = []
            
            for user_id in self.user_item_matrix.index:
                if user_id == target_user_id:
                    continue
                
                user_vector = self.user_item_matrix.loc[user_id].values
                
                # Рассчитываем косинусное сходство
                dot_product = np.dot(target_user_vector, user_vector)
                norm_target = np.linalg.norm(target_user_vector)
                norm_user = np.linalg.norm(user_vector)
                
                if norm_target > 0 and norm_user > 0:
                    similarity = dot_product / (norm_target * norm_user)
                    similarities.append((user_id, similarity))
            
            # Сортируем по убыванию схожести
            similarities.sort(key=lambda x: x[1], reverse=True)
            return similarities[:10]  # Возвращаем топ-10 похожих пользователей
            
        except Exception as e:
            self.logger.error(f"Ошибка при расчете схожести пользователей: {str(e)}")
            return []
    
    def get_hybrid_recommendations(self, user_id: int, 
                                 limit: int = 10) -> List[Recommendation]:
        """
        Получает гибридные рекомендации (комбинация подходов).
        
        Args:
            user_id: ID пользователя
            limit: Максимальное количество рекомендаций
            
        Returns:
            list: Список рекомендаций
        """
        try:
            # Получаем рекомендации разными методами
            content_based = self.get_content_based_recommendations(user_id, limit * 2)
            collaborative = self.get_collaborative_recommendations(user_id, limit * 2)
            
            # Комбинируем рекомендации
            all_recommendations = content_based + collaborative
            
            # Удаляем дубликаты
            unique_recommendations = []
            seen_targets = set()
            
            for rec in all_recommendations:
                if rec.target_id not in seen_targets:
                    unique_recommendations.append(rec)
                    seen_targets.add(rec.target_id)
            
            # Сортируем по комбинированной оценке
            unique_recommendations.sort(key=lambda x: x.score, reverse=True)
            
            # Применяем фактор разнообразия
            final_recommendations = self._apply_diversity_filter(unique_recommendations, limit)
            
            return final_recommendations
            
        except Exception as e:
            self.logger.error(f"Ошибка при получении гибридных рекомендаций: {str(e)}")
            return []
    
    def _apply_diversity_filter(self, recommendations: List[Recommendation], 
                              limit: int) -> List[Recommendation]:
        """
        Применяет фильтр разнообразия к рекомендациям.
        
        Args:
            recommendations: Список рекомендаций
            limit: Максимальное количество
            
        Returns:
            list: Отфильтрованные рекомендации
        """
        if not recommendations:
            return []
        
        diversity_factor = self.recommendation_config['diversity_factor']
        selected = []
        category_counts = defaultdict(int)
        
        for rec in recommendations:
            if len(selected) >= limit:
                break
            
            content_features = self.content_features.get(rec.target_id, {})
            category = content_features.get('category', 'unknown')
            
            # Рассчитываем штраф за дублирование категории
            category_penalty = category_counts[category] * (1 - diversity_factor)
            adjusted_score = rec.score * (1 - category_penalty)
            
            if len(selected) == 0 or adjusted_score > 0.3:  # Минимальный порог
                selected.append(rec)
                category_counts[category] += 1
        
        return selected
    
    def get_trending_recommendations(self, limit: int = 10) -> List[Recommendation]:
        """
        Получает трендовые рекомендации.
        
        Args:
            limit: Максимальное количество рекомендаций
            
        Returns:
            list: Список рекомендаций
        """
        try:
            trending_content = []
            
            # Рассчитываем трендовый рейтинг для каждого контента
            for content_id, features in self.content_features.items():
                trend_score = self._calculate_trend_score(content_id, features)
                trending_content.append((content_id, trend_score))
            
            # Сортируем по трендовому рейтингу
            trending_content.sort(key=lambda x: x[1], reverse=True)
            
            # Создаем рекомендации
            recommendations = []
            for i, (content_id, score) in enumerate(trending_content[:limit]):
                import uuid
                recommendation_id = str(uuid.uuid4())
                
                recommendation = Recommendation(
                    id=recommendation_id,
                    target_id=content_id,
                    target_type=self.content_features[content_id]['type'],
                    score=score,
                    recommendation_type=RecommendationType.TRENDING,
                    context=[RecommendationContext.TIME],
                    explanation="Популярный контент среди пользователей",
                    metadata={
                        'trend_factor': 'popularity_growth',
                        'confidence': round(score, 3)
                    }
                )
                
                self.recommendations[recommendation_id] = recommendation
                recommendations.append(recommendation)
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Ошибка при получении трендовых рекомендаций: {str(e)}")
            return []
    
    def _calculate_trend_score(self, content_id: str, 
                             content_features: Dict[str, Any]) -> float:
        """
        Рассчитывает трендовый рейтинг контента.
        
        Args:
            content_id: ID контента
            content_features: Характеристики контента
            
        Returns:
            float: Трендовый рейтинг
        """
        # Базовый рейтинг на основе популярности
        base_score = content_features.get('popularity_score', 0.5)
        
        # Фактор свежести (новый контент получает бонус)
        if 'created_at' in content_features:
            days_old = (datetime.now() - content_features['created_at']).days
            freshness_bonus = max(0, 1.0 - days_old / 30)  # Максимум 30 дней бонуса
            base_score *= (1 + 0.5 * freshness_bonus)
        
        # Фактор роста популярности (в реальной системе на основе исторических данных)
        growth_factor = 1.0 + random.uniform(-0.2, 0.3)  # Случайный фактор роста для демонстрации
        base_score *= growth_factor
        
        return min(1.0, max(0.0, base_score))
    
    def get_personalized_recommendations(self, user_id: int, 
                                       limit: int = 10) -> List[Recommendation]:
        """
        Получает персонализированные рекомендации.
        
        Args:
            user_id: ID пользователя
            limit: Максимальное количество рекомендаций
            
        Returns:
            list: Список рекомендаций
        """
        try:
            # Используем гибридный подход для персонализации
            return self.get_hybrid_recommendations(user_id, limit)
            
        except Exception as e:
            self.logger.error(f"Ошибка при получении персонализированных рекомендаций: {str(e)}")
            return []
    
    def record_user_interaction(self, user_id: int, content_id: str, 
                              interaction_type: str, rating: float = None) -> bool:
        """
        Записывает взаимодействие пользователя с контентом.
        
        Args:
            user_id: ID пользователя
            content_id: ID контента
            interaction_type: Тип взаимодействия
            rating: Оценка (опционально)
            
        Returns:
            bool: Успешность операции
        """
        try:
            if user_id not in self.user_preferences:
                self.user_preferences[user_id] = UserPreference(user_id=user_id)
            
            preference = self.user_preferences[user_id]
            
            interaction = {
                'content_id': content_id,
                'interaction_type': interaction_type,
                'timestamp': datetime.now(),
                'rating': rating
            }
            
            preference.interaction_history.append(interaction)
            
            # Ограничиваем историю взаимодействий
            if len(preference.interaction_history) > 100:
                preference.interaction_history = preference.interaction_history[-100:]
            
            # Обновляем матрицу пользователь-контент
            self._update_user_item_matrix(user_id, content_id, interaction_type, rating)
            
            self.logger.info(f"Взаимодействие пользователя {user_id} с контентом {content_id} записано")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при записи взаимодействия: {str(e)}")
            return False
    
    def _update_user_item_matrix(self, user_id: int, content_id: str, 
                               interaction_type: str, rating: float = None):
        """
        Обновляет матрицу пользователь-контент.
        
        Args:
            user_id: ID пользователя
            content_id: ID контента
            interaction_type: Тип взаимодействия
            rating: Оценка
        """
        try:
            if self.user_item_matrix is None:
                # Инициализируем матрицу если она не существует
                self.user_item_matrix = pd.DataFrame(
                    index=[user_id], 
                    columns=[content_id]
                ).fillna(0.0)
                return
            
            # Добавляем пользователя если нужно
            if user_id not in self.user_item_matrix.index:
                self.user_item_matrix.loc[user_id] = 0.0
            
            # Добавляем контент если нужно
            if content_id not in self.user_item_matrix.columns:
                self.user_item_matrix[content_id] = 0.0
            
            # Рассчитываем вес взаимодействия
            interaction_weights = {
                'view': 0.3,
                'like': 0.7,
                'share': 0.9,
                'complete': 1.0,
                'rate': rating or 0.5
            }
            
            weight = interaction_weights.get(interaction_type, 0.5)
            current_value = self.user_item_matrix.loc[user_id, content_id]
            
            # Обновляем значение (с учетом предыдущих взаимодействий)
            new_value = min(1.0, current_value + weight * 0.3)
            self.user_item_matrix.loc[user_id, content_id] = new_value
            
        except Exception as e:
            self.logger.error(f"Ошибка при обновлении матрицы: {str(e)}")
    
    def get_recommendation_statistics(self) -> Dict[str, Any]:
        """
        Получает статистику по рекомендациям.
        
        Returns:
            dict: Статистика системы рекомендаций
        """
        try:
            total_recommendations = len(self.recommendations)
            active_users = len(self.user_preferences)
            content_items = len(self.content_features)
            
            # Статистика по типам рекомендаций
            recommendation_types = defaultdict(int)
            for rec in self.recommendations.values():
                recommendation_types[rec.recommendation_type.value] += 1
            
            # Средние оценки
            avg_scores = defaultdict(list)
            for rec in self.recommendations.values():
                avg_scores[rec.recommendation_type.value].append(rec.score)
            
            avg_scores_result = {}
            for rec_type, scores in avg_scores.items():
                avg_scores_result[rec_type] = round(statistics.mean(scores), 3) if scores else 0
            
            return {
                'total_recommendations': total_recommendations,
                'active_users': active_users,
                'content_items': content_items,
                'recommendations_by_type': dict(recommendation_types),
                'average_scores_by_type': avg_scores_result,
                'user_clusters': len(set(self.user_clusters.values())) if self.user_clusters else 0,
                'content_similarity_matrix_size': self.content_similarity_matrix.shape if self.content_similarity_matrix is not None else (0, 0)
            }
            
        except Exception as e:
            self.logger.error(f"Ошибка при получении статистики рекомендаций: {str(e)}")
            return {}


def generate_ml_notifications():
    """Генерирует ML-уведомления для пользователей"""
    try:
        # Получаем все активные пользователи
        from app.models import User
        from app import db
        
        active_users = User.query.filter_by(is_active=True).all()
        notifications_generated = 0
        
        for user in active_users:
            # Генерируем персонализированные рекомендации
            recommendations = recommendation_engine.generate_personalized_recommendations(
                user_id=user.id, 
                num_recommendations=3
            )
            
            if recommendations:
                # Здесь можно добавить логику создания уведомлений
                notifications_generated += len(recommendations)
                
        logging.getLogger(__name__).info(f"Сгенерировано {notifications_generated} ML-уведомлений для {len(active_users)} пользователей")
        return True
        
    except Exception as e:
        logging.getLogger(__name__).error(f"Ошибка при генерации ML-уведомлений: {str(e)}")
        return False


# Глобальный экземпляр движка рекомендаций
recommendation_engine = MLRecommendationEngine()