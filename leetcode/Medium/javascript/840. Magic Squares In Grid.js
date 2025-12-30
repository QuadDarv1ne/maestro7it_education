/**
 * https://leetcode.com/problems/magic-squares-in-grid/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Magic Squares In Grid"
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
 * Подсчитывает количество магических квадратов 3x3 в заданной сетке.
 * 
 * @param {number[][]} grid - двумерный массив целых чисел
 * @return {number} - количество магических квадратов 3x3 в сетке
 * 
 * Магический квадрат 3x3 должен удовлетворять:
 * 1. Содержать все числа от 1 до 9 (без повторений)
 * 2. Суммы строк, столбцов и диагоналей равны 15
 */
var numMagicSquaresInside = function(grid) {
    const rows = grid.length;
    const cols = grid[0].length;
    
    // Если сетка меньше чем 3x3, не может быть магических квадратов
    if (rows < 3 || cols < 3) {
        return 0;
    }
    
    let count = 0;
    
    // Перебираем все возможные левые верхние углы квадратов 3x3
    for (let r = 0; r <= rows - 3; r++) {
        for (let c = 0; c <= cols - 3; c++) {
            // Оптимизация: центр магического квадрата 3x3 всегда должен быть 5
            if (grid[r + 1][c + 1] !== 5) {
                continue;
            }
            if (isMagic(grid, r, c)) {
                count++;
            }
        }
    }
    
    return count;
};

/**
 * Проверяет, является ли подматрица 3x3 магическим квадратом.
 * 
 * @param {number[][]} grid - исходная сетка
 * @param {number} r - начальная строка
 * @param {number} c - начальный столбец
 * @return {boolean} - true если подматрица является магическим квадратом
 */
function isMagic(grid, r, c) {
    // Проверяем, что все числа от 1 до 9 без повторений
    const nums = new Set();
    for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
            const num = grid[r + i][c + j];
            if (num < 1 || num > 9) {
                return false;
            }
            nums.add(num);
        }
    }
    
    if (nums.size !== 9) {
        return false;
    }
    
    // Проверяем суммы строк (должны быть равны 15)
    for (let i = 0; i < 3; i++) {
        let rowSum = 0;
        for (let j = 0; j < 3; j++) {
            rowSum += grid[r + i][c + j];
        }
        if (rowSum !== 15) {
            return false;
        }
    }
    
    // Проверяем суммы столбцов
    for (let j = 0; j < 3; j++) {
        let colSum = 0;
        for (let i = 0; i < 3; i++) {
            colSum += grid[r + i][c + j];
        }
        if (colSum !== 15) {
            return false;
        }
    }
    
    // Проверяем диагонали
    const diag1 = grid[r][c] + grid[r + 1][c + 1] + grid[r + 2][c + 2];
    const diag2 = grid[r][c + 2] + grid[r + 1][c + 1] + grid[r + 2][c];
    
    return diag1 === 15 && diag2 === 15;
}