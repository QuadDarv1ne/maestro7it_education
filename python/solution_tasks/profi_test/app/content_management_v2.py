# -*- coding: utf-8 -*-
"""
Модуль расширенной системы управления контентом для ПрофиТест
Предоставляет продвинутые возможности управления, модерации и оптимизации контента
"""
import re
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Set, Any, Tuple
import logging
from dataclasses import dataclass, field
from collections import defaultdict
import json
from flask import current_app


class ContentType(Enum):
    """Типы контента"""
    TEST = 'test'
    ARTICLE = 'article'
    VIDEO = 'video'
    COURSE = 'course'
    PODCAST = 'podcast'
    INTERACTIVE = 'interactive'


class ContentStatus(Enum):
    """Статусы контента"""
    DRAFT = 'draft'
    PENDING_REVIEW = 'pending_review'
    PUBLISHED = 'published'
    ARCHIVED = 'archived'
    REJECTED = 'rejected'


class ContentQuality(Enum):
    """Качество контента"""
    EXCELLENT = 'excellent'
    GOOD = 'good'
    AVERAGE = 'average'
    POOR = 'poor'
    NEEDS_IMPROVEMENT = 'needs_improvement'


@dataclass
class ContentItem:
    """Элемент контента"""
    id: str
    title: str
    description: str
    content_type: ContentType
    author_id: int
    status: ContentStatus
    quality_score: float
    quality_level: ContentQuality
    tags: List[str]
    category: str
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None
    views: int = 0
    likes: int = 0
    shares: int = 0
    completion_rate: float = 0.0
    avg_rating: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    version: int = 1


@dataclass
class ContentReview:
    """Отзыв по контенту"""
    id: str
    content_id: str
    reviewer_id: int
    status: ContentStatus
    comments: str
    quality_score: float
    quality_level: ContentQuality
    suggested_improvements: List[str]
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ContentMetrics:
    """Метрики контента"""
    content_id: str
    views: int
    unique_views: int
    likes: int
    shares: int
    completion_rate: float
    avg_time_spent: float
    bounce_rate: float
    engagement_score: float
    created_at: datetime = field(default_factory=datetime.now)


class ContentModerationEngine:
    """
    Движок модерации контента для системы ПрофиТест.
    Обеспечивает автоматическую и ручную модерацию контента.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.moderation_rules = self._initialize_moderation_rules()
        self.flagged_content: Dict[str, List[str]] = defaultdict(list)
        self.moderation_history: List[Dict[str, Any]] = []
    
    def _initialize_moderation_rules(self) -> Dict[str, Any]:
        """Инициализирует правила модерации."""
        return {
            'prohibited_words': [
                'spam', 'advertisement', 'promo', 'click here', 'buy now',
                'секс', 'порно', 'эротика', 'насильствие'
            ],
            'min_title_length': 10,
            'max_title_length': 200,
            'min_description_length': 50,
            'max_description_length': 1000,
            'required_tags': 1,
            'max_tags': 10,
            'suspicious_patterns': [
                r'\b\d{10,}\b',  # Длинные числа
                r'[^\w\s]{5,}',   # Много специальных символов
                r'(.)\1{4,}'      # Повторяющиеся символы
            ]
        }
    
    def moderate_content(self, content: ContentItem) -> Dict[str, Any]:
        """
        Модерирует контент по установленным правилам.
        
        Args:
            content: Элемент контента для модерации
            
        Returns:
            dict: Результат модерации
        """
        try:
            violations = []
            warnings = []
            score = 100.0
            
            # Проверка запрещенных слов
            text_to_check = f"{content.title} {content.description} {' '.join(content.tags)}"
            for word in self.moderation_rules['prohibited_words']:
                if word.lower() in text_to_check.lower():
                    violations.append(f"Обнаружено запрещенное слово: {word}")
                    score -= 20
            
            # Проверка длины заголовка
            if len(content.title) < self.moderation_rules['min_title_length']:
                violations.append(f"Заголовок слишком короткий (минимум {self.moderation_rules['min_title_length']} символов)")
                score -= 10
            elif len(content.title) > self.moderation_rules['max_title_length']:
                warnings.append(f"Заголовок слишком длинный (максимум {self.moderation_rules['max_title_length']} символов)")
                score -= 5
            
            # Проверка длины описания
            if len(content.description) < self.moderation_rules['min_description_length']:
                violations.append(f"Описание слишком короткое (минимум {self.moderation_rules['min_description_length']} символов)")
                score -= 15
            elif len(content.description) > self.moderation_rules['max_description_length']:
                warnings.append(f"Описание слишком длинное (максимум {self.moderation_rules['max_description_length']} символов)")
                score -= 5
            
            # Проверка тегов
            if len(content.tags) < self.moderation_rules['required_tags']:
                violations.append(f"Требуется минимум {self.moderation_rules['required_tags']} тега")
                score -= 10
            elif len(content.tags) > self.moderation_rules['max_tags']:
                warnings.append(f"Слишком много тегов (максимум {self.moderation_rules['max_tags']})")
                score -= 5
            
            # Проверка подозрительных паттернов
            for pattern in self.moderation_rules['suspicious_patterns']:
                if re.search(pattern, text_to_check, re.IGNORECASE):
                    warnings.append(f"Обнаружен подозрительный паттерн: {pattern}")
                    score -= 5
            
            # Определение статуса модерации
            if violations:
                status = 'rejected'
                final_score = 0
            elif warnings:
                status = 'pending_review'
                final_score = max(0, score)
            else:
                status = 'approved'
                final_score = score
            
            moderation_result = {
                'content_id': content.id,
                'status': status,
                'score': final_score,
                'violations': violations,
                'warnings': warnings,
                'moderated_at': datetime.now().isoformat()
            }
            
            # Сохраняем в историю модерации
            self.moderation_history.append({
                'content_id': content.id,
                'result': moderation_result,
                'timestamp': datetime.now()
            })
            
            # Если контент нарушает правила, добавляем в список отмеченного
            if status == 'rejected':
                self.flagged_content[content.id].append('moderation_violation')
            
            self.logger.info(f"Контент {content.id} промодерирован. Статус: {status}, Оценка: {final_score}")
            return moderation_result
            
        except Exception as e:
            self.logger.error(f"Ошибка при модерации контента {content.id}: {str(e)}")
            return {
                'content_id': content.id,
                'status': 'error',
                'score': 0,
                'violations': [f'Ошибка модерации: {str(e)}'],
                'warnings': [],
                'moderated_at': datetime.now().isoformat()
            }
    
    def get_moderation_history(self, content_id: str = None) -> List[Dict[str, Any]]:
        """
        Получает историю модерации.
        
        Args:
            content_id: ID контента (опционально)
            
        Returns:
            list: История модерации
        """
        if content_id:
            return [record for record in self.moderation_history 
                   if record['content_id'] == content_id]
        return self.moderation_history
    
    def get_flagged_content(self) -> Dict[str, List[str]]:
        """
        Получает список отмеченного контента.
        
        Returns:
            dict: Словарь отмеченного контента
        """
        return dict(self.flagged_content)


class ContentQualityAnalyzer:
    """
    Анализатор качества контента для системы ПрофиТест.
    Оценивает качество контента и предлагает улучшения.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.quality_criteria = self._initialize_quality_criteria()
    
    def _initialize_quality_criteria(self) -> Dict[str, Any]:
        """Инициализирует критерии качества."""
        return {
            'title_quality': {
                'min_words': 3,
                'max_words': 15,
                'keyword_density_target': 0.02,
                'capitalization_bonus': 10
            },
            'description_quality': {
                'min_words': 20,
                'max_words': 200,
                'paragraph_count_target': 2,
                'readability_score_target': 60
            },
            'engagement_factors': {
                'tags_relevance_weight': 0.3,
                'category_consistency_weight': 0.2,
                'metadata_completeness_weight': 0.5
            }
        }
    
    def analyze_content_quality(self, content: ContentItem) -> Dict[str, Any]:
        """
        Анализирует качество контента.
        
        Args:
            content: Элемент контента
            
        Returns:
            dict: Результат анализа качества
        """
        try:
            quality_scores = {}
            improvement_suggestions = []
            
            # Анализ заголовка
            title_analysis = self._analyze_title_quality(content.title)
            quality_scores['title'] = title_analysis['score']
            improvement_suggestions.extend(title_analysis['suggestions'])
            
            # Анализ описания
            description_analysis = self._analyze_description_quality(content.description)
            quality_scores['description'] = description_analysis['score']
            improvement_suggestions.extend(description_analysis['suggestions'])
            
            # Анализ тегов
            tags_analysis = self._analyze_tags_quality(content.tags, content.category)
            quality_scores['tags'] = tags_analysis['score']
            improvement_suggestions.extend(tags_analysis['suggestions'])
            
            # Анализ метаданных
            metadata_analysis = self._analyze_metadata_quality(content.metadata)
            quality_scores['metadata'] = metadata_analysis['score']
            improvement_suggestions.extend(metadata_analysis['suggestions'])
            
            # Общая оценка качества
            total_score = sum(quality_scores.values()) / len(quality_scores)
            
            # Определение уровня качества
            if total_score >= 85:
                quality_level = ContentQuality.EXCELLENT
            elif total_score >= 70:
                quality_level = ContentQuality.GOOD
            elif total_score >= 50:
                quality_level = ContentQuality.AVERAGE
            elif total_score >= 30:
                quality_level = ContentQuality.POOR
            else:
                quality_level = ContentQuality.NEEDS_IMPROVEMENT
            
            return {
                'content_id': content.id,
                'overall_score': round(total_score, 2),
                'quality_level': quality_level.value,
                'detailed_scores': quality_scores,
                'improvement_suggestions': improvement_suggestions,
                'analyzed_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Ошибка при анализе качества контента {content.id}: {str(e)}")
            return {
                'content_id': content.id,
                'overall_score': 0,
                'quality_level': ContentQuality.NEEDS_IMPROVEMENT.value,
                'detailed_scores': {},
                'improvement_suggestions': [f'Ошибка анализа: {str(e)}'],
                'analyzed_at': datetime.now().isoformat()
            }
    
    def _analyze_title_quality(self, title: str) -> Dict[str, Any]:
        """Анализирует качество заголовка."""
        suggestions = []
        score = 100
        
        # Подсчет слов
        words = title.split()
        word_count = len(words)
        
        if word_count < self.quality_criteria['title_quality']['min_words']:
            suggestions.append(f"Сделайте заголовок более информативным (минимум {self.quality_criteria['title_quality']['min_words']} слов)")
            score -= 20
        elif word_count > self.quality_criteria['title_quality']['max_words']:
            suggestions.append(f"Сократите заголовок (максимум {self.quality_criteria['title_quality']['max_words']} слов)")
            score -= 15
        
        # Проверка капитализации
        if title and title[0].isupper() and all(word[0].isupper() for word in words if len(word) > 3):
            score += self.quality_criteria['title_quality']['capitalization_bonus']
        else:
            suggestions.append("Используйте заглавные буквы для ключевых слов")
        
        return {
            'score': max(0, min(100, score)),
            'suggestions': suggestions
        }
    
    def _analyze_description_quality(self, description: str) -> Dict[str, Any]:
        """Анализирует качество описания."""
        suggestions = []
        score = 100
        
        # Подсчет слов
        words = description.split()
        word_count = len(words)
        
        if word_count < self.quality_criteria['description_quality']['min_words']:
            suggestions.append(f"Расширьте описание (минимум {self.quality_criteria['description_quality']['min_words']} слов)")
            score -= 25
        elif word_count > self.quality_criteria['description_quality']['max_words']:
            suggestions.append(f"Сократите описание (максимум {self.quality_criteria['description_quality']['max_words']} слов)")
            score -= 10
        
        # Проверка параграфов
        paragraphs = description.split('\n\n')
        if len(paragraphs) < self.quality_criteria['description_quality']['paragraph_count_target']:
            suggestions.append("Разделите описание на абзацы для лучшей читаемости")
            score -= 10
        
        return {
            'score': max(0, min(100, score)),
            'suggestions': suggestions
        }
    
    def _analyze_tags_quality(self, tags: List[str], category: str) -> Dict[str, Any]:
        """Анализирует качество тегов."""
        suggestions = []
        score = 100
        
        if not tags:
            suggestions.append("Добавьте теги для лучшей индексации")
            score -= 30
        elif len(tags) < 3:
            suggestions.append("Добавьте больше тегов (рекомендуется 3-7 тегов)")
            score -= 15
        
        # Проверка релевантности тегов категории
        if category and category not in tags:
            suggestions.append(f"Добавьте тег, соответствующий категории '{category}'")
            score -= 10
        
        return {
            'score': max(0, min(100, score)),
            'suggestions': suggestions
        }
    
    def _analyze_metadata_quality(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Анализирует качество метаданных."""
        suggestions = []
        score = 100
        
        required_fields = ['difficulty', 'estimated_time', 'target_audience']
        missing_fields = [field for field in required_fields if field not in metadata]
        
        if missing_fields:
            suggestions.append(f"Добавьте метаданные: {', '.join(missing_fields)}")
            score -= len(missing_fields) * 15
        
        # Проверка полноты метаданных
        metadata_completeness = len(metadata) / len(required_fields) if required_fields else 0
        if metadata_completeness < 0.8:
            suggestions.append("Заполните все поля метаданных")
            score -= 20
        
        return {
            'score': max(0, min(100, score)),
            'suggestions': suggestions
        }


class ContentOptimizer:
    """
    Оптимизатор контента для системы ПрофиТест.
    Предоставляет рекомендации по улучшению контента.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.optimization_rules = self._initialize_optimization_rules()
    
    def _initialize_optimization_rules(self) -> Dict[str, Any]:
        """Инициализирует правила оптимизации."""
        return {
            'seo_optimization': {
                'target_keyword_density': 0.02,
                'max_keyword_density': 0.05,
                'title_length_optimal': (50, 60),
                'description_length_optimal': (150, 160)
            },
            'engagement_optimization': {
                'recommended_tags_count': 5,
                'interactive_elements_min': 2,
                'multimedia_elements_min': 1
            },
            'performance_optimization': {
                'max_content_size_mb': 10,
                'min_loading_speed_score': 80,
                'mobile_friendly_required': True
            }
        }
    
    def generate_optimization_recommendations(self, content: ContentItem, 
                                            metrics: ContentMetrics = None) -> List[str]:
        """
        Генерирует рекомендации по оптимизации контента.
        
        Args:
            content: Элемент контента
            metrics: Метрики контента (опционально)
            
        Returns:
            list: Рекомендации по оптимизации
        """
        try:
            recommendations = []
            
            # SEO оптимизация
            seo_recs = self._generate_seo_recommendations(content)
            recommendations.extend(seo_recs)
            
            # Оптимизация вовлеченности
            engagement_recs = self._generate_engagement_recommendations(content, metrics)
            recommendations.extend(engagement_recs)
            
            # Техническая оптимизация
            technical_recs = self._generate_technical_recommendations(content)
            recommendations.extend(technical_recs)
            
            # Персонализация на основе метрик
            if metrics:
                personalization_recs = self._generate_personalized_recommendations(content, metrics)
                recommendations.extend(personalization_recs)
            
            self.logger.info(f"Сгенерированы {len(recommendations)} рекомендаций по оптимизации для контента {content.id}")
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Ошибка при генерации рекомендаций по оптимизации контента {content.id}: {str(e)}")
            return [f"Ошибка при генерации рекомендаций: {str(e)}"]
    
    def _generate_seo_recommendations(self, content: ContentItem) -> List[str]:
        """Генерирует SEO-рекомендации."""
        recommendations = []
        
        # Оптимизация заголовка
        if len(content.title) < 50:
            recommendations.append("Сделайте заголовок более информативным для SEO")
        elif len(content.title) > 60:
            recommendations.append("Сократите заголовок до 60 символов для лучшего отображения в поиске")
        
        # Оптимизация описания
        if len(content.description) < 150:
            recommendations.append("Расширьте описание для улучшения сниппета поиска")
        elif len(content.description) > 160:
            recommendations.append("Ограничьте описание 160 символами для сниппета поиска")
        
        # Оптимизация тегов
        if len(content.tags) < 5:
            recommendations.append("Добавьте больше тегов для лучшей индексации")
        elif len(content.tags) > 10:
            recommendations.append("Сократите количество тегов до 10 для лучшей фокусировки")
        
        return recommendations
    
    def _generate_engagement_recommendations(self, content: ContentItem, 
                                           metrics: ContentMetrics = None) -> List[str]:
        """Генерирует рекомендации по вовлеченности."""
        recommendations = []
        
        # На основе типа контента
        if content.content_type == ContentType.VIDEO:
            recommendations.append("Добавьте субтитры для лучшей доступности")
            recommendations.append("Создайте превью изображение для видео")
        elif content.content_type == ContentType.ARTICLE:
            recommendations.append("Добавьте изображения для иллюстрации материала")
            recommendations.append("Разделите текст на логические разделы")
        
        # На основе метрик
        if metrics:
            if metrics.completion_rate < 0.6:
                recommendations.append("Улучшите структуру контента для повышения завершаемости")
            if metrics.engagement_score < 50:
                recommendations.append("Добавьте интерактивные элементы")
        
        return recommendations
    
    def _generate_technical_recommendations(self, content: ContentItem) -> List[str]:
        """Генерирует технические рекомендации."""
        recommendations = []
        
        # Проверка размера контента
        if 'file_size' in content.metadata:
            file_size_mb = content.metadata['file_size'] / (1024 * 1024)
            if file_size_mb > self.optimization_rules['performance_optimization']['max_content_size_mb']:
                recommendations.append(f"Оптимизируйте размер файла (текущий: {file_size_mb:.1f}MB)")
        
        # Мобильная оптимизация
        if not content.metadata.get('mobile_friendly', False):
            recommendations.append("Оптимизируйте контент для мобильных устройств")
        
        return recommendations
    
    def _generate_personalized_recommendations(self, content: ContentItem, 
                                             metrics: ContentMetrics) -> List[str]:
        """Генерирует персонализированные рекомендации на основе метрик."""
        recommendations = []
        
        # На основе производительности
        if metrics.bounce_rate > 0.7:
            recommendations.append("Улучшите первые секунды взаимодействия с контентом")
        
        if metrics.avg_time_spent < 60:
            recommendations.append("Сделайте контент более увлекательным")
        
        # На основе рейтинга
        if metrics.engagement_score < 40 and content.avg_rating < 3.5:
            recommendations.append("Пересмотрите качество контента и его подачу")
        
        return recommendations


# Глобальные экземпляры систем управления контентом
content_moderation_engine = ContentModerationEngine()
content_quality_analyzer = ContentQualityAnalyzer()
content_optimizer = ContentOptimizer()