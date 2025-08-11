/**
 * https://leetcode.com/problems/minimum-window-substring/description/?envType=study-plan-v2&envId=top-interview-150
 */

#include <string>
#include <unordered_map>
#include <climits>

using namespace std;

class Solution {
public:
    /**
     * Возвращает минимальное окно в s, содержащее все символы t с учётом количества.
     *
     * @param s исходная строка
     * @param t строка с нужными символами
     * @return минимальное окно или пустую строку
     */
    string minWindow(string s, string t) {
        if (s.empty() || t.empty()) return "";

        unordered_map<char, int> dictT;
        for (char c : t) dictT[c]++;

        int required = dictT.size();
        unordered_map<char, int> windowCounts;

        int left = 0, right = 0, formed = 0;
        int minLen = INT_MAX, minLeft = 0;

        while (right < (int)s.size()) {
            char c = s[right];
            windowCounts[c]++;

            if (dictT.count(c) && windowCounts[c] == dictT[c]) {
                formed++;
            }

            while (left <= right && formed == required) {
                c = s[left];

                if (right - left + 1 < minLen) {
                    minLen = right - left + 1;
                    minLeft = left;
                }

                windowCounts[c]--;
                if (dictT.count(c) && windowCounts[c] < dictT[c]) {
                    formed--;
                }
                left++;
            }
            right++;
        }

        return minLen == INT_MAX ? "" : s.substr(minLeft, minLen);
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