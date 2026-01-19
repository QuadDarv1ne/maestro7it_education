/**
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

/**
 * @brief Класс LRU (Least Recently Used) кэша
 * 
 * Реализация с использованием:
 * 1. Map для хранения ключ-значение
 * 2. Map автоматически сохраняет порядок вставки (в ES6+)
 */
class LRUCache {
    /**
     * @brief Конструктор LRU кэша
     * @param {number} capacity Максимальная емкость кэша
     */
    constructor(capacity) {
        this.capacity = capacity;
        this.cache = new Map();  // Map сохраняет порядок вставки
    }
    
    /**
     * @brief Получает значение по ключу
     * @param {number} key Ключ для поиска
     * @return {number} Значение или -1
     */
    get(key) {
        if (!this.cache.has(key)) {
            return -1;
        }
        
        // Получаем значение
        const value = this.cache.get(key);
        
        // Обновляем порядок: удаляем и вставляем заново
        this.cache.delete(key);
        this.cache.set(key, value);
        
        return value;
    }
    
    /**
     * @brief Добавляет или обновляет пару ключ-значение
     * @param {number} key Ключ
     * @param {number} value Значение
     */
    put(key, value) {
        // Если ключ уже существует, удаляем его
        if (this.cache.has(key)) {
            this.cache.delete(key);
        }
        
        // Добавляем новый элемент
        this.cache.set(key, value);
        
        // Если превышена емкость, удаляем первый элемент (самый старый)
        if (this.cache.size > this.capacity) {
            // Первый ключ в Map - самый старый
            const oldestKey = this.cache.keys().next().value;
            this.cache.delete(oldestKey);
        }
    }
}

/**
 * @brief Альтернативная реализация с использованием двусвязного списка
 */
class LRUCacheWithLinkedList {
    constructor(capacity) {
        this.capacity = capacity;
        this.cache = new Map();
        this.head = { key: -1, value: -1, next: null, prev: null };
        this.tail = { key: -1, value: -1, next: null, prev: null };
        this.head.next = this.tail;
        this.tail.prev = this.head;
    }
    
    removeNode(node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }
    
    addToFront(node) {
        node.next = this.head.next;
        node.prev = this.head;
        this.head.next.prev = node;
        this.head.next = node;
    }
    
    moveToFront(node) {
        this.removeNode(node);
        this.addToFront(node);
    }
    
    removeLRU() {
        const lru = this.tail.prev;
        this.removeNode(lru);
        this.cache.delete(lru.key);
    }
    
    get(key) {
        if (!this.cache.has(key)) {
            return -1;
        }
        
        const node = this.cache.get(key);
        this.moveToFront(node);
        return node.value;
    }
    
    put(key, value) {
        if (this.cache.has(key)) {
            const node = this.cache.get(key);
            node.value = value;
            this.moveToFront(node);
        } else {
            if (this.cache.size >= this.capacity) {
                this.removeLRU();
            }
            
            const newNode = { key, value };
            this.addToFront(newNode);
            this.cache.set(key, newNode);
        }
    }
}