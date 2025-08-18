/**
 * https://leetcode.com/problems/word-break/description/
 */

/**
 * Определяет, можно ли строку s разбить на последовательность слов из словаря wordDict.
 *
 * @param {string} s — исходная строка
 * @param {string[]} wordDict — массив слов словаря
 * @return {boolean} — true, если строку можно разбить, иначе false
 *
 * Алгоритм:
 * Используется динамическое программирование.
 * dp[i] = true, если s[0..i-1] можно разбить на слова словаря.
 * Для каждого i перебираем j < i и проверяем:
 *   если dp[j] = true и s[j..i-1] ∈ wordDict → dp[i] = true
 *
 * Время: O(n^2 * k) — n = длина s, k = средняя длина слов
 * Память: O(n + m) — n = длина s, m = размер словаря
 */
var wordBreak = function(s, wordDict) {
    const wordSet = new Set(wordDict);
    const n = s.length;
    const dp = new Array(n + 1).fill(false);
    dp[0] = true; // пустая строка всегда "разбиваемая"

    for (let i = 1; i <= n; i++) {
        for (let j = 0; j < i; j++) {
            if (dp[j] && wordSet.has(s.substring(j, i))) {
                dp[i] = true;
                break;
            }
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