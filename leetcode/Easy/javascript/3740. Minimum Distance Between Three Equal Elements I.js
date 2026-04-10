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
 * Находит минимальное расстояние между тремя одинаковыми элементами в массиве.
 *
 * Расстояние вычисляется по формуле: |i - j| + |j - k| + |k - i|,
 * что для отсортированной тройки (i < j < k) упрощается до 2 * (k - i).
 *
 * Алгоритм:
 * 1. Создаем объект Map, где ключ - число, значение - массив его индексов.
 * 2. Для каждого числа, если количество индексов >= 3, перебираем все тройки
 *    и обновляем минимальное расстояние.
 *
 * @param {number[]} nums - Входной массив целых чисел.
 * @returns {number} - Минимальное расстояние или -1, если троек нет.
 */
var minimumDistance = function(nums) {
    // Шаг 1: Группировка индексов
    const positions = new Map();
    
    for (let i = 0; i < nums.length; i++) {
        const val = nums[i];
        if (!positions.has(val)) {
            positions.set(val, []);
        }
        positions.get(val).push(i);
    }

    let minDist = Infinity;

    // Шаг 2: Перебор сгруппированных значений
    for (const idxList of positions.values()) {
        const n = idxList.length;
        
        if (n < 3) continue;

        // Шаг 3: Перебор троек
        for (let i = 0; i < n - 2; i++) {
            for (let j = i + 1; j < n - 1; j++) {
                for (let k = j + 1; k < n; k++) {
                    const dist = 2 * (idxList[k] - idxList[i]);
                    if (dist < minDist) {
                        minDist = dist;
                    }
                }
            }
        }
    }

    return minDist === Infinity ? -1 : minDist;
};