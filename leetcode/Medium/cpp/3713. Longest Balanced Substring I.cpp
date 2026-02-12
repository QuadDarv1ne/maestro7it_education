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
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    /**
     * Возвращает длину самой длинной сбалансированной подстроки.
     * Сбалансированная подстрока — все различные символы встречаются
     * одинаковое количество раз.
     *
     * Алгоритм: полный перебор всех подстрок.
     * Для каждого левого индекса i проходим по правому j, обновляем
     * частоты символов. Если все ненулевые частоты равны — обновляем ответ.
     *
     * Сложность: O(26 * n^2) ≈ O(n^2) при n ≤ 1000, память O(1).
     */
    int longestBalanced(string s) {
        int n = s.size();
        int maxLen = 0;

        for (int i = 0; i < n; ++i) {
            vector<int> freq(26, 0);
            for (int j = i; j < n; ++j) {
                freq[s[j] - 'a']++;

                int minFreq = INT_MAX;
                int maxFreq = 0;
                for (int cnt : freq) {
                    if (cnt > 0) {
                        minFreq = min(minFreq, cnt);
                        maxFreq = max(maxFreq, cnt);
                    }
                }

                if (minFreq == maxFreq) {
                    maxLen = max(maxLen, j - i + 1);
                }
            }
        }
        return maxLen;
    }
};