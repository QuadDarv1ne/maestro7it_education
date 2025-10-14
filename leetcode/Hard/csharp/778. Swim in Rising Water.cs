/*
https://leetcode.com/problems/swim-in-rising-water/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

using System;
using System.Collections.Generic;

public class Solution {
    public int SwimInWater(int[][] grid) {
        int n = grid.Length;
        bool[,] seen = new bool[n, n];
        // Min-heap: используем PriorityQueue из .NET (если версия позволяет) или симуляция через SortedSet / другие структуры
        // Здесь я покажу с PriorityQueue (доступен в .NET 6+)
        var pq = new PriorityQueue<(int time, int x, int y), int>();
        pq.Enqueue((grid[0][0], 0, 0), grid[0][0]);
        seen[0, 0] = true;
        int res = 0;
        int[][] dirs = new int[][] {
            new int[]{1,0}, new int[]{-1,0}, new int[]{0,1}, new int[]{0,-1}
        };

        while (pq.Count > 0) {
            var cur = pq.Dequeue();
            int time = cur.time, x = cur.x, y = cur.y;
            res = Math.Max(res, time);
            if (x == n-1 && y == n-1) {
                return res;
            }
            foreach (var d in dirs) {
                int nx = x + d[0], ny = y + d[1];
                if (nx < 0 || nx >= n || ny < 0 || ny >= n) continue;
                if (seen[nx, ny]) continue;
                seen[nx, ny] = true;
                int nt = Math.Max(time, grid[nx][ny]);
                pq.Enqueue((nt, nx, ny), nt);
            }
        }
        return -1;
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