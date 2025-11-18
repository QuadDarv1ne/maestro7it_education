/**
 * Enhanced Form Validation for Simple HR
 */
class FormValidator {
    constructor(formElement, options = {}) {
        this.form = formElement;
        this.options = {
            validateOnBlur: true,
            validateOnInput: false,
            showErrors: true,
            scrollToError: true,
            errorClass: 'is-invalid',
            successClass: 'is-valid',
            ...options
        };
        
        this.validators = {};
        this.customMessages = {};
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupDefaultValidators();
    }

    setupEventListeners() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        
        if (this.options.validateOnBlur) {
            this.form.querySelectorAll('input, select, textarea').forEach(field => {
                field.addEventListener('blur', () => this.validateField(field));
            });
        }
        
        if (this.options.validateOnInput) {
            this.form.querySelectorAll('input, select, textarea').forEach(field => {
                field.addEventListener('input', () => this.validateField(field));
            });
        }
    }

    setupDefaultValidators() {
        // Email validator
        this.addValidator('email', (value) => {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(value);
        }, 'Введите корректный email адрес');

        // Phone validator
        this.addValidator('phone', (value) => {
            const phoneRegex = /^[\d\s\-\+\(\)]+$/;
            return phoneRegex.test(value) && value.replace(/\D/g, '').length >= 10;
        }, 'Введите корректный номер телефона');

        // URL validator
        this.addValidator('url', (value) => {
            try {
                new URL(value);
                return true;
            } catch {
                return false;
            }
        }, 'Введите корректный URL');

        // Min length validator
        this.addValidator('minlength', (value, minLength) => {
            return value.length >= parseInt(minLength);
        }, (value, minLength) => `Минимальная длина: ${minLength} символов`);

        // Max length validator
        this.addValidator('maxlength', (value, maxLength) => {
            return value.length <= parseInt(maxLength);
        }, (value, maxLength) => `Максимальная длина: ${maxLength} символов`);

        // Min value validator
        this.addValidator('min', (value, min) => {
            return parseFloat(value) >= parseFloat(min);
        }, (value, min) => `Минимальное значение: ${min}`);

        // Max value validator
        this.addValidator('max', (value, max) => {
            return parseFloat(value) <= parseFloat(max);
        }, (value, max) => `Максимальное значение: ${max}`);

        // Pattern validator
        this.addValidator('pattern', (value, pattern) => {
            const regex = new RegExp(pattern);
            return regex.test(value);
        }, 'Значение не соответствует требуемому формату');

        // Required validator
        this.addValidator('required', (value) => {
            return value.trim().length > 0;
        }, 'Это поле обязательно для заполнения');

        // Number validator
        this.addValidator('number', (value) => {
            return !isNaN(value) && value.trim() !== '';
        }, 'Введите числовое значение');

        // Date validator
        this.addValidator('date', (value) => {
            const date = new Date(value);
            return date instanceof Date && !isNaN(date);
        }, 'Введите корректную дату');

        // Passport validator (Russian format)
        this.addValidator('passport', (value) => {
            const passportRegex = /^\d{4}\s?\d{6}$/;
            return passportRegex.test(value);
        }, 'Введите паспорт в формате: 1234 567890');

        // SNILS validator (Russian social security number)
        this.addValidator('snils', (value) => {
            const snilsRegex = /^\d{3}-\d{3}-\d{3}\s?\d{2}$/;
            return snilsRegex.test(value);
        }, 'Введите СНИЛС в формате: 123-456-789 00');

        // INN validator (Russian tax ID)
        this.addValidator('inn', (value) => {
            const innRegex = /^\d{10}$|^\d{12}$/;
            return innRegex.test(value);
        }, 'Введите корректный ИНН (10 или 12 цифр)');
    }

    addValidator(name, validatorFn, message) {
        this.validators[name] = validatorFn;
        if (typeof message === 'string') {
            this.customMessages[name] = () => message;
        } else {
            this.customMessages[name] = message;
        }
    }

    validateField(field) {
        const value = field.value;
        const errors = [];

        // Clear previous validation state
        this.clearFieldErrors(field);

        // Skip validation if field is not required and empty
        if (!field.hasAttribute('required') && value.trim() === '') {
            return true;
        }

        // Check each validator
        for (const [validatorName, validatorFn] of Object.entries(this.validators)) {
            if (field.hasAttribute(`data-validate-${validatorName}`)) {
                const param = field.getAttribute(`data-validate-${validatorName}`);
                const isValid = param ? validatorFn(value, param) : validatorFn(value);
                
                if (!isValid) {
                    const message = typeof this.customMessages[validatorName] === 'function'
                        ? this.customMessages[validatorName](value, param)
                        : this.customMessages[validatorName];
                    errors.push(message);
                }
            }
        }

        // Check HTML5 validation
        if (field.validity && !field.validity.valid) {
            if (field.validity.valueMissing) {
                errors.push('Это поле обязательно для заполнения');
            }
            if (field.validity.typeMismatch) {
                errors.push(`Введите корректное значение для типа ${field.type}`);
            }
        }

        // Show errors or success
        if (errors.length > 0) {
            this.showFieldError(field, errors[0]);
            return false;
        } else if (value.trim() !== '') {
            this.showFieldSuccess(field);
            return true;
        }

        return true;
    }

    validateForm() {
        const fields = this.form.querySelectorAll('input, select, textarea');
        let isValid = true;
        let firstInvalidField = null;

        fields.forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
                if (!firstInvalidField) {
                    firstInvalidField = field;
                }
            }
        });

        if (!isValid && this.options.scrollToError && firstInvalidField) {
            firstInvalidField.scrollIntoView({ behavior: 'smooth', block: 'center' });
            firstInvalidField.focus();
        }

        return isValid;
    }

    handleSubmit(e) {
        if (!this.validateForm()) {
            e.preventDefault();
            
            // Show error notification
            if (this.options.showErrors) {
                this.showNotification('Пожалуйста, исправьте ошибки в форме', 'error');
            }
        }
    }

    showFieldError(field, message) {
        field.classList.remove(this.options.successClass);
        field.classList.add(this.options.errorClass);

        if (this.options.showErrors) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'invalid-feedback d-block';
            errorDiv.textContent = message;
            errorDiv.setAttribute('data-error-for', field.id || field.name);

            // Remove existing error message
            const existingError = field.parentElement.querySelector(`[data-error-for="${field.id || field.name}"]`);
            if (existingError) {
                existingError.remove();
            }

            // Insert error message
            field.parentElement.appendChild(errorDiv);
        }
    }

    showFieldSuccess(field) {
        field.classList.remove(this.options.errorClass);
        field.classList.add(this.options.successClass);
        this.clearFieldErrors(field);
    }

    clearFieldErrors(field) {
        field.classList.remove(this.options.errorClass, this.options.successClass);
        
        const errorDiv = field.parentElement.querySelector(`[data-error-for="${field.id || field.name}"]`);
        if (errorDiv) {
            errorDiv.remove();
        }
    }

    showNotification(message, type = 'info') {
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;

        // Add to toast container or create one
        let toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
            document.body.appendChild(toastContainer);
        }

        toastContainer.appendChild(toast);

        // Show toast using Bootstrap
        const bsToast = new bootstrap.Toast(toast, { autohide: true, delay: 3000 });
        bsToast.show();

        // Remove toast after hiding
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }

    reset() {
        const fields = this.form.querySelectorAll('input, select, textarea');
        fields.forEach(field => this.clearFieldErrors(field));
        this.form.reset();
    }
}

// Auto-initialize forms with data-validate attribute
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('form[data-validate]').forEach(form => {
        new FormValidator(form);
    });
});

// Export for use in other scripts
window.FormValidator = FormValidator;
