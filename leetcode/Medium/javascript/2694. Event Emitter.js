/**
 * https://leetcode.com/problems/house-robber-ii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "2619. Array Prototype Last"
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

class EventEmitter {
    constructor() {
        // Хранилище событий: ключ - имя события, значение - массив подписок
        // Каждая подписка - объект { callback, unsubscribe }
        this.events = new Map();
    }

    /**
     * Подписывает колбэк на событие.
     * @param {string} eventName - Имя события
     * @param {Function} callback - Функция-колбэк
     * @returns {{unsubscribe: Function}} Объект с методом для отписки
     */
    subscribe(eventName, callback) {
        // Если для события ещё нет подписок, создаём новый массив
        if (!this.events.has(eventName)) {
            this.events.set(eventName, []);
        }

        const subscriptions = this.events.get(eventName);
        const subscription = { callback }; // Можно хранить и доп. данные при необходимости

        subscriptions.push(subscription);

        // Возвращаем объект с методом unsubscribe
        return {
            unsubscribe: () => {
                // Находим индекс текущей подписки в массиве
                const index = subscriptions.indexOf(subscription);
                if (index !== -1) {
                    subscriptions.splice(index, 1); // Удаляем подписку
                }
                // Если подписок не осталось, можно удалить событие из Map (опционально)
                if (subscriptions.length === 0) {
                    this.events.delete(eventName);
                }
            }
        };
    }

    /**
     * Вызывает все колбэки, подписанные на событие.
     * @param {string} eventName - Имя события
     * @param {Array} args - Массив аргументов для передачи в колбэки
     * @returns {Array} Массив результатов вызовов колбэков (в порядке подписки)
     */
    emit(eventName, args = []) {
        // Если событие не существует или нет подписок, возвращаем пустой массив
        if (!this.events.has(eventName)) {
            return [];
        }

        const subscriptions = this.events.get(eventName);
        const results = [];

        // Вызываем каждый колбэк с переданными аргументами и собираем результаты
        for (const sub of subscriptions) {
            // Колбэки могут быть как обычными функциями, так и стрелочными
            // Принимаем, что они могут вернуть любое значение (включая undefined)
            results.push(sub.callback(...args));
        }

        return results;
    }
}