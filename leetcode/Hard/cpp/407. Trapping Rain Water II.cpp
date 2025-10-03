/*
https://leetcode.com/problems/trapping-rain-water-ii/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

using System;
using System.Collections.Generic;

public class Solution {
    /*
    Решение задачи "Trapping Rain Water II" (LeetCode 407).

    Идея:
    - Используем PriorityQueue (min-heap) для обхода клеток по возрастанию высоты.
    - Начинаем с внешних границ и постепенно "затягиваем" внутрь.
    - Если сосед ниже текущего уровня, добавляем воду.
    - visited реализован через замену на -1 прямо в heightMap для оптимизации памяти.
    */
    public int TrapRainWater(int[][] heightMap) {
        int m = heightMap.Length;
        if (m == 0) return 0;
        int n = heightMap[0].Length;
        if (m < 3 || n < 3) return 0;

        var pq = new SortedSet<(int, int, int)>(
            Comparer<(int, int, int)>.Create((a,b) => 
                a.Item1 != b.Item1 ? a.Item1 - b.Item1 : (a.Item2 != b.Item2 ? a.Item2 - b.Item2 : a.Item3 - b.Item3)
            )
        );

        // Границы
        for (int i = 0; i < m; i++) {
            pq.Add((heightMap[i][0], i, 0));
            pq.Add((heightMap[i][n-1], i, n-1));
            heightMap[i][0] = -1;
            heightMap[i][n-1] = -1;
        }
        for (int j = 1; j < n-1; j++) {
            pq.Add((heightMap[0][j], 0, j));
            pq.Add((heightMap[m-1][j], m-1, j));
            heightMap[0][j] = -1;
            heightMap[m-1][j] = -1;
        }

        int water = 0;
        int[,] dirs = { {1,0},{-1,0},{0,1},{0,-1} };

        while (pq.Count > 0) {
            var cur = pq.Min; pq.Remove(cur);
            int h = cur.Item1;
            int x = cur.Item2;
            int y = cur.Item3;
            for (int d = 0; d < 4; d++) {
                int nx = x + dirs[d,0], ny = y + dirs[d,1];
                if (nx < 0 || nx >= m || ny < 0 || ny >= n || heightMap[nx][ny] == -1) continue;
                int nh = heightMap[nx][ny];
                if (nh < h) water += h - nh;
                pq.Add((Math.Max(h, nh), nx, ny));
                heightMap[nx][ny] = -1;
            }
        }

        return water;
    }
}

/* Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07 
 * 2. Telegram №1 @quadd4rv1n7 
 * 3. Telegram №2 @dupley_maxim_1999 
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */
