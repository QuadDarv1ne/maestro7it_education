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

class Solution {
    public boolean hasValidPath(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int[][] dirs = {{-1,0}, {0,1}, {1,0}, {0,-1}}; // вверх, вправо, вниз, влево
        
        // Предрасчёт допустимых направлений для каждого типа труб (1-6)
        List<Integer>[] pipes = new List[7];
        for (int i = 0; i <= 6; i++) pipes[i] = new ArrayList<>();
        pipes[1] = Arrays.asList(1, 3);
        pipes[2] = Arrays.asList(0, 2);
        pipes[3] = Arrays.asList(2, 3);
        pipes[4] = Arrays.asList(1, 2);
        pipes[5] = Arrays.asList(0, 3);
        pipes[6] = Arrays.asList(0, 1);
        
        boolean[][] visited = new boolean[m][n];
        Queue<int[]> queue = new LinkedList<>();
        queue.offer(new int[]{0, 0});
        visited[0][0] = true;
        
        while (!queue.isEmpty()) {
            int[] cur = queue.poll();
            int x = cur[0], y = cur[1];
            if (x == m-1 && y == n-1) return true;
            
            int type = grid[x][y];
            for (int d : pipes[type]) {
                int nx = x + dirs[d][0], ny = y + dirs[d][1];
                if (nx < 0 || nx >= m || ny < 0 || ny >= n || visited[nx][ny]) continue;
                
                int nextType = grid[nx][ny];
                for (int rd : pipes[nextType]) {
                    if (rd == (d ^ 2)) {
                        visited[nx][ny] = true;
                        queue.offer(new int[]{nx, ny});
                        break;
                    }
                }
            }
        }
        return false;
    }
}