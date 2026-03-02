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
     * Вычисляет количество единичных битов для всех чисел от 0 до n.
     * Используется линейное динамическое программирование.
     *
     * @param n максимальное значение для расчёта
     * @return вектор целых чисел, где элемент i содержит число битов в i
     */
    vector<int> countBits(int n) {
        vector<int> ans(n + 1, 0);
        for (int i = 1; i <= n; ++i) {
            // i >> 1 — побитовый сдвиг вправо (деление на 2),
            // (i & 1) проверяет, был ли младший бит единицей
            ans[i] = ans[i >> 1] + (i & 1);
        }
        return ans;
    }
};