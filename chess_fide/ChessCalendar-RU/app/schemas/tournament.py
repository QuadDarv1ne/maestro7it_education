"""
Pydantic схемы для турниров
"""
from pydantic import BaseModel, Field, validator, HttpUrl
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
    
    @validator('end_date')
    def validate_dates(cls, v, values):
        """Проверка, что end_date >= start_date"""
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('end_date must be greater than or equal to start_date')
        return v
    
    @validator('name')
    def validate_name(cls, v):
        """Валидация названия"""
        if not v.strip():
            raise ValueError('name cannot be empty or whitespace')
        return v.strip()
    
    @validator('location')
    def validate_location(cls, v):
        """Валидация локации"""
        if not v.strip():
            raise ValueError('location cannot be empty or whitespace')
        return v.strip()
    
    class Config:
        use_enum_values = True


class TournamentCreate(TournamentBase):
    """Схема для создания турнира"""
    
    class Config:
        json_schema_extra = {
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
        }


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
    
    @validator('end_date')
    def validate_dates(cls, v, values):
        """Проверка дат при обновлении"""
        if v and 'start_date' in values and values['start_date']:
            if v < values['start_date']:
                raise ValueError('end_date must be greater than or equal to start_date')
        return v
    
    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "status": "Ongoing",
                "description": "Обновленное описание"
            }
        }


class TournamentResponse(TournamentBase):
    """Схема ответа с турниром"""
    id: int = Field(description="ID турнира")
    created_at: datetime = Field(description="Дата создания")
    updated_at: Optional[datetime] = Field(default=None, description="Дата обновления")
    average_rating: Optional[float] = Field(default=None, description="Средний рейтинг")
    favorites_count: Optional[int] = Field(default=None, description="Количество в избранном")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
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
    
    @validator('start_date_to')
    def validate_start_date_range(cls, v, values):
        """Валидация диапазона дат начала"""
        if v and 'start_date_from' in values and values['start_date_from']:
            if v < values['start_date_from']:
                raise ValueError('start_date_to must be >= start_date_from')
        return v
    
    @validator('end_date_to')
    def validate_end_date_range(cls, v, values):
        """Валидация диапазона дат окончания"""
        if v and 'end_date_from' in values and values['end_date_from']:
            if v < values['end_date_from']:
                raise ValueError('end_date_to must be >= end_date_from')
        return v
    
    class Config:
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "category": "National",
                "status": "Scheduled",
                "location": "Москва",
                "start_date_from": "2024-03-01T00:00:00",
                "start_date_to": "2024-12-31T23:59:59"
            }
        }


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
    
    class Config:
        json_schema_extra = {
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
        }


class TournamentRating(BaseModel):
    """Рейтинг турнира"""
    tournament_id: int = Field(description="ID турнира")
    rating: int = Field(ge=1, le=5, description="Рейтинг (1-5)")
    comment: Optional[str] = Field(default=None, max_length=500, description="Комментарий")
    
    class Config:
        json_schema_extra = {
            "example": {
                "tournament_id": 1,
                "rating": 5,
                "comment": "Отличный турнир!"
            }
        }


class TournamentSubscription(BaseModel):
    """Подписка на турнир"""
    tournament_id: int = Field(description="ID турнира")
    notify_before_days: int = Field(default=7, ge=1, le=30, description="За сколько дней уведомить")
    
    class Config:
        json_schema_extra = {
            "example": {
                "tournament_id": 1,
                "notify_before_days": 7
            }
        }
