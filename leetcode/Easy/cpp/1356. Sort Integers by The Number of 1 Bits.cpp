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
    vector<int> sortByBits(vector<int>& arr) {
        /**
         * Сортирует массив по количеству единичных битов,
         * а затем по значению числа.
         * 
         * @param arr входной массив
         * @return отсортированный массив
         */
        // Используем стандартную сортировку с кастомным компаратором
        sort(arr.begin(), arr.end(), [](int a, int b) {
            int bitsA = __builtin_popcount(a);
            int bitsB = __builtin_popcount(b);
            if (bitsA == bitsB) return a < b;  // при равенстве битов — по значению
            return bitsA < bitsB;               // иначе по количеству битов
        });
        return arr;
    }
};