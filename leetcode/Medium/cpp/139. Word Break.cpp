/**
 * https://leetcode.com/problems/word-break/description/?envType=study-plan-v2&envId=top-interview-150
 */

#include <string>
#include <vector>
#include <unordered_set>

/**
 * Определяет, можно ли строку s разбить на последовательность слов из словаря wordDict.
 *
 * @param s Исходная строка
 * @param wordDict Вектор слов словаря
 * @return true, если строку можно разбить, иначе false
 */
class Solution {
public:
    bool wordBreak(std::string s, std::vector<std::string>& wordDict) {
        std::unordered_set<std::string> wordSet(wordDict.begin(), wordDict.end());
        std::vector<bool> dp(s.size() + 1, false);
        dp[0] = true;

        for (size_t i = 1; i <= s.size(); ++i) {
            for (size_t j = 0; j < i; ++j) {
                if (dp[j] && wordSet.find(s.substr(j, i - j)) != wordSet.end()) {
                    dp[i] = true;
                    break;
                }
            }
        }
        return dp[s.size()];
    }
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