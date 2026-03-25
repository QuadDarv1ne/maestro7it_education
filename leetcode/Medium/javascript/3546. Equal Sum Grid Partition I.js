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
 * 
 * Определяет, можно ли разделить матрицу одним горизонтальным или вертикальным
 * разрезом на две непустые части с равной суммой элементов.
 * 
 * @param {number[][]} grid - матрица положительных целых чисел размером m x n
 * @return {boolean} - true, если существует разрез с равными суммами, иначе false
 * 
 * Примечания:
 *     - Разрез может быть горизонтальным (между строками) или вертикальным (между столбцами)
 *     - Обе части после разреза должны быть непустыми
 *     - Используется префиксная сумма для строк и столбцов
 *     - Сложность: O(m*n) по времени и O(1) дополнительной памяти
 */

var canPartitionGrid = function(grid) {
    let total = 0;
    const m = grid.length, n = grid[0].length;
    
    // Вычисляем общую сумму всех элементов
    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            total += grid[i][j];
        }
    }
    
    // Если общая сумма нечётная, разделение невозможно
    if (total % 2 !== 0) return false;
    
    const target = total / 2;
    
    // Проверяем горизонтальные разрезы
    let rowSum = 0;
    for (let i = 0; i < m - 1; i++) {
        for (let j = 0; j < n; j++) {
            rowSum += grid[i][j];
        }
        if (rowSum === target) return true;
    }
    
    // Проверяем вертикальные разрезы
    let colSum = 0;
    for (let j = 0; j < n - 1; j++) {
        for (let i = 0; i < m; i++) {
            colSum += grid[i][j];
        }
        if (colSum === target) return true;
    }
    
    return false;
};