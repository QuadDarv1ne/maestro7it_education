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
 * Для каждого индекса i:
 * - Если nums[i] > 0: перемещаемся на nums[i] шагов вправо (с зацикливанием)
 * - Если nums[i] < 0: перемещаемся на |nums[i]| шагов влево (с зацикливанием)
 * - Если nums[i] == 0: result[i] = 0
 * 
 * Временная сложность: O(n)
 * Пространственная сложность: O(n)
 * 
 * @param nums - Входной массив целых чисел
 * @returns Трансформированный массив той же длины
 * 
 * @example
 * constructTransformedArray([3, -2, 1, 1]) // [1, 1, 1, 3]
 * constructTransformedArray([-1, 4, -1]) // [-1, -1, 4]
 */
function constructTransformedArray(nums: number[]): number[] {
    const n: number = nums.length;
    const result: number[] = new Array(n);  // Инициализируем результирующий массив
    
    for (let i = 0; i < n; i++) {
        // Вычисляем целевой индекс с учетом зацикливания
        // TypeScript/JavaScript требует обработки отрицательного модуло
        const targetIndex: number = ((i + nums[i]) % n + n) % n;
        result[i] = nums[targetIndex];
    }
    
    return result;
}