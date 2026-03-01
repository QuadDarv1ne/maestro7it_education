/**
 * https://leetcode.com/problems/house-robber-ii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "2622. Cache With Time Limit"
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

class TimeLimitedCache {
    constructor() {
        // Хранилище: ключ -> объект { value, timeoutId }
        this.cache = new Map();
    }

    /**
     * Сохраняет значение с временем жизни.
     * @param {number} key
     * @param {number} value
     * @param {number} duration - время жизни в миллисекундах
     * @returns {boolean} true, если ключ уже существовал и был действителен
     */
    set(key, value, duration) {
        const existed = this.cache.has(key);
        if (existed) {
            // Очищаем предыдущий таймер, чтобы он не удалил перезаписанный ключ
            clearTimeout(this.cache.get(key).timeoutId);
        }
        // Создаём новый таймер для автоматического удаления ключа
        const timeoutId = setTimeout(() => {
            this.cache.delete(key);
        }, duration);
        // Сохраняем значение и идентификатор таймера
        this.cache.set(key, { value, timeoutId });
        return existed;
    }

    /**
     * Возвращает значение по ключу, если оно не истекло.
     * @param {number} key
     * @returns {number} значение или -1
     */
    get(key) {
        if (this.cache.has(key)) {
            return this.cache.get(key).value;
        }
        return -1;
    }

    /**
     * Возвращает количество неистекших ключей.
     * @returns {number}
     */
    count() {
        return this.cache.size;
    }
}