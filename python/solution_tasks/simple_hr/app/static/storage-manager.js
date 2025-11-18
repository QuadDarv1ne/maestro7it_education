/**
 * Storage Manager для Simple HR
 * Работа с localStorage и sessionStorage
 */
class StorageManager {
    constructor(prefix = 'simple_hr_') {
        this.prefix = prefix;
        this.storage = window.localStorage;
        this.sessionStorage = window.sessionStorage;
    }

    /**
     * Сохранить данные
     */
    set(key, value, options = {}) {
        const fullKey = this.prefix + key;
        const data = {
            value: value,
            timestamp: Date.now(),
            expires: options.expires || null
        };

        try {
            const storage = options.session ? this.sessionStorage : this.storage;
            storage.setItem(fullKey, JSON.stringify(data));
            return true;
        } catch (e) {
            console.error('Storage error:', e);
            return false;
        }
    }

    /**
     * Получить данные
     */
    get(key, defaultValue = null) {
        const fullKey = this.prefix + key;

        try {
            const item = this.storage.getItem(fullKey) || this.sessionStorage.getItem(fullKey);
            if (!item) return defaultValue;

            const data = JSON.parse(item);

            // Проверка истечения срока
            if (data.expires && Date.now() > data.expires) {
                this.remove(key);
                return defaultValue;
            }

            return data.value;
        } catch (e) {
            console.error('Storage error:', e);
            return defaultValue;
        }
    }

    /**
     * Удалить данные
     */
    remove(key) {
        const fullKey = this.prefix + key;
        this.storage.removeItem(fullKey);
        this.sessionStorage.removeItem(fullKey);
    }

    /**
     * Очистить все данные
     */
    clear() {
        const keys = this.keys();
        keys.forEach(key => this.remove(key));
    }

    /**
     * Получить все ключи
     */
    keys() {
        const allKeys = [...Object.keys(this.storage), ...Object.keys(this.sessionStorage)];
        return allKeys
            .filter(key => key.startsWith(this.prefix))
            .map(key => key.replace(this.prefix, ''));
    }

    /**
     * Проверить наличие ключа
     */
    has(key) {
        const fullKey = this.prefix + key;
        return this.storage.getItem(fullKey) !== null || this.sessionStorage.getItem(fullKey) !== null;
    }

    /**
     * Получить размер хранилища в байтах
     */
    size() {
        let size = 0;
        this.keys().forEach(key => {
            const fullKey = this.prefix + key;
            const item = this.storage.getItem(fullKey) || this.sessionStorage.getItem(fullKey);
            if (item) {
                size += item.length + fullKey.length;
            }
        });
        return size;
    }

    /**
     * Сохранить объект
     */
    setObject(key, obj, options = {}) {
        return this.set(key, obj, options);
    }

    /**
     * Получить объект
     */
    getObject(key, defaultValue = {}) {
        return this.get(key, defaultValue);
    }

    /**
     * Сохранить массив
     */
    setArray(key, arr, options = {}) {
        return this.set(key, arr, options);
    }

    /**
     * Получить массив
     */
    getArray(key, defaultValue = []) {
        return this.get(key, defaultValue);
    }

    /**
     * Добавить элемент в массив
     */
    pushToArray(key, value) {
        const arr = this.getArray(key);
        arr.push(value);
        return this.setArray(key, arr);
    }

    /**
     * Удалить элемент из массива
     */
    removeFromArray(key, predicate) {
        const arr = this.getArray(key);
        const filtered = arr.filter((item, index) => {
            if (typeof predicate === 'function') {
                return !predicate(item, index);
            }
            return item !== predicate;
        });
        return this.setArray(key, filtered);
    }

    /**
     * Увеличить счетчик
     */
    increment(key, amount = 1) {
        const current = this.get(key, 0);
        const newValue = (typeof current === 'number' ? current : 0) + amount;
        this.set(key, newValue);
        return newValue;
    }

    /**
     * Уменьшить счетчик
     */
    decrement(key, amount = 1) {
        return this.increment(key, -amount);
    }
}

/**
 * Cache Manager для кеширования данных с TTL
 */
class CacheManager {
    constructor(prefix = 'cache_') {
        this.storage = new StorageManager(prefix);
    }

    /**
     * Сохранить в кеш
     */
    set(key, value, ttl = 3600000) { // ttl по умолчанию 1 час
        return this.storage.set(key, value, {
            expires: Date.now() + ttl
        });
    }

    /**
     * Получить из кеша
     */
    get(key, defaultValue = null) {
        return this.storage.get(key, defaultValue);
    }

    /**
     * Получить или загрузить
     */
    async getOrFetch(key, fetchFn, ttl = 3600000) {
        const cached = this.get(key);
        if (cached !== null) {
            return cached;
        }

        try {
            const data = await fetchFn();
            this.set(key, data, ttl);
            return data;
        } catch (error) {
            console.error('Cache fetch error:', error);
            throw error;
        }
    }

    /**
     * Инвалидировать кеш
     */
    invalidate(key) {
        this.storage.remove(key);
    }

    /**
     * Очистить весь кеш
     */
    clear() {
        this.storage.clear();
    }

    /**
     * Получить статистику кеша
     */
    stats() {
        const keys = this.storage.keys();
        return {
            size: this.storage.size(),
            count: keys.length,
            keys: keys
        };
    }
}

/**
 * User Preferences Manager
 */
class PreferencesManager {
    constructor() {
        this.storage = new StorageManager('prefs_');
    }

    /**
     * Установить настройку
     */
    set(key, value) {
        return this.storage.set(key, value);
    }

    /**
     * Получить настройку
     */
    get(key, defaultValue = null) {
        return this.storage.get(key, defaultValue);
    }

    /**
     * Получить все настройки
     */
    getAll() {
        const prefs = {};
        this.storage.keys().forEach(key => {
            prefs[key] = this.storage.get(key);
        });
        return prefs;
    }

    /**
     * Сбросить настройки
     */
    reset() {
        this.storage.clear();
    }

    /**
     * Импорт настроек
     */
    import(prefs) {
        Object.entries(prefs).forEach(([key, value]) => {
            this.set(key, value);
        });
    }

    /**
     * Экспорт настроек
     */
    export() {
        return JSON.stringify(this.getAll(), null, 2);
    }
}

/**
 * Recent Items Manager
 */
class RecentItemsManager {
    constructor(maxItems = 10) {
        this.storage = new StorageManager('recent_');
        this.maxItems = maxItems;
    }

    /**
     * Добавить элемент
     */
    add(category, item) {
        const items = this.get(category);
        
        // Удалить дубликаты
        const filtered = items.filter(i => {
            if (typeof item === 'object' && item.id) {
                return i.id !== item.id;
            }
            return i !== item;
        });

        // Добавить в начало
        filtered.unshift(item);

        // Ограничить количество
        const limited = filtered.slice(0, this.maxItems);

        this.storage.setArray(category, limited);
        return limited;
    }

    /**
     * Получить элементы
     */
    get(category) {
        return this.storage.getArray(category);
    }

    /**
     * Очистить категорию
     */
    clear(category) {
        this.storage.remove(category);
    }

    /**
     * Очистить все
     */
    clearAll() {
        this.storage.clear();
    }
}

/**
 * Form State Manager
 */
class FormStateManager {
    constructor() {
        this.storage = new StorageManager('form_');
    }

    /**
     * Сохранить состояние формы
     */
    save(formId, data) {
        return this.storage.set(formId, data);
    }

    /**
     * Загрузить состояние формы
     */
    load(formId) {
        return this.storage.get(formId);
    }

    /**
     * Удалить состояние формы
     */
    clear(formId) {
        this.storage.remove(formId);
    }

    /**
     * Автосохранение формы
     */
    setupAutoSave(form, interval = 5000) {
        const formId = form.id || form.name;
        if (!formId) {
            console.error('Form must have id or name for autosave');
            return;
        }

        // Загрузить сохраненное состояние
        const savedState = this.load(formId);
        if (savedState) {
            this.restoreFormState(form, savedState);
        }

        // Настроить автосохранение
        let timeoutId;
        const saveFormState = () => {
            const formData = new FormData(form);
            const data = Object.fromEntries(formData);
            this.save(formId, data);
        };

        form.addEventListener('input', () => {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(saveFormState, interval);
        });

        // Очистить при отправке
        form.addEventListener('submit', () => {
            this.clear(formId);
        });
    }

    /**
     * Восстановить состояние формы
     */
    restoreFormState(form, data) {
        Object.entries(data).forEach(([name, value]) => {
            const field = form.elements[name];
            if (field) {
                if (field.type === 'checkbox') {
                    field.checked = value === 'on';
                } else if (field.type === 'radio') {
                    const radio = form.querySelector(`input[name="${name}"][value="${value}"]`);
                    if (radio) radio.checked = true;
                } else {
                    field.value = value;
                }
            }
        });
    }
}

// Глобальные экземпляры
const storage = new StorageManager();
const cache = new CacheManager();
const preferences = new PreferencesManager();
const recentItems = new RecentItemsManager();
const formState = new FormStateManager();

// Экспорт
window.storage = storage;
window.cache = cache;
window.preferences = preferences;
window.recentItems = recentItems;
window.formState = formState;
window.StorageManager = StorageManager;
window.CacheManager = CacheManager;
window.PreferencesManager = PreferencesManager;
window.RecentItemsManager = RecentItemsManager;
window.FormStateManager = FormStateManager;
