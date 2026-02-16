"""
Общие Pydantic схемы
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, Any, Dict, List
from datetime import datetime


class PaginationParams(BaseModel):
    """Параметры пагинации"""
    page: int = Field(default=1, ge=1, description="Номер страницы")
    per_page: int = Field(default=20, ge=1, le=100, description="Элементов на странице")
    
    class Config:
        json_schema_extra = {
            "example": {
                "page": 1,
                "per_page": 20
            }
        }


class PaginationResponse(BaseModel):
    """Ответ с пагинацией"""
    total: int = Field(description="Всего элементов")
    page: int = Field(description="Текущая страница")
    per_page: int = Field(description="Элементов на странице")
    pages: int = Field(description="Всего страниц")
    has_next: bool = Field(description="Есть следующая страница")
    has_prev: bool = Field(description="Есть предыдущая страница")


class ErrorResponse(BaseModel):
    """Ответ с ошибкой"""
    error: str = Field(description="Сообщение об ошибке")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Детали ошибки")
    code: Optional[str] = Field(default=None, description="Код ошибки")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Validation error",
                "details": {"field": "email", "message": "Invalid email format"},
                "code": "VALIDATION_ERROR"
            }
        }


class SuccessResponse(BaseModel):
    """Успешный ответ"""
    message: str = Field(description="Сообщение об успехе")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Дополнительные данные")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operation completed successfully",
                "data": {"id": 1}
            }
        }


class DateRangeFilter(BaseModel):
    """Фильтр по диапазону дат"""
    start_date: Optional[datetime] = Field(default=None, description="Начальная дата")
    end_date: Optional[datetime] = Field(default=None, description="Конечная дата")
    
    @validator('end_date')
    def validate_date_range(cls, v, values):
        """Проверка, что end_date >= start_date"""
        if v and 'start_date' in values and values['start_date']:
            if v < values['start_date']:
                raise ValueError('end_date must be greater than or equal to start_date')
        return v


class SearchParams(BaseModel):
    """Параметры поиска"""
    q: str = Field(min_length=1, max_length=200, description="Поисковый запрос")
    limit: int = Field(default=20, ge=1, le=100, description="Максимум результатов")
    
    class Config:
        json_schema_extra = {
            "example": {
                "q": "chess tournament",
                "limit": 20
            }
        }


class SortParams(BaseModel):
    """Параметры сортировки"""
    sort_by: str = Field(default="created_at", description="Поле для сортировки")
    order: str = Field(default="desc", pattern="^(asc|desc)$", description="Порядок сортировки")
    
    @validator('sort_by')
    def validate_sort_field(cls, v):
        """Валидация поля сортировки"""
        allowed_fields = ['id', 'name', 'created_at', 'updated_at', 'start_date', 'end_date']
        if v not in allowed_fields:
            raise ValueError(f'sort_by must be one of: {", ".join(allowed_fields)}')
        return v


class IDResponse(BaseModel):
    """Ответ с ID"""
    id: int = Field(description="ID созданного объекта")
    
    class Config:
        json_schema_extra = {
            "example": {"id": 123}
        }


class BulkOperationResponse(BaseModel):
    """Ответ на массовую операцию"""
    success_count: int = Field(description="Количество успешных операций")
    error_count: int = Field(description="Количество ошибок")
    errors: Optional[List[Dict[str, Any]]] = Field(default=None, description="Список ошибок")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success_count": 95,
                "error_count": 5,
                "errors": [
                    {"id": 1, "error": "Duplicate entry"},
                    {"id": 5, "error": "Invalid data"}
                ]
            }
        }


class HealthCheckResponse(BaseModel):
    """Ответ health check"""
    status: str = Field(description="Статус сервиса")
    timestamp: datetime = Field(description="Время проверки")
    version: str = Field(description="Версия приложения")
    services: Dict[str, str] = Field(description="Статус зависимых сервисов")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2024-02-16T12:00:00Z",
                "version": "2.0.0",
                "services": {
                    "database": "healthy",
                    "redis": "healthy",
                    "celery": "healthy"
                }
            }
        }
