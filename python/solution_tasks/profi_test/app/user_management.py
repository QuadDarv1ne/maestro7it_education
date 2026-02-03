# -*- coding: utf-8 -*-
"""
Модуль расширенного управления пользователями для ПрофиТест
Предоставляет продвинутые возможности управления пользователями и правами доступа
"""
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Set, Any
import logging
from dataclasses import dataclass, field
from collections import defaultdict
import hashlib
import secrets


class UserRole(Enum):
    """Роли пользователей"""
    GUEST = 'guest'
    USER = 'user'
    PREMIUM_USER = 'premium_user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    SUPER_ADMIN = 'super_admin'


class Permission(Enum):
    """Права доступа"""
    # Базовые права
    VIEW_PROFILE = 'view_profile'
    EDIT_PROFILE = 'edit_profile'
    VIEW_TESTS = 'view_tests'
    TAKE_TESTS = 'take_tests'
    
    # Премиум права
    ACCESS_PREMIUM_FEATURES = 'access_premium_features'
    VIEW_DETAILED_ANALYTICS = 'view_detailed_analytics'
    EXPORT_DATA = 'export_data'
    
    # Модераторские права
    MODERATE_CONTENT = 'moderate_content'
    MANAGE_COMMENTS = 'manage_comments'
    VIEW_USER_ACTIVITY = 'view_user_activity'
    
    # Административные права
    MANAGE_USERS = 'manage_users'
    MANAGE_TESTS = 'manage_tests'
    VIEW_SYSTEM_LOGS = 'view_system_logs'
    CONFIGURE_SYSTEM = 'configure_system'
    
    # Супер-административные права
    FULL_ACCESS = 'full_access'
    MANAGE_ADMINISTRATORS = 'manage_administrators'
    SYSTEM_MAINTENANCE = 'system_maintenance'


@dataclass
class User:
    """Класс пользователя"""
    id: int
    username: str
    email: str
    role: UserRole
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True
    is_verified: bool = False
    permissions: Set[Permission] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)
    login_attempts: int = 0
    last_password_change: Optional[datetime] = None
    two_factor_enabled: bool = False
    profile_completion: float = 0.0


class RoleHierarchy:
    """Иерархия ролей для определения наследования прав"""
    
    # Определяем иерархию ролей (более высокая роль включает права более низкой)
    HIERARCHY = {
        UserRole.GUEST: 0,
        UserRole.USER: 1,
        UserRole.PREMIUM_USER: 2,
        UserRole.MODERATOR: 3,
        UserRole.ADMIN: 4,
        UserRole.SUPER_ADMIN: 5
    }
    
    @classmethod
    def get_role_level(cls, role: UserRole) -> int:
        """Получает уровень роли"""
        return cls.HIERARCHY.get(role, 0)
    
    @classmethod
    def role_has_permission(cls, role: UserRole, permission: Permission) -> bool:
        """Проверяет, имеет ли роль определенное право"""
        role_permissions = cls._get_role_permissions(role)
        return permission in role_permissions
    
    @classmethod
    def _get_role_permissions(cls, role: UserRole) -> Set[Permission]:
        """Получает все права для роли с учетом иерархии"""
        permissions = set()
        role_level = cls.get_role_level(role)
        
        # Добавляем права всех ролей с уровнем ниже или равным текущему
        for hierarchy_role, level in cls.HIERARCHY.items():
            if level <= role_level:
                permissions.update(cls._get_base_permissions(hierarchy_role))
        
        return permissions
    
    @classmethod
    def _get_base_permissions(cls, role: UserRole) -> Set[Permission]:
        """Получает базовые права для конкретной роли"""
        base_permissions = {
            UserRole.GUEST: {
                Permission.VIEW_TESTS
            },
            UserRole.USER: {
                Permission.VIEW_PROFILE,
                Permission.EDIT_PROFILE,
                Permission.VIEW_TESTS,
                Permission.TAKE_TESTS
            },
            UserRole.PREMIUM_USER: {
                Permission.ACCESS_PREMIUM_FEATURES,
                Permission.VIEW_DETAILED_ANALYTICS,
                Permission.EXPORT_DATA
            },
            UserRole.MODERATOR: {
                Permission.MODERATE_CONTENT,
                Permission.MANAGE_COMMENTS,
                Permission.VIEW_USER_ACTIVITY
            },
            UserRole.ADMIN: {
                Permission.MANAGE_USERS,
                Permission.MANAGE_TESTS,
                Permission.VIEW_SYSTEM_LOGS,
                Permission.CONFIGURE_SYSTEM
            },
            UserRole.SUPER_ADMIN: {
                Permission.FULL_ACCESS,
                Permission.MANAGE_ADMINISTRATORS,
                Permission.SYSTEM_MAINTENANCE
            }
        }
        
        return base_permissions.get(role, set())


class AdvancedUserManager:
    """
    Расширенный менеджер пользователей для системы ПрофиТест.
    Обеспечивает управление пользователями, ролями и правами доступа.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.users: Dict[int, User] = {}
        self.username_index: Dict[str, int] = {}
        self.email_index: Dict[str, int] = {}
        self.role_counts: Dict[UserRole, int] = defaultdict(int)
        self.inactive_users: Set[int] = set()
        self.suspended_users: Dict[int, datetime] = {}
        
        # Инициализация системного администратора
        self._create_system_admin()
    
    def _create_system_admin(self):
        """Создает системного администратора по умолчанию"""
        admin_user = User(
            id=1,
            username='admin',
            email='admin@profi-test.ru',
            role=UserRole.SUPER_ADMIN,
            created_at=datetime.now(),
            is_active=True,
            is_verified=True,
            permissions=RoleHierarchy._get_role_permissions(UserRole.SUPER_ADMIN)
        )
        self.add_user(admin_user)
    
    def add_user(self, user: User) -> bool:
        """
        Добавляет нового пользователя.
        
        Args:
            user: Объект пользователя
            
        Returns:
            bool: Успешность операции
        """
        try:
            if user.id in self.users:
                self.logger.warning(f"Пользователь с ID {user.id} уже существует")
                return False
            
            if user.username in self.username_index:
                self.logger.warning(f"Пользователь с именем {user.username} уже существует")
                return False
            
            if user.email in self.email_index:
                self.logger.warning(f"Пользователь с email {user.email} уже существует")
                return False
            
            # Устанавливаем права доступа на основе роли
            user.permissions = RoleHierarchy._get_role_permissions(user.role)
            
            # Добавляем пользователя
            self.users[user.id] = user
            self.username_index[user.username] = user.id
            self.email_index[user.email] = user.id
            self.role_counts[user.role] += 1
            
            self.logger.info(f"Пользователь {user.username} (ID: {user.id}) успешно добавлен")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при добавлении пользователя: {str(e)}")
            return False
    
    def get_user(self, user_id: int) -> Optional[User]:
        """
        Получает пользователя по ID.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            User: Объект пользователя или None
        """
        return self.users.get(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Получает пользователя по имени.
        
        Args:
            username: Имя пользователя
            
        Returns:
            User: Объект пользователя или None
        """
        user_id = self.username_index.get(username)
        return self.users.get(user_id) if user_id else None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Получает пользователя по email.
        
        Args:
            email: Email пользователя
            
        Returns:
            User: Объект пользователя или None
        """
        user_id = self.email_index.get(email)
        return self.users.get(user_id) if user_id else None
    
    def update_user(self, user_id: int, **kwargs) -> bool:
        """
        Обновляет информацию о пользователе.
        
        Args:
            user_id: ID пользователя
            **kwargs: Поля для обновления
            
        Returns:
            bool: Успешность операции
        """
        try:
            user = self.get_user(user_id)
            if not user:
                self.logger.warning(f"Пользователь с ID {user_id} не найден")
                return False
            
            # Обновляем поля
            for key, value in kwargs.items():
                if hasattr(user, key):
                    # Обработка специальных полей
                    if key == 'role':
                        # Обновляем права доступа при изменении роли
                        old_role = user.role
                        user.role = value
                        user.permissions = RoleHierarchy._get_role_permissions(value)
                        self.role_counts[old_role] -= 1
                        self.role_counts[value] += 1
                    elif key == 'username':
                        # Обновляем индекс имен
                        if value in self.username_index and self.username_index[value] != user_id:
                            self.logger.warning(f"Имя пользователя {value} уже занято")
                            return False
                        del self.username_index[user.username]
                        self.username_index[value] = user_id
                        user.username = value
                    elif key == 'email':
                        # Обновляем индекс email
                        if value in self.email_index and self.email_index[value] != user_id:
                            self.logger.warning(f"Email {value} уже занят")
                            return False
                        del self.email_index[user.email]
                        self.email_index[value] = user_id
                        user.email = value
                    else:
                        setattr(user, key, value)
            
            self.logger.info(f"Пользователь {user.username} (ID: {user_id}) успешно обновлен")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при обновлении пользователя: {str(e)}")
            return False
    
    def delete_user(self, user_id: int) -> bool:
        """
        Удаляет пользователя.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            bool: Успешность операции
        """
        try:
            user = self.get_user(user_id)
            if not user:
                self.logger.warning(f"Пользователь с ID {user_id} не найден")
                return False
            
            # Удаляем из всех индексов
            del self.users[user_id]
            del self.username_index[user.username]
            del self.email_index[user.email]
            self.role_counts[user.role] -= 1
            
            if user_id in self.inactive_users:
                self.inactive_users.remove(user_id)
            
            if user_id in self.suspended_users:
                del self.suspended_users[user_id]
            
            self.logger.info(f"Пользователь {user.username} (ID: {user_id}) успешно удален")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при удалении пользователя: {str(e)}")
            return False
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Аутентифицирует пользователя.
        
        Args:
            username: Имя пользователя
            password: Пароль
            
        Returns:
            User: Объект пользователя или None
        """
        try:
            user = self.get_user_by_username(username)
            if not user:
                self.logger.warning(f"Пользователь {username} не найден")
                return None
            
            if not user.is_active:
                self.logger.warning(f"Пользователь {username} неактивен")
                return None
            
            # Проверяем, не заблокирован ли пользователь
            if user_id in self.suspended_users:
                suspension_end = self.suspended_users[user_id]
                if datetime.now() < suspension_end:
                    self.logger.warning(f"Пользователь {username} заблокирован до {suspension_end}")
                    return None
                else:
                    # Снимаем блокировку
                    del self.suspended_users[user_id]
            
            # Здесь должна быть проверка пароля (в реальной системе)
            # Пока используем заглушку
            if password == "correct_password":  # Заглушка для демонстрации
                user.last_login = datetime.now()
                user.login_attempts = 0
                self.logger.info(f"Пользователь {username} успешно аутентифицирован")
                return user
            else:
                user.login_attempts += 1
                self.logger.warning(f"Неверный пароль для пользователя {username}")
                return None
                
        except Exception as e:
            self.logger.error(f"Ошибка при аутентификации пользователя: {str(e)}")
            return None
    
    def change_user_role(self, user_id: int, new_role: UserRole) -> bool:
        """
        Изменяет роль пользователя.
        
        Args:
            user_id: ID пользователя
            new_role: Новая роль
            
        Returns:
            bool: Успешность операции
        """
        return self.update_user(user_id, role=new_role)
    
    def suspend_user(self, user_id: int, duration_hours: int = 24) -> bool:
        """
        Блокирует пользователя на определенное время.
        
        Args:
            user_id: ID пользователя
            duration_hours: Длительность блокировки в часах
            
        Returns:
            bool: Успешность операции
        """
        try:
            user = self.get_user(user_id)
            if not user:
                return False
            
            suspension_end = datetime.now() + timedelta(hours=duration_hours)
            self.suspended_users[user_id] = suspension_end
            
            self.logger.info(f"Пользователь {user.username} заблокирован до {suspension_end}")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при блокировке пользователя: {str(e)}")
            return False
    
    def unsuspend_user(self, user_id: int) -> bool:
        """
        Снимает блокировку с пользователя.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            bool: Успешность операции
        """
        try:
            if user_id in self.suspended_users:
                user = self.get_user(user_id)
                del self.suspended_users[user_id]
                self.logger.info(f"Блокировка с пользователя {user.username} снята")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Ошибка при снятии блокировки: {str(e)}")
            return False
    
    def get_users_by_role(self, role: UserRole) -> List[User]:
        """
        Получает список пользователей по роли.
        
        Args:
            role: Роль
            
        Returns:
            list: Список пользователей
        """
        return [user for user in self.users.values() if user.role == role]
    
    def get_active_users(self, days: int = 30) -> List[User]:
        """
        Получает список активных пользователей.
        
        Args:
            days: Количество дней для определения активности
            
        Returns:
            list: Список активных пользователей
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        return [user for user in self.users.values() 
                if user.is_active and user.last_login and user.last_login >= cutoff_date]
    
    def get_inactive_users(self, days: int = 90) -> List[User]:
        """
        Получает список неактивных пользователей.
        
        Args:
            days: Количество дней для определения неактивности
            
        Returns:
            list: Список неактивных пользователей
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        inactive = []
        for user in self.users.values():
            if not user.is_active or not user.last_login or user.last_login < cutoff_date:
                inactive.append(user)
        return inactive
    
    def check_permission(self, user_id: int, permission: Permission) -> bool:
        """
        Проверяет, имеет ли пользователь определенное право.
        
        Args:
            user_id: ID пользователя
            permission: Право доступа
            
        Returns:
            bool: Имеет ли право
        """
        user = self.get_user(user_id)
        if not user or not user.is_active:
            return False
        
        return permission in user.permissions
    
    def get_user_permissions(self, user_id: int) -> Set[Permission]:
        """
        Получает все права пользователя.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            set: Множество прав пользователя
        """
        user = self.get_user(user_id)
        return user.permissions if user else set()
    
    def add_permission(self, user_id: int, permission: Permission) -> bool:
        """
        Добавляет право пользователю.
        
        Args:
            user_id: ID пользователя
            permission: Право доступа
            
        Returns:
            bool: Успешность операции
        """
        try:
            user = self.get_user(user_id)
            if not user:
                return False
            
            user.permissions.add(permission)
            self.logger.info(f"Право {permission.value} добавлено пользователю {user.username}")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при добавлении права: {str(e)}")
            return False
    
    def remove_permission(self, user_id: int, permission: Permission) -> bool:
        """
        Удаляет право у пользователя.
        
        Args:
            user_id: ID пользователя
            permission: Право доступа
            
        Returns:
            bool: Успешность операции
        """
        try:
            user = self.get_user(user_id)
            if not user:
                return False
            
            user.permissions.discard(permission)
            self.logger.info(f"Право {permission.value} удалено у пользователя {user.username}")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при удалении права: {str(e)}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Получает статистику по пользователям.
        
        Returns:
            dict: Статистика пользователей
        """
        total_users = len(self.users)
        active_users = len([u for u in self.users.values() if u.is_active])
        verified_users = len([u for u in self.users.values() if u.is_verified])
        
        role_distribution = dict(self.role_counts)
        
        recent_logins = len(self.get_active_users(7))  # За последнюю неделю
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'inactive_users': total_users - active_users,
            'verified_users': verified_users,
            'unverified_users': total_users - verified_users,
            'role_distribution': role_distribution,
            'recent_logins': recent_logins,
            'suspended_users': len(self.suspended_users),
            'system_admin_exists': self.get_user_by_username('admin') is not None
        }
    
    def generate_user_report(self, user_id: int) -> Dict[str, Any]:
        """
        Генерирует отчет по пользователю.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            dict: Отчет по пользователю
        """
        user = self.get_user(user_id)
        if not user:
            return {'error': 'Пользователь не найден'}
        
        return {
            'user_info': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role.value,
                'created_at': user.created_at.isoformat(),
                'last_login': user.last_login.isoformat() if user.last_login else None,
                'is_active': user.is_active,
                'is_verified': user.is_verified,
                'profile_completion': user.profile_completion
            },
            'permissions': [p.value for p in user.permissions],
            'activity_stats': {
                'login_attempts': user.login_attempts,
                'two_factor_enabled': user.two_factor_enabled,
                'last_password_change': user.last_password_change.isoformat() if user.last_password_change else None
            },
            'status': {
                'is_suspended': user_id in self.suspended_users,
                'suspension_end': self.suspended_users.get(user_id, None)
            }
        }
    
    def bulk_update_users(self, user_updates: List[Dict]) -> Dict[str, int]:
        """
        Массовое обновление пользователей.
        
        Args:
            user_updates: Список обновлений {user_id: int, updates: dict}
            
        Returns:
            dict: Статистика выполнения
        """
        results = {'success': 0, 'failed': 0, 'errors': []}
        
        for update in user_updates:
            user_id = update.get('user_id')
            updates = update.get('updates', {})
            
            if self.update_user(user_id, **updates):
                results['success'] += 1
            else:
                results['failed'] += 1
                results['errors'].append(f"Не удалось обновить пользователя {user_id}")
        
        return results


# Глобальный экземпляр менеджера пользователей
user_manager = AdvancedUserManager()