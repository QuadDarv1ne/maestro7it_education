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

#include <string>
#include <algorithm>

class Solution {
public:
    /**
     * Возвращает максимальную длину подстроки, в которой каждый символ
     * встречается не более двух раз.
     * Используется метод скользящего окна.
     */
    int maximumLengthSubstring(std::string s) {
        int freq[26] = {0};
        int left = 0;
        int ans = 0;

        for (int right = 0; right < s.size(); ++right) {
            char ch = s[right];
            freq[ch - 'a']++;

            while (freq[ch - 'a'] > 2) {
                freq[s[left] - 'a']--;
                left++;
            }

            ans = std::max(ans, right - left + 1);
        }

        return ans;
    }
};