/**
 * https://leetcode.com/problems/maximum-area-of-longest-diagonal-rectangle/description/?envType=daily-question&envId=2025-08-26
 */

#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    /**
     * @brief Определение максимальной площади прямоугольника с самой длинной диагональю.
     *
     * Алгоритм:
     * 1. Для каждого прямоугольника считаем квадрат диагонали: diag_sq = l*l + w*w.
     * 2. Если диагональ больше текущего максимума — обновляем диагональ и площадь.
     * 3. Если диагональ равна текущему максимуму — выбираем максимальную площадь.
     *
     * @param dimensions Вектор пар {длина, ширина}
     * @return int Максимальная площадь прямоугольника
     */
    int areaOfMaxDiagonal(vector<vector<int>>& dimensions) {
        int max_diag_sq = 0, max_area = 0;
        for (auto &d : dimensions) {
            int l = d[0], w = d[1];
            int diag_sq = l*l + w*w;
            int area = l*w;
            if (diag_sq > max_diag_sq) {
                max_diag_sq = diag_sq;
                max_area = area;
            } else if (diag_sq == max_diag_sq) {
                max_area = max(max_area, area);
            }
        }
        return max_area;
    }
};

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/