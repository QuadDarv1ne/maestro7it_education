/**
 * https://leetcode.com/problems/find-the-minimum-area-to-cover-all-ones-ii/description/?envType=daily-question&envId=2025-08-23
 */

using System;

public class Solution {
    /*
     * Находит минимальную суммарную площадь трёх непересекающихся прямоугольников,
     * покрывающих все единицы в бинарной матрице.
     */
    public int MinimumSum(int[][] grid) {
        int m = grid.Length, n = grid[0].Length;
        int INF = m * n + 5;
        int ans = INF;

        int Area(int r1, int r2, int c1, int c2) {
            int rmin = int.MaxValue, rmax = int.MinValue;
            int cmin = int.MaxValue, cmax = int.MinValue;
            for (int r = r1; r <= r2; ++r) {
                for (int c = c1; c <= c2; ++c) {
                    if (grid[r][c] == 1) {
                        if (r < rmin) rmin = r;
                        if (r > rmax) rmax = r;
                        if (c < cmin) cmin = c;
                        if (c > cmax) cmax = c;
                    }
                }
            }
            if (rmin == int.MaxValue) return 0;
            return (rmax - rmin + 1) * (cmax - cmin + 1);
        }

        // три горизонтали
        for (int i = 1; i < m; ++i) {
            for (int j = i+1; j < m; ++j) {
                int a = Area(0, i-1, 0, n-1);
                int b = Area(i, j-1, 0, n-1);
                int c = Area(j, m-1, 0, n-1);
                ans = Math.Min(ans, a + b + c);
            }
        }

        // три вертикали
        for (int i = 1; i < n; ++i) {
            for (int j = i+1; j < n; ++j) {
                int a = Area(0, m-1, 0, i-1);
                int b = Area(0, m-1, i, j-1);
                int c = Area(0, m-1, j, n-1);
                ans = Math.Min(ans, a + b + c);
            }
        }

        // горизонтальный + вертикальный
        for (int i = 0; i < m-1; ++i) {
            for (int j = 0; j < n-1; ++j) {
                int topLeft = Area(0, i, 0, j);
                int topRight = Area(0, i, j+1, n-1);
                int bottom = Area(i+1, m-1, 0, n-1);
                ans = Math.Min(ans, topLeft + topRight + bottom);

                int top = Area(0, i, 0, n-1);
                int bottomLeft = Area(i+1, m-1, 0, j);
                int bottomRight = Area(i+1, m-1, j+1, n-1);
                ans = Math.Min(ans, top + bottomLeft + bottomRight);
            }
        }

        // вертикальный + горизонтальный
        for (int i = 0; i < n-1; ++i) {
            for (int j = 0; j < m-1; ++j) {
                int leftTop = Area(0, j, 0, i);
                int leftBottom = Area(j+1, m-1, 0, i);
                int right = Area(0, m-1, i+1, n-1);
                ans = Math.Min(ans, leftTop + leftBottom + right);

                int left = Area(0, m-1, 0, i);
                int rightTop = Area(0, j, i+1, n-1);
                int rightBottom = Area(j+1, m-1, i+1, n-1);
                ans = Math.Min(ans, left + rightTop + rightBottom);
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