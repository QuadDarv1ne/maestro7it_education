/**
 * https://leetcode.com/problems/find-the-minimum-area-to-cover-all-ones-ii/description/?envType=daily-question&envId=2025-08-23
 */

import java.util.*;

public class Solution {
    /**
     * Находит минимальную суммарную площадь трёх непересекающихся прямоугольников,
     * покрывающих все единицы в бинарной матрице.
     */
    public int minimumSum(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int INF = m * n + 5;
        int ans = INF;

        // вспомогательная функция
        final class Helper {
            int area(int r1, int r2, int c1, int c2) {
                int rmin = Integer.MAX_VALUE, rmax = Integer.MIN_VALUE;
                int cmin = Integer.MAX_VALUE, cmax = Integer.MIN_VALUE;
                for (int r = r1; r <= r2; ++r) {
                    for (int c = c1; c <= c2; ++c) {
                        if (grid[r][c] == 1) {
                            rmin = Math.min(rmin, r); rmax = Math.max(rmax, r);
                            cmin = Math.min(cmin, c); cmax = Math.max(cmax, c);
                        }
                    }
                }
                if (rmin == Integer.MAX_VALUE) return 0;
                return (rmax - rmin + 1) * (cmax - cmin + 1);
            }
        }
        Helper h = new Helper();

        // три горизонтали
        for (int i = 1; i < m; ++i) {
            for (int j = i+1; j < m; ++j) {
                int a = h.area(0, i-1, 0, n-1);
                int b = h.area(i, j-1, 0, n-1);
                int c = h.area(j, m-1, 0, n-1);
                ans = Math.min(ans, a + b + c);
            }
        }

        // три вертикали
        for (int i = 1; i < n; ++i) {
            for (int j = i+1; j < n; ++j) {
                int a = h.area(0, m-1, 0, i-1);
                int b = h.area(0, m-1, i, j-1);
                int c = h.area(0, m-1, j, n-1);
                ans = Math.min(ans, a + b + c);
            }
        }

        // горизонтальный + вертикальный внутри верх/низ
        for (int i = 0; i < m-1; ++i) {
            for (int j = 0; j < n-1; ++j) {
                int topLeft = h.area(0, i, 0, j);
                int topRight = h.area(0, i, j+1, n-1);
                int bottom = h.area(i+1, m-1, 0, n-1);
                ans = Math.min(ans, topLeft + topRight + bottom);

                int top = h.area(0, i, 0, n-1);
                int bottomLeft = h.area(i+1, m-1, 0, j);
                int bottomRight = h.area(i+1, m-1, j+1, n-1);
                ans = Math.min(ans, top + bottomLeft + bottomRight);
            }
        }

        // вертикальный + горизонтальный внутри лево/право
        for (int i = 0; i < n-1; ++i) {
            for (int j = 0; j < m-1; ++j) {
                int leftTop = h.area(0, j, 0, i);
                int leftBottom = h.area(j+1, m-1, 0, i);
                int right = h.area(0, m-1, i+1, n-1);
                ans = Math.min(ans, leftTop + leftBottom + right);

                int left = h.area(0, m-1, 0, i);
                int rightTop = h.area(0, j, i+1, n-1);
                int rightBottom = h.area(j+1, m-1, i+1, n-1);
                ans = Math.min(ans, left + rightTop + rightBottom);
            }
        }

        return (ans == INF) ? 0 : ans;
    }
}

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