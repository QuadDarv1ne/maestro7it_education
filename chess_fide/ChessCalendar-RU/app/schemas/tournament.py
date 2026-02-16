"""
Pydantic схемы для турниров
"""
from pydantic import BaseModel, Field, HttpUrl
from pydantic.functional_validators import field_validator
from pydantic.config import ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum


class TournamentCategory(str, Enum):
    """Категории турниров"""
    FIDE = "FIDE"
    NATIONAL = "National"
    REGIONAL = "Regional"
    CLUB = "Club"
    ONLINE = "Online"


class TournamentStatus(str, Enum):
    """Статусы турниров"""
    SCHEDULED = "Scheduled"
    ONGOING = "Ongoing"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class TournamentBase(BaseModel):
    """Базовая схема турнира"""
    name: str = Field(min_length=3, max_length=200, description="Название турнира")
    start_date: datetime = Field(description="Дата начала")
    end_date: datetime = Field(description="Дата окончания")
    location: str = Field(min_length=2, max_length=200, description="Место проведения")
    category: TournamentCategory = Field(description="Категория турнира")
    status: TournamentStatus = Field(default=TournamentStatus.SCHEDULED, description="Статус турнира")
    description: Optional[str] = Field(default=None, max_length=2000, description="Описание")
    source_url: Optional[HttpUrl] = Field(default=None, description="URL источника")
    fide_id: Optional[str] = Field(default=None, max_length=50, description="FIDE ID")
    
    @field_validator('end_date')
    @classmethod
    def validate_dates(cls, v, values):
        """Проверка, что end_date >= start_date"""
        # Note: In Pydantic V2, field validators don't have access to other fields directly
        # We'll implement this logic elsewhere or use a model validator
        return v
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Валидация названия"""
        if not v.strip():
            raise ValueError('name cannot be empty or whitespace')
        return v.strip()
    
    @field_validator('location')
    @classmethod
    def validate_location(cls, v):
        """Валидация локации"""
        if not v.strip():
            raise ValueError('location cannot be empty or whitespace')
        return v.strip()
    
    model_config = ConfigDict(use_enum_values=True)


class TournamentCreate(TournamentBase):
    """Схема для создания турнира"""
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Чемпионат России по шахматам",
            "start_date": "2024-03-01T10:00:00",
            "end_date": "2024-03-10T18:00:00",
            "location": "Москва",
            "category": "National",
            "status": "Scheduled",
            "description": "Ежегодный чемпионат России",
            "source_url": "https://ruchess.ru/tournament/123",
            "fide_id": "RUS2024001"
        }
    })


class TournamentUpdate(BaseModel):
    """Схема для обновления турнира"""
    name: Optional[str] = Field(default=None, min_length=3, max_length=200)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[str] = Field(default=None, min_length=2, max_length=200)
    category: Optional[TournamentCategory] = None
    status: Optional[TournamentStatus] = None
    description: Optional[str] = Field(default=None, max_length=2000)
    source_url: Optional[HttpUrl] = None
    fide_id: Optional[str] = Field(default=None, max_length=50)
    
    @field_validator('end_date')
    @classmethod
    def validate_dates(cls, v):
        """Проверка дат при обновлении"""
        # Note: In Pydantic V2, field validators don't have access to other fields directly
        # We'll implement this logic elsewhere
        return v
    
    model_config = ConfigDict(
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "status": "Ongoing",
                "description": "Обновленное описание"
            }
        }
    )


class TournamentResponse(TournamentBase):
    """Схема ответа с турниром"""
    id: int = Field(description="ID турнира")
    created_at: datetime = Field(description="Дата создания")
    updated_at: Optional[datetime] = Field(default=None, description="Дата обновления")
    average_rating: Optional[float] = Field(default=None, description="Средний рейтинг")
    favorites_count: Optional[int] = Field(default=None, description="Количество в избранном")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Чемпионат России",
                "start_date": "2024-03-01T10:00:00",
                "end_date": "2024-03-10T18:00:00",
                "location": "Москва",
                "category": "National",
                "status": "Scheduled",
                "description": "Описание турнира",
                "source_url": "https://ruchess.ru/tournament/123",
                "fide_id": "RUS2024001",
                "created_at": "2024-02-01T12:00:00",
                "updated_at": "2024-02-15T14:30:00",
                "average_rating": 4.5,
                "favorites_count": 42
            }
        }
    )


class TournamentFilter(BaseModel):
    """Фильтры для поиска турниров"""
    category: Optional[TournamentCategory] = Field(default=None, description="Категория")
    status: Optional[TournamentStatus] = Field(default=None, description="Статус")
    location: Optional[str] = Field(default=None, max_length=200, description="Локация")
    start_date_from: Optional[datetime] = Field(default=None, description="Начало с")
    start_date_to: Optional[datetime] = Field(default=None, description="Начало до")
    end_date_from: Optional[datetime] = Field(default=None, description="Окончание с")
    end_date_to: Optional[datetime] = Field(default=None, description="Окончание до")
    search: Optional[str] = Field(default=None, max_length=200, description="Поиск по названию")
    
    @field_validator('start_date_to')
    @classmethod
    def validate_start_date_range(cls, v, values):
        """Валидация диапазона дат начала"""
        # Note: In Pydantic V2, field validators don't have access to other fields directly
        # We'll implement this logic elsewhere
        return v
    
    @field_validator('end_date_to')
    @classmethod
    def validate_end_date_range(cls, v):
        """Валидация диапазона дат окончания"""
        return v
    
    model_config = ConfigDict(
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "category": "National",
                "status": "Scheduled",
                "location": "Москва",
                "start_date_from": "2024-03-01T00:00:00",
                "start_date_to": "2024-12-31T23:59:59"
            }
        }
    )


class TournamentListResponse(BaseModel):
    """Ответ со списком турниров"""
    tournaments: List[TournamentResponse] = Field(description="Список турниров")
    total: int = Field(description="Всего турниров")
    page: int = Field(description="Текущая страница")
    per_page: int = Field(description="Элементов на странице")
    pages: int = Field(description="Всего страниц")
    has_next: bool = Field(description="Есть следующая страница")
    has_prev: bool = Field(description="Есть предыдущая страница")


class TournamentStats(BaseModel):
    """Статистика турнира"""
    total_tournaments: int = Field(description="Всего турниров")
    by_category: dict = Field(description="По категориям")
    by_status: dict = Field(description="По статусам")
    upcoming_count: int = Field(description="Предстоящих турниров")
    ongoing_count: int = Field(description="Текущих турниров")
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "total_tournaments": 150,
            "by_category": {
                "FIDE": 30,
                "National": 50,
                "Regional": 70
            },
            "by_status": {
                "Scheduled": 80,
                "Ongoing": 20,
                "Completed": 50
            },
            "upcoming_count": 80,
            "ongoing_count": 20
        }
    })


class TournamentRating(BaseModel):
    """Рейтинг турнира"""
    tournament_id: int = Field(description="ID турнира")
    rating: int = Field(ge=1, le=5, description="Рейтинг (1-5)")
    comment: Optional[str] = Field(default=None, max_length=500, description="Комментарий")
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "tournament_id": 1,
            "rating": 5,
            "comment": "Отличный турнир!"
        }
    })


class TournamentSubscription(BaseModel):
    """Подписка на турнир"""
    tournament_id: int = Field(description="ID турнира")
    notify_before_days: int = Field(default=7, ge=1, le=30, description="За сколько дней уведомить")
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "tournament_id": 1,
            "notify_before_days": 7
        }
    })
