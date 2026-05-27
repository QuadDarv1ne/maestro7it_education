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

class Solution {
public:
    int numberOfSpecialChars(string word) {
        const int INF = 1e9;
        vector<int> lastLower(26, -1);
        vector<int> firstUpper(26, INF);

        for (int i = 0; i < word.size(); i++) {
            char c = word[i];
            if (c >= 'a' && c <= 'z') {
                lastLower[c - 'a'] = i;
            } else {
                int idx = c - 'A';
                if (firstUpper[idx] == INF) {
                    firstUpper[idx] = i;
                }
            }
        }

        int ans = 0;
        for (int i = 0; i < 26; i++) {
            if (lastLower[i] != -1 && firstUpper[i] != INF 
                && lastLower[i] < firstUpper[i]) {
                ans++;
            }
        }
        return ans;
    }
};