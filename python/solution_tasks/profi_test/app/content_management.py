# -*- coding: utf-8 -*-
"""
Модуль расширенного управления контентом для ПрофиТест
Предоставляет продвинутые возможности управления контентом и медиа-файлами
"""
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Any, Union
import logging
from dataclasses import dataclass, field
from collections import defaultdict
import hashlib
import os
from pathlib import Path


class ContentType(Enum):
    """Типы контента"""
    TEXT = 'text'
    IMAGE = 'image'
    VIDEO = 'video'
    AUDIO = 'audio'
    DOCUMENT = 'document'
    TEST = 'test'
    QUESTION = 'question'
    ANSWER = 'answer'
    COMMENT = 'comment'
    REVIEW = 'review'


class ContentStatus(Enum):
    """Статусы контента"""
    DRAFT = 'draft'
    PENDING_REVIEW = 'pending_review'
    PUBLISHED = 'published'
    ARCHIVED = 'archived'
    DELETED = 'deleted'
    FLAGGED = 'flagged'


class ContentCategory(Enum):
    """Категории контента"""
    EDUCATIONAL = 'educational'
    ENTERTAINMENT = 'entertainment'
    NEWS = 'news'
    TUTORIAL = 'tutorial'
    REFERENCE = 'reference'
    USER_GENERATED = 'user_generated'


@dataclass
class ContentMetadata:
    """Метаданные контента"""
    title: str
    description: str
    tags: List[str] = field(default_factory=list)
    category: ContentCategory = ContentCategory.EDUCATIONAL
    language: str = 'ru'
    difficulty_level: int = 1  # 1-5
    estimated_time: int = 0  # в минутах
    target_audience: str = 'general'
    prerequisites: List[str] = field(default_factory=list)
    learning_outcomes: List[str] = field(default_factory=list)


@dataclass
class Content:
    """Класс контента"""
    id: str
    content_type: ContentType
    content_data: Union[str, Dict[str, Any]]
    author_id: int
    status: ContentStatus
    metadata: ContentMetadata
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None
    version: int = 1
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)
    likes: int = 0
    views: int = 0
    shares: int = 0
    comments_count: int = 0
    rating: float = 0.0
    ratings_count: int = 0
    flags: int = 0
    is_featured: bool = False
    is_premium: bool = False
    access_level: int = 0  # 0 - публичный, 1-3 - уровни доступа


class ContentModeration:
    """Система модерации контента"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.flagged_content: Set[str] = set()
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
                'min_content_length': 10,
                'action': 'flag'
            },
            'duplicate_detection': {
                'enabled': True,
                'similarity_threshold': 0.8,
                'action': 'flag'
            }
        }
    
    def check_content(self, content: Content) -> Dict[str, Any]:
        """
        Проверяет контент на соответствие правилам.
        
        Args:
            content: Контент для проверки
            
        Returns:
            dict: Результат проверки
        """
        issues = []
        
        # Проверка на неприемлемый контент
        if self._check_profanity(content):
            issues.append('Обнаружен неприемлемый контент')
        
        # Проверка на спам
        if self._check_spam(content):
            issues.append('Подозрение на спам')
        
        # Проверка на дубликаты
        if self._check_duplicates(content):
            issues.append('Возможный дубликат')
        
        # Проверка метаданных
        if not content.metadata.title or len(content.metadata.title) < 3:
            issues.append('Заголовок слишком короткий')
        
        if not content.metadata.description or len(content.metadata.description) < 10:
            issues.append('Описание слишком короткое')
        
        return {
            'passed': len(issues) == 0,
            'issues': issues,
            'severity': 'high' if len(issues) > 2 else 'medium' if len(issues) > 0 else 'low'
        }
    
    def _check_profanity(self, content: Content) -> bool:
        """Проверяет контент на неприемлемые слова"""
        if not self.auto_moderation_rules['profanity_filter']['enabled']:
            return False
        
        # В реальной системе здесь будет проверка через словарь неприемлемых слов
        # Пока возвращаем False как заглушку
        return False
    
    def _check_spam(self, content: Content) -> bool:
        """Проверяет контент на спам"""
        if not self.auto_moderation_rules['spam_detection']['enabled']:
            return False
        
        rules = self.auto_moderation_rules['spam_detection']
        
        # Проверка длины контента
        content_length = len(str(content.content_data))
        if content_length < rules['min_content_length']:
            return True
        
        # Проверка количества ссылок (заглушка)
        # В реальной системе нужно парсить контент и считать ссылки
        return False
    
    def _check_duplicates(self, content: Content) -> bool:
        """Проверяет контент на дубликаты"""
        if not self.auto_moderation_rules['duplicate_detection']['enabled']:
            return False
        
        # В реальной системе здесь будет сравнение с существующим контентом
        # Пока возвращаем False как заглушку
        return False
    
    def flag_content(self, content_id: str, reason: str, moderator_id: int) -> bool:
        """
        Помечает контент как подозрительный.
        
        Args:
            content_id: ID контента
            reason: Причина флагов
            moderator_id: ID модератора
            
        Returns:
            bool: Успешность операции
        """
        try:
            self.flagged_content.add(content_id)
            
            # Добавляем в историю модерации
            self.moderation_history[content_id].append({
                'timestamp': datetime.now().isoformat(),
                'moderator_id': moderator_id,
                'action': 'flag',
                'reason': reason
            })
            
            self.logger.info(f"Контент {content_id} помечен как подозрительный: {reason}")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при флаговании контента: {str(e)}")
            return False
    
    def approve_content(self, content_id: str, moderator_id: int) -> bool:
        """
        Одобряет контент.
        
        Args:
            content_id: ID контента
            moderator_id: ID модератора
            
        Returns:
            bool: Успешность операции
        """
        try:
            if content_id in self.flagged_content:
                self.flagged_content.remove(content_id)
            
            # Добавляем в историю модерации
            self.moderation_history[content_id].append({
                'timestamp': datetime.now().isoformat(),
                'moderator_id': moderator_id,
                'action': 'approve',
                'reason': 'Контент одобрен модератором'
            })
            
            self.logger.info(f"Контент {content_id} одобрен модератором {moderator_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при одобрении контента: {str(e)}")
            return False
    
    def reject_content(self, content_id: str, reason: str, moderator_id: int) -> bool:
        """
        Отклоняет контент.
        
        Args:
            content_id: ID контента
            reason: Причина отклонения
            moderator_id: ID модератора
            
        Returns:
            bool: Успешность операции
        """
        try:
            # Добавляем в историю модерации
            self.moderation_history[content_id].append({
                'timestamp': datetime.now().isoformat(),
                'moderator_id': moderator_id,
                'action': 'reject',
                'reason': reason
            })
            
            self.logger.info(f"Контент {content_id} отклонен: {reason}")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при отклонении контента: {str(e)}")
            return False
    
    def get_moderation_queue(self) -> List[str]:
        """Получает очередь на модерацию"""
        return self.moderation_queue.copy()
    
    def add_to_moderation_queue(self, content_id: str) -> bool:
        """
        Добавляет контент в очередь на модерацию.
        
        Args:
            content_id: ID контента
            
        Returns:
            bool: Успешность операции
        """
        try:
            if content_id not in self.moderation_queue:
                self.moderation_queue.append(content_id)
                self.logger.info(f"Контент {content_id} добавлен в очередь на модерацию")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Ошибка при добавлении в очередь модерации: {str(e)}")
            return False


class AdvancedContentManager:
    """
    Расширенный менеджер контента для системы ПрофиТест.
    Обеспечивает управление контентом, модерацию и организацию.
    """
    
    def __init__(self, content_storage_path: str = 'content'):
        self.logger = logging.getLogger(__name__)
        self.content_storage_path = Path(content_storage_path)
        self.content_storage_path.mkdir(exist_ok=True)
        
        self.content: Dict[str, Content] = {}
        self.content_index: Dict[str, Set[str]] = defaultdict(set)  # tag -> content_ids
        self.author_index: Dict[int, Set[str]] = defaultdict(set)   # author_id -> content_ids
        self.category_index: Dict[ContentCategory, Set[str]] = defaultdict(set)
        self.status_index: Dict[ContentStatus, Set[str]] = defaultdict(set)
        
        self.moderation = ContentModeration()
        self.media_files: Dict[str, Dict[str, Any]] = {}
        
        # Инициализация системного контента
        self._create_system_content()
    
    def _create_system_content(self):
        """Создает системный контент по умолчанию"""
        # Создаем пример теста
        system_test = Content(
            id='system_test_1',
            content_type=ContentType.TEST,
            content_data={
                'title': 'Пример теста',
                'questions': [
                    {
                        'id': 1,
                        'text': 'Какой ваш любимый цвет?',
                        'options': ['Красный', 'Синий', 'Зеленый', 'Желтый'],
                        'correct_answer': 1
                    }
                ]
            },
            author_id=1,  # Системный администратор
            status=ContentStatus.PUBLISHED,
            metadata=ContentMetadata(
                title='Пример теста',
                description='Тест для демонстрации системы'
            ),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            published_at=datetime.now()
        )
        
        self.add_content(system_test)
    
    def add_content(self, content: Content) -> bool:
        """
        Добавляет новый контент.
        
        Args:
            content: Объект контента
            
        Returns:
            bool: Успешность операции
        """
        try:
            if content.id in self.content:
                self.logger.warning(f"Контент с ID {content.id} уже существует")
                return False
            
            # Автоматическая модерация
            moderation_result = self.moderation.check_content(content)
            if not moderation_result['passed']:
                content.status = ContentStatus.FLAGGED
                self.moderation.add_to_moderation_queue(content.id)
                self.logger.info(f"Контент {content.id} отправлен на модерацию")
            
            # Добавляем контент
            self.content[content.id] = content
            
            # Обновляем индексы
            self._update_indexes(content, 'add')
            
            # Сохраняем контент в файловую систему
            self._save_content_to_file(content)
            
            self.logger.info(f"Контент {content.id} успешно добавлен")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при добавлении контента: {str(e)}")
            return False
    
    def get_content(self, content_id: str) -> Optional[Content]:
        """
        Получает контент по ID.
        
        Args:
            content_id: ID контента
            
        Returns:
            Content: Объект контента или None
        """
        return self.content.get(content_id)
    
    def update_content(self, content_id: str, **kwargs) -> bool:
        """
        Обновляет контент.
        
        Args:
            content_id: ID контента
            **kwargs: Поля для обновления
            
        Returns:
            bool: Успешность операции
        """
        try:
            content = self.get_content(content_id)
            if not content:
                self.logger.warning(f"Контент с ID {content_id} не найден")
                return False
            
            # Сохраняем старые значения для обновления индексов
            old_content = Content(**content.__dict__)
            
            # Обновляем поля
            for key, value in kwargs.items():
                if hasattr(content, key):
                    setattr(content, key, value)
            
            # Обновляем время изменения
            content.updated_at = datetime.now()
            content.version += 1
            
            # Обновляем индексы
            self._update_indexes(old_content, 'remove')
            self._update_indexes(content, 'add')
            
            # Сохраняем обновленный контент
            self._save_content_to_file(content)
            
            self.logger.info(f"Контент {content_id} успешно обновлен")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при обновлении контента: {str(e)}")
            return False
    
    def delete_content(self, content_id: str) -> bool:
        """
        Удаляет контент.
        
        Args:
            content_id: ID контента
            
        Returns:
            bool: Успешность операции
        """
        try:
            content = self.get_content(content_id)
            if not content:
                self.logger.warning(f"Контент с ID {content_id} не найден")
                return False
            
            # Обновляем индексы
            self._update_indexes(content, 'remove')
            
            # Удаляем из основного хранилища
            del self.content[content_id]
            
            # Помечаем как удаленный в файловой системе
            self._mark_content_as_deleted(content_id)
            
            self.logger.info(f"Контент {content_id} успешно удален")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при удалении контента: {str(e)}")
            return False
    
    def search_content(self, query: str, filters: Dict[str, Any] = None) -> List[Content]:
        """
        Поиск контента по различным критериям.
        
        Args:
            query: Поисковый запрос
            filters: Дополнительные фильтры
            
        Returns:
            list: Список найденного контента
        """
        if filters is None:
            filters = {}
        
        results = []
        query_lower = query.lower()
        
        for content in self.content.values():
            # Применяем фильтры
            if not self._matches_filters(content, filters):
                continue
            
            # Поиск по тексту
            if (query_lower in content.metadata.title.lower() or
                query_lower in content.metadata.description.lower() or
                query_lower in ' '.join(content.metadata.tags).lower()):
                results.append(content)
        
        # Сортировка по релевантности и дате
        results.sort(key=lambda x: (x.rating, x.views, x.created_at), reverse=True)
        
        return results
    
    def _matches_filters(self, content: Content, filters: Dict[str, Any]) -> bool:
        """Проверяет, соответствует ли контент фильтрам"""
        # Фильтр по статусу
        if 'status' in filters and content.status.value != filters['status']:
            return False
        
        # Фильтр по типу
        if 'content_type' in filters and content.content_type.value != filters['content_type']:
            return False
        
        # Фильтр по категории
        if 'category' in filters and content.metadata.category.value != filters['category']:
            return False
        
        # Фильтр по автору
        if 'author_id' in filters and content.author_id != filters['author_id']:
            return False
        
        # Фильтр по премиум-статусу
        if 'is_premium' in filters and content.is_premium != filters['is_premium']:
            return False
        
        # Фильтр по флагам
        if 'flagged_only' in filters and filters['flagged_only'] and content.flags == 0:
            return False
        
        return True
    
    def get_content_by_author(self, author_id: int) -> List[Content]:
        """
        Получает контент по автору.
        
        Args:
            author_id: ID автора
            
        Returns:
            list: Список контента автора
        """
        content_ids = self.author_index.get(author_id, set())
        return [self.content[cid] for cid in content_ids if cid in self.content]
    
    def get_content_by_category(self, category: ContentCategory) -> List[Content]:
        """
        Получает контент по категории.
        
        Args:
            category: Категория
            
        Returns:
            list: Список контента в категории
        """
        content_ids = self.category_index.get(category, set())
        return [self.content[cid] for cid in content_ids if cid in self.content]
    
    def get_content_by_status(self, status: ContentStatus) -> List[Content]:
        """
        Получает контент по статусу.
        
        Args:
            status: Статус
            
        Returns:
            list: Список контента со статусом
        """
        content_ids = self.status_index.get(status, set())
        return [self.content[cid] for cid in content_ids if cid in self.content]
    
    def get_popular_content(self, limit: int = 10) -> List[Content]:
        """
        Получает популярный контент.
        
        Args:
            limit: Максимальное количество
            
        Returns:
            list: Список популярного контента
        """
        contents = list(self.content.values())
        contents.sort(key=lambda x: (x.views, x.likes, x.rating), reverse=True)
        return contents[:limit]
    
    def get_featured_content(self) -> List[Content]:
        """
        Получает избранный контент.
        
        Returns:
            list: Список избранного контента
        """
        return [c for c in self.content.values() if c.is_featured and c.status == ContentStatus.PUBLISHED]
    
    def get_flagged_content(self) -> List[Content]:
        """
        Получает контент с флагами.
        
        Returns:
            list: Список контента с флагами
        """
        return [c for c in self.content.values() if c.flags > 0]
    
    def increment_view_count(self, content_id: str) -> bool:
        """
        Увеличивает счетчик просмотров.
        
        Args:
            content_id: ID контента
            
        Returns:
            bool: Успешность операции
        """
        return self.update_content(content_id, views=self.content[content_id].views + 1)
    
    def increment_like_count(self, content_id: str) -> bool:
        """
        Увеличивает счетчик лайков.
        
        Args:
            content_id: ID контента
            
        Returns:
            bool: Успешность операции
        """
        return self.update_content(content_id, likes=self.content[content_id].likes + 1)
    
    def add_rating(self, content_id: str, rating: float) -> bool:
        """
        Добавляет рейтинг контенту.
        
        Args:
            content_id: ID контента
            rating: Рейтинг (1-5)
            
        Returns:
            bool: Успешность операции
        """
        try:
            content = self.get_content(content_id)
            if not content:
                return False
            
            # Обновляем средний рейтинг
            total_rating = content.rating * content.ratings_count + rating
            content.ratings_count += 1
            content.rating = total_rating / content.ratings_count
            
            self._save_content_to_file(content)
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при добавлении рейтинга: {str(e)}")
            return False
    
    def upload_media_file(self, file_data: bytes, filename: str, content_type: str) -> str:
        """
        Загружает медиа-файл.
        
        Args:
            file_data: Данные файла
            filename: Имя файла
            content_type: Тип контента
            
        Returns:
            str: ID загруженного файла
        """
        try:
            file_id = hashlib.md5(file_data).hexdigest()
            file_path = self.content_storage_path / f"{file_id}_{filename}"
            
            # Сохраняем файл
            with open(file_path, 'wb') as f:
                f.write(file_data)
            
            # Сохраняем метаданные файла
            self.media_files[file_id] = {
                'filename': filename,
                'content_type': content_type,
                'size': len(file_data),
                'path': str(file_path),
                'uploaded_at': datetime.now().isoformat()
            }
            
            self.logger.info(f"Медиа-файл {filename} загружен (ID: {file_id})")
            return file_id
            
        except Exception as e:
            self.logger.error(f"Ошибка при загрузке медиа-файла: {str(e)}")
            return ""
    
    def get_media_file_info(self, file_id: str) -> Optional[Dict[str, Any]]:
        """
        Получает информацию о медиа-файле.
        
        Args:
            file_id: ID файла
            
        Returns:
            dict: Информация о файле или None
        """
        return self.media_files.get(file_id)
    
    def _update_indexes(self, content: Content, operation: str):
        """
        Обновляет индексы контента.
        
        Args:
            content: Контент
            operation: Операция ('add' или 'remove')
        """
        if operation == 'add':
            # Добавляем в индексы
            for tag in content.metadata.tags:
                self.content_index[tag].add(content.id)
            self.author_index[content.author_id].add(content.id)
            self.category_index[content.metadata.category].add(content.id)
            self.status_index[content.status].add(content.id)
        else:
            # Удаляем из индексов
            for tag in content.metadata.tags:
                if content.id in self.content_index[tag]:
                    self.content_index[tag].remove(content.id)
            if content.id in self.author_index[content.author_id]:
                self.author_index[content.author_id].remove(content.id)
            if content.id in self.category_index[content.metadata.category]:
                self.category_index[content.metadata.category].remove(content.id)
            if content.id in self.status_index[content.status]:
                self.status_index[content.status].remove(content.id)
    
    def _save_content_to_file(self, content: Content):
        """
        Сохраняет контент в файловую систему.
        
        Args:
            content: Контент для сохранения
        """
        try:
            import json
            content_file = self.content_storage_path / f"{content.id}.json"
            content_dict = {
                'id': content.id,
                'content_type': content.content_type.value,
                'content_data': content.content_data,
                'author_id': content.author_id,
                'status': content.status.value,
                'metadata': {
                    'title': content.metadata.title,
                    'description': content.metadata.description,
                    'tags': content.metadata.tags,
                    'category': content.metadata.category.value,
                    'language': content.metadata.language,
                    'difficulty_level': content.metadata.difficulty_level
                },
                'created_at': content.created_at.isoformat(),
                'updated_at': content.updated_at.isoformat(),
                'published_at': content.published_at.isoformat() if content.published_at else None,
                'version': content.version,
                'likes': content.likes,
                'views': content.views,
                'rating': content.rating,
                'ratings_count': content.ratings_count,
                'flags': content.flags
            }
            
            with open(content_file, 'w', encoding='utf-8') as f:
                json.dump(content_dict, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            self.logger.error(f"Ошибка при сохранении контента в файл: {str(e)}")
    
    def _mark_content_as_deleted(self, content_id: str):
        """
        Помечает контент как удаленный в файловой системе.
        
        Args:
            content_id: ID контента
        """
        try:
            content_file = self.content_storage_path / f"{content_id}.json"
            if content_file.exists():
                deleted_file = self.content_storage_path / f"{content_id}.deleted"
                content_file.rename(deleted_file)
        except Exception as e:
            self.logger.error(f"Ошибка при пометке контента как удаленного: {str(e)}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Получает статистику по контенту.
        
        Returns:
            dict: Статистика контента
        """
        total_content = len(self.content)
        published_content = len(self.get_content_by_status(ContentStatus.PUBLISHED))
        draft_content = len(self.get_content_by_status(ContentStatus.DRAFT))
        flagged_content = len(self.get_flagged_content())
        featured_content = len(self.get_featured_content())
        
        content_types = {}
        for content in self.content.values():
            content_type = content.content_type.value
            content_types[content_type] = content_types.get(content_type, 0) + 1
        
        return {
            'total_content': total_content,
            'published_content': published_content,
            'draft_content': draft_content,
            'flagged_content': flagged_content,
            'featured_content': featured_content,
            'content_by_type': content_types,
            'total_authors': len(self.author_index),
            'total_categories': len(self.category_index),
            'total_views': sum(c.views for c in self.content.values()),
            'total_likes': sum(c.likes for c in self.content.values())
        }


# Глобальный экземпляр менеджера контента
content_manager = AdvancedContentManager()