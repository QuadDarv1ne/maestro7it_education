/**
 * https://leetcode.com/problems/wildcard-matching/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "Wildcard Matching" на JavaScript
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

var isMatch = function(s, p) {
    const m = s.length, n = p.length;
    const dp = Array.from({length: m + 1}, () => new Array(n + 1).fill(false));
    
    dp[0][0] = true;
    
    for (let j = 1; j <= n; j++) {
        if (p[j-1] === '*') {
            dp[0][j] = dp[0][j-1];
        }
    }
    
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (p[j-1] === '*') {
                dp[i][j] = dp[i][j-1] || dp[i-1][j];
            } else if (p[j-1] === '?' || p[j-1] === s[i-1]) {
                dp[i][j] = dp[i-1][j-1];
            }
        }
    }
    
    return dp[m][n];
};