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
    double champagneTower(int poured, int query_row, int query_glass) {
        // Текущий ряд (ряд 0)
        vector<double> curr(1, poured);

        for (int row = 0; row < query_row; ++row) {
            // Следующий ряд: размер row+2
            vector<double> next(row + 2, 0.0);
            for (int i = 0; i < curr.size(); ++i) {
                if (curr[i] > 1.0) {
                    double excess = (curr[i] - 1.0) / 2.0;
                    next[i] += excess;
                    next[i + 1] += excess;
                }
            }
            curr = move(next);
        }

        // Индекс query_glass гарантированно существует
        return min(1.0, curr[query_glass]);
    }
};