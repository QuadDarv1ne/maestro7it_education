/**
 * https://leetcode.com/problems/find-the-number-of-ways-to-place-people-ii/description/?envType=daily-question&envId=2025-09-03
 */

public class Solution {
    /// <summary>
    /// Возвращает количество допустимых пар (Alice, Bob), таких что
    /// Alice — верхний левый угол, Bob — нижний правый, и внутри или
    /// на границе прямоугольника нет других точек.
    /// </summary>
    public int NumberOfPairs(int[][] points) {
        Array.Sort(points, (a, b) => {
            if (a[0] == b[0]) return b[1] - a[1]; // x равны → сортируем по y убыванию
            return a[0] - b[0]; // иначе по x возрастанию
        });

        int ans = 0;
        int n = points.Length;

        for (int i = 0; i < n; i++) {
            int y1 = points[i][1];
            int maxY = int.MinValue;
            for (int j = i + 1; j < n; j++) {
                int y2 = points[j][1];
                if (maxY < y2 && y2 <= y1) {
                    ans++;
                    maxY = y2;
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