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
    /**
     * Возвращает минимальное количество переворотов битов (type-2),
     * необходимое для превращения строки в чередующуюся после любого числа
     * циклических сдвигов (type-1).
     *
     * @param s исходная двоичная строка
     * @return минимальное количество переворотов
     */
    int minFlips(string s) {
        int n = s.size();
        string t = s + s; // удвоенная строка
        vector<int> diff(2 * n, 0);
        for (int j = 0; j < 2 * n; ++j) {
            char expected = (j % 2 == 0) ? '0' : '1';
            diff[j] = (t[j] != expected) ? 1 : 0;
        }

        // префиксные суммы
        vector<int> pref(2 * n + 1, 0);
        for (int j = 0; j < 2 * n; ++j) {
            pref[j + 1] = pref[j] + diff[j];
        }

        int ans = n;
        for (int i = 0; i < n; ++i) {
            int flips = pref[i + n] - pref[i];
            ans = min(ans, min(flips, n - flips));
        }
        return ans;
    }
};