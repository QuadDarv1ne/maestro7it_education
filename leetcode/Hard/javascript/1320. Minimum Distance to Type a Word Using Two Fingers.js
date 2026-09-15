// JavaScript
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
 * LeetCode 1320. Minimum Distance to Type a Word Using Two Fingers  [JavaScript]
 *
 * Условие:
 *     Клавиатура — сетка 4×6. Расстояние = манхэттенское.
 *     Напечатать слово двумя пальцами с минимальной суммарной стоимостью.
 *
 * Подход — DP:
 *     dp[i][j] — мин. стоимость: первый палец на word[i], второй на j
 *     (j == 26 → второй ещё не размещён).
 *
 *     Переходы для word[i] → word[i+1]:
 *       1) Первый палец → nxt  : dp[i+1][j]   = min(..., dp[i][j] + dist(cur, nxt))
 *       2) Второй палец → nxt  : dp[i+1][cur] = min(..., dp[i][j] + dist(j, nxt))
 *          j == 26 → dist = 0
 *
 * @param  {string} word  — строка из заглавных латинских букв
 * @return {number}       — минимальная суммарная стоимость перемещений
 *
 * Сложность: O(n × 27) времени, O(n × 27) памяти.
 */
var minimumDistance = function(word) {
    const dist = (a, b) =>
        Math.abs(Math.floor(a / 6) - Math.floor(b / 6)) + Math.abs(a % 6 - b % 6);

    const INF = Infinity, n = word.length;
    const dp = Array.from({ length: n }, () => new Array(27).fill(INF));
    dp[0][26] = 0;

    for (let i = 0; i < n - 1; i++) {
        const cur = word.charCodeAt(i)     - 65;
        const nxt = word.charCodeAt(i + 1) - 65;

        for (let j = 0; j < 27; j++) {
            if (dp[i][j] === INF) continue;
            const costJ = j === 26 ? 0 : dist(j, nxt);

            // Вариант 1: первый палец → nxt, второй остаётся на j
            dp[i+1][j]   = Math.min(dp[i+1][j],   dp[i][j] + dist(cur, nxt));
            // Вариант 2: второй палец → nxt, первый замирает на cur
            dp[i+1][cur] = Math.min(dp[i+1][cur], dp[i][j] + costJ);
        }
    }
    return Math.min(...dp[n-1]);
};