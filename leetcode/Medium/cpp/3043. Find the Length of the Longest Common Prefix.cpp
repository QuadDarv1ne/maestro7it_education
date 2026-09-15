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

#include <vector>
#include <unordered_set>
#include <string>
#include <algorithm>
using namespace std;

class Solution {
public:
    int longestCommonPrefix(vector<int>& arr1, vector<int>& arr2) {
        /*
         * Находит длину самого длинного общего префикса среди всех пар (x, y).
         * Использует unordered_set для хранения всех префиксов arr1.
         */
        unordered_set<int> prefixes;

        // Собираем все префиксы чисел из arr1
        for (int x : arr1) {
            while (x > 0) {
                prefixes.insert(x);
                x /= 10;
            }
        }

        int max_len = 0;

        // Проверяем префиксы чисел из arr2
        for (int y : arr2) {
            while (y > 0) {
                if (prefixes.count(y)) {
                    max_len = max(max_len, (int)to_string(y).length());
                    break; // Нашли самый длинный префикс для этого числа
                }
                y /= 10;
            }
        }

        return max_len;
    }
};