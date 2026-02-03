# -*- coding: utf-8 -*-
"""
Модуль расширенной системы поиска для ПрофиТест
Предоставляет продвинутые возможности поиска по контенту и пользователям
"""
import re
import nltk
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Set, Any, Tuple
import logging
from dataclasses import dataclass, field
from collections import defaultdict
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import heapq


class SearchType(Enum):
    """Типы поиска"""
    CONTENT = 'content'
    USER = 'user'
    TEST = 'test'
    ARTICLE = 'article'
    VIDEO = 'video'
    ALL = 'all'


class SearchFilter(Enum):
    """Фильтры поиска"""
    CATEGORY = 'category'
    DATE_RANGE = 'date_range'
    RATING = 'rating'
    DIFFICULTY = 'difficulty'
    CONTENT_TYPE = 'content_type'
    STATUS = 'status'
    TAGS = 'tags'


@dataclass
class SearchResult:
    """Результат поиска"""
    id: str
    title: str
    description: str
    content_type: str
    score: float
    relevance_factors: List[str]
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    highlights: List[str] = field(default_factory=list)


@dataclass
class SearchQuery:
    """Запрос поиска"""
    query: str
    search_type: SearchType
    filters: Dict[str, Any]
    sort_by: str
    sort_order: str  # 'asc' or 'desc'
    page: int
    per_page: int
    user_id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)


class SearchIndex:
    """Индекс поиска"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.documents: Dict[str, Dict[str, Any]] = {}
        self.inverted_index: Dict[str, Set[str]] = defaultdict(set)
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2
        )
        self.tfidf_matrix = None
        self.document_ids = []
        
        # Инициализация NLTK
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            from nltk.corpus import stopwords
            self.stop_words = set(stopwords.words('english'))
        except:
            self.stop_words = set()
    
    def add_document(self, doc_id: str, content: Dict[str, Any]) -> bool:
        """
        Добавляет документ в индекс поиска.
        
        Args:
            doc_id: ID документа
            content: Содержание документа
            
        Returns:
            bool: Успешность операции
        """
        try:
            # Сохраняем документ
            self.documents[doc_id] = content
            
            # Создаем текст для индексации
            index_text = self._create_index_text(content)
            
            # Добавляем в инвертированный индекс
            words = self._tokenize_text(index_text)
            for word in words:
                self.inverted_index[word].add(doc_id)
            
            # Перестраиваем TF-IDF матрицу
            self._rebuild_tfidf_matrix()
            
            self.logger.info(f"Документ {doc_id} добавлен в индекс поиска")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при добавлении документа в индекс: {str(e)}")
            return False
    
    def remove_document(self, doc_id: str) -> bool:
        """
        Удаляет документ из индекса.
        
        Args:
            doc_id: ID документа
            
        Returns:
            bool: Успешность операции
        """
        try:
            if doc_id in self.documents:
                # Удаляем из документов
                del self.documents[doc_id]
                
                # Удаляем из инвертированного индекса
                words_to_remove = []
                for word, doc_ids in self.inverted_index.items():
                    if doc_id in doc_ids:
                        doc_ids.remove(doc_id)
                        if not doc_ids:  # Если список пуст, помечаем для удаления
                            words_to_remove.append(word)
                
                # Удаляем пустые записи из инвертированного индекса
                for word in words_to_remove:
                    del self.inverted_index[word]
                
                # Перестраиваем TF-IDF матрицу
                self._rebuild_tfidf_matrix()
                
                self.logger.info(f"Документ {doc_id} удален из индекса поиска")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Ошибка при удалении документа из индекса: {str(e)}")
            return False
    
    def _create_index_text(self, content: Dict[str, Any]) -> str:
        """
        Создает текст для индексации из содержания документа.
        
        Args:
            content: Содержание документа
            
        Returns:
            str: Текст для индексации
        """
        text_parts = []
        
        # Добавляем основные поля
        for field in ['title', 'description', 'content', 'name']:
            if field in content and content[field]:
                text_parts.append(str(content[field]))
        
        # Добавляем теги
        if 'tags' in content and content['tags']:
            if isinstance(content['tags'], list):
                text_parts.extend(content['tags'])
            else:
                text_parts.append(str(content['tags']))
        
        # Добавляем категории
        if 'category' in content and content['category']:
            text_parts.append(str(content['category']))
        
        return ' '.join(text_parts)
    
    def _tokenize_text(self, text: str) -> List[str]:
        """
        Токенизирует текст.
        
        Args:
            text: Текст для токенизации
            
        Returns:
            list: Список токенов
        """
        # Простая токенизация
        words = re.findall(r'\b\w+\b', text.lower())
        # Удаляем стоп-слова
        words = [word for word in words if word not in self.stop_words and len(word) > 2]
        return words
    
    def _rebuild_tfidf_matrix(self):
        """Перестраивает TF-IDF матрицу."""
        try:
            if not self.documents:
                self.tfidf_matrix = None
                self.document_ids = []
                return
            
            # Создаем тексты для всех документов
            texts = []
            self.document_ids = []
            
            for doc_id, content in self.documents.items():
                text = self._create_index_text(content)
                if text.strip():
                    texts.append(text)
                    self.document_ids.append(doc_id)
            
            if texts:
                self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
            else:
                self.tfidf_matrix = None
                
        except Exception as e:
            self.logger.error(f"Ошибка при перестройке TF-IDF матрицы: {str(e)}")
            self.tfidf_matrix = None
    
    def search(self, query: str, filters: Dict[str, Any] = None, 
               limit: int = 20) -> List[Tuple[str, float]]:
        """
        Выполняет поиск по индексу.
        
        Args:
            query: Поисковый запрос
            filters: Фильтры поиска
            limit: Максимальное количество результатов
            
        Returns:
            list: Список (doc_id, score) отсортированный по релевантности
        """
        try:
            if not self.documents:
                return []
            
            # Базовый поиск по инвертированному индексу
            basic_results = self._basic_search(query)
            
            # TF-IDF поиск
            tfidf_results = self._tfidf_search(query)
            
            # Комбинируем результаты
            combined_scores = defaultdict(float)
            
            # Веса для разных методов поиска
            basic_weight = 0.3
            tfidf_weight = 0.7
            
            # Комбинируем оценки
            for doc_id, score in basic_results:
                combined_scores[doc_id] += score * basic_weight
            
            for doc_id, score in tfidf_results:
                combined_scores[doc_id] += score * tfidf_weight
            
            # Применяем фильтры
            if filters:
                filtered_docs = self._apply_filters(list(combined_scores.keys()), filters)
                combined_scores = {doc_id: score for doc_id, score in combined_scores.items() 
                                 if doc_id in filtered_docs}
            
            # Сортируем по релевантности
            sorted_results = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
            
            return sorted_results[:limit]
            
        except Exception as e:
            self.logger.error(f"Ошибка при выполнении поиска: {str(e)}")
            return []
    
    def _basic_search(self, query: str) -> List[Tuple[str, float]]:
        """
        Базовый поиск по инвертированному индексу.
        
        Args:
            query: Поисковый запрос
            
        Returns:
            list: Список (doc_id, score)
        """
        query_words = self._tokenize_text(query)
        if not query_words:
            return []
        
        # Находим документы, содержащие слова запроса
        doc_scores = defaultdict(float)
        
        for word in query_words:
            if word in self.inverted_index:
                doc_ids = self.inverted_index[word]
                # Оценка на основе частоты слова в документе
                for doc_id in doc_ids:
                    doc_scores[doc_id] += 1.0 / len(query_words)
        
        return list(doc_scores.items())
    
    def _tfidf_search(self, query: str) -> List[Tuple[str, float]]:
        """
        Поиск на основе TF-IDF.
        
        Args:
            query: Поисковый запрос
            
        Returns:
            list: Список (doc_id, score)
        """
        if self.tfidf_matrix is None or not self.document_ids:
            return []
        
        try:
            # Векторизуем запрос
            query_vector = self.tfidf_vectorizer.transform([query])
            
            # Рассчитываем косинусное сходство
            similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
            
            # Создаем список результатов
            results = []
            for i, similarity in enumerate(similarities):
                if similarity > 0.01:  # Минимальный порог
                    doc_id = self.document_ids[i]
                    results.append((doc_id, float(similarity)))
            
            return results
            
        except Exception as e:
            self.logger.error(f"Ошибка при TF-IDF поиске: {str(e)}")
            return []
    
    def _apply_filters(self, doc_ids: List[str], filters: Dict[str, Any]) -> Set[str]:
        """
        Применяет фильтры к документам.
        
        Args:
            doc_ids: Список ID документов
            filters: Фильтры
            
        Returns:
            set: Отфильтрованные ID документов
        """
        filtered_docs = set(doc_ids)
        
        for doc_id in doc_ids:
            if doc_id not in self.documents:
                filtered_docs.discard(doc_id)
                continue
            
            doc = self.documents[doc_id]
            
            # Применяем фильтры
            for filter_name, filter_value in filters.items():
                if not self._check_filter(doc, filter_name, filter_value):
                    filtered_docs.discard(doc_id)
                    break
        
        return filtered_docs
    
    def _check_filter(self, doc: Dict[str, Any], filter_name: str, filter_value: Any) -> bool:
        """
        Проверяет соответствие документа фильтру.
        
        Args:
            doc: Документ
            filter_name: Название фильтра
            filter_value: Значение фильтра
            
        Returns:
            bool: Соответствует ли фильтру
        """
        try:
            if filter_name == 'category':
                return doc.get('category') == filter_value
            
            elif filter_name == 'content_type':
                return doc.get('type') == filter_value
            
            elif filter_name == 'status':
                return doc.get('status') == filter_value
            
            elif filter_name == 'tags':
                doc_tags = doc.get('tags', [])
                if isinstance(filter_value, list):
                    return any(tag in doc_tags for tag in filter_value)
                else:
                    return filter_value in doc_tags
            
            elif filter_name == 'date_range':
                if isinstance(filter_value, dict) and 'start' in filter_value and 'end' in filter_value:
                    doc_date = doc.get('created_at')
                    if doc_date:
                        if isinstance(doc_date, str):
                            from datetime import datetime
                            doc_date = datetime.fromisoformat(doc_date.replace('Z', '+00:00'))
                        return filter_value['start'] <= doc_date <= filter_value['end']
            
            elif filter_name == 'rating':
                if isinstance(filter_value, dict) and 'min' in filter_value and 'max' in filter_value:
                    doc_rating = doc.get('rating', 0)
                    return filter_value['min'] <= doc_rating <= filter_value['max']
            
            elif filter_name == 'difficulty':
                return doc.get('difficulty') == filter_value
            
            return True  # Если фильтр не распознан, пропускаем
            
        except Exception as e:
            self.logger.error(f"Ошибка при проверке фильтра {filter_name}: {str(e)}")
            return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Получает статистику индекса поиска.
        
        Returns:
            dict: Статистика
        """
        return {
            'total_documents': len(self.documents),
            'indexed_words': len(self.inverted_index),
            'average_document_length': sum(len(self._create_index_text(doc).split()) 
                                         for doc in self.documents.values()) / len(self.documents) if self.documents else 0,
            'tfidf_matrix_shape': self.tfidf_matrix.shape if self.tfidf_matrix is not None else (0, 0)
        }


class AdvancedSearchEngine:
    """
    Расширенный движок поиска для системы ПрофиТест.
    Обеспечивает комплексный поиск по контенту и пользователям.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.search_indices: Dict[SearchType, SearchIndex] = {}
        self.search_queries: Dict[str, SearchQuery] = {}
        self.search_history: List[Dict[str, Any]] = []
        
        # Создаем индексы для разных типов поиска
        for search_type in SearchType:
            self.search_indices[search_type] = SearchIndex()
        
        # Инициализация системных данных
        self._initialize_system_data()
    
    def _initialize_system_data(self):
        """Инициализирует системные данные для поиска."""
        # Добавляем тестовые документы
        self._add_sample_content()
        self._add_sample_users()
    
    def _add_sample_content(self):
        """Добавляет тестовый контент в индексы поиска."""
        sample_content = [
            {
                'id': 'content_1',
                'type': 'test',
                'title': 'Профориентационный тест Холланда',
                'description': 'Классический тест для определения профессиональных интересов',
                'category': 'psychology',
                'tags': ['психология', 'карьера', 'профориентация', 'Холланд'],
                'difficulty': 'medium',
                'status': 'published',
                'rating': 4.5,
                'created_at': datetime.now() - timedelta(days=30)
            },
            {
                'id': 'content_2',
                'type': 'article',
                'title': 'Как выбрать профессию в 2024 году',
                'description': 'Актуальные советы по выбору профессии',
                'category': 'career',
                'tags': ['карьера', 'советы', '2024', 'профессия'],
                'difficulty': 'easy',
                'status': 'published',
                'rating': 4.2,
                'created_at': datetime.now() - timedelta(days=15)
            },
            {
                'id': 'content_3',
                'type': 'video',
                'title': 'Тренды рынка труда 2024',
                'description': 'Анализ текущих трендов на рынке труда',
                'category': 'market',
                'tags': ['рынок труда', 'тренды', '2024', 'аналитика'],
                'difficulty': 'medium',
                'status': 'published',
                'rating': 4.0,
                'created_at': datetime.now() - timedelta(days=7)
            }
        ]
        
        for content in sample_content:
            self.add_content(content)
    
    def _add_sample_users(self):
        """Добавляет тестовых пользователей в индекс поиска."""
        sample_users = [
            {
                'id': 'user_1',
                'type': 'user',
                'name': 'Алексей Петров',
                'username': 'alex_petrov',
                'bio': 'Психолог, специализирующийся на профориентации',
                'skills': ['психология', 'профориентация', 'консультирование'],
                'interests': ['психология', 'образование', 'развитие'],
                'status': 'active',
                'created_at': datetime.now() - timedelta(days=100)
            },
            {
                'id': 'user_2',
                'type': 'user',
                'name': 'Мария Иванова',
                'username': 'maria_ivanova',
                'bio': 'HR-специалист с 5-летним стажем',
                'skills': ['HR', 'рекрутинг', 'подбор персонала'],
                'interests': ['HR', 'управление', 'команды'],
                'status': 'active',
                'created_at': datetime.now() - timedelta(days=200)
            }
        ]
        
        for user in sample_users:
            self.add_user(user)
    
    def add_content(self, content: Dict[str, Any]) -> bool:
        """
        Добавляет контент в индексы поиска.
        
        Args:
            content: Данные контента
            
        Returns:
            bool: Успешность операции
        """
        try:
            content_id = content.get('id')
            if not content_id:
                return False
            
            # Добавляем в общий индекс
            self.search_indices[SearchType.ALL].add_document(content_id, content)
            
            # Добавляем в специализированные индексы
            content_type = content.get('type')
            if content_type:
                try:
                    search_type = SearchType(content_type)
                    self.search_indices[search_type].add_document(content_id, content)
                except ValueError:
                    # Если тип не соответствует enum, добавляем в контентный индекс
                    self.search_indices[SearchType.CONTENT].add_document(content_id, content)
            
            self.logger.info(f"Контент {content_id} добавлен в индексы поиска")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при добавлении контента в индексы: {str(e)}")
            return False
    
    def add_user(self, user: Dict[str, Any]) -> bool:
        """
        Добавляет пользователя в индекс поиска.
        
        Args:
            user: Данные пользователя
            
        Returns:
            bool: Успешность операции
        """
        try:
            user_id = user.get('id')
            if not user_id:
                return False
            
            # Добавляем в индекс пользователей
            self.search_indices[SearchType.USER].add_document(user_id, user)
            
            # Добавляем в общий индекс
            self.search_indices[SearchType.ALL].add_document(user_id, user)
            
            self.logger.info(f"Пользователь {user_id} добавлен в индекс поиска")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при добавлении пользователя в индекс: {str(e)}")
            return False
    
    def search(self, query: str, search_type: SearchType = SearchType.ALL,
               filters: Dict[str, Any] = None, sort_by: str = 'relevance',
               sort_order: str = 'desc', page: int = 1, per_page: int = 20,
               user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Выполняет поиск.
        
        Args:
            query: Поисковый запрос
            search_type: Тип поиска
            filters: Фильтры
            sort_by: Поле сортировки
            sort_order: Порядок сортировки
            page: Номер страницы
            per_page: Результатов на страницу
            user_id: ID пользователя (для истории)
            
        Returns:
            dict: Результаты поиска
        """
        try:
            import uuid
            search_id = str(uuid.uuid4())
            
            # Создаем объект запроса
            search_query = SearchQuery(
                query=query,
                search_type=search_type,
                filters=filters or {},
                sort_by=sort_by,
                sort_order=sort_order,
                page=page,
                per_page=per_page,
                user_id=user_id
            )
            
            self.search_queries[search_id] = search_query
            
            # Выполняем поиск в соответствующем индексе
            index = self.search_indices.get(search_type)
            if not index:
                return {
                    'success': False,
                    'message': 'Некорректный тип поиска',
                    'search_id': search_id
                }
            
            # Выполняем поиск
            raw_results = index.search(query, filters, per_page * page)
            
            # Преобразуем результаты
            results = []
            for doc_id, score in raw_results:
                if doc_id in index.documents:
                    doc = index.documents[doc_id]
                    result = SearchResult(
                        id=doc_id,
                        title=doc.get('title', doc.get('name', 'Без названия')),
                        description=doc.get('description', ''),
                        content_type=doc.get('type', 'unknown'),
                        score=score,
                        relevance_factors=['text_match', 'tfidf_similarity'],
                        metadata={
                            'category': doc.get('category'),
                            'tags': doc.get('tags', []),
                            'rating': doc.get('rating'),
                            'difficulty': doc.get('difficulty')
                        },
                        created_at=doc.get('created_at', datetime.now()),
                        updated_at=doc.get('updated_at', datetime.now()),
                        highlights=self._generate_highlights(query, doc)
                    )
                    results.append(result)
            
            # Сортировка
            if sort_by == 'relevance':
                results.sort(key=lambda x: x.score, reverse=(sort_order == 'desc'))
            elif sort_by == 'date':
                results.sort(key=lambda x: x.created_at, reverse=(sort_order == 'desc'))
            elif sort_by == 'rating':
                results.sort(key=lambda x: x.metadata.get('rating', 0), reverse=(sort_order == 'desc'))
            
            # Пагинация
            total_results = len(results)
            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            paginated_results = results[start_idx:end_idx]
            
            # Сохраняем в историю поиска
            if user_id:
                self.search_history.append({
                    'search_id': search_id,
                    'user_id': user_id,
                    'query': query,
                    'search_type': search_type.value,
                    'timestamp': datetime.now().isoformat(),
                    'results_count': total_results
                })
            
            return {
                'success': True,
                'search_id': search_id,
                'query': query,
                'results': [
                    {
                        'id': result.id,
                        'title': result.title,
                        'description': result.description,
                        'content_type': result.content_type,
                        'score': round(result.score, 3),
                        'relevance_factors': result.relevance_factors,
                        'metadata': result.metadata,
                        'highlights': result.highlights,
                        'created_at': result.created_at.isoformat()
                    }
                    for result in paginated_results
                ],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total_results,
                    'pages': (total_results + per_page - 1) // per_page
                },
                'filters_applied': filters or {},
                'sort_by': sort_by,
                'sort_order': sort_order
            }
            
        except Exception as e:
            self.logger.error(f"Ошибка при выполнении поиска: {str(e)}")
            return {
                'success': False,
                'message': str(e)
            }
    
    def _generate_highlights(self, query: str, document: Dict[str, Any]) -> List[str]:
        """
        Генерирует подсветку найденных фрагментов.
        
        Args:
            query: Поисковый запрос
            document: Документ
            
        Returns:
            list: Список подсвеченных фрагментов
        """
        highlights = []
        query_words = re.findall(r'\b\w+\b', query.lower())
        
        # Ищем совпадения в различных полях
        search_fields = ['title', 'description', 'content', 'name', 'bio']
        
        for field in search_fields:
            if field in document and document[field]:
                text = str(document[field])
                # Создаем фрагмент с подсветкой
                highlighted_text = text
                for word in query_words:
                    highlighted_text = re.sub(
                        f'(\\b{re.escape(word)}\\b)',
                        r'**\\1**',
                        highlighted_text,
                        flags=re.IGNORECASE
                    )
                
                # Ограничиваем длину фрагмента
                if len(highlighted_text) > 100:
                    # Находим позицию первого совпадения
                    first_match = len(highlighted_text)
                    for word in query_words:
                        match = re.search(re.escape(word), highlighted_text, re.IGNORECASE)
                        if match and match.start() < first_match:
                            first_match = match.start()
                    
                    # Создаем фрагмент вокруг совпадения
                    start = max(0, first_match - 50)
                    end = min(len(highlighted_text), first_match + 150)
                    highlighted_text = highlighted_text[start:end]
                    
                    # Добавляем многоточия если нужно
                    if start > 0:
                        highlighted_text = '...' + highlighted_text
                    if end < len(text):
                        highlighted_text = highlighted_text + '...'
                
                if '**' in highlighted_text:  # Если есть совпадения
                    highlights.append(f"{field}: {highlighted_text}")
                
                if len(highlights) >= 3:  # Ограничиваем количество фрагментов
                    break
        
        return highlights[:3]
    
    def get_search_suggestions(self, query_prefix: str, limit: int = 10) -> List[str]:
        """
        Получает предложения для автозаполнения поиска.
        
        Args:
            query_prefix: Префикс запроса
            limit: Максимальное количество предложений
            
        Returns:
            list: Список предложений
        """
        try:
            suggestions = set()
            prefix_lower = query_prefix.lower()
            
            # Ищем в заголовках и тегах
            for index in self.search_indices.values():
                for doc in index.documents.values():
                    # Проверяем заголовки
                    title = doc.get('title', doc.get('name', ''))
                    if title and prefix_lower in title.lower():
                        suggestions.add(title)
                    
                    # Проверяем теги
                    tags = doc.get('tags', [])
                    if isinstance(tags, list):
                        for tag in tags:
                            if prefix_lower in tag.lower():
                                suggestions.add(tag)
                    
                    if len(suggestions) >= limit * 2:  # Собираем больше для сортировки
                        break
                
                if len(suggestions) >= limit * 2:
                    break
            
            # Сортируем по релевантности и ограничиваем
            suggestions_list = sorted(list(suggestions), 
                                    key=lambda x: x.lower().startswith(prefix_lower), 
                                    reverse=True)
            
            return suggestions_list[:limit]
            
        except Exception as e:
            self.logger.error(f"Ошибка при получении предложений поиска: {str(e)}")
            return []
    
    def get_popular_searches(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Получает популярные поисковые запросы.
        
        Args:
            limit: Максимальное количество
            
        Returns:
            list: Список популярных запросов
        """
        try:
            # Считаем частоту запросов
            query_counts = defaultdict(int)
            for search_record in self.search_history:
                query_counts[search_record['query']] += 1
            
            # Сортируем по частоте
            popular_queries = sorted(query_counts.items(), key=lambda x: x[1], reverse=True)
            
            return [
                {
                    'query': query,
                    'count': count,
                    'trend': 'rising' if count > 5 else 'stable'
                }
                for query, count in popular_queries[:limit]
            ]
            
        except Exception as e:
            self.logger.error(f"Ошибка при получении популярных поисков: {str(e)}")
            return []
    
    def get_search_statistics(self) -> Dict[str, Any]:
        """
        Получает статистику по поиску.
        
        Returns:
            dict: Статистика поиска
        """
        try:
            total_searches = len(self.search_history)
            
            # Статистика по типам поиска
            search_type_counts = defaultdict(int)
            for search_record in self.search_history:
                search_type_counts[search_record['search_type']] += 1
            
            # Статистика по индексам
            index_stats = {}
            for search_type, index in self.search_indices.items():
                index_stats[search_type.value] = index.get_statistics()
            
            # Уникальные пользователи
            unique_users = len(set(record['user_id'] for record in self.search_history if record['user_id']))
            
            return {
                'total_searches': total_searches,
                'unique_users': unique_users,
                'searches_by_type': dict(search_type_counts),
                'index_statistics': index_stats,
                'recent_searches': len([r for r in self.search_history 
                                       if datetime.fromisoformat(r['timestamp']) > datetime.now() - timedelta(days=7)]),
                'average_results_per_search': sum(r['results_count'] for r in self.search_history) / total_searches if total_searches > 0 else 0
            }
            
        except Exception as e:
            self.logger.error(f"Ошибка при получении статистики поиска: {str(e)}")
            return {}


# Глобальный экземпляр движка поиска
search_engine = AdvancedSearchEngine()