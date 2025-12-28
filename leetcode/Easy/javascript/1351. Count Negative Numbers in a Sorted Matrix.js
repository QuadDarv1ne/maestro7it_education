/**
 * https://leetcode.com/problems/count-negative-numbers-in-a-sorted-matrix/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Count Negative Numbers in a Sorted Matrix"
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
 * Подсчитывает количество отрицательных чисел в отсортированной матрице.
 * 
 * @param {number[][]} grid матрица m x n, отсортированная по убыванию
 * @return {number} количество отрицательных чисел в матрице
 * 
 * Алгоритм:
 * - Сложность: O(m + n)
 * - Начинаем с правого верхнего угла
 * - Если текущий элемент отрицательный, все элементы ниже тоже отрицательные
 * - Двигаемся влево при отрицательном элементе, вниз - при положительном
 */
var countNegatives = function(grid) {
    const m = grid.length;
    const n = grid[0].length;
    let count = 0;
    
    // Начинаем с правого верхнего угла (0, n-1)
    let row = 0, col = n - 1;
    
    while (row < m && col >= 0) {
        if (grid[row][col] < 0) {
            // Все элементы в этом столбце ниже текущей строки тоже отрицательные
            count += (m - row);
            // Переходим к столбцу слева
            col--;
        } else {
            // Текущий элемент неотрицательный, переходим к следующей строке
            row++;
        }
    }
    
    return count;
};