// Управление задачами - улучшенная версия
class TaskManager {
    constructor() {
        this.tasks = this.loadTasks();
        this.currentFilter = 'all';
        this.currentView = 'list';
        this.searchQuery = '';
        this.sortBy = 'dateNew';
        this.init();
    }

    init() {
        this.updateCurrentDate();
        this.renderTasks();
        this.updateStats();
        this.attachEventListeners();
        this.startAutoSave();
    }

    attachEventListeners() {
        const taskInput = document.getElementById('taskInput');
        const addBtn = document.getElementById('addTaskBtn');
        const searchInput = document.getElementById('searchInput');
        const sortSelect = document.getElementById('sortSelect');
        const charCounter = document.getElementById('charCounter');

        // Добавление задачи
        addBtn.addEventListener('click', () => this.addTask());
        taskInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.addTask();
            }
        });

        // Счетчик символов
        taskInput.addEventListener('input', (e) => {
            const length = e.target.value.length;
            charCounter.textContent = `${length}/150`;
            charCounter.style.color = length > 140 ? '#f44336' : '#7f8c8d';
        });

        // Фильтры
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                e.currentTarget.classList.add('active');
                this.currentFilter = e.currentTarget.dataset.filter;
                this.renderTasks();
            });
        });

        // Переключение вида
        document.querySelectorAll('.view-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
                e.currentTarget.classList.add('active');
                this.currentView = e.currentTarget.dataset.view;
                this.updateView();
            });
        });

        // Поиск
        searchInput.addEventListener('input', (e) => {
            this.searchQuery = e.target.value.toLowerCase();
            this.renderTasks();
        });

        // Сортировка
        sortSelect.addEventListener('change', (e) => {
            this.sortBy = e.target.value;
            this.renderTasks();
        });

        // Действия
        document.getElementById('clearCompletedBtn').addEventListener('click', () => this.clearCompleted());
        document.getElementById('clearAllBtn').addEventListener('click', () => this.clearAll());
        document.getElementById('exportBtn').addEventListener('click', () => this.exportTasks());

        // Модальное окно
        document.getElementById('modalCancel').addEventListener('click', () => this.hideModal());
    }

    updateCurrentDate() {
        const options = { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        };
        const dateStr = new Date().toLocaleDateString('ru-RU', options);
        document.getElementById('currentDate').textContent = dateStr;
    }

    addTask() {
        const input = document.getElementById('taskInput');
        const prioritySelect = document.getElementById('prioritySelect');
        const categorySelect = document.getElementById('categorySelect');
        const dueDateInput = document.getElementById('dueDateInput');
        const text = input.value.trim();

        if (text === '') {
            this.showNotification('⚠️ Пожалуйста, введите текст задачи', 'warning');
            input.focus();
            return;
        }

        const task = {
            id: Date.now(),
            text: text,
            completed: false,
            priority: prioritySelect.value,
            category: categorySelect.value,
            dueDate: dueDateInput.value || null,
            createdAt: new Date().toISOString(),
            completedAt: null
        };

        this.tasks.unshift(task);
        this.saveTasks();
        this.renderTasks();
        this.updateStats();

        // Очистка формы
        input.value = '';
        prioritySelect.value = 'medium';
        categorySelect.value = 'work';
        dueDateInput.value = '';
        document.getElementById('charCounter').textContent = '0/150';

        this.showNotification('✅ Задача успешно добавлена!', 'success');
        
        // Анимация добавления
        const firstTask = document.querySelector('.task-item');
        if (firstTask) {
            firstTask.style.animation = 'none';
            setTimeout(() => {
                firstTask.style.animation = 'slideIn 0.3s ease-out';
            }, 10);
        }
    }

    toggleTask(id) {
        const task = this.tasks.find(t => t.id === id);
        if (task) {
            task.completed = !task.completed;
            task.completedAt = task.completed ? new Date().toISOString() : null;
            this.saveTasks();
            this.renderTasks();
            this.updateStats();
            
            if (task.completed) {
                this.showNotification('🎉 Отличная работа! Задача выполнена!', 'success');
                this.celebrateCompletion();
            } else {
                this.showNotification('↩️ Задача возвращена в активные', 'info');
            }
        }
    }

    celebrateCompletion() {
        // Простая анимация конфетти (эффект)
        const colors = ['#667eea', '#764ba2', '#4caf50', '#ff9800', '#f44336'];
        for (let i = 0; i < 20; i++) {
            setTimeout(() => {
                const confetti = document.createElement('div');
                confetti.style.cssText = `
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    width: 10px;
                    height: 10px;
                    background: ${colors[Math.floor(Math.random() * colors.length)]};
                    border-radius: 50%;
                    pointer-events: none;
                    z-index: 9999;
                    animation: confettiFall 1s ease-out forwards;
                `;
                document.body.appendChild(confetti);
                
                const angle = (Math.PI * 2 * i) / 20;
                const velocity = 100 + Math.random() * 100;
                confetti.style.setProperty('--x', Math.cos(angle) * velocity + 'px');
                confetti.style.setProperty('--y', Math.sin(angle) * velocity + 'px');
                
                setTimeout(() => confetti.remove(), 1000);
            }, i * 30);
        }
    }

    editTask(id) {
        const task = this.tasks.find(t => t.id === id);
        if (task) {
            const newText = prompt('Редактировать задачу:', task.text);
            if (newText !== null && newText.trim() !== '') {
                task.text = newText.trim();
                this.saveTasks();
                this.renderTasks();
                this.showNotification('✏️ Задача обновлена!', 'success');
            }
        }
    }

    deleteTask(id) {
        this.showModal(
            'Удаление задачи',
            'Вы уверены, что хотите удалить эту задачу?',
            () => {
                this.tasks = this.tasks.filter(t => t.id !== id);
                this.saveTasks();
                this.renderTasks();
                this.updateStats();
                this.showNotification('🗑️ Задача удалена', 'info');
            }
        );
    }

    clearCompleted() {
        const completedCount = this.tasks.filter(t => t.completed).length;
        if (completedCount === 0) {
            this.showNotification('ℹ️ Нет выполненных задач для удаления', 'info');
            return;
        }

        this.showModal(
            'Очистить выполненные',
            `Удалить ${completedCount} выполненных задач?`,
            () => {
                this.tasks = this.tasks.filter(t => !t.completed);
                this.saveTasks();
                this.renderTasks();
                this.updateStats();
                this.showNotification(`🗑️ Удалено ${completedCount} задач`, 'success');
            }
        );
    }

    clearAll() {
        if (this.tasks.length === 0) {
            this.showNotification('ℹ️ Список задач уже пуст', 'info');
            return;
        }

        this.showModal(
            'Удалить все задачи',
            'Это действие удалит все задачи без возможности восстановления!',
            () => {
                const count = this.tasks.length;
                this.tasks = [];
                this.saveTasks();
                this.renderTasks();
                this.updateStats();
                this.showNotification(`🗑️ Удалено ${count} задач`, 'success');
            }
        );
    }

    exportTasks() {
        if (this.tasks.length === 0) {
            this.showNotification('ℹ️ Нет задач для экспорта', 'info');
            return;
        }

        const dataStr = JSON.stringify(this.tasks, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `TaskFlow_${new Date().toISOString().split('T')[0]}.json`;
        link.click();
        URL.revokeObjectURL(url);
        
        this.showNotification('📥 Задачи экспортированы!', 'success');
    }

    filterTasks() {
        let filtered = this.tasks;
        const today = new Date().toISOString().split('T')[0];

        // Применяем фильтр
        switch (this.currentFilter) {
            case 'active':
                filtered = filtered.filter(t => !t.completed);
                break;
            case 'completed':
                filtered = filtered.filter(t => t.completed);
                break;
            case 'high':
                filtered = filtered.filter(t => t.priority === 'high' && !t.completed);
                break;
            case 'today':
                filtered = filtered.filter(t => t.dueDate === today && !t.completed);
                break;
        }

        // Применяем поиск
        if (this.searchQuery) {
            filtered = filtered.filter(t => 
                t.text.toLowerCase().includes(this.searchQuery) ||
                this.getCategoryLabel(t.category).toLowerCase().includes(this.searchQuery)
            );
        }

        return filtered;
    }

    sortTasks(tasks) {
        const sorted = [...tasks];
        
        switch (this.sortBy) {
            case 'dateNew':
                sorted.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
                break;
            case 'dateOld':
                sorted.sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt));
                break;
            case 'priority':
                const priorityOrder = { high: 0, medium: 1, low: 2 };
                sorted.sort((a, b) => priorityOrder[a.priority] - priorityOrder[b.priority]);
                break;
            case 'alphabetical':
                sorted.sort((a, b) => a.text.localeCompare(b.text));
                break;
            case 'dueDate':
                sorted.sort((a, b) => {
                    if (!a.dueDate) return 1;
                    if (!b.dueDate) return -1;
                    return new Date(a.dueDate) - new Date(b.dueDate);
                });
                break;
        }

        return sorted;
    }

    renderTasks() {
        const taskList = document.getElementById('taskList');
        const filteredTasks = this.filterTasks();
        const sortedTasks = this.sortTasks(filteredTasks);
        
        document.getElementById('visibleTaskCount').textContent = sortedTasks.length;

        if (sortedTasks.length === 0) {
            taskList.innerHTML = `
                <div class="empty-state">
                    ${this.searchQuery ? '🔍 Задачи не найдены' : '📝 Нет задач для отображения'}
                    <br><small style="opacity: 0.8; font-size: 1rem; margin-top: 10px; display: block;">
                        ${!this.searchQuery ? 'Создайте свою первую задачу!' : 'Попробуйте другой запрос'}
                    </small>
                </div>
            `;
            return;
        }

        taskList.innerHTML = sortedTasks.map(task => {
            const isOverdue = this.isOverdue(task);
            const dueDateFormatted = task.dueDate ? this.formatDate(task.dueDate) : null;
            
            return `
                <div class="task-item ${task.completed ? 'completed' : ''} priority-${task.priority} ${isOverdue ? 'overdue' : ''}" data-id="${task.id}">
                    <input 
                        type="checkbox" 
                        class="task-checkbox" 
                        ${task.completed ? 'checked' : ''}
                        onchange="taskManager.toggleTask(${task.id})"
                    >
                    <div class="task-content">
                        <div class="task-text">${this.escapeHtml(task.text)}</div>
                        <div class="task-meta">
                            <span class="meta-badge priority-badge priority-${task.priority}">
                                ${this.getPriorityIcon(task.priority)} ${this.getPriorityLabel(task.priority)}
                            </span>
                            <span class="meta-badge category-badge">
                                ${this.getCategoryIcon(task.category)} ${this.getCategoryLabel(task.category)}
                            </span>
                            ${dueDateFormatted ? `
                                <span class="meta-badge date-badge ${isOverdue ? 'overdue' : ''}">
                                    📅 ${dueDateFormatted}
                                    ${isOverdue ? ' (просрочено)' : ''}
                                </span>
                            ` : ''}
                        </div>
                    </div>
                    <div class="task-actions">
                        <button class="task-btn edit-btn" onclick="taskManager.editTask(${task.id})">
                            ✏️ Изменить
                        </button>
                        <button class="task-btn delete-btn" onclick="taskManager.deleteTask(${task.id})">
                            🗑️ Удалить
                        </button>
                    </div>
                </div>
            `;
        }).join('');
    }

    updateView() {
        const taskList = document.getElementById('taskList');
        taskList.className = `task-list ${this.currentView}-view`;
    }

    updateStats() {
        const total = this.tasks.length;
        const active = this.tasks.filter(t => !t.completed).length;
        const completed = this.tasks.filter(t => t.completed).length;
        const productivity = total > 0 ? Math.round((completed / total) * 100) : 0;

        this.animateNumber('totalTasks', total);
        this.animateNumber('activeTasks', active);
        this.animateNumber('completedTasks', completed);
        
        const productivityElement = document.getElementById('productivityScore');
        this.animateNumber('productivityScore', productivity, '%');

        // Обновляем прогресс-бары
        this.updateProgressBar('totalProgress', total > 0 ? 100 : 0);
        this.updateProgressBar('activeProgress', total > 0 ? (active / total) * 100 : 0);
        this.updateProgressBar('completedProgress', total > 0 ? (completed / total) * 100 : 0);
        this.updateProgressBar('productivityProgress', productivity);
    }

    updateProgressBar(id, percentage) {
        const bar = document.getElementById(id);
        if (bar) {
            bar.style.width = percentage + '%';
        }
    }

    animateNumber(elementId, targetValue, suffix = '') {
        const element = document.getElementById(elementId);
        const currentValue = parseInt(element.textContent) || 0;
        const duration = 500;
        const steps = 20;
        const stepValue = (targetValue - currentValue) / steps;
        let currentStep = 0;

        const timer = setInterval(() => {
            currentStep++;
            const newValue = Math.round(currentValue + (stepValue * currentStep));
            element.textContent = newValue + suffix;

            if (currentStep >= steps) {
                element.textContent = targetValue + suffix;
                clearInterval(timer);
            }
        }, duration / steps);
    }

    isOverdue(task) {
        if (!task.dueDate || task.completed) return false;
        const today = new Date().toISOString().split('T')[0];
        return task.dueDate < today;
    }

    formatDate(dateString) {
        const date = new Date(dateString + 'T00:00:00');
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const taskDate = new Date(date);
        taskDate.setHours(0, 0, 0, 0);
        
        const diffTime = taskDate - today;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays === 0) return 'Сегодня';
        if (diffDays === 1) return 'Завтра';
        if (diffDays === -1) return 'Вчера';
        if (diffDays > 0 && diffDays <= 7) return `Через ${diffDays} дн.`;
        if (diffDays < 0 && diffDays >= -7) return `${Math.abs(diffDays)} дн. назад`;
        
        return date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' });
    }

    getPriorityIcon(priority) {
        const icons = { low: '🟢', medium: '🟡', high: '🔴' };
        return icons[priority] || '⚪';
    }

    getPriorityLabel(priority) {
        const labels = { low: 'Низкий', medium: 'Средний', high: 'Высокий' };
        return labels[priority] || priority;
    }

    getCategoryIcon(category) {
        const icons = {
            work: '💼',
            personal: '🏠',
            shopping: '🛒',
            health: '💪',
            study: '📚',
            other: '📌'
        };
        return icons[category] || '📌';
    }

    getCategoryLabel(category) {
        const labels = {
            work: 'Работа',
            personal: 'Личное',
            shopping: 'Покупки',
            health: 'Здоровье',
            study: 'Обучение',
            other: 'Другое'
        };
        return labels[category] || category;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    showModal(title, message, onConfirm) {
        const modal = document.getElementById('confirmModal');
        document.getElementById('modalTitle').textContent = title;
        document.getElementById('modalMessage').textContent = message;
        
        modal.classList.add('active');
        
        const confirmBtn = document.getElementById('modalConfirm');
        const newConfirmBtn = confirmBtn.cloneNode(true);
        confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);
        
        newConfirmBtn.addEventListener('click', () => {
            onConfirm();
            this.hideModal();
        });
    }

    hideModal() {
        document.getElementById('confirmModal').classList.remove('active');
    }

    showNotification(message, type = 'info') {
        const colors = {
            success: '#4caf50',
            error: '#f44336',
            warning: '#ff9800',
            info: '#2196f3'
        };

        const notification = document.createElement('div');
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 16px 24px;
            background: ${colors[type]};
            color: white;
            border-radius: 12px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);
            z-index: 10000;
            font-weight: 500;
            font-size: 1rem;
            max-width: 350px;
            animation: slideInRight 0.3s ease-out;
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        }, 3500);
    }

    startAutoSave() {
        setInterval(() => {
            this.saveTasks();
        }, 60000); // Автосохранение каждую минуту
    }

    saveTasks() {
        localStorage.setItem('taskFlowTasks', JSON.stringify(this.tasks));
    }

    loadTasks() {
        const saved = localStorage.getItem('taskFlowTasks');
        return saved ? JSON.parse(saved) : [];
    }
}

// Добавляем CSS для анимаций
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
    
    @keyframes confettiFall {
        to {
            transform: translate(var(--x), var(--y));
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Инициализация приложения
const taskManager = new TaskManager();

// Приветственное сообщение
if (taskManager.tasks.length === 0) {
    setTimeout(() => {
        taskManager.showNotification('👋 Добро пожаловать в Task Flow! Создайте свою первую задачу', 'info');
    }, 1000);
} else {
    setTimeout(() => {
        const active = taskManager.tasks.filter(t => !t.completed).length;
        if (active > 0) {
            taskManager.showNotification(`💪 У вас ${active} активных задач. Продолжайте в том же духе!`, 'info');
        }
    }, 1000);
}