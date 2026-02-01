"""Система управления задачами на основе Reflex 0.8.26."""

import reflex as rx
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum
from pydantic import BaseModel, Field


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

    class Config:
        arbitrary_types_allowed = True


class State(rx.State):
    """Состояние приложения управления задачами."""
    
    # Список задач
    tasks: List[Task] = []
    
    # Поля для новой задачи
    new_task_title: str = ""
    new_task_description: str = ""
    new_task_priority: str = Priority.NORMAL
    new_task_due_date: str = ""
    new_task_assigned_to: str = ""
    
    # Поля для редактирования
    editing_task_id: Optional[int] = None
    edit_title: str = ""
    edit_description: str = ""
    edit_priority: str = Priority.NORMAL
    edit_due_date: str = ""
    edit_assigned_to: str = ""
    show_edit_dialog: bool = False
    
    # Поля для фильтрации и сортировки
    filter_status: str = "All"
    filter_priority: str = "All"
    search_query: str = ""
    sort_by: str = "created_at"
    sort_ascending: bool = False
    
    # Счетчик для генерации ID
    task_counter: int = 0
    
    # UI состояние
    show_completed: bool = True
    is_loading: bool = False
    
    @rx.var
    def filtered_tasks(self) -> List[Task]:
        """Получить отфильтрованные и отсортированные задачи."""
        result = self.tasks
        
        if self.search_query.strip():
            query = self.search_query.lower()
            result = [
                task for task in result 
                if query in task.title.lower() 
                or query in task.description.lower()
                or query in task.assigned_to.lower()
            ]
        
        if self.filter_status != "All":
            result = [task for task in result if task.status == self.filter_status]
        
        if self.filter_priority != "All":
            result = [task for task in result if task.priority == self.filter_priority]
        
        if not self.show_completed:
            result = [task for task in result if task.status != TaskStatus.COMPLETED]
        
        if self.sort_by == "priority":
            priority_order = {Priority.CRITICAL: 0, Priority.HIGH: 1, Priority.NORMAL: 2, Priority.LOW: 3}
            result.sort(key=lambda t: priority_order.get(t.priority, 4), reverse=not self.sort_ascending)
        elif self.sort_by == "due_date":
            result.sort(key=lambda t: t.due_date or "9999-12-31", reverse=not self.sort_ascending)
        elif self.sort_by == "title":
            result.sort(key=lambda t: t.title.lower(), reverse=not self.sort_ascending)
        elif self.sort_by == "status":
            result.sort(key=lambda t: t.status, reverse=not self.sort_ascending)
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
                          and t.status not in [TaskStatus.COMPLETED, TaskStatus.CANCELLED])
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
            due_date=self.new_task_due_date if self.new_task_due_date else None,
            assigned_to=self.new_task_assigned_to.strip()
        )
        
        self.tasks.append(task)
        self.task_counter += 1
        self.clear_form()
    
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
    
    def update_task_status(self, task_id: int, new_status: str):
        """Обновить статус задачи."""
        for task in self.tasks:
            if task.id == task_id:
                task.status = new_status
                task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break
    
    def toggle_task_completion(self, task_id: int):
        """Переключить статус выполнения задачи."""
        for task in self.tasks:
            if task.id == task_id:
                task.status = TaskStatus.COMPLETED if task.status != TaskStatus.COMPLETED else TaskStatus.PENDING
                task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break
    
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
                task.due_date = self.edit_due_date if self.edit_due_date else None
                task.assigned_to = self.edit_assigned_to.strip()
                task.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                break
        
        self.close_edit_dialog()
    
    def clear_all_filters(self):
        """Сбросить все фильтры."""
        self.filter_status = "All"
        self.filter_priority = "All"
        self.search_query = ""
    
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
            
            rx.flex(
                rx.select(
                    [Priority.LOW, Priority.NORMAL, Priority.HIGH, Priority.CRITICAL],
                    placeholder="Приоритет",
                    value=State.new_task_priority,
                    on_change=State.set_new_task_priority,
                    width="100%"
                ),
                
                rx.input(
                    type="date",
                    placeholder="Срок",
                    value=State.new_task_due_date,
                    on_change=State.set_new_task_due_date,
                    width="100%"
                ),
                
                rx.input(
                    placeholder="Исполнитель",
                    value=State.new_task_assigned_to,
                    on_change=State.set_new_task_assigned_to,
                    width="100%"
                ),
                
                spacing="2",
                width="100%",
                direction="row",
                wrap="wrap"
            ),
            
            rx.flex(
                rx.button(
                    rx.icon("plus", size=16),
                    "Добавить",
                    on_click=State.add_task,
                    size="2",
                ),
                rx.button(
                    "Очистить",
                    on_click=State.clear_form,
                    size="2",
                    variant="soft",
                    color_scheme="gray"
                ),
                spacing="2",
                justify="end",
                width="100%"
            ),
            
            spacing="3",
            width="100%"
        ),
        width="100%"
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
                rx.input(
                    type="date",
                    value=State.edit_due_date,
                    on_change=State.set_edit_due_date,
                    width="100%"
                ),
                rx.input(
                    value=State.edit_assigned_to,
                    on_change=State.set_edit_assigned_to,
                    placeholder="Исполнитель",
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
    """Карточка задачи."""
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
    
    return rx.card(
        rx.vstack(
            rx.flex(
                rx.badge(
                    task.priority,
                    color_scheme=priority_colors.get(task.priority, "gray"),
                    variant="solid",
                    size="1"
                ),
                rx.badge(
                    task.status,
                    color_scheme=status_colors.get(task.status, "gray"),
                    variant="soft",
                    size="1"
                ),
                rx.spacer(),
                rx.icon_button(
                    rx.icon("pencil", size=16),
                    on_click=lambda: State.open_edit_dialog(task.id),
                    color_scheme="blue",
                    variant="soft",
                    size="2"
                ),
                rx.icon_button(
                    rx.icon("trash-2", size=16),
                    on_click=lambda: State.delete_task(task.id),
                    color_scheme="red",
                    variant="soft",
                    size="2"
                ),
                width="100%",
                align="center",
                spacing="2"
            ),
            
            rx.heading(task.title, size="4"),
            
            rx.cond(
                task.description != "",
                rx.text(task.description, size="2", color_scheme="gray"),
                rx.fragment()
            ),
            
            rx.flex(
                rx.cond(
                    task.assigned_to != "",
                    rx.flex(
                        rx.icon("user", size=14),
                        rx.text(task.assigned_to, size="1"),
                        spacing="1",
                        align="center"
                    ),
                    rx.fragment()
                ),
                rx.spacer(),
                rx.cond(
                    task.due_date != None,
                    rx.flex(
                        rx.icon("calendar", size=14),
                        rx.text(task.due_date, size="1"),
                        spacing="1",
                        align="center"
                    ),
                    rx.fragment()
                ),
                width="100%",
                align="center"
            ),
            
            rx.divider(),
            
            rx.flex(
                rx.button(
                    rx.icon("check", size=14),
                    on_click=lambda: State.toggle_task_completion(task.id),
                    size="1"
                ),
                rx.button(
                    "В работе",
                    on_click=lambda: State.update_task_status(task.id, TaskStatus.IN_PROGRESS),
                    size="1"
                ),
                rx.button(
                    "Отменить",
                    on_click=lambda: State.update_task_status(task.id, TaskStatus.CANCELLED),
                    size="1"
                ),
                width="100%",
                spacing="2",
                wrap="wrap"
            ),
            
            spacing="3",
            width="100%"
        ),
        width="100%"
    )


def stats_panel() -> rx.Component:
    """Панель статистики."""
    return rx.card(
        rx.flex(
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
            spacing="4",
            width="100%",
            justify="between",
            align="center",
            wrap="wrap"
        ),
        width="100%"
    )


def filter_controls() -> rx.Component:
    """Элементы управления фильтрами."""
    return rx.card(
        rx.vstack(
            rx.input(
                placeholder="🔍 Поиск...",
                value=State.search_query,
                on_change=State.set_search_query,
                width="100%",
                size="2"
            ),
            
            rx.flex(
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
                
                rx.flex(
                    rx.select(
                        ["created_at", "due_date", "priority", "title", "status"],
                        value=State.sort_by,
                        on_change=State.set_sort_by,
                        width="100%"
                    ),
                    rx.icon_button(
                        rx.cond(
                            State.sort_ascending,
                            rx.icon("arrow-up", size=16),
                            rx.icon("arrow-down", size=16)
                        ),
                        on_click=State.toggle_sort_direction,
                        variant="soft",
                        size="2"
                    ),
                    spacing="2",
                    width="100%",
                    align="center"
                ),
                
                spacing="2",
                width="100%",
                direction="row",
                wrap="wrap"
            ),
            
            rx.flex(
                rx.switch(
                    checked=State.show_completed,
                    on_change=State.set_show_completed
                ),
                rx.text("Показать выполненные", size="2"),
                rx.spacer(),
                rx.button(
                    "Сбросить фильтры",
                    on_click=State.clear_all_filters,
                    variant="soft",
                    size="2"
                ),
                width="100%",
                align="center",
                spacing="2"
            ),
            
            spacing="3",
            width="100%"
        ),
        width="100%"
    )


def index() -> rx.Component:
    """Главная страница."""
    return rx.box(
        rx.color_mode.button(position="top-right"),
        edit_dialog(),
        rx.container(
            rx.vstack(
                rx.heading("📋 Управление задачами", size="8", align="center"),
                stats_panel(),
                task_form(),
                filter_controls(),
                rx.divider(),
                
                rx.cond(
                    State.filtered_tasks.length() > 0,
                    rx.flex(
                        rx.foreach(State.filtered_tasks, task_card),
                        spacing="3",
                        width="100%",
                        direction="row",
                        wrap="wrap"
                    ),
                    rx.center(
                        rx.vstack(
                            rx.icon("inbox", size=48),
                            rx.text("Нет задач", size="4"),
                            spacing="3",
                            align="center"
                        ),
                        height="200px"
                    )
                ),
                
                spacing="5",
                width="100%",
                padding_y="5"
            ),
            size="4"
        )
    )


app = rx.App()
app.add_page(index, route="/", title="Управление задачами")