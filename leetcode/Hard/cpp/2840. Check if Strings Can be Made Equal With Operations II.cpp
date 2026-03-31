/**
 * https://leetcode.com/problems/check-if-strings-can-be-made-equal-with-operations-ii/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Решение задачи "2840. Check if Strings Can be Made Equal With Operations II" на JavaScript
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

using namespace std;

class Solution {
public:
    bool checkStrings(string s1, string s2) {
        if (s1.length() != s2.length()) return false;
        
        int even[26] = {0};
        int odd[26] = {0};
        
        for (int i = 0; i < s1.length(); ++i) {
            if (i % 2 == 0) {
                even[s1[i] - 'a']++;
                even[s2[i] - 'a']--;
            } else {
                odd[s1[i] - 'a']++;
                odd[s2[i] - 'a']--;
            }
        }
        
        for (int i = 0; i < 26; ++i) {
            if (even[i] != 0 || odd[i] != 0) {
                return false;
            }
        }
        
        return true;
    }
};