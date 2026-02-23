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
#include <unordered_set>
using namespace std;

class Solution {
public:
    /**
     * Проверяет, содержит ли строка s все бинарные коды длины k.
     *
     * @param s входная бинарная строка
     * @param k длина кода
     * @return true, если все коды присутствуют, иначе false
     */
    bool hasAllCodes(string s, int k) {
        int need = 1 << k;  // 2^k
        if (s.length() < need + k - 1) {
            return false;
        }
        
        unordered_set<string> seen;
        for (int i = 0; i <= (int)s.length() - k; ++i) {
            seen.insert(s.substr(i, k));
            if (seen.size() == need) {
                return true;
            }
        }
        return seen.size() == need;
    }
};