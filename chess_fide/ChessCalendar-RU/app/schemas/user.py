"""
Pydantic схемы для пользователей
"""
from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Базовая схема пользователя"""
    username: str = Field(min_length=3, max_length=80, description="Имя пользователя")
    email: EmailStr = Field(description="Email адрес")
    
    @validator('username')
    def validate_username(cls, v):
        """Валидация username"""
        if not v.isalnum() and '_' not in v:
            raise ValueError('username must contain only alphanumeric characters and underscores')
        return v.lower()


class UserCreate(UserBase):
    """Схема для создания пользователя"""
    password: str = Field(min_length=8, max_length=128, description="Пароль")
    
    @validator('password')
    def validate_password(cls, v):
        """Валидация пароля"""
        if not any(c.isupper() for c in v):
            raise ValueError('password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('password must contain at least one digit')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password": "SecurePass123"
            }
        }


class UserUpdate(BaseModel):
    """Схема для обновления пользователя"""
    username: Optional[str] = Field(default=None, min_length=3, max_length=80)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    
    @validator('username')
    def validate_username(cls, v):
        """Валидация username"""
        if v and (not v.isalnum() and '_' not in v):
            raise ValueError('username must contain only alphanumeric characters and underscores')
        return v.lower() if v else v
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "newemail@example.com",
                "is_active": True
            }
        }


class UserResponse(UserBase):
    """Схема ответа с пользователем"""
    id: int = Field(description="ID пользователя")
    is_admin: bool = Field(description="Флаг администратора")
    is_active: bool = Field(description="Активен ли пользователь")
    created_at: datetime = Field(description="Дата создания")
    last_login: Optional[datetime] = Field(default=None, description="Последний вход")
    two_factor_enabled: bool = Field(default=False, description="Включен ли 2FA")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "johndoe",
                "email": "john@example.com",
                "is_admin": False,
                "is_active": True,
                "created_at": "2024-01-01T12:00:00",
                "last_login": "2024-02-16T10:30:00",
                "two_factor_enabled": False
            }
        }


class UserLogin(BaseModel):
    """Схема для входа"""
    username: str = Field(min_length=3, max_length=80, description="Имя пользователя")
    password: str = Field(min_length=1, description="Пароль")
    totp_code: Optional[str] = Field(default=None, min_length=6, max_length=6, description="2FA код")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "SecurePass123",
                "totp_code": "123456"
            }
        }


class UserPasswordChange(BaseModel):
    """Схема для смены пароля"""
    old_password: str = Field(min_length=1, description="Старый пароль")
    new_password: str = Field(min_length=8, max_length=128, description="Новый пароль")
    
    @validator('new_password')
    def validate_password(cls, v):
        """Валидация нового пароля"""
        if not any(c.isupper() for c in v):
            raise ValueError('password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('password must contain at least one digit')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "old_password": "OldPass123",
                "new_password": "NewSecurePass456"
            }
        }


class UserProfile(UserResponse):
    """Расширенный профиль пользователя"""
    favorites_count: int = Field(default=0, description="Количество избранных турниров")
    ratings_count: int = Field(default=0, description="Количество оценок")
    subscriptions_count: int = Field(default=0, description="Количество подписок")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "johndoe",
                "email": "john@example.com",
                "is_admin": False,
                "is_active": True,
                "created_at": "2024-01-01T12:00:00",
                "last_login": "2024-02-16T10:30:00",
                "two_factor_enabled": False,
                "favorites_count": 5,
                "ratings_count": 10,
                "subscriptions_count": 3
            }
        }


class UserPreferences(BaseModel):
    """Настройки пользователя"""
    email_notifications: bool = Field(default=True, description="Email уведомления")
    push_notifications: bool = Field(default=True, description="Push уведомления")
    newsletter: bool = Field(default=False, description="Подписка на рассылку")
    preferred_categories: Optional[list] = Field(default=None, description="Предпочитаемые категории")
    preferred_locations: Optional[list] = Field(default=None, description="Предпочитаемые локации")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email_notifications": True,
                "push_notifications": True,
                "newsletter": False,
                "preferred_categories": ["National", "FIDE"],
                "preferred_locations": ["Москва", "Санкт-Петербург"]
            }
        }


class TokenResponse(BaseModel):
    """Ответ с токенами"""
    access_token: str = Field(description="Access токен")
    refresh_token: str = Field(description="Refresh токен")
    token_type: str = Field(default="bearer", description="Тип токена")
    expires_in: int = Field(description="Время жизни токена в секундах")
    user: UserResponse = Field(description="Данные пользователя")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 3600,
                "user": {
                    "id": 1,
                    "username": "johndoe",
                    "email": "john@example.com",
                    "is_admin": False,
                    "is_active": True,
                    "created_at": "2024-01-01T12:00:00",
                    "last_login": "2024-02-16T10:30:00",
                    "two_factor_enabled": False
                }
            }
        }


class TwoFactorSetupResponse(BaseModel):
    """Ответ при настройке 2FA"""
    secret: str = Field(description="Секрет для 2FA")
    qr_code_url: str = Field(description="URL для QR кода")
    backup_codes: Optional[list] = Field(default=None, description="Резервные коды")
    
    class Config:
        json_schema_extra = {
            "example": {
                "secret": "JBSWY3DPEHPK3PXP",
                "qr_code_url": "otpauth://totp/ChessCalendar:johndoe?secret=JBSWY3DPEHPK3PXP&issuer=ChessCalendar",
                "backup_codes": ["ABCD1234", "EFGH5678", "IJKL9012"]
            }
        }


class TwoFactorVerify(BaseModel):
    """Схема для проверки 2FA"""
    totp_code: str = Field(min_length=6, max_length=6, description="TOTP код")
    
    class Config:
        json_schema_extra = {
            "example": {
                "totp_code": "123456"
            }
        }


class TwoFactorDisable(BaseModel):
    """Схема для отключения 2FA"""
    password: str = Field(min_length=1, description="Пароль")
    totp_code: str = Field(min_length=6, max_length=6, description="TOTP код")
    
    class Config:
        json_schema_extra = {
            "example": {
                "password": "SecurePass123",
                "totp_code": "123456"
            }
        }
