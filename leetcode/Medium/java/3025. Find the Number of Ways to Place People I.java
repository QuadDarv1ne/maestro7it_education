/**
 * https://leetcode.com/problems/find-the-number-of-ways-to-place-people-i/description/?envType=daily-question&envId=2025-09-02
 */

class Solution {
    /**
     * Задача:
     * Найти количество способов выбрать упорядоченные пары точек (i, j),
     * такие что:
     * 1) x1 <= x2 и y1 >= y2
     * 2) в прямоугольнике, образованном (x1, y1) и (x2, y2), нет других точек
     *
     * @param points массив точек [x, y]
     * @return количество допустимых пар
     */
    public int numberOfPairs(int[][] points) {
        int n = points.length;
        int ans = 0;

        for (int i = 0; i < n; i++) {
            int x1 = points[i][0], y1 = points[i][1];
            for (int j = 0; j < n; j++) {
                if (i == j) continue;
                int x2 = points[j][0], y2 = points[j][1];
                if (x1 <= x2 && y1 >= y2) {
                    boolean blocked = false;
                    for (int k = 0; k < n; k++) {
                        if (k == i || k == j) continue;
                        int xk = points[k][0], yk = points[k][1];
                        if (x1 <= xk && xk <= x2 && y2 <= yk && yk <= y1) {
                            blocked = true;
                            break;
                        }
                    }
                    if (!blocked) ans++;
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