/**
 * https://leetcode.com/problems/house-robber-ii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "2625. Flatten Deeply Nested Array"
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
 * @param {any[]} arr - Исходный многомерный массив
 * @param {number} n - Глубина уплощения
 * @return {any[]} Уплощённый массив
 */
var flat = function (arr, n) {
    const result = [];

    // Вспомогательная рекурсивная функция
    function flattenHelper(currentArr, currentDepth) {
        for (let item of currentArr) {
            if (Array.isArray(item) && currentDepth < n) {
                // Если элемент массив и глубина позволяет, рекурсивно уплощаем его
                flattenHelper(item, currentDepth + 1);
            } else {
                // Иначе просто добавляем элемент (число или массив, который уже не уплощаем)
                result.push(item);
            }
        }
    }

    flattenHelper(arr, 0);
    return result;
};