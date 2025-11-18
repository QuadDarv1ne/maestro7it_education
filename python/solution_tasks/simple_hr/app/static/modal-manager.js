/**
 * Modal Manager для Simple HR
 * Упрощенная работа с Bootstrap модальными окнами
 */
class ModalManager {
    constructor() {
        this.modals = new Map();
        this.container = null;
        this.init();
    }

    /**
     * Инициализация
     */
    init() {
        // Создать контейнер для модальных окон
        this.container = document.createElement('div');
        this.container.id = 'modal-container';
        document.body.appendChild(this.container);
    }

    /**
     * Создать модальное окно
     */
    create(id, options = {}) {
        const {
            title = 'Модальное окно',
            content = '',
            footer = null,
            size = '', // '', 'sm', 'lg', 'xl'
            centered = false,
            scrollable = false,
            backdrop = true,
            keyboard = true,
            closeButton = true,
            onShow = null,
            onHide = null,
            onShown = null,
            onHidden = null
        } = options;

        // Проверить существование
        if (this.modals.has(id)) {
            console.warn(`Modal ${id} already exists`);
            return this.modals.get(id);
        }

        // Создать HTML
        const modalHTML = `
            <div class="modal fade" id="${id}" tabindex="-1" aria-labelledby="${id}-label" aria-hidden="true" data-bs-backdrop="${backdrop}" data-bs-keyboard="${keyboard}">
                <div class="modal-dialog ${size ? 'modal-' + size : ''} ${centered ? 'modal-dialog-centered' : ''} ${scrollable ? 'modal-dialog-scrollable' : ''}">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="${id}-label">${title}</h5>
                            ${closeButton ? '<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>' : ''}
                        </div>
                        <div class="modal-body">
                            ${content}
                        </div>
                        ${footer !== null ? `<div class="modal-footer">${footer}</div>` : ''}
                    </div>
                </div>
            </div>
        `;

        // Добавить в контейнер
        this.container.insertAdjacentHTML('beforeend', modalHTML);

        // Получить элемент
        const element = document.getElementById(id);

        // Создать экземпляр Bootstrap Modal
        const bsModal = new bootstrap.Modal(element, {
            backdrop: backdrop,
            keyboard: keyboard
        });

        // Добавить обработчики событий
        if (onShow) element.addEventListener('show.bs.modal', onShow);
        if (onShown) element.addEventListener('shown.bs.modal', onShown);
        if (onHide) element.addEventListener('hide.bs.modal', onHide);
        if (onHidden) element.addEventListener('hidden.bs.modal', onHidden);

        // Сохранить ссылки
        this.modals.set(id, { element, bsModal });

        return { element, bsModal };
    }

    /**
     * Показать модальное окно
     */
    show(id) {
        const modal = this.modals.get(id);
        if (modal) {
            modal.bsModal.show();
        } else {
            console.error(`Modal ${id} not found`);
        }
    }

    /**
     * Скрыть модальное окно
     */
    hide(id) {
        const modal = this.modals.get(id);
        if (modal) {
            modal.bsModal.hide();
        } else {
            console.error(`Modal ${id} not found`);
        }
    }

    /**
     * Уничтожить модальное окно
     */
    destroy(id) {
        const modal = this.modals.get(id);
        if (modal) {
            modal.bsModal.dispose();
            modal.element.remove();
            this.modals.delete(id);
        }
    }

    /**
     * Обновить заголовок
     */
    setTitle(id, title) {
        const modal = this.modals.get(id);
        if (modal) {
            const titleElement = modal.element.querySelector('.modal-title');
            if (titleElement) {
                titleElement.textContent = title;
            }
        }
    }

    /**
     * Обновить содержимое
     */
    setContent(id, content) {
        const modal = this.modals.get(id);
        if (modal) {
            const bodyElement = modal.element.querySelector('.modal-body');
            if (bodyElement) {
                bodyElement.innerHTML = content;
            }
        }
    }

    /**
     * Обновить футер
     */
    setFooter(id, footer) {
        const modal = this.modals.get(id);
        if (modal) {
            let footerElement = modal.element.querySelector('.modal-footer');
            
            if (!footerElement && footer) {
                // Создать футер если его нет
                const content = modal.element.querySelector('.modal-content');
                footerElement = document.createElement('div');
                footerElement.className = 'modal-footer';
                content.appendChild(footerElement);
            }
            
            if (footerElement) {
                footerElement.innerHTML = footer;
            }
        }
    }

    /**
     * Модальное окно подтверждения
     */
    confirm(options = {}) {
        const {
            title = 'Подтверждение',
            message = 'Вы уверены?',
            confirmText = 'Да',
            cancelText = 'Нет',
            confirmClass = 'btn-primary',
            cancelClass = 'btn-secondary',
            onConfirm = null,
            onCancel = null
        } = options;

        return new Promise((resolve, reject) => {
            const modalId = 'confirm-modal-' + Date.now();

            const footer = `
                <button type="button" class="btn ${cancelClass}" data-bs-dismiss="modal">${cancelText}</button>
                <button type="button" class="btn ${confirmClass}" id="${modalId}-confirm">${confirmText}</button>
            `;

            this.create(modalId, {
                title,
                content: `<p>${message}</p>`,
                footer,
                size: 'sm',
                centered: true,
                onShown: () => {
                    const confirmBtn = document.getElementById(`${modalId}-confirm`);
                    confirmBtn.addEventListener('click', () => {
                        if (onConfirm) onConfirm();
                        this.hide(modalId);
                        resolve(true);
                    });
                },
                onHidden: () => {
                    if (onCancel) onCancel();
                    this.destroy(modalId);
                }
            });

            this.show(modalId);
        });
    }

    /**
     * Модальное окно предупреждения
     */
    alert(options = {}) {
        const {
            title = 'Внимание',
            message = '',
            buttonText = 'OK',
            buttonClass = 'btn-primary',
            icon = 'info',
            onClose = null
        } = options;

        return new Promise((resolve) => {
            const modalId = 'alert-modal-' + Date.now();

            const icons = {
                info: '<i class="fas fa-info-circle text-info fa-3x mb-3"></i>',
                success: '<i class="fas fa-check-circle text-success fa-3x mb-3"></i>',
                warning: '<i class="fas fa-exclamation-triangle text-warning fa-3x mb-3"></i>',
                danger: '<i class="fas fa-times-circle text-danger fa-3x mb-3"></i>'
            };

            const content = `
                <div class="text-center">
                    ${icons[icon] || icons.info}
                    <p>${message}</p>
                </div>
            `;

            const footer = `
                <button type="button" class="btn ${buttonClass}" data-bs-dismiss="modal">${buttonText}</button>
            `;

            this.create(modalId, {
                title,
                content,
                footer,
                size: 'sm',
                centered: true,
                onHidden: () => {
                    if (onClose) onClose();
                    this.destroy(modalId);
                    resolve(true);
                }
            });

            this.show(modalId);
        });
    }

    /**
     * Модальное окно с формой
     */
    form(options = {}) {
        const {
            title = 'Форма',
            fields = [],
            submitText = 'Отправить',
            cancelText = 'Отмена',
            submitClass = 'btn-primary',
            cancelClass = 'btn-secondary',
            onSubmit = null,
            onCancel = null
        } = options;

        return new Promise((resolve, reject) => {
            const modalId = 'form-modal-' + Date.now();
            const formId = modalId + '-form';

            // Создать HTML полей формы
            const fieldsHTML = fields.map(field => {
                const {
                    name,
                    label,
                    type = 'text',
                    placeholder = '',
                    required = false,
                    value = '',
                    options = []
                } = field;

                let inputHTML = '';

                switch (type) {
                    case 'select':
                        inputHTML = `
                            <select class="form-select" name="${name}" ${required ? 'required' : ''}>
                                ${options.map(opt => `<option value="${opt.value}">${opt.label}</option>`).join('')}
                            </select>
                        `;
                        break;
                    case 'textarea':
                        inputHTML = `
                            <textarea class="form-control" name="${name}" placeholder="${placeholder}" ${required ? 'required' : ''}>${value}</textarea>
                        `;
                        break;
                    case 'checkbox':
                        inputHTML = `
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" name="${name}" ${value ? 'checked' : ''}>
                                <label class="form-check-label">${label}</label>
                            </div>
                        `;
                        break;
                    default:
                        inputHTML = `
                            <input type="${type}" class="form-control" name="${name}" placeholder="${placeholder}" value="${value}" ${required ? 'required' : ''}>
                        `;
                }

                return `
                    <div class="mb-3">
                        ${type !== 'checkbox' ? `<label class="form-label">${label}${required ? '<span class="text-danger">*</span>' : ''}</label>` : ''}
                        ${inputHTML}
                    </div>
                `;
            }).join('');

            const content = `
                <form id="${formId}" novalidate>
                    ${fieldsHTML}
                </form>
            `;

            const footer = `
                <button type="button" class="btn ${cancelClass}" data-bs-dismiss="modal">${cancelText}</button>
                <button type="submit" form="${formId}" class="btn ${submitClass}">${submitText}</button>
            `;

            this.create(modalId, {
                title,
                content,
                footer,
                centered: true,
                onShown: () => {
                    const form = document.getElementById(formId);
                    form.addEventListener('submit', async (e) => {
                        e.preventDefault();
                        
                        if (!form.checkValidity()) {
                            form.classList.add('was-validated');
                            return;
                        }

                        const formData = new FormData(form);
                        const data = Object.fromEntries(formData);

                        if (onSubmit) {
                            try {
                                await onSubmit(data);
                                this.hide(modalId);
                                resolve(data);
                            } catch (error) {
                                console.error('Form submit error:', error);
                                reject(error);
                            }
                        } else {
                            this.hide(modalId);
                            resolve(data);
                        }
                    });
                },
                onHidden: () => {
                    if (onCancel) onCancel();
                    this.destroy(modalId);
                }
            });

            this.show(modalId);
        });
    }

    /**
     * Модальное окно с загрузкой
     */
    loading(options = {}) {
        const {
            title = 'Загрузка...',
            message = 'Пожалуйста, подождите',
            spinner = 'border'
        } = options;

        const modalId = 'loading-modal-' + Date.now();

        const content = `
            <div class="text-center py-4">
                <div class="spinner-${spinner} text-primary mb-3" role="status" style="width: 3rem; height: 3rem;">
                    <span class="visually-hidden">Загрузка...</span>
                </div>
                <p class="mb-0">${message}</p>
            </div>
        `;

        this.create(modalId, {
            title,
            content,
            size: 'sm',
            centered: true,
            backdrop: 'static',
            keyboard: false,
            closeButton: false
        });

        this.show(modalId);

        return modalId;
    }

    /**
     * Закрыть окно загрузки
     */
    closeLoading(modalId) {
        this.hide(modalId);
        setTimeout(() => {
            this.destroy(modalId);
        }, 300);
    }
}

// Глобальный экземпляр
const modalManager = new ModalManager();

// Экспорт
window.modalManager = modalManager;
window.ModalManager = ModalManager;
