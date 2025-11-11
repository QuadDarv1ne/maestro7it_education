/*
https://leetcode.com/problems/ones-and-zeroes/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

var findMaxForm = function(strs, m, n) {
    // dp[i][j] — макс. кол-во строк при i нулях и j единиц
    let dp = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));
    
    for (let s of strs) {
        let zeros = (s.match(/0/g) || []).length;
        let ones = s.length - zeros;
        
        // Обновление в обратном порядке
        for (let i = m; i >= zeros; i--) {
            for (let j = n; j >= ones; j--) {
                dp[i][j] = Math.max(dp[i][j], dp[i - zeros][j - ones] + 1);
            }
        }
    }
    return dp[m][n];
};

/* Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
*/