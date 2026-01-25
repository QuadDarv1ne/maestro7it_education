/**
 * @file Решение задачи LeetCode 1984. Minimum Difference Between Highest and Lowest of K Scores
 * @see {@link https://leetcode.com/problems/minimum-difference-between-highest-and-lowest-of-k-scores/}
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
 * Алгоритм находит минимальную возможную разницу между наибольшим и 
 * наименьшим значением в любой группе из k элементов массива.
 * 
 * Основная идея:
 * 1. Отсортировать массив по возрастанию
 * 2. Использовать скользящее окно размера k для поиска минимальной разницы
 *    между первым и последним элементом в каждом окне
 * 3. Минимальная разница будет минимальной среди всех возможных окон
 * 
 * Сложность:
 * - Время: O(n log n) - доминирует операция сортировки
 * - Память: O(1) для сортировки на месте, но зависит от реализации сортировки
 * 
 * @param {number[]} nums - Массив целых чисел (оценки учащихся)
 * @param {number} k - Количество элементов для выбора в группе
 * @return {number} Минимальную возможную разницу между максимальным и минимальным 
 *                  значением в группе из k элементов
 */
var minimumDifference = function(nums, k) {
    // Обработка тривиального случая
    if (k <= 1) return 0;
    
    // Сортируем массив для применения скользящего окна
    // Важно: для чисел используем функцию сравнения, иначе сортировка лексикографическая
    nums.sort((a, b) => a - b);
    
    let minDiff = Infinity;
    const n = nums.length;
    
    // Проходим по всем возможным позициям окна длины k
    for (let i = 0; i <= n - k; i++) {
        // Разница между максимальным и минимальным в текущем окне
        const currentDiff = nums[i + k - 1] - nums[i];
        if (currentDiff < minDiff) {
            minDiff = currentDiff;
        }
    }
    
    return minDiff;
};