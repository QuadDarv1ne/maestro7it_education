/**
 * https://leetcode.com/problems/triangle/description/?envType=study-plan-v2&envId=top-interview-150
 */

using System;
using System.Collections.Generic;

public class Solution {
    /// <summary>
    /// Находит минимальную сумму пути от вершины треугольника до основания.
    /// Двигаемся по соседним числам на каждом уровне, используя динамическое программирование.
    /// </summary>
    /// <param name="triangle">Список списков целых чисел, представляющих треугольник.</param>
    /// <returns>Минимальная сумма пути.</returns>
    public int MinimumTotal(IList<IList<int>> triangle) {
        int n = triangle.Count;
        int[] dp = new int[n];
        
        // Копируем последний уровень
        for (int i = 0; i < n; i++) {
            dp[i] = triangle[n - 1][i];
        }

        // Проходим снизу вверх
        for (int row = n - 2; row >= 0; row--) {
            for (int i = 0; i <= row; i++) {
                dp[i] = triangle[row][i] + Math.Min(dp[i], dp[i + 1]);
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