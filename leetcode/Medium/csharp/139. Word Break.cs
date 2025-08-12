/**
 * https://leetcode.com/problems/word-break/description/?envType=study-plan-v2&envId=top-interview-150
 */

using System;
using System.Collections.Generic;

/**
 * Класс для решения задачи Word Break.
 */
public class Solution {
    /**
     * Определяет, можно ли строку s разбить на последовательность слов из словаря wordDict.
     *
     * @param s Исходная строка
     * @param wordDict Список слов словаря
     * @return true, если строку можно разбить, иначе false
     */
    public bool WordBreak(string s, IList<string> wordDict) {
        HashSet<string> wordSet = new HashSet<string>(wordDict);
        bool[] dp = new bool[s.Length + 1];
        dp[0] = true; // Пустая строка всегда может быть разбита

        for (int i = 1; i <= s.Length; i++) {
            for (int j = 0; j < i; j++) {
                if (dp[j] && wordSet.Contains(s.Substring(j, i - j))) {
                    dp[i] = true;
                    break;
                }
            }
        }
        return dp[s.Length];
    }
}

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