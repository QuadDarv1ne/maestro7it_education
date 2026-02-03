# -*- coding: utf-8 -*-
"""
Модуль расширенной системы комментариев и отзывов для ПрофиТест
Предоставляет продвинутые возможности управления комментариями и отзывами
"""
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Any
import logging
from dataclasses import dataclass, field
from collections import defaultdict
import re


class CommentType(Enum):
    """Типы комментариев"""
    COMMENT = 'comment'
    REVIEW = 'review'
    QUESTION = 'question'
    ANSWER = 'answer'
    FEEDBACK = 'feedback'
    SUGGESTION = 'suggestion'


class CommentStatus(Enum):
    """Статусы комментариев"""
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    FLAGGED = 'flagged'
    DELETED = 'deleted'


class RatingType(Enum):
    """Типы оценок"""
    STAR_RATING = 'star'
    LIKE_DISLIKE = 'like_dislike'
    THUMBS = 'thumbs'
    HEART = 'heart'


@dataclass
class Comment:
    """Класс комментария"""
    id: str
    content: str
    author_id: int
    target_id: str  # ID контента, к которому относится комментарий
    target_type: str  # тип контента (test, article, user и т.д.)
    comment_type: CommentType
    status: CommentStatus
    created_at: datetime
    updated_at: datetime
    parent_id: Optional[str] = None  # для вложенных комментариев
    likes: int = 0
    dislikes: int = 0
    reports: int = 0
    rating: Optional[float] = None  # для отзывов
    metadata: Dict[str, Any] = field(default_factory=dict)
    is_edited: bool = False
    edited_at: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)


class CommentModeration:
    """Система модерации комментариев"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.flagged_comments: Set[str] = set()
        self.moderation_queue: List[str] = []
        self.moderation_history: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.auto_moderation_rules: Dict[str, Any] = {}
        
        # Инициализация правил автоматической модерации
        self._setup_auto_moderation_rules()
    
    def _setup_auto_moderation_rules(self):
        """Настройка правил автоматической модерации"""
        self.auto_moderation_rules = {
            'profanity_filter': {
                'enabled': True,
                'words': ['недопустимые', 'слова'],  # Заглушка
                'action': 'flag'
            },
            'spam_detection': {
                'enabled': True,
                'max_links': 3,
                'min_content_length': 5,
                'max_content_length': 1000,
                'action': 'flag'
            },
            'duplicate_detection': {
                'enabled': True,
                'time_window_minutes': 5,
                'action': 'flag'
            }
        }
    
    def check_comment(self, comment: Comment) -> Dict[str, Any]:
        """
        Проверяет комментарий на соответствие правилам.
        
        Args:
            comment: Комментарий для проверки
            
        Returns:
            dict: Результат проверки
        """
        issues = []
        
        # Проверка на неприемлемый контент
        if self._check_profanity(comment):
            issues.append('Обнаружен неприемлемый контент')
        
        # Проверка на спам
        if self._check_spam(comment):
            issues.append('Подозрение на спам')
        
        # Проверка длины
        if len(comment.content) < self.auto_moderation_rules['spam_detection']['min_content_length']:
            issues.append('Комментарий слишком короткий')
        
        if len(comment.content) > self.auto_moderation_rules['spam_detection']['max_content_length']:
            issues.append('Комментарий слишком длинный')
        
        # Проверка на дубликаты
        if self._check_duplicates(comment):
            issues.append('Возможный дубликат')
        
        return {
            'passed': len(issues) == 0,
            'issues': issues,
            'severity': 'high' if len(issues) > 2 else 'medium' if len(issues) > 0 else 'low'
        }
    
    def _check_profanity(self, comment: Comment) -> bool:
        """Проверяет комментарий на неприемлемые слова"""
        if not self.auto_moderation_rules['profanity_filter']['enabled']:
            return False
        
        # В реальной системе здесь будет проверка через словарь неприемлемых слов
        return False
    
    def _check_spam(self, comment: Comment) -> bool:
        """Проверяет комментарий на спам"""
        if not self.auto_moderation_rules['spam_detection']['enabled']:
            return False
        
        # Проверка количества ссылок
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, comment.content)
        if len(urls) > self.auto_moderation_rules['spam_detection']['max_links']:
            return True
        
        return False
    
    def _check_duplicates(self, comment: Comment) -> bool:
        """Проверяет комментарий на дубликаты"""
        if not self.auto_moderation_rules['duplicate_detection']['enabled']:
            return False
        
        # В реальной системе здесь будет сравнение с недавними комментариями
        return False
    
    def flag_comment(self, comment_id: str, reason: str, moderator_id: int) -> bool:
        """
        Помечает комментарий как подозрительный.
        
        Args:
            comment_id: ID комментария
            reason: Причина флагов
            moderator_id: ID модератора
            
        Returns:
            bool: Успешность операции
        """
        try:
            self.flagged_comments.add(comment_id)
            
            # Добавляем в историю модерации
            self.moderation_history[comment_id].append({
                'timestamp': datetime.now().isoformat(),
                'moderator_id': moderator_id,
                'action': 'flag',
                'reason': reason
            })
            
            self.logger.info(f"Комментарий {comment_id} помечен как подозрительный: {reason}")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при флаговании комментария: {str(e)}")
            return False
    
    def approve_comment(self, comment_id: str, moderator_id: int) -> bool:
        """
        Одобряет комментарий.
        
        Args:
            comment_id: ID комментария
            moderator_id: ID модератора
            
        Returns:
            bool: Успешность операции
        """
        try:
            if comment_id in self.flagged_comments:
                self.flagged_comments.remove(comment_id)
            
            # Добавляем в историю модерации
            self.moderation_history[comment_id].append({
                'timestamp': datetime.now().isoformat(),
                'moderator_id': moderator_id,
                'action': 'approve',
                'reason': 'Комментарий одобрен модератором'
            })
            
            self.logger.info(f"Комментарий {comment_id} одобрен модератором {moderator_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при одобрении комментария: {str(e)}")
            return False


class AdvancedCommentManager:
    """
    Расширенный менеджер комментариев для системы ПрофиТест.
    Обеспечивает управление комментариями, модерацию и организацию.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.comments: Dict[str, Comment] = {}
        self.target_index: Dict[str, Set[str]] = defaultdict(set)  # target_id -> comment_ids
        self.author_index: Dict[int, Set[str]] = defaultdict(set)  # author_id -> comment_ids
        self.type_index: Dict[CommentType, Set[str]] = defaultdict(set)
        self.status_index: Dict[CommentStatus, Set[str]] = defaultdict(set)
        self.parent_child_index: Dict[str, Set[str]] = defaultdict(set)  # parent_id -> child_ids
        
        self.moderation = CommentModeration()
        self.user_ratings: Dict[str, Dict[int, float]] = defaultdict(dict)  # comment_id -> {user_id: rating}
        
        # Инициализация системных комментариев
        self._create_system_comments()
    
    def _create_system_comments(self):
        """Создает системные комментарии по умолчанию"""
        pass  # Пока пусто, можно добавить примеры позже
    
    def add_comment(self, comment: Comment) -> bool:
        """
        Добавляет новый комментарий.
        
        Args:
            comment: Объект комментария
            
        Returns:
            bool: Успешность операции
        """
        try:
            if comment.id in self.comments:
                self.logger.warning(f"Комментарий с ID {comment.id} уже существует")
                return False
            
            # Автоматическая модерация
            moderation_result = self.moderation.check_comment(comment)
            if not moderation_result['passed']:
                comment.status = CommentStatus.FLAGGED
                self.moderation.flag_comment(comment.id, '; '.join(moderation_result['issues']), 0)
                self.logger.info(f"Комментарий {comment.id} отправлен на модерацию")
            
            # Добавляем комментарий
            self.comments[comment.id] = comment
            
            # Обновляем индексы
            self._update_indexes(comment, 'add')
            
            self.logger.info(f"Комментарий {comment.id} успешно добавлен")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при добавлении комментария: {str(e)}")
            return False
    
    def get_comment(self, comment_id: str) -> Optional[Comment]:
        """
        Получает комментарий по ID.
        
        Args:
            comment_id: ID комментария
            
        Returns:
            Comment: Объект комментария или None
        """
        return self.comments.get(comment_id)
    
    def update_comment(self, comment_id: str, **kwargs) -> bool:
        """
        Обновляет комментарий.
        
        Args:
            comment_id: ID комментария
            **kwargs: Поля для обновления
            
        Returns:
            bool: Успешность операции
        """
        try:
            comment = self.get_comment(comment_id)
            if not comment:
                self.logger.warning(f"Комментарий с ID {comment_id} не найден")
                return False
            
            # Сохраняем старые значения для обновления индексов
            old_comment = Comment(**comment.__dict__)
            
            # Обновляем поля
            for key, value in kwargs.items():
                if hasattr(comment, key):
                    setattr(comment, key, value)
            
            # Обновляем время изменения
            comment.updated_at = datetime.now()
            comment.is_edited = True
            comment.edited_at = datetime.now()
            
            # Обновляем индексы
            self._update_indexes(old_comment, 'remove')
            self._update_indexes(comment, 'add')
            
            self.logger.info(f"Комментарий {comment_id} успешно обновлен")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при обновлении комментария: {str(e)}")
            return False
    
    def delete_comment(self, comment_id: str) -> bool:
        """
        Удаляет комментарий.
        
        Args:
            comment_id: ID комментария
            
        Returns:
            bool: Успешность операции
        """
        try:
            comment = self.get_comment(comment_id)
            if not comment:
                self.logger.warning(f"Комментарий с ID {comment_id} не найден")
                return False
            
            # Обновляем индексы
            self._update_indexes(comment, 'remove')
            
            # Удаляем из основного хранилища
            del self.comments[comment_id]
            
            self.logger.info(f"Комментарий {comment_id} успешно удален")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при удалении комментария: {str(e)}")
            return False
    
    def get_comments_by_target(self, target_id: str, comment_type: CommentType = None) -> List[Comment]:
        """
        Получает комментарии по целевому объекту.
        
        Args:
            target_id: ID целевого объекта
            comment_type: Тип комментариев (опционально)
            
        Returns:
            list: Список комментариев
        """
        comment_ids = self.target_index.get(target_id, set())
        comments = [self.comments[cid] for cid in comment_ids if cid in self.comments]
        
        if comment_type:
            comments = [c for c in comments if c.comment_type == comment_type]
        
        # Сортировка по дате создания
        comments.sort(key=lambda x: x.created_at, reverse=True)
        return comments
    
    def get_comments_by_author(self, author_id: int) -> List[Comment]:
        """
        Получает комментарии по автору.
        
        Args:
            author_id: ID автора
            
        Returns:
            list: Список комментариев автора
        """
        comment_ids = self.author_index.get(author_id, set())
        return [self.comments[cid] for cid in comment_ids if cid in self.comments]
    
    def get_comments_by_status(self, status: CommentStatus) -> List[Comment]:
        """
        Получает комментарии по статусу.
        
        Args:
            status: Статус
            
        Returns:
            list: Список комментариев со статусом
        """
        comment_ids = self.status_index.get(status, set())
        return [self.comments[cid] for cid in comment_ids if cid in self.comments]
    
    def get_child_comments(self, parent_id: str) -> List[Comment]:
        """
        Получает дочерние комментарии.
        
        Args:
            parent_id: ID родительского комментария
            
        Returns:
            list: Список дочерних комментариев
        """
        child_ids = self.parent_child_index.get(parent_id, set())
        return [self.comments[cid] for cid in child_ids if cid in self.comments]
    
    def add_like(self, comment_id: str, user_id: int) -> bool:
        """
        Добавляет лайк комментарию.
        
        Args:
            comment_id: ID комментария
            user_id: ID пользователя
            
        Returns:
            bool: Успешность операции
        """
        try:
            comment = self.get_comment(comment_id)
            if not comment:
                return False
            
            comment.likes += 1
            self.logger.info(f"Лайк добавлен к комментарию {comment_id} от пользователя {user_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при добавлении лайка: {str(e)}")
            return False
    
    def add_dislike(self, comment_id: str, user_id: int) -> bool:
        """
        Добавляет дизлайк комментарию.
        
        Args:
            comment_id: ID комментария
            user_id: ID пользователя
            
        Returns:
            bool: Успешность операции
        """
        try:
            comment = self.get_comment(comment_id)
            if not comment:
                return False
            
            comment.dislikes += 1
            self.logger.info(f"Дизлайк добавлен к комментарию {comment_id} от пользователя {user_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при добавлении дизлайка: {str(e)}")
            return False
    
    def report_comment(self, comment_id: str, user_id: int, reason: str) -> bool:
        """
        Отмечает комментарий как неприемлемый.
        
        Args:
            comment_id: ID комментария
            user_id: ID пользователя
            reason: Причина жалобы
            
        Returns:
            bool: Успешность операции
        """
        try:
            comment = self.get_comment(comment_id)
            if not comment:
                return False
            
            comment.reports += 1
            
            # Автоматически флагуем при большом количестве жалоб
            if comment.reports >= 3:
                self.moderation.flag_comment(comment_id, f"Множественные жалобы: {reason}", user_id)
                comment.status = CommentStatus.FLAGGED
            
            self.logger.info(f"Жалоба на комментарий {comment_id} от пользователя {user_id}: {reason}")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при подаче жалобы: {str(e)}")
            return False
    
    def add_rating(self, comment_id: str, user_id: int, rating: float) -> bool:
        """
        Добавляет рейтинг к комментарию.
        
        Args:
            comment_id: ID комментария
            user_id: ID пользователя
            rating: Рейтинг (0-5)
            
        Returns:
            bool: Успешность операции
        """
        try:
            if not (0 <= rating <= 5):
                return False
            
            comment = self.get_comment(comment_id)
            if not comment:
                return False
            
            # Сохраняем рейтинг пользователя
            self.user_ratings[comment_id][user_id] = rating
            
            # Пересчитываем средний рейтинг
            ratings = list(self.user_ratings[comment_id].values())
            comment.rating = sum(ratings) / len(ratings) if ratings else 0.0
            
            self.logger.info(f"Рейтинг {rating} добавлен к комментарию {comment_id} от пользователя {user_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при добавлении рейтинга: {str(e)}")
            return False
    
    def search_comments(self, query: str, filters: Dict[str, Any] = None) -> List[Comment]:
        """
        Поиск комментариев по различным критериям.
        
        Args:
            query: Поисковый запрос
            filters: Дополнительные фильтры
            
        Returns:
            list: Список найденных комментариев
        """
        if filters is None:
            filters = {}
        
        results = []
        query_lower = query.lower()
        
        for comment in self.comments.values():
            # Применяем фильтры
            if not self._matches_filters(comment, filters):
                continue
            
            # Поиск по тексту
            if query_lower in comment.content.lower():
                results.append(comment)
        
        # Сортировка по релевантности и дате
        results.sort(key=lambda x: (x.likes - x.dislikes, x.created_at), reverse=True)
        
        return results
    
    def _matches_filters(self, comment: Comment, filters: Dict[str, Any]) -> bool:
        """Проверяет, соответствует ли комментарий фильтрам"""
        # Фильтр по статусу
        if 'status' in filters and comment.status.value != filters['status']:
            return False
        
        # Фильтр по типу
        if 'comment_type' in filters and comment.comment_type.value != filters['comment_type']:
            return False
        
        # Фильтр по автору
        if 'author_id' in filters and comment.author_id != filters['author_id']:
            return False
        
        # Фильтр по целевому объекту
        if 'target_id' in filters and comment.target_id != filters['target_id']:
            return False
        
        # Фильтр по флагам
        if 'flagged_only' in filters and filters['flagged_only'] and comment.reports == 0:
            return False
        
        return True
    
    def _update_indexes(self, comment: Comment, operation: str):
        """
        Обновляет индексы комментария.
        
        Args:
            comment: Комментарий
            operation: Операция ('add' или 'remove')
        """
        if operation == 'add':
            # Добавляем в индексы
            self.target_index[comment.target_id].add(comment.id)
            self.author_index[comment.author_id].add(comment.id)
            self.type_index[comment.comment_type].add(comment.id)
            self.status_index[comment.status].add(comment.id)
            if comment.parent_id:
                self.parent_child_index[comment.parent_id].add(comment.id)
        else:
            # Удаляем из индексов
            if comment.id in self.target_index[comment.target_id]:
                self.target_index[comment.target_id].remove(comment.id)
            if comment.id in self.author_index[comment.author_id]:
                self.author_index[comment.author_id].remove(comment.id)
            if comment.id in self.type_index[comment.comment_type]:
                self.type_index[comment.comment_type].remove(comment.id)
            if comment.id in self.status_index[comment.status]:
                self.status_index[comment.status].remove(comment.id)
            if comment.parent_id and comment.id in self.parent_child_index[comment.parent_id]:
                self.parent_child_index[comment.parent_id].remove(comment.id)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Получает статистику по комментариям.
        
        Returns:
            dict: Статистика комментариев
        """
        total_comments = len(self.comments)
        approved_comments = len(self.get_comments_by_status(CommentStatus.APPROVED))
        flagged_comments = len(self.get_comments_by_status(CommentStatus.FLAGGED))
        pending_comments = len(self.get_comments_by_status(CommentStatus.PENDING))
        
        comment_types = {}
        for comment in self.comments.values():
            comment_type = comment.comment_type.value
            comment_types[comment_type] = comment_types.get(comment_type, 0) + 1
        
        total_likes = sum(c.likes for c in self.comments.values())
        total_dislikes = sum(c.dislikes for c in self.comments.values())
        total_reports = sum(c.reports for c in self.comments.values())
        
        return {
            'total_comments': total_comments,
            'approved_comments': approved_comments,
            'flagged_comments': flagged_comments,
            'pending_comments': pending_comments,
            'comments_by_type': comment_types,
            'total_authors': len(self.author_index),
            'total_targets': len(self.target_index),
            'total_likes': total_likes,
            'total_dislikes': total_dislikes,
            'total_reports': total_reports,
            'moderation_queue_size': len(self.moderation.moderation_queue)
        }


# Глобальный экземпляр менеджера комментариев
comment_manager = AdvancedCommentManager()