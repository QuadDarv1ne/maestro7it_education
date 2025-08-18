/**
 * https://leetcode.com/problems/decode-ways/description/
 */

/**
 * Подсчитывает количество способов декодирования строки цифр по схеме A-Z = 1-26.
 *
 * @param {string} s — строка цифр
 * @return {number} — число способов декодирования
 *
 * Алгоритм:
 * dp[0] = 1
 * Для i от 1 до n:
 *   если s[i-1] != '0': dp[i] += dp[i-1]
 *   если i>=2 и '10'<=s[i-2..i-1]<='26': dp[i] += dp[i-2]
 *
 * Время: O(n)
 * Память: O(n)
 */
var numDecodings = function(s) {
    if (!s || s[0] === '0') return 0;
    const n = s.length;
    const dp = new Array(n + 1).fill(0);
    dp[0] = 1;
    dp[1] = 1;
    for (let i = 2; i <= n; i++) {
        if (s[i - 1] !== '0') {
            dp[i] += dp[i - 1];
        }
        const two = s.substring(i - 2, i);
        if (two[0] !== '0' && Number(two) >= 10 && Number(two) <= 26) {
            dp[i] += dp[i - 2];
        }
    }
    return dp[n];
};

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/