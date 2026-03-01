/**
 * https://leetcode.com/problems/house-robber-ii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "2722. Join Two Arrays by ID"
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
 * @param {Array} arr1
 * @param {Array} arr2
 * @return {Array}
 */
var join = function(arr1, arr2) {
    const map = new Map();

    // 1. Добавляем все объекты из arr1 в Map
    for (const obj of arr1) {
        map.set(obj.id, { ...obj }); // Создаём копию, чтобы не мутировать исходный
    }

    // 2. Обрабатываем объекты из arr2
    for (const obj of arr2) {
        if (!map.has(obj.id)) {
            // Если id нет, просто добавляем копию объекта
            map.set(obj.id, { ...obj });
        } else {
            // Если id есть, объединяем: старые значения перезаписываются новыми из obj2
            const existingObj = map.get(obj.id);
            map.set(obj.id, { ...existingObj, ...obj });
        }
    }

    // 3. Преобразуем Map в массив и сортируем по id
    const joinedArray = Array.from(map.values());
    joinedArray.sort((a, b) => a.id - b.id);

    return joinedArray;
};