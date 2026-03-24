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
 * Находит максимальное неотрицательное произведение на пути из (0,0) в (m-1,n-1).
 * 
 * @param {number[][]} grid - матрица целых чисел размером m x n
 * @return {number} - максимальное неотрицательное произведение по модулю 10^9+7,
 *                    или -1, если такого произведения нет
 * 
 * Примечания:
 *     - Движение возможно только вправо или вниз
 *     - Отрицательные числа могут менять знак произведения
 *     - Используется динамическое программирование с отслеживанием
 *       максимального и минимального произведения в каждой ячейке
 *     - Сложность: O(m*n) по времени и O(m*n) по памяти
 */

var maxProductPath = function(grid) {
    const MOD = BigInt(1000000007);
    const m = grid.length, n = grid[0].length;
    
    // Используем BigInt для точности
    const maxDP = Array(m).fill().map(() => Array(n).fill(0n));
    const minDP = Array(m).fill().map(() => Array(n).fill(0n));
    
    // Инициализация начальной ячейки
    maxDP[0][0] = minDP[0][0] = BigInt(grid[0][0]);
    
    // Заполняем первую строку
    for (let j = 1; j < n; j++) {
        maxDP[0][j] = minDP[0][j] = maxDP[0][j-1] * BigInt(grid[0][j]);
    }
    
    // Заполняем первый столбец
    for (let i = 1; i < m; i++) {
        maxDP[i][0] = minDP[i][0] = maxDP[i-1][0] * BigInt(grid[i][0]);
    }
    
    // Основной DP
    for (let i = 1; i < m; i++) {
        for (let j = 1; j < n; j++) {
            const curr = BigInt(grid[i][j]);
            const candidates = [
                maxDP[i-1][j] * curr,
                minDP[i-1][j] * curr,
                maxDP[i][j-1] * curr,
                minDP[i][j-1] * curr
            ];
            maxDP[i][j] = candidates.reduce((max, val) => val > max ? val : max, candidates[0]);
            minDP[i][j] = candidates.reduce((min, val) => val < min ? val : min, candidates[0]);
        }
    }
    
    const result = maxDP[m-1][n-1];
    if (result < 0n) return -1;
    return Number(result % MOD);
};