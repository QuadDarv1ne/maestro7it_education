/*
https://leetcode.com/problems/trapping-rain-water-ii/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

import java.util.*;

class Solution {
    /*
    Решение задачи "Trapping Rain Water II" (LeetCode 407).
    - Используется PriorityQueue (min-heap) по высоте.
    - Начало с границ.
    - visited встроен через замену на -1 в heightMap.
    */
    public int trapRainWater(int[][] heightMap) {
        int m = heightMap.length;
        if (m == 0) return 0;
        int n = heightMap[0].length;
        if (m < 3 || n < 3) return 0;

        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[0]));

        for (int i = 0; i < m; i++) {
            pq.offer(new int[]{heightMap[i][0], i, 0});
            pq.offer(new int[]{heightMap[i][n-1], i, n-1});
            heightMap[i][0] = -1; heightMap[i][n-1] = -1;
        }
        for (int j = 1; j < n-1; j++) {
            pq.offer(new int[]{heightMap[0][j], 0, j});
            pq.offer(new int[]{heightMap[m-1][j], m-1, j});
            heightMap[0][j] = -1; heightMap[m-1][j] = -1;
        }

        int water = 0;
        int[][] dirs = {{1,0},{-1,0},{0,1},{0,-1}};

        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            int h = cur[0], x = cur[1], y = cur[2];
            for (int[] d : dirs) {
                int nx = x + d[0], ny = y + d[1];
                if (nx < 0 || nx >= m || ny < 0 || ny >= n || heightMap[nx][ny] == -1) continue;
                int nh = heightMap[nx][ny];
                if (nh < h) water += h - nh;
                pq.offer(new int[]{Math.max(h, nh), nx, ny});
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
