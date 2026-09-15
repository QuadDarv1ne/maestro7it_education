/**
 * https://leetcode.com/problems/balance-a-binary-search-tree/description/
 * Автор: Дуплей Максим Игоревич - AGLA
 * ORCID: https://orcid.org/0009-0007-7605-539X
 * GitHub: https://github.com/QuadDarv1ne/
 * 
 * Полезные ссылки:
 * 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
 * 2. Telegram №1 @quadd4rv1n7
 * 3. Telegram №2 @dupley_maxim_1999
 * 4. Rutube канал: https://rutube.ru/channel/4218729/
 * 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
 * 6. YouTube канал: https://www.youtube.com/@it-coders
 * 7. ВК группа: https://vk.com/science_geeks
 */

public class Solution {
    public bool HasValidPath(int[][] grid) {
        int m = grid.Length, n = grid[0].Length;
        // delta для направлений 0: вверх, 1: вправо, 2: вниз, 3: влево
        int[][] dirs = new int[][] { new int[] {-1, 0}, new int[] {0, 1}, new int[] {1, 0}, new int[] {0, -1} };
        
        // Предрасчёт допустимых направлений для каждого типа труб (1-6)
        List<int>[] pipes = new List<int>[7];
        for (int i = 0; i <= 6; i++) pipes[i] = new List<int>();
        pipes[1] = new List<int> { 1, 3 };
        pipes[2] = new List<int> { 0, 2 };
        pipes[3] = new List<int> { 2, 3 };
        pipes[4] = new List<int> { 1, 2 };
        pipes[5] = new List<int> { 0, 3 };
        pipes[6] = new List<int> { 0, 1 };
        
        bool[,] visited = new bool[m, n];
        Queue<(int, int)> queue = new Queue<(int, int)>();
        queue.Enqueue((0, 0));
        visited[0, 0] = true;
        
        while (queue.Count > 0) {
            var (x, y) = queue.Dequeue();
            if (x == m-1 && y == n-1) return true;
            
            int type = grid[x][y];
            foreach (int d in pipes[type]) {
                int nx = x + dirs[d][0], ny = y + dirs[d][1];
                if (nx < 0 || nx >= m || ny < 0 || ny >= n || visited[nx, ny]) continue;
                
                int nextType = grid[nx][ny];
                foreach (int rd in pipes[nextType]) {
                    if (rd == (d ^ 2)) {
                        visited[nx, ny] = true;
                        queue.Enqueue((nx, ny));
                        break;
                    }
                }
            }
        }
        return false;
    }
}