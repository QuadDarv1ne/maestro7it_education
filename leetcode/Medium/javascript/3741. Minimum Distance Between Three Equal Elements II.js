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
 * Находит минимальное расстояние между тремя равными элементами в массиве.
 * 
 * @param {number[]} nums - Входной массив целых чисел.
 * @returns {number} Минимальное расстояние или -1, если таких троек нет.
 * 
 * Алгоритм:
 * 1. Сгруппировать индексы по значениям с помощью Map.
 * 2. Для каждой группы с количеством элементов ≥ 3 вычислить расстояние
 *    между первой и третьей позицией в каждой тройке последовательных индексов.
 * 3. Вернуть минимальное из найденных расстояний.
 */
var minimumDistance = function(nums) {
    const map = new Map();
    for (let i = 0; i < nums.length; i++) {
        const val = nums[i];
        if (!map.has(val)) {
            map.set(val, []);
        }
        map.get(val).push(i);
    }

    let minDist = Infinity;
    for (const indices of map.values()) {
        if (indices.length >= 3) {
            for (let i = 0; i <= indices.length - 3; i++) {
                const dist = 2 * (indices[i + 2] - indices[i]);
                minDist = Math.min(minDist, dist);
            }
        }
    }
    return minDist === Infinity ? -1 : minDist;
};