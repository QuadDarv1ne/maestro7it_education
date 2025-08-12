/**
 * https://leetcode.com/problems/triangle/description/?envType=study-plan-v2&envId=top-interview-150
 */

import java.util.List;

class Solution {
    /**
     * Находит минимальную сумму пути от вершины треугольника до основания.
     * Двигаемся по соседним числам на каждом уровне, используя динамическое программирование.
     *
     * @param triangle Список списков целых чисел, представляющих треугольник.
     * @return Минимальная сумма пути.
     */
    public int minimumTotal(List<List<Integer>> triangle) {
        int[] dp = new int[triangle.size()];
        // Инициализация dp последним уровнем треугольника
        List<Integer> lastRow = triangle.get(triangle.size() - 1);
        for (int i = 0; i < lastRow.size(); i++) {
            dp[i] = lastRow.get(i);
        }

        // Проход снизу вверх
        for (int row = triangle.size() - 2; row >= 0; row--) {
            List<Integer> currentRow = triangle.get(row);
            for (int i = 0; i < currentRow.size(); i++) {
                dp[i] = currentRow.get(i) + Math.min(dp[i], dp[i + 1]);
            }
        }

        return dp[0];
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