/**
 * https://leetcode.com/problems/find-the-minimum-area-to-cover-all-ones-ii/description/?envType=daily-question&envId=2025-08-23
 */

#include <bits/stdc++.h>
using namespace std;

class Solution {
public:
    /**
     * Находит минимальную суммарную площадь трёх непересекающихся прямоугольников,
     * покрывающих все единицы в бинарной матрице.
     *
     * Подход: перебираем все возможные комбинации разрезов, которые
     * покрывают все возможные топологии трёх прямоугольников:
     *  - три горизонтальных полосы
     *  - три вертикальных полосы
     *  - одна горизонтальная полоса + нижняя/верхняя часть разбивается вертикально (две конфигурации)
     *  - одна вертикальная полоса + левая/правая часть разбивается горизонтально (две конфигурации)
     *
     * Для каждой такой конфигурации считаем области минимальных прямоугольников, покрывающих единицы
     * в соответствующих подпрямоугольниках.
     */
    int minimumSum(vector<vector<int>>& grid) {
        int m = grid.size();
        int n = grid[0].size();
        int INF = m * n + 5;
        int ans = INF;

        auto area = [&](int r1, int r2, int c1, int c2)->int {
            // возвращает площадь минимального прямоугольника, покрывающего все 1 внутри [r1..r2] x [c1..c2]
            // если единиц нет — возвращает 0
            int rmin = INT_MAX, rmax = INT_MIN, cmin = INT_MAX, cmax = INT_MIN;
            for (int r = r1; r <= r2; ++r) {
                for (int c = c1; c <= c2; ++c) {
                    if (grid[r][c]) {
                        rmin = min(rmin, r);
                        rmax = max(rmax, r);
                        cmin = min(cmin, c);
                        cmax = max(cmax, c);
                    }
                }
            }
            if (rmin == INT_MAX) return 0;
            return (rmax - rmin + 1) * (cmax - cmin + 1);
        };

        // 1) Три горизонтальных полосы: [0..i-1], [i..j-1], [j..m-1]
        for (int i = 1; i < m; ++i) {
            for (int j = i+1; j < m; ++j) {
                int a = area(0, i-1, 0, n-1);
                int b = area(i, j-1, 0, n-1);
                int c = area(j, m-1, 0, n-1);
                ans = min(ans, a + b + c);
            }
        }

        // 2) Три вертикальных полосы: [0..i-1], [i..j-1], [j..n-1]
        for (int i = 1; i < n; ++i) {
            for (int j = i+1; j < n; ++j) {
                int a = area(0, m-1, 0, i-1);
                int b = area(0, m-1, i, j-1);
                int c = area(0, m-1, j, n-1);
                ans = min(ans, a + b + c);
            }
        }

        // 3) Горизонтальный разрез + вертикальный разрез в верхней части
        // Разрез по строке i: верх [0..i], низ [i+1..m-1]
        // Верхнюю часть делим вертикально на (0..j) и (j+1..n-1)
        for (int i = 0; i < m-1; ++i) {
            // делим верх (0..i) на два столбца
            for (int j = 0; j < n-1; ++j) {
                int topLeft = area(0, i, 0, j);
                int topRight = area(0, i, j+1, n-1);
                int bottom = area(i+1, m-1, 0, n-1);
                ans = min(ans, topLeft + topRight + bottom);
            }
            // делим нижнюю часть (i+1..m-1) на два столбца
            for (int j = 0; j < n-1; ++j) {
                int top = area(0, i, 0, n-1);
                int bottomLeft = area(i+1, m-1, 0, j);
                int bottomRight = area(i+1, m-1, j+1, n-1);
                ans = min(ans, top + bottomLeft + bottomRight);
            }
        }

        // 4) Вертикальный разрез + горизонтальный разрез в левой/правой части (симметрично)
        for (int i = 0; i < n-1; ++i) {
            // делим левую часть (0..i) по строкам
            for (int j = 0; j < m-1; ++j) {
                int leftTop = area(0, j, 0, i);
                int leftBottom = area(j+1, m-1, 0, i);
                int right = area(0, m-1, i+1, n-1);
                ans = min(ans, leftTop + leftBottom + right);
            }
            // делим правую часть (i+1..n-1) по строкам
            for (int j = 0; j < m-1; ++j) {
                int left = area(0, m-1, 0, i);
                int rightTop = area(0, j, i+1, n-1);
                int rightBottom = area(j+1, m-1, i+1, n-1);
                ans = min(ans, left + rightTop + rightBottom);
            }
        }

        return ans;
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