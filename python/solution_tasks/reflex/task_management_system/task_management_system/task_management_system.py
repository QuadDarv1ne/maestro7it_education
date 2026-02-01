"""Система управления задачами на основе Reflex 0.8.26."""

import reflex as rx
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum
from pydantic import BaseModel, Field
import json


class Priority(str, Enum):
    """Приоритеты задач."""
    LOW = "Low"
    NORMAL = "Normal"
    HIGH = "High"
    CRITICAL = "Critical"


class TaskStatus(str, Enum):
    """Статусы задач."""
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class Category(str, Enum):
    """Категории задач."""
    WORK = "Work"
    PERSONAL = "Personal"
    HEALTH = "Health"
    FINANCE = "Finance"
    EDUCATION = "Education"
    OTHER = "Other"


class Tag(BaseModel):
    """Модель тега."""
    id: int
    name: str
    color: str = "blue"  # Цвет тега
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


class Comment(BaseModel):
    """Модель комментария к задаче."""
    id: int
    task_id: int
    author: str
    content: str
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


class Task(BaseModel):
    """Модель задачи."""
    id: int
    title: str
    description: str = ""
    priority: str = Field(default=Priority.NORMAL)
    status: str = Field(default=TaskStatus.PENDING)
    due_date: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    assigned_to: str = ""
    updated_at: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    category: str = Field(default=Category.OTHER)
    
    # Dependency tracking
    dependencies: List[int] = []  # List of task IDs that this task depends on
    dependent_tasks: List[int] = []  # List of task IDs that depend on this task
    
    # Sub-task functionality
    parent_id: Optional[int] = None  # ID of parent task if this is a sub-task
    sub_tasks: List[int] = []  # List of sub-task IDs
    
    # Progress tracking for tasks with sub-tasks
    progress: int = 0  # 0-100% completion for sub-tasks
    
    # Comments functionality
    comments: List[int] = []  # List of comment IDs
    
    # Tags functionality
    tags: List[int] = []  # List of tag IDs

    class Config:
        arbitrary_types_allowed = True


class State(rx.State):
    """Состояние приложения управления задачами."""
    
    # User authentication
    current_user: str = "Гость"
    is_authenticated: bool = False
    show_login_dialog: bool = False
    login_username: str = ""
    login_password: str = ""
    
    # User management
    users: Dict[str, str] = {
        "admin": "admin123",
        "user1": "password1",
        "user2": "password2"
    }
    
    # Explicit setters to avoid deprecation warnings
    def set_new_task_title(self, value: str):
        self.new_task_title = value
    
    def set_new_task_description(self, value: str):
        self.new_task_description = value
    
    def set_new_task_priority(self, value: str):
        self.new_task_priority = value
    
    def set_new_task_category(self, value: str):
        self.new_task_category = value
    
    def set_new_task_due_date(self, value: str):
        self.new_task_due_date = value
    
    def set_new_task_assigned_to(self, value: str):
        self.new_task_assigned_to = value
    
    def set_edit_title(self, value: str):
        self.edit_title = value
    
    def set_edit_description(self, value: str):
        self.edit_description = value
    
    def set_edit_priority(self, value: str):
        self.edit_priority = value
    
    def set_edit_category(self, value: str):
        self.edit_category = value
    
    def set_edit_due_date(self, value: str):
        self.edit_due_date = value
    
    def set_edit_assigned_to(self, value: str):
        self.edit_assigned_to = value
    
    def set_show_edit_dialog(self, value: bool):
        self.show_edit_dialog = value
    
    def set_search_query(self, value: str):
        self.search_query = value
    
    def set_filter_status(self, value: str):
        self.filter_status = value
    
    def set_filter_priority(self, value: str):
        self.filter_priority = value
    
    def set_filter_category(self, value: str):
        self.filter_category = value
    
    def set_filter_assigned_to(self, value: str):
        self.filter_assigned_to = value
    
    def set_show_completed(self, value: bool):
        self.show_completed = value
    
    def set_filter_date_from(self, value: str):
        self.filter_date_from = value
    
    def set_filter_date_to(self, value: str):
        self.filter_date_to = value
    
    def set_filter_created_today(self, value: bool):
        self.filter_created_today = value
    
    def set_filter_due_today(self, value: bool):
        self.filter_due_today = value
    
    def set_filter_search_in_description(self, value: bool):
        self.filter_search_in_description = value
    
    def set_filter_search_in_assignee(self, value: bool):
        self.filter_search_in_assignee = value
    
    def set_filter_overdue_only(self, value: bool):
        self.filter_overdue_only = value
    
    def set_filter_completed_only(self, value: bool):
        self.filter_completed_only = value
    
    def set_sort_by(self, value: str):
        self.sort_by = value
    
    def set_search_in_description(self, value: bool):
        self.search_in_description = value
    
    def set_search_in_comments(self, value: bool):
        self.search_in_comments = value
    
    def set_search_in_subtasks(self, value: bool):
        self.search_in_subtasks = value
    
    def set_search_exact_match(self, value: bool):
        self.search_exact_match = value
    
    def set_show_notifications(self, value: bool):
        self.show_notifications = value
    
    def set_theme(self, value: str):
        self.theme = value
    
    def toggle_theme(self):
        """Переключить тему между светлой и темной."""
        self.theme = "dark" if self.theme == "light" else "light"
        rx.set_local_storage("theme", self.theme)
        self.add_notification(f"🎨 Тема изменена на: {self.theme}", "info")
    
    def set_virtual_scroll_enabled(self, value: bool):
        self.virtual_scroll_enabled = value
    
    def set_items_per_page(self, value: int):
        self.items_per_page = value
    
    def set_current_page(self, value: int):
        self.current_page = value
    
    def set_search_debounce_time(self, value: float):
        self.search_debounce_time = value
    
    def set_search_debounce_time_str(self, value: str):
        """Установить задержку поиска из строки."""
        try:
            self.search_debounce_time = float(value) if value else 0.3
        except ValueError:
            self.search_debounce_time = 0.3
    
    # Methods for comments functionality
    def set_show_comments(self, value: bool):
        self.show_comments = value
    
    def set_selected_task_for_comments(self, value: Optional[int]):
        self.selected_task_for_comments = value
    
    def set_new_comment_content(self, value: str):
        self.new_comment_content = value
    
    def set_editing_comment_id(self, value: Optional[int]):
        self.editing_comment_id = value
    
    def set_edit_comment_content(self, value: str):
        self.edit_comment_content = value
    
    # Methods for tags functionality
    def set_show_tags(self, value: bool):
        self.show_tags = value
    
    def set_selected_task_for_tags(self, value: Optional[int]):
        self.selected_task_for_tags = value
    
    def set_new_tag_name(self, value: str):
        self.new_tag_name = value
    
    def set_new_tag_color(self, value: str):
        self.new_tag_color = value
    
    def save_to_local_storage(self):
        """Автоматическое сохранение всех данных в localStorage."""
        self.saving = True
        try:
            # Сохраняем задачи
            self.tasks_json = json.dumps(
                [task.model_dump(mode='json') for task in self.tasks],
                ensure_ascii=False,
                default=str
            )
            
            # Сохраняем комментарии
            self.comments_json = json.dumps(
                [c.model_dump(mode='json') for c in self.comments],
                ensure_ascii=False,
                default=str
            )
            
            # Сохраняем теги
            self.tags_json = json.dumps(
                [t.model_dump(mode='json') for t in self.tags],
                ensure_ascii=False,
                default=str
            )
        except Exception as e:
            print(f"Error saving to localStorage: {e}")
        finally:
            self.saving = False
    
    # Удален дублирующий метод save_tasks
    # def save_tasks(self): pass
    
    @rx.event
    def load_from_storage(self, data: str):
        """Загрузить задачи из localStorage."""
        if not data:
            return
        try:
            tasks_data = json.loads(data)
            self.tasks = [Task(**t) for t in tasks_data]
            self.task_counter = max((t["id"] for t in tasks_data), default=0) + 1
        except:
            self.tasks = []
            self.task_counter = 0
    
    @rx.event
    def set_tasks_from_json(self, json_str: str):
        """Загрузить задачи из JSON строки."""
        if not json_str:
            return
        try:
            data = json.loads(json_str)
            self.tasks = [Task(**t) for t in data]
            self.task_counter = max((t.get("id", 0) for t in data), default=0) + 1
        except:
            self.tasks = []
    
    @rx.event
    def set_comments_from_json(self, json_str: str):
        """Загрузить комментарии из JSON строки."""
        if not json_str:
            return
        try:
            self.comments = [Comment(**c) for c in json.loads(json_str)]
        except:
            self.comments = []
    
    @rx.event
    def set_tags_from_json(self, json_str: str):
        """Загрузить теги из JSON строки."""
        if not json_str:
            return
        try:
            self.tags = [Tag(**t) for t in json.loads(json_str)]
        except:
            self.tags = []
    
    def get_task_comments(self, task_id: int) -> List[Comment]:
        """Получить комментарии для задачи."""
        task = next((t for t in self.tasks if t.id == task_id), None)
        if not task:
            return []
        return [c for c in self.comments if c.id in task.comments]
    
    def add_comment(self):
        """Добавить комментарий к задаче."""
        if not self.new_comment_content.strip() or not self.selected_task_for_comments:
            return
        
        comment_id = max([c.id for c in self.comments], default=0) + 1
        new_comment = Comment(
            id=comment_id,
            task_id=self.selected_task_for_comments,
            author=self.current_user,
            content=self.new_comment_content.strip()
        )
        
        self.comments.append(new_comment)
        
        # Добавляем ID комментария в задачу
        task = next((t for t in self.tasks if t.id == self.selected_task_for_comments), None)
        if task:
            task.comments.append(comment_id)
            task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.new_comment_content = ""
        self.add_notification("Комментарий добавлен", "success")
        self.save_all_data()
    
    def start_edit_comment(self, comment_id: int):
        """Начать редактирование комментария."""
        comment = next((c for c in self.comments if c.id == comment_id), None)
        if comment:
            self.editing_comment_id = comment_id
            self.edit_comment_content = comment.content
    
    def save_comment_edit(self):
        """Сохранить изменения в комментарии."""
        if not self.editing_comment_id or not self.edit_comment_content.strip():
            return
        
        comment = next((c for c in self.comments if c.id == self.editing_comment_id), None)
        if comment:
            comment.content = self.edit_comment_content.strip()
            comment.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Обновляем дату обновления задачи
            task = next((t for t in self.tasks if t.id == comment.task_id), None)
            if task:
                task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.editing_comment_id = None
        self.edit_comment_content = ""
        self.add_notification("Комментарий обновлен", "success")
        self.save_all_data()
    
    def delete_comment(self, comment_id: int):
        """Удалить комментарий."""
        comment = next((c for c in self.comments if c.id == comment_id), None)
        if not comment:
            return
        
        # Удаляем комментарий из списка
        self.comments = [c for c in self.comments if c.id != comment_id]
        
        # Удаляем ID комментария из задачи
        task = next((t for t in self.tasks if t.id == comment.task_id), None)
        if task:
            task.comments = [c_id for c_id in task.comments if c_id != comment_id]
            task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.add_notification("Комментарий удален", "success")
        self.save_all_data()
    
    def cancel_comment_edit(self):
        """Отменить редактирование комментария."""
        self.editing_comment_id = None
        self.edit_comment_content = ""
    
    def open_comments(self, task_id: int):
        """Открыть панель комментариев для задачи."""
        self.selected_task_for_comments = task_id
        self.show_comments = True
    
    def close_comments(self):
        """Закрыть панель комментариев."""
        self.show_comments = False
        self.selected_task_for_comments = None
        self.new_comment_content = ""
        self.editing_comment_id = None
        self.edit_comment_content = ""
    
    def get_task_tags(self, task_id: int) -> List[Tag]:
        """Получить теги для задачи."""
        task = next((t for t in self.tasks if t.id == task_id), None)
        if not task:
            return []
        return [tag for tag in self.tags if tag.id in task.tags]
    
    def add_tag(self):
        """Добавить новый тег."""
        if not self.new_tag_name.strip():
            return
        
        # Проверяем, существует ли уже такой тег
        existing_tag = next((t for t in self.tags if t.name.lower() == self.new_tag_name.strip().lower()), None)
        if existing_tag:
            self.add_notification("Тег с таким именем уже существует", "error")
            return
        
        tag_id = max([t.id for t in self.tags], default=0) + 1
        new_tag = Tag(
            id=tag_id,
            name=self.new_tag_name.strip(),
            color=self.new_tag_color
        )
        
        self.tags.append(new_tag)
        self.new_tag_name = ""
        self.add_notification("Тег добавлен", "success")
        self.save_all_data()
    
    def add_tag_to_task(self, tag_id: int):
        """Добавить тег к задаче."""
        if not self.selected_task_for_tags:
            return
        
        task = next((t for t in self.tasks if t.id == self.selected_task_for_tags), None)
        if not task:
            return
        
        if tag_id not in task.tags:
            task.tags.append(tag_id)
            task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.add_notification("Тег добавлен к задаче", "success")
            self.save_all_data()
    
    def remove_tag_from_task(self, tag_id: int):
        """Удалить тег из задачи."""
        if not self.selected_task_for_tags:
            return
        
        task = next((t for t in self.tasks if t.id == self.selected_task_for_tags), None)
        if not task:
            return
        
        task.tags = [t_id for t_id in task.tags if t_id != tag_id]
        task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.add_notification("Тег удален из задачи", "success")
        self.save_all_data()
    
    def delete_tag(self, tag_id: int):
        """Удалить тег полностью."""
        # Удаляем тег из всех задач
        for task in self.tasks:
            if tag_id in task.tags:
                task.tags = [t_id for t_id in task.tags if t_id != tag_id]
                task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Удаляем тег из списка
        self.tags = [t for t in self.tags if t.id != tag_id]
        self.add_notification("Тег удален", "success")
        self.save_all_data()
    
    def open_tags(self, task_id: int):
        """Открыть панель тегов для задачи."""
        self.selected_task_for_tags = task_id
        self.show_tags = True
    
    def close_tags(self):
        """Закрыть панель тегов."""
        self.show_tags = False
        self.selected_task_for_tags = None
        self.new_tag_name = ""
        self.new_tag_color = "blue"
    
    def set_items_per_page_str(self, value: str):
        """Установить количество задач на странице из строки."""
        try:
            self.items_per_page = int(value) if value else 20
        except ValueError:
            self.items_per_page = 20
    
    def get_paginated_tasks(self) -> List[Task]:
        """Получить задачи для текущей страницы."""
        if not self.virtual_scroll_enabled:
            return self.filtered_tasks
        
        start_idx = self.current_page * self.items_per_page
        end_idx = start_idx + self.items_per_page
        return self.filtered_tasks[start_idx:end_idx]
    
    def get_total_pages(self) -> int:
        """Получить общее количество страниц."""
        if not self.virtual_scroll_enabled:
            return 1
        return max(1, (len(self.filtered_tasks) + self.items_per_page - 1) // self.items_per_page)
    
    def get_filtered_tasks_count(self) -> int:
        """Получить количество отфильтрованных задач."""
        return len(self.filtered_tasks)
    
    def needs_pagination(self) -> bool:
        """Проверить, нужна ли пагинация."""
        return self.virtual_scroll_enabled and self.get_total_pages() > 1
    
    def is_last_page(self) -> rx.Var[bool]:
        """Проверить, является ли текущая страница последней."""
        return self.current_page == self.get_total_pages() - 1
    
    def go_to_page(self, page: int):
        """Перейти к указанной странице."""
        if 0 <= page < self.get_total_pages():
            self.current_page = page
    
    def go_to_next_page(self):
        """Перейти к следующей странице."""
        if self.current_page < self.get_total_pages() - 1:
            self.current_page += 1
    
    def go_to_previous_page(self):
        """Перейти к предыдущей странице."""
        if self.current_page > 0:
            self.current_page -= 1
    
    def add_notification(self, message: str, notification_type: str = "info"):
        """Добавить уведомление."""
        notification = {
            "id": str(datetime.now().timestamp()),
            "message": message,
            "type": notification_type,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "read": False
        }
        self.notifications = [notification] + self.notifications
        
        # Ограничиваем количество уведомлений
        if len(self.notifications) > 10:
            self.notifications = self.notifications[:10]
    
    def remove_notification(self, notification_id: str):
        """Удалить уведомление."""
        self.notifications = [
            n for n in self.notifications 
            if n["id"] != notification_id
        ]
    
    def mark_notification_as_read(self, notification_id: str):
        """Пометить уведомление как прочитанное."""
        for notification in self.notifications:
            if notification["id"] == notification_id:
                notification["read"] = True
                break
    
    def clear_all_notifications(self):
        """Очистить все уведомления."""
        self.notifications = []
    
    def check_task_notifications(self):
        """Проверить задачи и создать соответствующие уведомления."""
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        
        for task in self.tasks:
            if not task.due_date:
                continue
                
            try:
                due_date = datetime.strptime(task.due_date, "%Y-%m-%d").date()
                
                # Уведомление о просроченных задачах
                if due_date < today and task.status not in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]:
                    self.add_notification(
                        f"⚠️ Задача просрочена: {task.title}",
                        "error"
                    )
                
                # Уведомление о задачах на завтра
                elif due_date == tomorrow and task.status not in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]:
                    self.add_notification(
                        f"📅 Задача на завтра: {task.title}",
                        "warning"
                    )
                
                # Уведомление о задачах, назначенных пользователю
                elif task.assigned_to == self.current_user and task.status == TaskStatus.PENDING:
                    self.add_notification(
                        f"📌 Новая задача назначена: {task.title}",
                        "info"
                    )
                    
            except ValueError:
                continue
    
    # User authentication methods
    def set_login_username(self, value: str):
        self.login_username = value
    
    def set_login_password(self, value: str):
        self.login_password = value
    
    def set_show_login_dialog(self, value: bool):
        self.show_login_dialog = value
    
    def login(self):
        if self.login_username in self.users and self.users[self.login_username] == self.login_password:
            self.current_user = self.login_username
            self.is_authenticated = True
            self.show_login_dialog = False
            rx.set_cookie("current_user", self.login_username, path="/")
            self.login_username = ""
            self.login_password = ""

            # Полная очистка старого состояния
            self.tasks = []
            self.comments = []
            self.tags = []
            self.task_counter = 0

            # Даём JavaScript время обновить *_json поля
            # Это самый простой и надёжный способ в Reflex 0.8.x без кастомного event bridge
            rx.call_script("""
                setTimeout(() => {
                    let user = localStorage.getItem("current_user") || "guest";
                    let tasks = localStorage.getItem("tasks_" + user);
                    let comments = localStorage.getItem("comments_" + user);
                    let tags = localStorage.getItem("tags_" + user);
                    
                    if (tasks)    Reflex.setState({ tasks_json: tasks });
                    if (comments) Reflex.setState({ comments_json: comments });
                    if (tags)     Reflex.setState({ tags_json: tags });
                    
                    // Вызываем парсинг сразу после установки
                    Reflex.callMethod("State.set_tasks_from_json", [tasks || ""]);
                    Reflex.callMethod("State.set_comments_from_json", [comments || ""]);
                    Reflex.callMethod("State.set_tags_from_json", [tags || ""]);
                }, 150);
            """)

            self.add_notification(f"Добро пожаловать, {self.current_user}!", "success")
        else:
            self.add_notification("Неверное имя пользователя или пароль", "error")
    
    def load_user_data(self):
        """Загрузка данных пользователя - будет вызвана из JavaScript."""
        # Этот метод будет вызван из JavaScript
        pass
    
    def watch_storage(self):
        """Периодическая проверка и загрузка данных из localStorage."""
        # Можно вызывать периодически или по событию
        self.set_tasks_from_json(self.tasks_json)
        self.set_comments_from_json(self.comments_json)
        self.set_tags_from_json(self.tags_json)
    
    def hide_context_menu(self):
        """Скрыть контекстное меню."""
        self.show_context_menu = False
        self.context_menu_task_id = 0
    
    def logout(self):
        """User logout."""
        # Save current user's tasks
        self.save_to_local_storage()
        self.current_user = "Гость"
        self.is_authenticated = False
        self.tasks = []
        self.task_counter = 0
    
    def load_user_tasks(self):
        """Load tasks for current user."""
        try:
            # Используем клиентский скрипт для загрузки из localStorage
            pass  # Загрузка будет происходить через клиентский JavaScript
        except Exception as e:
            print(f"Error loading user tasks: {e}")
            self.tasks = []
            self.task_counter = 0
    
    def save_user_tasks(self):
        """Save tasks for current user."""
        try:
            # Сохраняем в состояние для доступа из JavaScript
            self.tasks_json = json.dumps([task.dict() for task in self.tasks])
        except Exception as e:
            print(f"Error saving user tasks: {e}")
    
    # Список задач
    tasks: List[Task] = []
    
    # Список комментариев
    comments: List[Comment] = []
    
    # Список тегов
    tags: List[Tag] = []
    
    # Список членов команды
    team_members: List[str] = ["Алексей", "Мария", "Иван", "Елена", "Дмитрий", "Ольга", "Сергей", "Анна"]
    
    # Поля для новой задачи
    new_task_title: str = ""
    new_task_description: str = ""
    new_task_priority: str = Priority.NORMAL
    new_task_category: str = Category.WORK
    new_task_due_date: str = ""
    new_task_assigned_to: str = ""
    
    # Поля для редактирования
    editing_task_id: Optional[int] = None
    edit_title: str = ""
    edit_description: str = ""
    edit_priority: str = Priority.NORMAL
    edit_category: str = Category.WORK
    edit_due_date: str = ""
    edit_assigned_to: str = ""
    show_edit_dialog: bool = False
    
    # Поля для фильтрации и сортировки
    filter_status: str = "All"
    filter_priority: str = "All"
    filter_category: str = "All"
    filter_assigned_to: str = "All"
    search_query: str = ""
    sort_by: str = "created_at"
    sort_ascending: bool = False
    
    # Расширенный поиск
    search_in_description: bool = True
    search_in_comments: bool = False
    search_in_subtasks: bool = False
    search_exact_match: bool = False
    
    # Расширенные фильтры
    filter_date_from: str = ""
    filter_date_to: str = ""
    filter_created_today: bool = False
    filter_due_today: bool = False
    filter_search_in_description: bool = True
    filter_search_in_assignee: bool = True
    filter_overdue_only: bool = False
    filter_completed_only: bool = False
    
    # Счетчик для генерации ID
    task_counter: int = 0
    
    # UI состояние
    show_completed: bool = True
    is_loading: bool = False
    
    # Для работы с localStorage через JavaScript
    tasks_json: str = ""
    comments_json: str = ""
    tags_json: str = ""
    
    # Упрощенная система сохранения
    user_prefix: str = "guest"
    
    def get_storage_key(self, entity: str) -> str:
        return f"{entity}_{self.current_user if self.is_authenticated else 'guest'}"
    
    def save_all_data(self):
        if not self.is_authenticated:
            return
            
        rx.call_script(f"""
            localStorage.setItem('{self.get_storage_key("tasks")}', {json.dumps([t.model_dump() for t in self.tasks])});
            localStorage.setItem('{self.get_storage_key("comments")}', {json.dumps([c.model_dump() for c in self.comments])});
            localStorage.setItem('{self.get_storage_key("tags")}', {json.dumps([t.model_dump() for t in self.tags])});
        """)
    
    # Индикатор сохранения
    saving: bool = False
    
    # Для контекстного меню
    show_context_menu: bool = False
    context_menu_task_id: Optional[int] = None
    context_menu_position: Dict[str, int] = {"x": 0, "y": 0}
    
    # Тема приложения
    theme: str = "light"  # "light" или "dark"
    
    # Оптимизация производительности
    virtual_scroll_enabled: bool = True
    items_per_page: int = 20
    current_page: int = 0
    search_debounce_time: float = 0.3  # секунды
    
    # Система уведомлений
    notifications: List[Dict[str, str]] = []
    show_notifications: bool = True
    notification_message: str = ""
    
    # Bulk operations
    selected_tasks: List[int] = []
    show_bulk_actions: bool = False
    
    # Calendar view
    show_calendar: bool = False
    calendar_current_date: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    calendar_view_type: str = "month"  # month, week, day
    
    # Task dependencies and sub-tasks
    show_dependencies: bool = False
    selected_dependency_task: Optional[int] = None
    show_subtasks: bool = False
    selected_parent_task: Optional[int] = None
    
    # Comments functionality
    show_comments: bool = False
    selected_task_for_comments: Optional[int] = None
    new_comment_content: str = ""
    editing_comment_id: Optional[int] = None
    edit_comment_content: str = ""
    
    # Tags functionality
    show_tags: bool = False
    selected_task_for_tags: Optional[int] = None
    new_tag_name: str = ""
    new_tag_color: str = "blue"
    available_tag_colors: List[str] = ["blue", "green", "red", "yellow", "purple", "orange", "pink", "gray"]
    
    def load_tasks(self):
        """Загрузить задачи из локального хранилища."""
        self.load_user_tasks()
        # Проверяем уведомления
        self.check_task_notifications()
    
    # Удален дублирующий метод save_tasks
    # def save_tasks(self): pass
    
    def on_load(self):
        """Вызывается при загрузке приложения."""
        self.load_tasks()
        self.check_overdue_tasks()
    
    @rx.event
    def export_tasks_csv(self):
        """Экспортировать задачи в CSV."""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(["ID", "Title", "Description", "Priority", "Status", "Due Date", "Created At", "Assigned To", "Category"])
        
        # Write tasks
        for task in self.tasks:
            writer.writerow([
                task.id,
                task.title,
                task.description,
                task.priority,
                task.status,
                task.due_date,
                task.created_at,
                task.assigned_to,
                task.category
            ])
        
        csv_content = output.getvalue()
        output.close()
        
        # Return the CSV as a downloadable file
        return rx.download(data=csv_content.encode('utf-8'), filename=f"tasks_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    
    @rx.event
    def export_filtered_tasks_csv(self):
        """Экспортировать отфильтрованные задачи в CSV."""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(["ID", "Title", "Description", "Priority", "Status", "Due Date", "Created At", "Assigned To", "Category"])
        
        # Write filtered tasks
        for task in self.filtered_tasks:
            writer.writerow([
                task.id,
                task.title,
                task.description,
                task.priority,
                task.status,
                task.due_date,
                task.created_at,
                task.assigned_to,
                task.category
            ])
        
        csv_content = output.getvalue()
        output.close()
        
        # Return the CSV as a downloadable file
        return rx.download(data=csv_content.encode('utf-8'), filename=f"filtered_tasks_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    
    @rx.event
    def export_tasks_json(self):
        """Экспортировать задачи в JSON."""
        import json
        
        tasks_data = []
        for task in self.tasks:
            task_dict = task.dict()
            tasks_data.append(task_dict)
        
        json_content = json.dumps(tasks_data, indent=2, ensure_ascii=False)
        
        # Return the JSON as a downloadable file
        return rx.download(data=json_content.encode('utf-8'), filename=f"tasks_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    
    @rx.event
    def export_filtered_tasks_json(self):
        """Экспортировать отфильтрованные задачи в JSON."""
        import json
        
        tasks_data = []
        for task in self.filtered_tasks:
            task_dict = task.dict()
            tasks_data.append(task_dict)
        
        json_content = json.dumps(tasks_data, indent=2, ensure_ascii=False)
        
        # Return the JSON as a downloadable file
        return rx.download(data=json_content.encode('utf-8'), filename=f"filtered_tasks_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    
    def advanced_search_matches(self, task: Task, query: str) -> bool:
        """Проверить совпадение задачи с расширенным поиском."""
        if not query:
            return True
            
        query_lower = query.lower()
        search_fields = []
        
        # Поиск в заголовке
        search_fields.append(task.title.lower())
        
        # Поиск в описании (если включено)
        if self.search_in_description and task.description:
            search_fields.append(task.description.lower())
        
        # Поиск в исполнителе (если включено)
        if self.filter_search_in_assignee and task.assigned_to:
            search_fields.append(task.assigned_to.lower())
        
        # Поиск в категории
        search_fields.append(task.category.lower())
        
        search_text = " ".join(search_fields)
        
        if self.search_exact_match:
            return query_lower in search_text
        else:
            # Частичное совпадение
            return any(word in search_text for word in query_lower.split())
    
    @rx.var
    def filtered_tasks(self) -> List[Task]:
        """Получить отфильтрованные и отсортированные задачи."""
        result = self.tasks
        
        # Расширенный поиск
        if self.search_query.strip():
            result = [
                task for task in result 
                if self.advanced_search_matches(task, self.search_query)
            ]
        
        # Базовые фильтры
        if self.filter_status != "All":
            result = [task for task in result if task.status == self.filter_status]
        
        if self.filter_priority != "All":
            result = [task for task in result if task.priority == self.filter_priority]
        
        if self.filter_category != "All":
            result = [task for task in result if task.category == self.filter_category]
        
        if self.filter_assigned_to != "All":
            result = [task for task in result if task.assigned_to == self.filter_assigned_to]
        
        # Расширенные фильтры по датам
        today = datetime.now().strftime("%Y-%m-%d")
        
        if self.filter_date_from:
            from_date = datetime.strptime(self.filter_date_from, "%Y-%m-%d")
            result = [
                task for task in result 
                if datetime.strptime(task.created_at.split()[0], "%Y-%m-%d") >= from_date
            ]
        
        if self.filter_date_to:
            to_date = datetime.strptime(self.filter_date_to, "%Y-%m-%d")
            result = [
                task for task in result 
                if datetime.strptime(task.created_at.split()[0], "%Y-%m-%d") <= to_date
            ]
        
        if self.filter_created_today:
            result = [
                task for task in result 
                if task.created_at.split()[0] == today
            ]
        
        if self.filter_due_today:
            result = [task for task in result if task.due_date == today]
        
        if self.filter_overdue_only:
            result = [
                task for task in result
                if task.due_date and task.due_date < today
                and task.status not in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]
            ]
        
        if self.filter_completed_only:
            result = [task for task in result if task.status == TaskStatus.COMPLETED]
        
        if not self.show_completed and not self.filter_completed_only:
            result = [task for task in result if task.status != TaskStatus.COMPLETED]
        
        # Сортировка
        if self.sort_by == "priority":
            priority_order = {Priority.CRITICAL: 0, Priority.HIGH: 1, Priority.NORMAL: 2, Priority.LOW: 3}
            result.sort(key=lambda t: priority_order.get(t.priority, 4), reverse=not self.sort_ascending)
        elif self.sort_by == "due_date":
            def due_key(t):
                if not t.due_date:
                    return datetime.max if self.sort_ascending else datetime.min
                return datetime.strptime(t.due_date, "%Y-%m-%d")
            result.sort(key=due_key, reverse=not self.sort_ascending)
        elif self.sort_by == "title":
            result.sort(key=lambda t: t.title.lower(), reverse=not self.sort_ascending)
        elif self.sort_by == "status":
            result.sort(key=lambda t: t.status, reverse=not self.sort_ascending)
        elif self.sort_by == "category":
            result.sort(key=lambda t: t.category.lower(), reverse=not self.sort_ascending)
        elif self.sort_by == "assigned_to":
            result.sort(key=lambda t: t.assigned_to.lower(), reverse=not self.sort_ascending)
        else:
            result.sort(key=lambda t: t.created_at, reverse=not self.sort_ascending)
            
        return result
    
    @rx.var
    def task_stats(self) -> Dict[str, int]:
        """Получить статистику по задачам."""
        today = datetime.now().strftime("%Y-%m-%d")
        return {
            "total": len(self.tasks),
            "pending": sum(1 for t in self.tasks if t.status == TaskStatus.PENDING),
            "in_progress": sum(1 for t in self.tasks if t.status == TaskStatus.IN_PROGRESS),
            "completed": sum(1 for t in self.tasks if t.status == TaskStatus.COMPLETED),
            "cancelled": sum(1 for t in self.tasks if t.status == TaskStatus.CANCELLED),
            "overdue": sum(1 for t in self.tasks 
                          if t.due_date and t.due_date < today
                          and t.status not in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]),
            "work": sum(1 for t in self.tasks if t.category == Category.WORK),
            "personal": sum(1 for t in self.tasks if t.category == Category.PERSONAL),
            "health": sum(1 for t in self.tasks if t.category == Category.HEALTH),
            "finance": sum(1 for t in self.tasks if t.category == Category.FINANCE),
            "education": sum(1 for t in self.tasks if t.category == Category.EDUCATION),
            "other": sum(1 for t in self.tasks if t.category == Category.OTHER)
        }
    
    @rx.var
    def productivity_stats(self) -> Dict[str, str]:
        """Получить статистику продуктивности."""
        if not self.tasks:
            return {
                "completion_rate": "0",
                "avg_completion_time": "0",
                "tasks_per_day": "0",
                "most_productive_day": "Нет данных",
                "busiest_category": "Нет данных"
            }
        
        # Completion rate
        completed_tasks = sum(1 for t in self.tasks if t.status == TaskStatus.COMPLETED)
        completion_rate = (completed_tasks / len(self.tasks)) * 100 if self.tasks else 0
        
        # Average completion time
        completed_with_dates = [
            t for t in self.tasks 
            if t.status == TaskStatus.COMPLETED and t.created_at and t.updated_at
        ]
        avg_completion_time = 0
        if completed_with_dates:
            # This is a simplified calculation
            avg_completion_time = len(completed_with_dates)  # Just count for now
        
        # Tasks per day (simplified)
        tasks_per_day = len(self.tasks) / max(1, 7)  # Assume 7 days for demo
        
        # Most productive day and category (simplified)
        most_productive_day = "Сегодня"
        category_counts = {}
        for task in self.tasks:
            category_counts[task.category] = category_counts.get(task.category, 0) + 1
        busiest_category = max(category_counts, key=category_counts.get) if category_counts else "Нет данных"
        
        return {
            "completion_rate": str(round(completion_rate, 1)),
            "avg_completion_time": str(avg_completion_time),
            "tasks_per_day": str(round(tasks_per_day, 1)),
            "most_productive_day": most_productive_day,
            "busiest_category": busiest_category
        }
    
    def add_task(self):
        """Добавить новую задачу."""
        if not self.new_task_title.strip():
            return
            
        task = Task(
            id=self.task_counter,
            title=self.new_task_title.strip(),
            description=self.new_task_description.strip(),
            priority=self.new_task_priority,
            category=self.new_task_category,
            due_date=self.new_task_due_date if self.new_task_due_date else None,
            assigned_to=self.new_task_assigned_to.strip()
        )
        
        self.tasks.append(task)
        self.task_counter += 1
        self.clear_form()
        self.save_to_local_storage()
        
        # Добавляем уведомление
        self.add_notification(f"✅ Задача создана: {task.title}", "success")
        self.save_to_local_storage()
    
    def clear_form(self):
        """Очистить форму добавления задачи."""
        self.new_task_title = ""
        self.new_task_description = ""
        self.new_task_priority = Priority.NORMAL
        self.new_task_due_date = ""
        self.new_task_assigned_to = ""
    
    def delete_task(self, task_id: int):
        """Удалить задачу по ID."""
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.save_to_local_storage()
        self.save_to_local_storage()
    
    def update_task_status(self, task_id: int, new_status: str):
        """Обновить статус задачи."""
        for task in self.tasks:
            if task.id == task_id:
                task.status = new_status
                task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break
        self.save_to_local_storage()
        self.save_to_local_storage()
    
    def toggle_task_completion(self, task_id: int):
        """Переключить статус выполнения задачи."""
        for task in self.tasks:
            if task.id == task_id:
                task.status = TaskStatus.COMPLETED if task.status != TaskStatus.COMPLETED else TaskStatus.PENDING
                task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break
        self.save_to_local_storage()
        self.save_to_local_storage()
    
    def open_edit_dialog(self, task_id: int):
        """Открыть диалог редактирования."""
        for task in self.tasks:
            if task.id == task_id:
                self.editing_task_id = task_id
                self.edit_title = task.title
                self.edit_description = task.description
                self.edit_priority = task.priority
                self.edit_due_date = task.due_date or ""
                self.edit_assigned_to = task.assigned_to
                self.show_edit_dialog = True
                break
    
    def close_edit_dialog(self):
        """Закрыть диалог редактирования."""
        self.show_edit_dialog = False
        self.editing_task_id = None
    
    def save_edit(self):
        """Сохранить изменения задачи."""
        if self.editing_task_id is None:
            return
            
        for task in self.tasks:
            if task.id == self.editing_task_id:
                task.title = self.edit_title.strip()
                task.description = self.edit_description.strip()
                task.priority = self.edit_priority
                task.category = self.edit_category
                task.due_date = self.edit_due_date if self.edit_due_date else None
                task.assigned_to = self.edit_assigned_to.strip()
                task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break
        
        self.close_edit_dialog()
        self.save_to_local_storage()
        self.save_to_local_storage()
    
    def clear_all_filters(self):
        """Сбросить все фильтры."""
        self.filter_status = "All"
        self.filter_priority = "All"
        self.filter_category = "All"
        self.filter_assigned_to = "All"
        self.search_query = ""
        
        # Сброс расширенных фильтров
        self.filter_date_from = ""
        self.filter_date_to = ""
        self.filter_overdue_only = False
        self.filter_completed_only = False
        self.filter_created_today = False
        self.filter_due_today = False
        self.filter_search_in_description = True
        self.filter_search_in_assignee = True
    
    def assign_task_to_member(self, task_id: int, member_name: str):
        """Назначить задачу члену команды."""
        for task in self.tasks:
            if task.id == task_id:
                task.assigned_to = member_name
                task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break
        self.save_to_local_storage()
        self.save_to_local_storage()
    
    def unassign_task(self, task_id: int):
        """Отменить назначение задачи."""
        for task in self.tasks:
            if task.id == task_id:
                task.assigned_to = ""
                task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break
        self.save_to_local_storage()
        self.save_to_local_storage()
    
    # Bulk operations methods
    def toggle_task_selection(self, task_id: int):
        """Переключить выбор задачи для массовых операций."""
        if task_id in self.selected_tasks:
            self.selected_tasks.remove(task_id)
        else:
            self.selected_tasks.append(task_id)
        
        # Show bulk actions if any tasks are selected
        self.show_bulk_actions = len(self.selected_tasks) > 0
    
    def select_all_filtered_tasks(self):
        """Выбрать все отфильтрованные задачи."""
        self.selected_tasks = [task.id for task in self.filtered_tasks]
        self.show_bulk_actions = len(self.selected_tasks) > 0
    
    def clear_selection(self):
        """Очистить выбор задач."""
        self.selected_tasks = []
        self.show_bulk_actions = False
    
    def bulk_delete_tasks(self):
        """Удалить все выбранные задачи."""
        self.tasks = [task for task in self.tasks if task.id not in self.selected_tasks]
        self.selected_tasks = []
        self.show_bulk_actions = False
        self.save_to_local_storage()
        self.save_to_local_storage()
    
    def bulk_update_status(self, new_status: str):
        """Обновить статус всех выбранных задач."""
        for task in self.tasks:
            if task.id in self.selected_tasks:
                task.status = new_status
                task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.selected_tasks = []
        self.show_bulk_actions = False
        self.save_to_local_storage()
        self.save_to_local_storage()
    
    def bulk_assign_to_member(self, member_name: str):
        """Назначить все выбранные задачи члену команды."""
        for task in self.tasks:
            if task.id in self.selected_tasks:
                task.assigned_to = member_name
                task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.selected_tasks = []
        self.show_bulk_actions = False
        self.save_to_local_storage()
        self.save_to_local_storage()
    
    # Notification methods
    def check_overdue_tasks(self):
        """Проверить просроченные задачи и показать уведомления."""
        today = datetime.now().strftime("%Y-%m-%d")
        overdue_tasks = [
            task for task in self.tasks
            if task.due_date and task.due_date < today
            and task.status not in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]
        ]
        
        if overdue_tasks:
            self.notification_message = f"⚠️ У вас {len(overdue_tasks)} просроченных задач!"
            self.show_notifications = True
        else:
            self.notification_message = ""
            self.show_notifications = False
    
    def dismiss_notification(self):
        """Отключить показ уведомлений."""
        self.show_notifications = False
        self.notification_message = ""
    
    # Calendar methods
    def toggle_calendar_view(self):
        """Переключить вид календаря."""
        self.show_calendar = not self.show_calendar
    
    def set_calendar_date(self, date_str: str):
        """Установить текущую дату календаря."""
        self.calendar_current_date = date_str
    
    def set_calendar_view_type(self, view_type: str):
        """Установить тип представления календаря."""
        self.calendar_view_type = view_type
    
    def get_tasks_for_date(self, date_str: str) -> List[Task]:
        """Получить задачи для конкретной даты."""
        return [
            task for task in self.tasks
            if task.due_date == date_str
            or task.created_at.startswith(date_str)
        ]
    
    # Quick actions and context menu methods
    def show_context_menu_for_task(self, task_id: int, x: int, y: int):
        """Показать контекстное меню для задачи."""
        self.context_menu_task_id = task_id
        self.show_context_menu = True
        self.context_menu_position = {"x": x, "y": y}
    
    def hide_context_menu(self):
        """Скрыть контекстное меню."""
        self.show_context_menu = False
        self.context_menu_task_id = None
    
    def quick_assign_task(self, task_id: int, member_name: str):
        """Быстро назначить задачу члену команды."""
        self.assign_task_to_member(task_id, member_name)
        self.add_notification(f"📌 Задача назначена: {member_name}", "info")
        self.hide_context_menu()
    
    def quick_change_priority(self, task_id: int, new_priority: str):
        """Быстро изменить приоритет задачи."""
        for task in self.tasks:
            if task.id == task_id:
                task.priority = new_priority
                task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break
        self.save_to_local_storage()
        self.add_notification(f"⚡ Приоритет изменен на: {new_priority}", "info")
        self.hide_context_menu()
    
    def quick_change_status(self, task_id: int, new_status: str):
        """Быстро изменить статус задачи."""
        self.update_task_status(task_id, new_status)
        self.add_notification(f"🔄 Статус изменен на: {new_status}", "info")
        self.hide_context_menu()
    
    def quick_duplicate_task(self, task_id: int):
        """Быстро дублировать задачу."""
        original_task = next((task for task in self.tasks if task.id == task_id), None)
        if original_task:
            new_task = Task(
                id=self.task_counter,
                title=f"{original_task.title} (копия)",
                description=original_task.description,
                priority=original_task.priority,
                category=original_task.category,
                due_date=original_task.due_date,
                assigned_to=original_task.assigned_to
            )
            self.tasks.append(new_task)
            self.task_counter += 1
            self.save_to_local_storage()
            self.add_notification(f"📋 Задача дублирована: {new_task.title}", "success")
        self.hide_context_menu()
    
    def quick_set_due_date(self, task_id: int, days_from_now: int):
        """Быстро установить дату выполнения."""
        due_date = (datetime.now() + timedelta(days=days_from_now)).strftime("%Y-%m-%d")
        for task in self.tasks:
            if task.id == task_id:
                task.due_date = due_date
                task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break
        self.save_to_local_storage()
        self.add_notification(f"📅 Срок установлен на: {due_date}", "info")
        self.hide_context_menu()
    
    def quick_add_subtask(self, task_id: int):
        """Быстро добавить подзадачу."""
        # Открываем диалог создания подзадачи
        self.selected_parent_task = task_id
        self.show_subtasks = True
        self.add_notification("📝 Создайте подзадачу", "info")
        self.hide_context_menu()
    
    def quick_add_dependency(self, task_id: int):
        """Быстро добавить зависимость."""
        # Открываем диалог добавления зависимости
        self.selected_dependency_task = task_id
        self.show_dependencies = True
        self.add_notification("🔗 Выберите зависимую задачу", "info")
        self.hide_context_menu()
    
    def get_calendar_days(self) -> List[Dict]:
        """Получить дни для отображения в календаре (месячный вид)."""
        from datetime import datetime, timedelta
        
        current_date = datetime.strptime(self.calendar_current_date, "%Y-%m-%d")
        year, month = current_date.year, current_date.month
        
        # Первый день месяца
        first_day = datetime(year, month, 1)
        # Последний день месяца
        if month == 12:
            next_month = datetime(year + 1, 1, 1)
        else:
            next_month = datetime(year, month + 1, 1)
        last_day = next_month - timedelta(days=1)
        
        # Дни для отображения (включая дни предыдущего и следующего месяца)
        start_weekday = first_day.weekday()  # 0 = Monday, 6 = Sunday
        days = []
        
        # Дни предыдущего месяца
        prev_month_day = first_day - timedelta(days=1)
        for i in range(start_weekday - 1, -1, -1):
            day_date = prev_month_day - timedelta(days=i)
            days.append({
                "date": day_date.strftime("%Y-%m-%d"),
                "day": day_date.day,
                "is_current_month": False,
                "tasks": self.get_tasks_for_date(day_date.strftime("%Y-%m-%d"))
            })
        
        # Дни текущего месяца
        for day in range(1, last_day.day + 1):
            day_date = datetime(year, month, day)
            days.append({
                "date": day_date.strftime("%Y-%m-%d"),
                "day": day,
                "is_current_month": True,
                "tasks": self.get_tasks_for_date(day_date.strftime("%Y-%m-%d"))
            })
        
        # Дни следующего месяца
        next_month_start = last_day + timedelta(days=1)
        days_needed = 42 - len(days)  # 6 weeks * 7 days
        for i in range(days_needed):
            day_date = next_month_start + timedelta(days=i)
            days.append({
                "date": day_date.strftime("%Y-%m-%d"),
                "day": day_date.day,
                "is_current_month": False,
                "tasks": self.get_tasks_for_date(day_date.strftime("%Y-%m-%d"))
            })
        
        return days
    
    def navigate_calendar(self, direction: str):
        """Навигация по календарю (предыдущий/следующий месяц)."""
        from datetime import datetime, timedelta
        
        current_date = datetime.strptime(self.calendar_current_date, "%Y-%m-%d")
        
        if direction == "prev":
            # Предыдущий месяц
            if current_date.month == 1:
                new_date = datetime(current_date.year - 1, 12, 1)
            else:
                new_date = datetime(current_date.year, current_date.month - 1, 1)
        else:  # "next"
            # Следующий месяц
            if current_date.month == 12:
                new_date = datetime(current_date.year + 1, 1, 1)
            else:
                new_date = datetime(current_date.year, current_date.month + 1, 1)
        
        self.calendar_current_date = new_date.strftime("%Y-%m-%d")
    
    @rx.var
    def calendar_display_month(self) -> str:
        """Получить отформатированное отображение текущего месяца календаря."""
        try:
            from datetime import datetime
            current_date = datetime.strptime(self.calendar_current_date, "%Y-%m-%d")
            # Russian month names
            months_ru = [
                "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
            ]
            return f"{months_ru[current_date.month - 1]} {current_date.year}"
        except:
            return "Ошибка отображения даты"
    
    # Dependency and sub-task methods
    def add_dependency(self, task_id: int, dependency_id: int):
        """Добавить зависимость к задаче."""
        for task in self.tasks:
            if task.id == task_id and dependency_id not in task.dependencies:
                task.dependencies.append(dependency_id)
                # Update the dependent task
                for dep_task in self.tasks:
                    if dep_task.id == dependency_id:
                        dep_task.dependent_tasks.append(task_id)
                        break
                task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break
        self.save_to_local_storage()
    
    def remove_dependency(self, task_id: int, dependency_id: int):
        """Удалить зависимость у задачи."""
        for task in self.tasks:
            if task.id == task_id and dependency_id in task.dependencies:
                task.dependencies.remove(dependency_id)
                # Update the dependent task
                for dep_task in self.tasks:
                    if dep_task.id == dependency_id and task_id in dep_task.dependent_tasks:
                        dep_task.dependent_tasks.remove(task_id)
                        break
                task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break
        self.save_to_local_storage()
    
    def create_sub_task(self, parent_id: int, title: str, description: str = ""):
        """Создать подзадачу для родительской задачи."""
        if not title.strip():
            return
        
        # Create sub-task
        sub_task = Task(
            id=self.task_counter,
            title=title.strip(),
            description=description.strip(),
            priority=Priority.NORMAL,
            category=Category.OTHER,
            parent_id=parent_id,
            status=TaskStatus.PENDING
        )
        
        self.tasks.append(sub_task)
        
        # Update parent task
        for task in self.tasks:
            if task.id == parent_id:
                task.sub_tasks.append(self.task_counter)
                task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break
        
        self.task_counter += 1
        self.save_to_local_storage()
    
    def update_task_progress(self, task_id: int, progress: int):
        """Обновить прогресс задачи с подзадачами."""
        progress = max(0, min(100, progress))  # Clamp between 0 and 100
        
        for task in self.tasks:
            if task.id == task_id:
                task.progress = progress
                # Auto-update status based on progress
                if progress == 100:
                    task.status = TaskStatus.COMPLETED
                elif progress > 0 and task.status == TaskStatus.PENDING:
                    task.status = TaskStatus.IN_PROGRESS
                task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break
        
        self.save_to_local_storage()
    
    def calculate_sub_task_progress(self, parent_id: int) -> int:
        """Рассчитать прогресс родительской задачи на основе подзадач."""
        parent_task = None
        sub_tasks = []
        
        for task in self.tasks:
            if task.id == parent_id:
                parent_task = task
            elif task.parent_id == parent_id:
                sub_tasks.append(task)
        
        if not parent_task or not sub_tasks:
            return 0
        
        total_progress = sum(task.progress for task in sub_tasks)
        calculated_progress = total_progress // len(sub_tasks) if sub_tasks else 0
        
        # Update parent task progress
        self.update_task_progress(parent_id, calculated_progress)
        return calculated_progress
    
    def get_dependent_tasks(self, task_id: int) -> List[Task]:
        """Получить список задач, зависящих от указанной задачи."""
        dependent_ids = []
        for task in self.tasks:
            if task.id == task_id:
                dependent_ids = task.dependent_tasks
                break
        
        return [task for task in self.tasks if task.id in dependent_ids]
    
    def get_task_dependencies(self, task_id: int) -> List[Task]:
        """Получить список задач, от которых зависит указанная задача."""
        dependency_ids = []
        for task in self.tasks:
            if task.id == task_id:
                dependency_ids = task.dependencies
                break
        
        return [task for task in self.tasks if task.id in dependency_ids]
    
    def get_sub_tasks(self, parent_id: int) -> List[Task]:
        """Получить список подзадач для родительской задачи."""
        return [task for task in self.tasks if task.parent_id == parent_id]
    
    def can_start_task(self, task_id: int) -> bool:
        """Проверить, можно ли начать выполнение задачи (все зависимости завершены)."""
        dependencies = self.get_task_dependencies(task_id)
        return all(dep.status == TaskStatus.COMPLETED for dep in dependencies)
    
    def toggle_sort_direction(self):
        """Переключить направление сортировки."""
        self.sort_ascending = not self.sort_ascending


def task_form() -> rx.Component:
    """Форма для добавления новой задачи."""
    return rx.card(
        rx.vstack(
            rx.heading("Новая задача", size="4"),
            
            rx.input(
                placeholder="Название задачи *",
                value=State.new_task_title,
                on_change=State.set_new_task_title,
                width="100%",
                size="3"
            ),
            
            rx.text_area(
                placeholder="Описание задачи",
                value=State.new_task_description,
                on_change=State.set_new_task_description,
                width="100%",
                height="80px",
                size="2"
            ),
            
            rx.grid(
                rx.select(
                    [Priority.LOW, Priority.NORMAL, Priority.HIGH, Priority.CRITICAL],
                    placeholder="Приоритет",
                    value=State.new_task_priority,
                    on_change=State.set_new_task_priority,
                    width="100%"
                ),
                
                rx.select(
                    [Category.WORK, Category.PERSONAL, Category.HEALTH, Category.FINANCE, Category.EDUCATION, Category.OTHER],
                    placeholder="Категория",
                    value=State.new_task_category,
                    on_change=State.set_new_task_category,
                    width="100%"
                ),
                
                rx.select(
                    State.team_members,
                    placeholder="Назначить исполнителя",
                    value=State.new_task_assigned_to,
                    on_change=State.set_new_task_assigned_to,
                    width="100%"
                ),
                
                rx.input(
                    type="date",
                    placeholder="Срок",
                    value=State.new_task_due_date,
                    on_change=State.set_new_task_due_date,
                    width="100%"
                ),
                
                columns="4",
                spacing="3",
                width="100%"
            ),
            
            rx.flex(
                rx.button(
                    rx.icon("plus", size=16),
                    "Добавить",
                    on_click=State.add_task,
                    size="3",
                    variant="solid"
                ),
                rx.button(
                    "Очистить",
                    on_click=State.clear_form,
                    size="3",
                    variant="outline",
                    color_scheme="gray"
                ),
                spacing="3",
                justify="end",
                width="100%"
            ),
            
            spacing="4",
            width="100%"
        ),
        width="100%",
        padding="1.5em",
        shadow="lg",
        border_radius="lg"
    )


def login_dialog() -> rx.Component:
    """Диалог входа в систему."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Вход в систему"),
            rx.vstack(
                rx.input(
                    placeholder="Имя пользователя",
                    value=State.login_username,
                    on_change=State.set_login_username,
                    width="100%"
                ),
                rx.input(
                    placeholder="Пароль",
                    type="password",
                    value=State.login_password,
                    on_change=State.set_login_password,
                    width="100%"
                ),
                rx.text(
                    "Доступные учетные записи: admin/admin123, user1/password1, user2/password2",
                    size="1",
                    color="gray.500",
                    text_align="center"
                ),
                spacing="3",
                width="100%"
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Отмена",
                        variant="soft", 
                        color_scheme="gray"
                    )
                ),
                rx.dialog.close(
                    rx.button(
                        "Войти", 
                        on_click=State.login
                    )
                ),
                spacing="2",
                justify="end",
                width="100%"
            ),
        ),
        open=State.show_login_dialog,
        on_open_change=State.set_show_login_dialog
    )


def user_menu() -> rx.Component:
    """Меню пользователя."""
    return rx.cond(
        State.is_authenticated,
        rx.dropdown_menu.root(
            rx.dropdown_menu.trigger(
                rx.button(
                    rx.icon("user", size=16),
                    State.current_user,
                    variant="ghost",
                    size="2"
                )
            ),
            rx.dropdown_menu.content(
                rx.dropdown_menu.item(
                    "Профиль",
                    on_click=lambda: None
                ),
                rx.dropdown_menu.item(
                    "Настройки",
                    on_click=lambda: None
                ),
                rx.dropdown_menu.separator(),
                rx.dropdown_menu.item(
                    "Выйти",
                    on_click=State.logout,
                    color="red"
                )
            )
        ),
        rx.button(
            "Войти",
            on_click=lambda: State.set_show_login_dialog(True),
            variant="solid",
            size="2"
        )
    )


def edit_dialog() -> rx.Component:
    """Глобальный диалог редактирования задачи."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Редактировать задачу"),
            rx.vstack(
                rx.input(
                    value=State.edit_title,
                    on_change=State.set_edit_title,
                    placeholder="Название",
                    width="100%"
                ),
                rx.text_area(
                    value=State.edit_description,
                    on_change=State.set_edit_description,
                    placeholder="Описание",
                    width="100%",
                    height="100px"
                ),
                rx.select(
                    [Priority.LOW, Priority.NORMAL, Priority.HIGH, Priority.CRITICAL],
                    value=State.edit_priority,
                    on_change=State.set_edit_priority,
                    width="100%"
                ),
                rx.select(
                    [Category.WORK, Category.PERSONAL, Category.HEALTH, Category.FINANCE, Category.EDUCATION, Category.OTHER],
                    value=State.edit_category,
                    on_change=State.set_edit_category,
                    width="100%"
                ),
                rx.select(
                    State.team_members,
                    value=State.edit_assigned_to,
                    on_change=State.set_edit_assigned_to,
                    placeholder="Назначить исполнителя",
                    width="100%"
                ),
                rx.input(
                    type="date",
                    value=State.edit_due_date,
                    on_change=State.set_edit_due_date,
                    width="100%"
                ),
                spacing="3",
                width="100%"
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Отмена",
                        variant="soft", 
                        color_scheme="gray"
                    )
                ),
                rx.dialog.close(
                    rx.button(
                        "Сохранить", 
                        on_click=State.save_edit
                    )
                ),
                spacing="2",
                justify="end",
                width="100%",
                margin_top="1em"
            ),
        ),
        open=State.show_edit_dialog,
        on_open_change=State.set_show_edit_dialog
    )


def task_card(task: Task) -> rx.Component:
    priority_colors = {
        Priority.LOW: "green",
        Priority.NORMAL: "blue", 
        Priority.HIGH: "orange",
        Priority.CRITICAL: "red"
    }
    
    status_colors = {
        TaskStatus.PENDING: "yellow",
        TaskStatus.IN_PROGRESS: "blue",
        TaskStatus.COMPLETED: "green",
        TaskStatus.CANCELLED: "gray"
    }
    
    category_colors = {
        Category.WORK: "blue",
        Category.PERSONAL: "green",
        Category.HEALTH: "red",
        Category.FINANCE: "purple",
        Category.EDUCATION: "orange",
        Category.OTHER: "gray"
    }

    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.checkbox(
                    checked=task.status == TaskStatus.COMPLETED,
                    on_change=lambda: State.toggle_task_completion(task.id),
                    size="1"
                ),
                rx.heading(task.title, size="4", weight="bold"),
                rx.spacer(),
                rx.badge(
                    task.priority,
                    color_scheme=priority_colors.get(task.priority, "gray"),
                    variant="solid"
                ),
                rx.badge(
                    task.status,
                    color_scheme=status_colors.get(task.status, "gray"),
                    variant="soft"
                ),
                spacing="3",
                width="100%",
                align="center",
            ),

            rx.text(task.description or "Без описания", size="2", color="gray.700"),
            
            rx.hstack(
                rx.text(f"Исполнитель: {task.assigned_to or '—'}", size="2"),
                rx.spacer(),
                rx.text(
                    f"Срок: {task.due_date or 'Без срока'}",
                    size="2",
                    color=rx.cond(
                        task.due_date and datetime.strptime(task.due_date, "%Y-%m-%d").date() < datetime.now().date(),
                        "red",
                        "gray.700"
                    )
                ),
                width="100%",
            ),

            # Теги (если есть)
            rx.cond(
                task.tags.length() > 0,
                rx.hstack(
                    rx.foreach(
                        State.get_task_tags(task.id),
                        lambda tag: rx.badge(
                            tag.name,
                            color_scheme=tag.color,
                            variant="solid",
                            size="1"
                        )
                    ),
                    spacing="1",
                    wrap="wrap"
                )
            ),

            rx.hstack(
                rx.button(
                    "Редактировать",
                    size="1",
                    variant="soft",
                    on_click=lambda: State.open_edit_dialog(task.id)
                ),
                rx.button(
                    "Комментарии",
                    size="1",
                    variant="outline",
                    on_click=lambda: State.open_comments(task.id)
                ),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon_button(rx.icon("more-horizontal"), size="1", variant="ghost")
                    ),
                    rx.menu.content(
                        rx.menu.item("Добавить подзадачу", on_click=lambda: State.quick_add_subtask(task.id)),
                        rx.menu.item("Зависимости", on_click=lambda: State.quick_add_dependency(task.id)),
                        rx.menu.separator(),
                        rx.menu.item("Удалить", color="red", on_click=lambda: State.delete_task(task.id)),
                    )
                ),
                spacing="2",
                margin_top="2",
            ),

            # Подзадачи и зависимости
            rx.accordion.root(
                rx.accordion.item(
                    header=rx.text("Подзадачи"),
                    content=sub_task_manager(task)
                ),
                rx.accordion.item(
                    header=rx.text("Зависимости"),
                    content=dependency_manager(task)
                ),
                allow_multiple=True
            ),

            spacing="3",
            width="100%",
            align_items="start",
        ),
        width="100%",
        # динамический цвет в зависимости от приоритета/просрочки и активности
        background=rx.cond(
            (task.due_date and datetime.strptime(task.due_date, "%Y-%m-%d").date() < datetime.now().date() and task.status != TaskStatus.COMPLETED),
            "red.50",
            rx.cond(
                (State.selected_task_for_comments == task.id) | (State.selected_task_for_tags == task.id),
                "blue.100" if State.theme == "light" else "blue.900",
                "white" if State.theme == "light" else "gray.800"
            )
        ),
        class_name="task-card",
        **{"data-task-id": str(task.id)}
    )


def notification_item(notification: Dict[str, str]) -> rx.Component:
    """Компонент отдельного уведомления."""
    return rx.card(
        rx.hstack(
            rx.icon("info", size=20, color="blue.500"),
            rx.vstack(
                rx.text(notification["message"], size="2", weight="medium"),
                rx.text(notification["timestamp"], size="1", color="gray.500"),
                spacing="1"
            ),
            rx.spacer(),
            rx.icon_button(
                rx.icon("x", size=16),
                on_click=lambda: State.remove_notification(notification["id"]),
                size="1",
                variant="ghost"
            ),
            align="start",
            width="100%"
        ),
        padding="0.75em",
        border_left="4px solid blue.500",
        background_color="blue.50"
    )


def notifications_panel() -> rx.Component:
    """Панель уведомлений."""
    return rx.cond(
        State.show_notifications & State.notifications.length() > 0,
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.heading("🔔 Уведомления", size="4"),
                    rx.spacer(),
                    rx.icon_button(
                        rx.icon("x", size=16),
                        on_click=State.clear_all_notifications,
                        size="2",
                        variant="ghost"
                    ),
                    width="100%"
                ),
                rx.divider(),
                rx.scroll_area(
                    rx.foreach(State.notifications, notification_item),
                    max_height="300px",
                    width="100%"
                ),
                spacing="3",
                width="100%"
            ),
            width="100%",
            margin_top="1em"
        )
    )


def productivity_analytics() -> rx.Component:
    """Панель аналитики продуктивности."""
    return rx.card(
        rx.vstack(
            rx.heading("📊 Аналитика продуктивности", size="4", margin_bottom="1em"),
            rx.flex(
                rx.card(
                    rx.vstack(
                        rx.text("Уровень завершения", size="2", color="gray.600"),
                        rx.text(f"{State.productivity_stats['completion_rate']}%", size="6", weight="bold", color="green.600"),
                        spacing="2",
                        align="center"
                    ),
                    padding="1em",
                    width="100%"
                ),
                rx.card(
                    rx.vstack(
                        rx.text("Задач в день", size="2", color="gray.600"),
                        rx.text(State.productivity_stats["tasks_per_day"], size="6", weight="bold", color="blue.600"),
                        spacing="2",
                        align="center"
                    ),
                    padding="1em",
                    width="100%"
                ),
                rx.card(
                    rx.vstack(
                        rx.text("Самая активная категория", size="2", color="gray.600"),
                        rx.text(State.productivity_stats["busiest_category"], size="4", weight="bold", color="purple.600"),
                        spacing="2",
                        align="center"
                    ),
                    padding="1em",
                    width="100%"
                ),
                rx.card(
                    rx.vstack(
                        rx.text("Самый продуктивный день", size="2", color="gray.600"),
                        rx.text(State.productivity_stats["most_productive_day"], size="4", weight="bold", color="orange.600"),
                        spacing="2",
                        align="center"
                    ),
                    padding="1em",
                    width="100%"
                ),
                wrap="wrap",
                spacing="4",
                width="100%"
            ),
            spacing="4",
            width="100%"
        ),
        width="100%",
        margin_top="1em"
    )


def stats_panel() -> rx.Component:
    """Панель статистики."""
    return rx.card(
        rx.vstack(
            rx.grid(
                rx.vstack(
                    rx.text("Всего", size="1", color_scheme="gray"),
                    rx.heading(State.task_stats["total"], size="5"),
                    spacing="1",
                    align="center"
                ),
                rx.vstack(
                    rx.text("Ожидание", size="1", color_scheme="gray"),
                    rx.heading(State.task_stats["pending"], size="5", color_scheme="yellow"),
                    spacing="1",
                    align="center"
                ),
                rx.vstack(
                    rx.text("В работе", size="1", color_scheme="gray"),
                    rx.heading(State.task_stats["in_progress"], size="5", color_scheme="blue"),
                    spacing="1",
                    align="center"
                ),
                rx.vstack(
                    rx.text("Готово", size="1", color_scheme="gray"),
                    rx.heading(State.task_stats["completed"], size="5", color_scheme="green"),
                    spacing="1",
                    align="center"
                ),
                rx.vstack(
                    rx.text("Просрочено", size="1", color_scheme="gray"),
                    rx.heading(State.task_stats["overdue"], size="5", color_scheme="red"),
                    spacing="1",
                    align="center"
                ),
                columns="5",
                width="100%",
                spacing="4"
            ),
            rx.grid(
                rx.vstack(
                    rx.text("Работа", size="1", color_scheme="gray"),
                    rx.heading(State.task_stats["work"], size="5", color_scheme="blue"),
                    spacing="1",
                    align="center"
                ),
                rx.vstack(
                    rx.text("Личное", size="1", color_scheme="gray"),
                    rx.heading(State.task_stats["personal"], size="5", color_scheme="green"),
                    spacing="1",
                    align="center"
                ),
                rx.vstack(
                    rx.text("Здоровье", size="1", color_scheme="gray"),
                    rx.heading(State.task_stats["health"], size="5", color_scheme="red"),
                    spacing="1",
                    align="center"
                ),
                rx.vstack(
                    rx.text("Финансы", size="1", color_scheme="gray"),
                    rx.heading(State.task_stats["finance"], size="5", color_scheme="purple"),
                    spacing="1",
                    align="center"
                ),
                rx.vstack(
                    rx.text("Образование", size="1", color_scheme="gray"),
                    rx.heading(State.task_stats["education"], size="5", color_scheme="orange"),
                    spacing="1",
                    align="center"
                ),
                columns="5",
                width="100%",
                spacing="4"
            ),
            spacing="4",
            width="100%"
        ),
        width="100%"
    )


def advanced_search_panel() -> rx.Component:
    """Панель расширенного поиска."""
    return rx.card(
        rx.vstack(
            rx.heading("🔍 Расширенный поиск", size="4", margin_bottom="1em"),
            rx.grid(
                rx.checkbox(
                    "Искать в описании",
                    checked=State.search_in_description,
                    on_change=State.set_search_in_description,
                    size="2"
                ),
                rx.checkbox(
                    "Искать в комментариях",
                    checked=State.search_in_comments,
                    on_change=State.set_search_in_comments,
                    size="2"
                ),
                rx.checkbox(
                    "Искать в подзадачах",
                    checked=State.search_in_subtasks,
                    on_change=State.set_search_in_subtasks,
                    size="2"
                ),
                rx.checkbox(
                    "Точное совпадение",
                    checked=State.search_exact_match,
                    on_change=State.set_search_exact_match,
                    size="2"
                ),
                columns="2",
                spacing="4",
                width="100%"
            ),
            spacing="4",
            width="100%"
        ),
        width="100%",
        margin_top="1em"
    )


def filter_controls() -> rx.Component:
    """Элементы управления фильтрами."""
    return rx.card(
        rx.vstack(
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger("Основные", value="basic"),
                    rx.tabs.trigger("Расширенные", value="advanced"),
                    rx.tabs.trigger("Сортировка", value="sort")
                ),
                
                rx.tabs.content(
                    rx.vstack(
                        rx.input(
                            placeholder="🔍 Поиск задач...",
                            value=State.search_query,
                            on_change=State.set_search_query,
                            width="100%",
                            size="3"
                        ),
                        
                        rx.grid(
                            rx.select(
                                ["All", TaskStatus.PENDING, TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED, TaskStatus.CANCELLED],
                                placeholder="Статус",
                                value=State.filter_status,
                                on_change=State.set_filter_status,
                                width="100%"
                            ),
                            
                            rx.select(
                                ["All", Priority.LOW, Priority.NORMAL, Priority.HIGH, Priority.CRITICAL],
                                placeholder="Приоритет",
                                value=State.filter_priority,
                                on_change=State.set_filter_priority,
                                width="100%"
                            ),
                            
                            rx.select(
                                ["All", Category.WORK, Category.PERSONAL, Category.HEALTH, Category.FINANCE, Category.EDUCATION, Category.OTHER],
                                placeholder="Категория",
                                value=State.filter_category,
                                on_change=State.set_filter_category,
                                width="100%"
                            ),
                            
                            rx.select(
                                ["All", "Алексей", "Мария", "Иван", "Елена", "Дмитрий", "Ольга", "Сергей", "Анна"],
                                placeholder="Исполнитель",
                                value=State.filter_assigned_to,
                                on_change=State.set_filter_assigned_to,
                                width="100%"
                            ),
                            
                            columns="4",
                            spacing="3",
                            width="100%"
                        ),
                        
                        rx.flex(
                            rx.checkbox(
                                rx.text("Показать выполненные", size="2"),
                                checked=State.show_completed,
                                on_change=State.set_show_completed
                            ),
                            rx.spacer(),
                            rx.button(
                                "🔄 Сбросить фильтры",
                                on_click=State.clear_all_filters,
                                variant="outline",
                                size="2"
                            ),
                            width="100%",
                            align="center"
                        ),
                        
                        spacing="4",
                        width="100%"
                    )
                ),
                
                rx.tabs.content(
                    rx.vstack(
                        rx.heading("📅 Фильтры по датам", size="3"),
                        rx.grid(
                            rx.input(
                                type="date",
                                placeholder="Создано с",
                                value=State.filter_date_from,
                                on_change=State.set_filter_date_from,
                                width="100%"
                            ),
                            rx.input(
                                type="date",
                                placeholder="Создано по",
                                value=State.filter_date_to,
                                on_change=State.set_filter_date_to,
                                width="100%"
                            ),
                            rx.checkbox(
                                rx.text("Создано сегодня", size="2"),
                                checked=State.filter_created_today,
                                on_change=State.set_filter_created_today
                            ),
                            rx.checkbox(
                                rx.text("На сегодня", size="2"),
                                checked=State.filter_due_today,
                                on_change=State.set_filter_due_today
                            ),
                            columns="2",
                            spacing="3",
                            width="100%"
                        ),
                        
                        rx.heading("🔍 Расширенный поиск", size="3", margin_top="1em"),
                        rx.grid(
                            rx.checkbox(
                                rx.text("Искать в описании", size="2"),
                                checked=State.filter_search_in_description,
                                on_change=State.set_filter_search_in_description
                            ),
                            rx.checkbox(
                                rx.text("Искать по исполнителю", size="2"),
                                checked=State.filter_search_in_assignee,
                                on_change=State.set_filter_search_in_assignee
                            ),
                            rx.checkbox(
                                rx.text("Искать в комментариях", size="2"),
                                checked=State.search_in_comments,
                                on_change=State.set_search_in_comments
                            ),
                            rx.checkbox(
                                rx.text("Искать в подзадачах", size="2"),
                                checked=State.search_in_subtasks,
                                on_change=State.set_search_in_subtasks
                            ),
                            rx.checkbox(
                                rx.text("Точное совпадение", size="2"),
                                checked=State.search_exact_match,
                                on_change=State.set_search_exact_match
                            ),
                            columns="2",
                            spacing="3",
                            width="100%"
                        ),
                        
                        rx.heading("📊 Специальные фильтры", size="3", margin_top="1em"),
                        rx.grid(
                            rx.checkbox(
                                rx.text("Только просроченные", size="2"),
                                checked=State.filter_overdue_only,
                                on_change=State.set_filter_overdue_only
                            ),
                            rx.checkbox(
                                rx.text("Только выполненные", size="2"),
                                checked=State.filter_completed_only,
                                on_change=State.set_filter_completed_only
                            ),
                            columns="2",
                            spacing="3",
                            width="100%"
                        ),
                        
                        spacing="3",
                        width="100%"
                    )
                ),
                
                rx.tabs.content(
                    rx.vstack(
                        rx.select(
                            ["created_at", "due_date", "priority", "title", "status", "category", "assigned_to"],
                            placeholder="Сортировка по",
                            value=State.sort_by,
                            on_change=State.set_sort_by,
                            width="100%"
                        ),
                        
                        rx.flex(
                            rx.icon_button(
                                rx.cond(
                                    State.sort_ascending,
                                    rx.icon("arrow-up", size=16),
                                    rx.icon("arrow-down", size=16)
                                ),
                                on_click=State.toggle_sort_direction,
                                variant="solid",
                                size="3"
                            ),
                            # Export buttons
                            rx.dropdown_menu.root(
                                rx.dropdown_menu.trigger(
                                    rx.button(
                                        "📤 Экспорт",
                                        variant="solid",
                                        size="3"
                                    )
                                ),
                                rx.dropdown_menu.content(
                                    rx.dropdown_menu.item(
                                        "Все задачи (CSV)",
                                        on_click=State.export_tasks_csv
                                    ),
                                    rx.dropdown_menu.item(
                                        "Все задачи (JSON)",
                                        on_click=State.export_tasks_json
                                    ),
                                    rx.dropdown_menu.separator(),
                                    rx.dropdown_menu.item(
                                        "Отфильтрованные (CSV)",
                                        on_click=State.export_filtered_tasks_csv
                                    ),
                                    rx.dropdown_menu.item(
                                        "Отфильтрованные (JSON)",
                                        on_click=State.export_filtered_tasks_json
                                    )
                                )
                            ),
                            spacing="2",
                            align="center"
                        ),
                        
                        spacing="3",
                        width="100%"
                    )
                ),
                
                default_value="basic",
                width="100%"
            ),
            
            spacing="4",
            width="100%"
        ),
        width="100%",
        padding="1.5em",
        shadow="md",
        border_radius="lg"
    )


def bulk_actions_bar() -> rx.Component:
    """Панель массовых операций."""
    return rx.cond(
        State.show_bulk_actions,
        rx.card(
            rx.flex(
                rx.text(
                    "Выбрано: ", State.selected_tasks.length(), " задач",
                    size="2",
                    weight="bold"
                ),
                rx.spacer(),
                rx.button(
                    "Выбрать все отфильтрованные",
                    on_click=State.select_all_filtered_tasks,
                    size="2",
                    variant="outline"
                ),
                rx.dropdown_menu.root(
                    rx.dropdown_menu.trigger(
                        rx.button(
                            "Обновить статус",
                            variant="solid",
                            size="2"
                        )
                    ),
                    rx.dropdown_menu.content(
                        rx.dropdown_menu.item(
                            "В ожидании",
                            on_click=lambda: State.bulk_update_status(TaskStatus.PENDING)
                        ),
                        rx.dropdown_menu.item(
                            "В работе",
                            on_click=lambda: State.bulk_update_status(TaskStatus.IN_PROGRESS)
                        ),
                        rx.dropdown_menu.item(
                            "Выполнено",
                            on_click=lambda: State.bulk_update_status(TaskStatus.COMPLETED)
                        ),
                        rx.dropdown_menu.item(
                            "Отменено",
                            on_click=lambda: State.bulk_update_status(TaskStatus.CANCELLED)
                        )
                    )
                ),
                rx.dropdown_menu.root(
                    rx.dropdown_menu.trigger(
                        rx.button(
                            "Назначить",
                            variant="solid",
                            size="2"
                        )
                    ),
                    rx.dropdown_menu.content(
                        rx.foreach(
                            State.team_members,
                            lambda member: rx.dropdown_menu.item(
                                member,
                                on_click=lambda: State.bulk_assign_to_member(member)
                            )
                        ),
                        rx.dropdown_menu.separator(),
                        rx.dropdown_menu.item(
                            "Отменить назначение",
                            on_click=lambda: State.bulk_assign_to_member("")
                        )
                    )
                ),
                rx.button(
                    "Удалить",
                    on_click=State.bulk_delete_tasks,
                    size="2",
                    color_scheme="red",
                    variant="solid"
                ),
                rx.button(
                    "Отменить",
                    on_click=State.clear_selection,
                    size="2",
                    variant="outline",
                    color_scheme="gray"
                ),
                spacing="3",
                width="100%",
                align="center",
                wrap="wrap"
            ),
            width="100%",
            padding="1em",
            background_color="rgba(0, 123, 255, 0.1)",
            border="1px solid blue",
            border_radius="md"
        ),
        rx.fragment()
    )

def dependency_manager(task: Task) -> rx.Component:
    """Компонент управления зависимостями задачи."""
    return rx.card(
        rx.vstack(
            rx.heading("Зависимости задачи", size="3"),
            
            # Current dependencies
            rx.cond(
                task.dependencies.length() > 0,
                rx.vstack(
                    rx.text("Зависит от:", size="2", weight="bold"),
                    rx.foreach(
                        State.get_task_dependencies(task.id),
                        lambda dep_task: rx.hstack(
                            rx.badge(
                                dep_task.title,
                                color_scheme={
                                    TaskStatus.PENDING: "yellow",
                                    TaskStatus.IN_PROGRESS: "blue",
                                    TaskStatus.COMPLETED: "green",
                                    TaskStatus.CANCELLED: "gray"
                                }.get(dep_task.status, "gray")
                            ),
                            rx.icon_button(
                                rx.icon("x", size=12),
                                on_click=lambda: State.remove_dependency(task.id, dep_task.id),
                                size="1",
                                variant="ghost",
                                color_scheme="red"
                            ),
                            spacing="2",
                            align="center"
                        )
                    ),
                    spacing="2"
                ),
                rx.text("Нет зависимостей", size="2", color="gray.500")
            ),
            
            # Dependent tasks
            rx.cond(
                task.dependent_tasks.length() > 0,
                rx.vstack(
                    rx.text("От этой задачи зависят:", size="2", weight="bold", margin_top="1em"),
                    rx.foreach(
                        State.get_dependent_tasks(task.id),
                        lambda dep_task: rx.badge(
                            dep_task.title,
                            color_scheme={
                                TaskStatus.PENDING: "yellow",
                                TaskStatus.IN_PROGRESS: "blue",
                                TaskStatus.COMPLETED: "green",
                                TaskStatus.CANCELLED: "gray"
                            }.get(dep_task.status, "gray"),
                            size="2"
                        )
                    ),
                    spacing="2"
                ),
                rx.fragment()
            ),
            
            # Add dependency
            rx.vstack(
                rx.text("Добавить зависимость:", size="2", weight="bold", margin_top="1em"),
                rx.select(
                    [
                        other_task.title 
                        for other_task in State.tasks 
                        if other_task.id != task.id 
                        and other_task.id not in task.dependencies
                        and other_task.id not in task.sub_tasks
                        and other_task.parent_id != task.id
                    ],
                    placeholder="Выберите задачу",
                    on_change=lambda selection: State.add_dependency(
                        task.id, 
                        next(t.id for t in State.tasks if t.title == selection)
                    ) if selection else None,
                    width="100%"
                ),
                spacing="2"
            ),
            
            spacing="3",
            width="100%"
        ),
        width="100%",
        padding="1em",
        background_color="rgba(59, 130, 246, 0.05)",
        border="1px solid blue.200",
        border_radius="md"
    )

def sub_task_manager(task: Task) -> rx.Component:
    """Компонент управления подзадачами."""
    return rx.card(
        rx.vstack(
            rx.heading("Подзадачи", size="3"),
            
            # Progress bar for parent tasks
            rx.cond(
                task.sub_tasks.length() > 0,
                rx.vstack(
                    rx.flex(
                        rx.text("Прогресс:", size="2", weight="bold"),
                        rx.text(f"{task.progress}%", size="2", color="blue.600"),
                        spacing="2",
                        align="center"
                    ),
                    rx.progress(value=task.progress, width="100%"),
                    spacing="2"
                ),
                rx.fragment()
            ),
            
            # List of sub-tasks
            rx.cond(
                task.sub_tasks.length() > 0,
                rx.vstack(
                    rx.foreach(
                        State.get_sub_tasks(task.id),
                        lambda sub_task: rx.card(
                            rx.flex(
                                rx.checkbox(
                                    checked=sub_task.status == TaskStatus.COMPLETED,
                                    on_change=lambda: State.toggle_task_completion(sub_task.id),
                                    size="1"
                                ),
                                rx.text(sub_task.title, size="2"),
                                rx.spacer(),
                                rx.badge(
                                    f"{sub_task.progress}%",
                                    color_scheme="blue",
                                    size="1"
                                ),
                                rx.icon_button(
                                    rx.icon("trash-2", size=12),
                                    on_click=lambda: State.delete_task(sub_task.id),
                                    size="1",
                                    variant="ghost",
                                    color_scheme="red"
                                ),
                                width="100%",
                                align="center",
                                spacing="2"
                            ),
                            padding="0.75em",
                            width="100%"
                        )
                    ),
                    spacing="2"
                ),
                rx.text("Нет подзадач", size="2", color="gray.500")
            ),
            
            # Add sub-task form
            rx.vstack(
                rx.text("Добавить подзадачу:", size="2", weight="bold", margin_top="1em"),
                rx.input(
                    placeholder="Название подзадачи",
                    id=f"subtask-title-{task.id}",
                    size="2"
                ),
                rx.text_area(
                    placeholder="Описание (необязательно)",
                    id=f"subtask-desc-{task.id}",
                    size="1",
                    height="60px"
                ),
                rx.button(
                    "Добавить подзадачу",
                    on_click=lambda: State.create_sub_task(
                        task.id,
                        rx.get_value(f"subtask-title-{task.id}"),
                        rx.get_value(f"subtask-desc-{task.id}")
                    ),
                    size="2",
                    variant="solid"
                ),
                spacing="2"
            ),
            
            spacing="3",
            width="100%"
        ),
        width="100%",
        padding="1em",
        background_color="rgba(34, 197, 94, 0.05)",
        border="1px solid green.200",
        border_radius="md"
    )

def calendar_view() -> rx.Component:
    """Календарный вид задач."""
    return rx.cond(
        State.show_calendar,
        rx.card(
            rx.vstack(
                # Calendar header
                rx.flex(
                    rx.button(
                        "←",
                        on_click=lambda: State.navigate_calendar("prev"),
                        variant="ghost",
                        size="2"
                    ),
                    rx.vstack(
                        rx.heading(
                            State.calendar_display_month,
                            size="4",
                            text_align="center"
                        ),
                        rx.hstack(
                            rx.button(
                                "Месяц",
                                on_click=lambda: State.set_calendar_view_type("month"),
                                variant=rx.cond(State.calendar_view_type == "month", "solid", "outline"),
                                size="1"
                            ),
                            rx.button(
                                "Неделя",
                                on_click=lambda: State.set_calendar_view_type("week"),
                                variant=rx.cond(State.calendar_view_type == "week", "solid", "outline"),
                                size="1"
                            ),
                            rx.button(
                                "День",
                                on_click=lambda: State.set_calendar_view_type("day"),
                                variant=rx.cond(State.calendar_view_type == "day", "solid", "outline"),
                                size="1"
                            ),
                            spacing="1"
                        ),
                        spacing="1",
                        align="center"
                    ),
                    rx.button(
                        "→",
                        on_click=lambda: State.navigate_calendar("next"),
                        variant="ghost",
                        size="2"
                    ),
                    width="100%",
                    justify="between",
                    align="center"
                ),
                
                # Calendar grid
                rx.cond(
                    State.calendar_view_type == "month",
                    rx.vstack(
                        # Weekday headers
                        rx.grid(
                            rx.foreach(
                                ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
                                lambda day: rx.center(
                                    rx.text(day, size="1", font_weight="bold", color="gray.600"),
                                    height="2em"
                                )
                            ),
                            columns="7",
                            width="100%"
                        ),
                        
                        # Simple calendar display
                        rx.center(
                            rx.text(
                                "Календарь задач",
                                size="2",
                                color="gray.600"
                            ),
                            height="300px"
                        ),
                        
                        spacing="2",
                        width="100%"
                    ),
                    rx.text("Другие виды календаря будут реализованы в будущих обновлениях", size="2", color="gray.500")
                ),
                
                # Close button
                rx.flex(
                    rx.button(
                        "Закрыть календарь",
                        on_click=State.toggle_calendar_view,
                        variant="outline",
                        size="2"
                    ),
                    width="100%",
                    justify="center"
                ),
                
                spacing="4",
                width="100%"
            ),
            width="100%",
            max_width="800px",
            margin="0 auto",
            padding="1.5em",
            shadow="lg",
            border_radius="lg"
        ),
        rx.fragment()
    )

def notification_banner() -> rx.Component:
    """Баннер уведомлений."""
    return rx.cond(
        State.show_notifications,
        rx.card(
            rx.flex(
                rx.icon("triangle_alert", size=20, color="red"),
                rx.text(State.notification_message, size="2", weight="bold"),
                rx.spacer(),
                rx.icon_button(
                    rx.icon("x", size=16),
                    on_click=State.dismiss_notification,
                    variant="ghost",
                    size="1"
                ),
                spacing="2",
                align="center",
                width="100%"
            ),
            background_color="rgba(239, 68, 68, 0.1)",
            border="1px solid red.300",
            border_radius="md",
            padding="1em",
            width="100%"
        ),
        rx.fragment()
    )

def theme_toggle() -> rx.Component:
    """Компонент переключения темы."""
    return rx.icon_button(
        rx.cond(
            State.theme == "light",
            rx.icon("moon", size=20),
            rx.icon("sun", size=20)
        ),
        on_click=State.toggle_theme,
        size="3",
        variant="outline"
    )


def pagination_controls() -> rx.Component:
    """Компонент управления пагинацией."""
    return rx.cond(
        State.virtual_scroll_enabled,
        rx.card(
            rx.flex(
                rx.button(
                    "⬅️ Предыдущая",
                    on_click=State.go_to_previous_page,
                    disabled=State.current_page == 0,
                    size="2",
                    variant="outline"
                ),
                
                rx.text(
                    f"Страница {State.current_page + 1} из {State.get_total_pages()}",
                    size="2",
                    weight="bold"
                ),
                
                rx.button(
                    "Следующая ➡️",
                    on_click=State.go_to_next_page,
                    size="2",
                    variant="outline"
                ),
                
                rx.select(
                    ["10", "20", "50", "100"],
                    placeholder="Задач на странице",
                    value=str(State.items_per_page),
                    on_change=State.set_items_per_page_str,
                    size="2",
                    width="150px"
                ),
                
                spacing="4",
                align="center",
                wrap="wrap"
            ),
            width="100%",
            padding="1em"
        )
    )


def performance_settings() -> rx.Component:
    """Компонент настроек производительности."""
    return rx.card(
        rx.vstack(
            rx.heading("⚙️ Настройки производительности", size="4"),
            
            rx.grid(
                rx.checkbox(
                    "Виртуальная прокрутка",
                    checked=State.virtual_scroll_enabled,
                    on_change=State.set_virtual_scroll_enabled,
                    size="2"
                ),
                
                rx.flex(
                    rx.text("Задержка поиска (сек):", size="2"),
                    rx.input(
                        type="number",
                        value=str(State.search_debounce_time),
                        on_change=State.set_search_debounce_time_str,
                        width="100px",
                        size="2"
                    ),
                    spacing="2",
                    align="center"
                ),
                
                columns="2",
                spacing="4",
                width="100%"
            ),
            
            rx.text(
                rx.cond(
                    State.virtual_scroll_enabled,
                    f"Всего задач: {State.get_filtered_tasks_count()} | Отображается: {State.items_per_page} задач на странице",
                    f"Всего задач: {State.get_filtered_tasks_count()} | Отображается: все задачи"
                ),
                size="2",
                color="gray.500"
            ),
            
            spacing="4",
            width="100%"
        ),
        width="100%",
        margin_top="1em"
    )


def comment_card(comment: Comment) -> rx.Component:
    """Карточка комментария - упрощенная версия для избежания ошибок."""
    return rx.card(
        rx.text("Комментарий", size="2"),
        padding="1em",
        width="100%"
    )


def tag_badge(tag: Tag) -> rx.Component:
    """Бейдж тега - упрощенная версия."""
    return rx.badge("Тег", size="1")


def tag_card(tag: Tag) -> rx.Component:
    """Карточка тега в панели - упрощенная версия."""
    return rx.card(
        rx.text("Тег", size="2"),
        padding="0.75em",
        width="100%"
    )


def task_tag_badge(tag: Tag, task_id: int) -> rx.Component:
    """Бейдж тега задачи - упрощенная версия."""
    return rx.badge("Тег", size="1")


def tags_panel() -> rx.Component:
    return rx.cond(
        State.show_tags,
        rx.box(
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.heading("Теги задачи", size="4"),
                        rx.spacer(),
                        rx.icon_button(
                            rx.icon("x"),
                            on_click=State.close_tags,
                            variant="ghost",
                            size="2"
                        ),
                        width="100%",
                        align="center"
                    ),
                    rx.divider(),
                    
                    # Список тегов задачи
                    rx.cond(
                        State.selected_task_for_tags,
                        rx.vstack(
                            rx.heading("Теги задачи:", size="2"),
                            rx.flex(
                                rx.foreach(
                                    State.get_task_tags(State.selected_task_for_tags),
                                    lambda tag: rx.badge(
                                        tag.name,
                                        color_scheme=tag.color,
                                        variant="solid",
                                        size="1"
                                    )
                                ),
                                spacing="2",
                                wrap="wrap"
                            ),
                            spacing="2",
                            width="100%"
                        )
                    ),
                    
                    rx.divider(),
                    
                    # Все доступные теги
                    rx.vstack(
                        rx.heading("Все теги:", size="2"),
                        rx.cond(
                            State.tags.length() > 0,
                            rx.foreach(State.tags, tag_card),
                            rx.text("Нет тегов", size="2", color="gray.500")
                        ),
                        spacing="2",
                        width="100%"
                    ),
                    
                    rx.divider(),
                    
                    # Форма добавления нового тега
                    rx.vstack(
                        rx.heading("Создать новый тег:", size="2"),
                        rx.input(
                            value=State.new_tag_name,
                            on_change=State.set_new_tag_name,
                            placeholder="Название тега",
                            size="2",
                            width="100%"
                        ),
                        rx.select(
                            State.available_tag_colors,
                            placeholder="Выберите цвет",
                            value=State.new_tag_color,
                            on_change=State.set_new_tag_color,
                            size="2",
                            width="100%"
                        ),
                        rx.button(
                            "Добавить тег",
                            on_click=State.add_tag,
                            size="2",
                            variant="solid"
                        ),
                        spacing="2",
                        width="100%"
                    ),
                    
                    spacing="4",
                    width="100%"
                ),
                width="100%",
                height="100%"
            ),
            position="fixed",
            right="0",
            top="0",
            bottom="0",
            width="380px",
            background="white" if State.theme == "light" else "gray.800",
            box_shadow="-4px 0 20px rgba(0,0,0,0.15)",
            z_index="1000",
            padding="1.5em",
            overflow_y="auto"
        )
    )


def comments_panel() -> rx.Component:
    return rx.cond(
        State.show_comments,
        rx.box(
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.heading("Комментарии к задаче", size="4"),
                        rx.spacer(),
                        rx.icon_button(
                            rx.icon("x"),
                            on_click=State.close_comments,
                            variant="ghost",
                            size="2"
                        ),
                        width="100%",
                        align="center"
                    ),
                    rx.divider(),
                    rx.text("Комментарии временно недоступны", color="gray.500"),
                    rx.divider(margin_y="1em"),
                    rx.text_area(
                        placeholder="Напишите комментарий...",
                        value=State.new_comment_content,
                        on_change=State.set_new_comment_content,
                        height="80px"
                    ),
                    rx.flex(
                        rx.button(
                            "Отправить",
                            on_click=State.add_comment,
                            variant="solid"
                        ),
                        rx.button(
                            "Отмена",
                            on_click=State.close_comments,
                            variant="soft",
                            color_scheme="gray"
                        ),
                        spacing="3",
                        justify="end"
                    ),
                    spacing="4",
                    width="100%"
                ),
                width="100%",
                height="100%"
            ),
            position="fixed",
            right="0",
            top="0",
            bottom="0",
            width="380px",
            background="white" if State.theme == "light" else "gray.800",
            box_shadow="-4px 0 20px rgba(0,0,0,0.15)",
            z_index="1000",
            padding="1.5em",
            overflow_y="auto"
        )
    )


def context_menu() -> rx.Component:
    return rx.cond(
        State.show_context_menu,
        rx.box(
            rx.vstack(
                rx.heading("Действия", size="3", margin_bottom="2"),
                rx.button(
                    rx.icon("message-circle", size=14), "Комментарии",
                    on_click=lambda: [State.open_comments(State.context_menu_task_id), State.hide_context_menu()],
                    variant="ghost", width="100%", justify="start"
                ),
                rx.button(
                    rx.icon("tag", size=14), "Теги",
                    on_click=lambda: [State.open_tags(State.context_menu_task_id), State.hide_context_menu()],
                    variant="ghost", width="100%", justify="start"
                ),
                rx.button(
                    rx.icon("check_check", size=14), "Завершить",
                    on_click=lambda: [State.toggle_task_completion(State.context_menu_task_id), State.hide_context_menu()],
                    variant="ghost", width="100%", justify="start"
                ),
                rx.button(
                    rx.icon("trash-2", size=14), "Удалить",
                    on_click=lambda: [State.delete_task(State.context_menu_task_id), State.hide_context_menu()],
                    color_scheme="red", variant="ghost", width="100%", justify="start"
                ),
            ),
            position="fixed",
            left=State.context_menu_position["x"],
            top=State.context_menu_position["y"],
            background="white",
            border="1px solid #e2e8f0",
            border_radius="8px",
            padding="8px",
            box_shadow="0 10px 15px -3px rgba(0, 0, 0, 0.1)",
            z_index="2000",
            min_width="180px",
            on_click=State.hide_context_menu,
        )
    )


def index() -> rx.Component:
    """Главная страница."""
    return rx.box(
        # Применяем стили темы
        apply_theme_styles(),
        
        # Добавляем переключатель темы в правый верхний угол
        rx.flex(
            theme_toggle(),
            position="fixed",
            top="20px",
            right="20px",
            z_index="1000"
        ),
        
        # JavaScript для работы с localStorage
        rx.script("""
            function loadUserData() {
                let user = localStorage.getItem("current_user") || "guest";
                        
                let tasks    = localStorage.getItem("tasks_"    + user);
                let comments = localStorage.getItem("comments_" + user);
                let tags     = localStorage.getItem("tags_"     + user);
                        
                if (tasks)    Reflex.setState({ tasks_json: tasks });
                if (comments) Reflex.setState({ comments_json: comments });
                if (tags)     Reflex.setState({ tags_json: tags });
            }
        
            // Вызываем при каждой загрузке страницы
            window.addEventListener('load', loadUserData);
        
            // Также можно вызывать после логина (опционально)
            // но в вашем случае лучше полагаться на on_mount и load
        """),
                
        # JavaScript для контекстного меню
        rx.script("""
            document.addEventListener('contextmenu', function(e) {
                let card = e.target.closest('.task-card');
                if (card) {
                    e.preventDefault();
                    const x = e.clientX;
                    const y = e.clientY;
                    // Находим ID задачи (можно хранить в data-task-id)
                    const taskId = card.dataset.taskId;
                    if (taskId) {
                        Reflex.setState({
                            context_menu_task_id: parseInt(taskId),
                            context_menu_position: { x: x, y: y },
                            show_context_menu: true
                        });
                    }
                }
            });
        """),
        login_dialog(),
        edit_dialog(),
        calendar_view(),
        context_menu(),
        comments_panel(),
        tags_panel(),
        rx.container(
            rx.vstack(
                rx.flex(
                    rx.flex(
                        rx.heading("📋 Управление задачами", size="8"),
                        rx.cond(
                            State.saving,
                            rx.flex(
                                rx.spinner(size="1"),
                                rx.text("Сохранение...", size="2", color="gray.600"),
                                spacing="2",
                                align="center",
                                margin_left="auto"
                            ),
                            rx.fragment()
                        ),
                        spacing="3",
                        align="center"
                    ),
                    rx.button(
                        rx.icon("calendar", size=20),
                        "Календарь",
                        on_click=State.toggle_calendar_view,
                        variant=rx.cond(State.show_calendar, "solid", "outline"),
                        size="3"
                    ),
                    width="100%",
                    justify="between",
                    align="center"
                ),
                notification_banner(),
                notifications_panel(),
                stats_panel(),
                productivity_analytics(),
                performance_settings(),
                bulk_actions_bar(),
                
                rx.cond(
                    State.is_authenticated,
                    rx.grid(
                        task_form(),
                        filter_controls(),
                        columns="2",
                        spacing="4",
                        width="100%"
                    ),
                    rx.center(
                        rx.vstack(
                            rx.icon("lock", size=48, color="gray.400"),
                            rx.heading("Для работы с задачами необходимо войти в систему", size="4"),
                            rx.button(
                                "Войти",
                                on_click=lambda: State.set_show_login_dialog(True),
                                size="3",
                                variant="solid"
                            ),
                            spacing="4",
                            align="center"
                        ),
                        height="300px"
                    )
                ),
                
                rx.divider(),
                
                # Добавляем пагинацию
                pagination_controls(),
                
                rx.cond(
                    State.is_authenticated & State.filtered_tasks.length() > 0,
                    rx.vstack(
                        rx.foreach(State.get_paginated_tasks(), task_card),
                        spacing="4",
                        width="100%"
                    ),
                    rx.cond(
                        State.is_authenticated,
                        rx.center(
                            rx.vstack(
                                rx.icon("inbox", size=48),
                                rx.text("Нет задач", size="4"),
                                spacing="3",
                                align="center"
                            ),
                            height="300px"
                        ),
                        rx.fragment()
                    )
                ),
                
                spacing="5",
                width="100%",
                padding_y="5"
            ),
            size="4"
        ),
        on_mount=State.on_load
    )


# Custom theme styles
DARK_MODE_STYLES = {
    "body": {"background_color": "var(--gray-12)", "color": "var(--gray-1)"},
    ".card": {"background_color": "var(--gray-9)", "border_color": "var(--gray-8)"},
    "input, select, textarea": {"background_color": "var(--gray-8)", "border_color": "var(--gray-7)", "color": "var(--gray-1)"},
    ".badge": {"background_color": "var(--gray-7) !important", "color": "white"},
    "button": {"background_color": "var(--blue-9)", "color": "white"},
    "[data-radix-popper-content-wrapper]": {"background_color": "var(--gray-9)", "color": "white"},
    ".accordion-content": {"background_color": "var(--gray-9)", "color": "white"},
    ".progress": {"background_color": "var(--gray-7)"},
    "h1, h2, h3, h4, h5, h6, .heading": {"color": "white"},
    ".text, p, span, div": {"color": "var(--gray-3)"},
}

LIGHT_MODE_STYLES = {
    "body": {
        "background_color": "gray.50",
        "color": "gray.900"
    },
    ".card": {
        "background_color": "white",
        "border_color": "gray.200"
    },
    ".input, .select": {
        "background_color": "white",
        "border_color": "gray.300",
        "color": "gray.900"
    }
}

# Theme-based styling function
def get_theme_styles(theme: str) -> Dict[str, Dict[str, str]]:
    """Получить стили в зависимости от темы."""
    if theme == "dark":
        return DARK_MODE_STYLES
    else:
        return LIGHT_MODE_STYLES

app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
    ],
    style={
        "font_family": "Inter, sans-serif",
        "antialias": True
    },
    head_components=[
        rx.script("""
            document.documentElement.classList.toggle('dark', localStorage.getItem('theme') === 'dark');
        """)
    ]
)

# Добавляем динамические стили для темы
def apply_theme_styles():
    """Применить стили в зависимости от текущей темы."""
    return rx.cond(
        State.theme == "dark",
        rx.box(style=DARK_MODE_STYLES),
        rx.box(style=LIGHT_MODE_STYLES)
    )
app.add_page(index, route="/", title="Управление задачами")
