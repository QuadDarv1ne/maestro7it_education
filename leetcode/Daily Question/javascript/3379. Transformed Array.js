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
 * Создает трансформированный массив на основе циклического массива nums.
 * 
 * Временная сложность: O(n)
 * Пространственная сложность: O(n)
 * 
 * @param {number[]} nums - Входной массив целых чисел
 * @return {number[]} - Трансформированный массив
 */
var constructTransformedArray = function(nums) {
    const n = nums.length;
    const result = new Array(n);  // Инициализируем результирующий массив
    
    for (let i = 0; i < n; i++) {
        // Вычисляем целевой индекс с учетом зацикливания
        // JavaScript также требует обработки отрицательного модуло
        const targetIndex = ((i + nums[i]) % n + n) % n;
        result[i] = nums[targetIndex];
    }
    
    return result;
};