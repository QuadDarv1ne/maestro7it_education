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
 * Находит минимальное количество полных квадратов, дающих в сумме n.
 * 
 * @param {number} n - Целое положительное число
 * @return {number} Минимальное количество квадратов
 * 
 * @example
 * // Возвращает 3 (4 + 4 + 4)
 * numSquares(12)
 * @example
 * // Возвращает 2 (4 + 9)
 * numSquares(13)
 * 
 * Сложность:
 *   Время: O(n * √n)
 *   Память: O(n)
 */
var numSquares = function(n) {
    const dp = new Array(n + 1).fill(Infinity);
    dp[0] = 0;  // Базовый случай
    
    // Генерируем все квадраты, не превышающие n
    const squares = [];
    for (let i = 1; i * i <= n; i++) {
        squares.push(i * i);
    }
    
    for (let i = 1; i <= n; i++) {
        for (const square of squares) {
            if (square > i) break;
            dp[i] = Math.min(dp[i], dp[i - square] + 1);
        }
    }
    
    return dp[n];
};