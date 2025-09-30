/**
 * https://leetcode.com/problems/largest-triangle-area/description/?envType=daily-question&envId=2025-09-27
 */

using System;

public class Solution {
    public double LargestTriangleArea(int[][] points) {
        int n = points.Length;
        double ans = 0.0;
        for (int i = 0; i < n; i++) {
            int x1 = points[i][0], y1 = points[i][1];
            for (int j = i + 1; j < n; j++) {
                int x2 = points[j][0], y2 = points[j][1];
                for (int k = j + 1; k < n; k++) {
                    int x3 = points[k][0], y3 = points[k][1];
                    double cross = (double)(x2 - x1) * (y3 - y1) - (double)(x3 - x1) * (y2 - y1);
                    double area = Math.Abs(cross) / 2.0;
                    if (area > ans) {
                        ans = area;
                    }
                }
            }
        }
        return ans;
    }
}

/*
''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/