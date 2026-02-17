"""
Форматирование API ответов в единообразном стиле
"""
from typing import Any, Dict, List, Optional
from datetime import datetime, date
from flask import jsonify, Response
from enum import Enum


class ResponseStatus(Enum):
    """Статусы ответов"""
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"


class APIResponse:
    """Класс для форматирования API ответов"""
    
    @staticmethod
    def success(
        data: Any = None,
        message: Optional[str] = None,
        meta: Optional[Dict] = None,
        status_code: int = 200
    ) -> Response:
        """
        Успешный ответ
        
        Args:
            data: данные ответа
            message: сообщение
            meta: метаданные (пагинация, версия и т.д.)
            status_code: HTTP статус код
        """
        response = {
            'status': ResponseStatus.SUCCESS.value,
            'data': data
        }
        
        if message:
            response['message'] = message
        
        if meta:
            response['meta'] = meta
        
        response['timestamp'] = datetime.utcnow().isoformat()
        
        return jsonify(response), status_code
    
    @staticmethod
    def error(
        message: str,
        errors: Optional[Dict] = None,
        error_code: Optional[str] = None,
        status_code: int = 400
    ) -> Response:
        """
        Ответ с ошибкой
        
        Args:
            message: сообщение об ошибке
            errors: детали ошибок
            error_code: код ошибки
            status_code: HTTP статус код
        """
        response = {
            'status': ResponseStatus.ERROR.value,
            'message': message
        }
        
        if errors:
            response['errors'] = errors
        
        if error_code:
            response['error_code'] = error_code
        
        response['timestamp'] = datetime.utcnow().isoformat()
        
        return jsonify(response), status_code
    
    @staticmethod
    def validation_error(
        errors: Dict[str, List[str]],
        message: str = "Validation failed"
    ) -> Response:
        """
        Ответ с ошибкой валидации
        
        Args:
            errors: словарь ошибок {field: [errors]}
            message: общее сообщение
        """
        return APIResponse.error(
            message=message,
            errors=errors,
            error_code='VALIDATION_ERROR',
            status_code=422
        )
    
    @staticmethod
    def not_found(
        resource: str = "Resource",
        resource_id: Optional[Any] = None
    ) -> Response:
        """
        Ответ 404
        
        Args:
            resource: название ресурса
            resource_id: ID ресурса
        """
        message = f"{resource} not found"
        if resource_id:
            message += f" (ID: {resource_id})"
        
        return APIResponse.error(
            message=message,
            error_code='NOT_FOUND',
            status_code=404
        )
    
    @staticmethod
    def unauthorized(
        message: str = "Authentication required"
    ) -> Response:
        """Ответ 401"""
        return APIResponse.error(
            message=message,
            error_code='UNAUTHORIZED',
            status_code=401
        )
    
    @staticmethod
    def forbidden(
        message: str = "Access denied"
    ) -> Response:
        """Ответ 403"""
        return APIResponse.error(
            message=message,
            error_code='FORBIDDEN',
            status_code=403
        )
    
    @staticmethod
    def conflict(
        message: str = "Resource already exists",
        details: Optional[Dict] = None
    ) -> Response:
        """Ответ 409"""
        return APIResponse.error(
            message=message,
            errors=details,
            error_code='CONFLICT',
            status_code=409
        )
    
    @staticmethod
    def rate_limit_exceeded(
        retry_after: int = 60
    ) -> Response:
        """Ответ 429"""
        response = APIResponse.error(
            message="Rate limit exceeded",
            error_code='RATE_LIMIT_EXCEEDED',
            status_code=429
        )
        
        # Добавляем заголовок Retry-After
        response[0].headers['Retry-After'] = str(retry_after)
        
        return response
    
    @staticmethod
    def server_error(
        message: str = "Internal server error",
        error_id: Optional[str] = None
    ) -> Response:
        """Ответ 500"""
        response_data = {
            'message': message,
            'error_code': 'INTERNAL_ERROR'
        }
        
        if error_id:
            response_data['error_id'] = error_id
            response_data['message'] += f" (Error ID: {error_id})"
        
        return APIResponse.error(**response_data, status_code=500)
    
    @staticmethod
    def paginated(
        items: List[Any],
        page: int,
        per_page: int,
        total: int,
        message: Optional[str] = None
    ) -> Response:
        """
        Ответ с пагинацией
        
        Args:
            items: список элементов
            page: текущая страница
            per_page: элементов на странице
            total: всего элементов
            message: сообщение
        """
        total_pages = (total + per_page - 1) // per_page
        
        meta = {
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1
            }
        }
        
        return APIResponse.success(
            data=items,
            message=message,
            meta=meta
        )
    
    @staticmethod
    def created(
        data: Any,
        message: str = "Resource created successfully",
        resource_id: Optional[Any] = None
    ) -> Response:
        """
        Ответ 201 (создано)
        
        Args:
            data: созданный ресурс
            message: сообщение
            resource_id: ID созданного ресурса
        """
        meta = {}
        if resource_id:
            meta['resource_id'] = resource_id
        
        return APIResponse.success(
            data=data,
            message=message,
            meta=meta if meta else None,
            status_code=201
        )
    
    @staticmethod
    def no_content() -> Response:
        """Ответ 204 (нет содержимого)"""
        return '', 204
    
    @staticmethod
    def accepted(
        task_id: Optional[str] = None,
        message: str = "Request accepted for processing"
    ) -> Response:
        """
        Ответ 202 (принято)
        
        Args:
            task_id: ID асинхронной задачи
            message: сообщение
        """
        meta = {}
        if task_id:
            meta['task_id'] = task_id
        
        return APIResponse.success(
            message=message,
            meta=meta if meta else None,
            status_code=202
        )


class DataSerializer:
    """Сериализация данных для API"""
    
    @staticmethod
    def serialize(obj: Any) -> Any:
        """
        Сериализация объекта
        
        Поддерживает:
        - SQLAlchemy модели
        - datetime/date
        - Enum
        - списки и словари
        """
        if obj is None:
            return None
        
        # datetime/date
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, date):
            return obj.isoformat()
        
        # Enum
        if isinstance(obj, Enum):
            return obj.value
        
        # Список
        if isinstance(obj, list):
            return [DataSerializer.serialize(item) for item in obj]
        
        # Словарь
        if isinstance(obj, dict):
            return {key: DataSerializer.serialize(value) for key, value in obj.items()}
        
        # SQLAlchemy модель
        if hasattr(obj, '__table__'):
            return DataSerializer.serialize_model(obj)
        
        # Примитивные типы
        return obj
    
    @staticmethod
    def serialize_model(model: Any, exclude: Optional[List[str]] = None) -> Dict:
        """
        Сериализация SQLAlchemy модели
        
        Args:
            model: модель для сериализации
            exclude: список полей для исключения
        """
        exclude = exclude or []
        result = {}
        
        for column in model.__table__.columns:
            if column.name not in exclude:
                value = getattr(model, column.name)
                result[column.name] = DataSerializer.serialize(value)
        
        return result
    
    @staticmethod
    def serialize_list(
        models: List[Any],
        exclude: Optional[List[str]] = None
    ) -> List[Dict]:
        """Сериализация списка моделей"""
        return [DataSerializer.serialize_model(model, exclude) for model in models]


class ResponseBuilder:
    """Построитель ответов с цепочкой вызовов"""
    
    def __init__(self):
        self._data = None
        self._message = None
        self._meta = {}
        self._status_code = 200
        self._errors = None
        self._error_code = None
    
    def data(self, data: Any) -> 'ResponseBuilder':
        """Установить данные"""
        self._data = DataSerializer.serialize(data)
        return self
    
    def message(self, message: str) -> 'ResponseBuilder':
        """Установить сообщение"""
        self._message = message
        return self
    
    def meta(self, key: str, value: Any) -> 'ResponseBuilder':
        """Добавить метаданные"""
        self._meta[key] = value
        return self
    
    def pagination(
        self,
        page: int,
        per_page: int,
        total: int
    ) -> 'ResponseBuilder':
        """Добавить пагинацию"""
        total_pages = (total + per_page - 1) // per_page
        
        self._meta['pagination'] = {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
        return self
    
    def status_code(self, code: int) -> 'ResponseBuilder':
        """Установить статус код"""
        self._status_code = code
        return self
    
    def errors(self, errors: Dict) -> 'ResponseBuilder':
        """Установить ошибки"""
        self._errors = errors
        return self
    
    def error_code(self, code: str) -> 'ResponseBuilder':
        """Установить код ошибки"""
        self._error_code = code
        return self
    
    def build(self) -> Response:
        """Построить ответ"""
        if self._errors:
            return APIResponse.error(
                message=self._message or "Error occurred",
                errors=self._errors,
                error_code=self._error_code,
                status_code=self._status_code
            )
        
        return APIResponse.success(
            data=self._data,
            message=self._message,
            meta=self._meta if self._meta else None,
            status_code=self._status_code
        )


# Удобные функции
def success_response(*args, **kwargs) -> Response:
    """Быстрый успешный ответ"""
    return APIResponse.success(*args, **kwargs)


def error_response(*args, **kwargs) -> Response:
    """Быстрый ответ с ошибкой"""
    return APIResponse.error(*args, **kwargs)


def paginated_response(*args, **kwargs) -> Response:
    """Быстрый ответ с пагинацией"""
    return APIResponse.paginated(*args, **kwargs)
