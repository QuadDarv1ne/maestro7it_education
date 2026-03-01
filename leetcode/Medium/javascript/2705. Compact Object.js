/**
 * https://leetcode.com/problems/house-robber-ii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "2705. Compact Object"
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
 * @param {Object|Array} obj
 * @return {Object|Array}
 */
var compactObject = function(obj) {
    // Базовый случай: если это примитив (не объект) или null, возвращаем как есть
    if (typeof obj !== 'object' || obj === null) {
        return obj;
    }

    // Обработка массива
    if (Array.isArray(obj)) {
        const newArr = [];
        for (const item of obj) {
            const nested = compactObject(item); // рекурсивно обрабатываем каждый элемент
            // Добавляем только truthy значения (пустые массивы/объекты считаются truthy)
            if (nested) {
                newArr.push(nested);
            }
        }
        return newArr;
    }

    // Обработка объекта
    const newObj = {};
    for (const key in obj) {
        const nested = compactObject(obj[key]); // рекурсивно обрабатываем значение
        // Добавляем только truthy значения
        if (nested) {
            newObj[key] = nested;
        }
    }
    return newObj;
};