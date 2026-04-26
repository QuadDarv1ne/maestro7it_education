/**
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
    public bool ContainsCycle(char[][] grid) {
        int m = grid.Length, n = grid[0].Length;
        bool[][] visited = new bool[m][];
        for (int i = 0; i < m; i++) visited[i] = new bool[n];
        int[][] dir = new int[][] { new[] {0, 1}, new[] {1, 0}, new[] {0, -1}, new[] {-1, 0} };
        
        bool Dfs(int x, int y, int px, int py) {
            visited[x][y] = true;
            foreach (var d in dir) {
                int nx = x + d[0], ny = y + d[1];
                if (nx < 0 || nx >= m || ny < 0 || ny >= n || grid[nx][ny] != grid[x][y]) 
                    continue;
                if (nx == px && ny == py) 
                    continue;
                if (visited[nx][ny]) 
                    return true;
                if (Dfs(nx, ny, x, y)) 
                    return true;
            }
            return false;
        }
        
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (!visited[i][j] && Dfs(i, j, -1, -1)) {
                    return true;
                }
            }
        }
        return false;
    }
}