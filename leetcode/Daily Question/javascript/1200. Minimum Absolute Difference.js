/**
 * Автор: Дуплей Максим Игоревич
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
 * Находит все пары элементов с минимальной абсолютной разностью в массиве.
 * 
 * @param {number[]} arr - массив различных целых чисел.
 * @return {number[][]} - массив пар [a, b], где:
 *         - a < b
 *         - |a - b| минимально среди всех возможных пар
 *         - Пары отсортированы в порядке возрастания внутри каждой пары
 *           и по первому элементу между парами
 * 
 * @note Алгоритм работает за O(n log n) из-за сортировки и использует O(n) памяти.
 *       Важно: в JavaScript нужно передавать функцию сравнения в sort().
 * 
 * @example
 *   minimumAbsDifference([4, 2, 1, 3]); // возвращает [[1,2],[2,3],[3,4]]
 *   minimumAbsDifference([1, 3, 6, 10, 15]); // возвращает [[1,3]]
 */
var minimumAbsDifference = function(arr) {
    // Сортируем массив для нахождения последовательных элементов с минимальной разностью
    // Важно: в JavaScript нужно передавать функцию сравнения для числовой сортировки
    arr.sort((a, b) => a - b);
    
    let minDiff = Infinity;
    const result = [];
    
    // Первый проход: находим минимальную разность
    for (let i = 1; i < arr.length; i++) {
        const diff = arr[i] - arr[i-1];
        if (diff < minDiff) {
            minDiff = diff;
        }
    }
    
    // Второй проход: собираем пары с минимальной разностью
    for (let i = 1; i < arr.length; i++) {
        if (arr[i] - arr[i-1] === minDiff) {
            result.push([arr[i-1], arr[i]]);
        }
    }
    
    return result;
};