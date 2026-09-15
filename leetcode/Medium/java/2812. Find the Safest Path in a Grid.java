import java.util.*;

class Solution {
    /**
     * Находит максимальный коэффициент безопасности пути в сетке с ворами.
     * 
     * Коэффициент безопасности пути определяется как минимальное манхэттенское 
     * расстояние от любой клетки на пути до ближайшего вора.
     * 
     * Алгоритм:
     * 1. Многопроходный BFS от всех воров для вычисления расстояния до ближайшего вора
     * 2. Бинарный поиск по возможному значению коэффициента безопасности
     * 3. Проверка достижимости с использованием BFS
     * 
     * @param grid Квадратная матрица n x n, где 1 - вор, 0 - пустая клетка
     * @return Максимальный возможный коэффициент безопасности пути
     */
    public int maximumSafenessFactor(List<List<Integer>> grid) {
        int n = grid.size();
        
        // Шаг 1: BFS от всех воров для вычисления расстояний
        int[][] dist = new int[n][n];
        for (int[] row : dist) {
            Arrays.fill(row, -1);
        }
        
        Queue<int[]> q = new LinkedList<>();
        
        // Инициализация очереди всеми ворами
        for (int r = 0; r < n; r++) {
            for (int c = 0; c < n; c++) {
                if (grid.get(r).get(c) == 1) {
                    dist[r][c] = 0;
                    q.offer(new int[]{r, c});
                }
            }
        }
        
        // Направления движения (вверх, вниз, влево, вправо)
        int[][] dirs = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
        
        // Многопроходный BFS
        while (!q.isEmpty()) {
            int[] cell = q.poll();
            int r = cell[0], c = cell[1];
            
            for (int[] dir : dirs) {
                int nr = r + dir[0], nc = c + dir[1];
                if (nr >= 0 && nr < n && nc >= 0 && nc < n && dist[nr][nc] == -1) {
                    dist[nr][nc] = dist[r][c] + 1;
                    q.offer(new int[]{nr, nc});
                }
            }
        }
        
        // Шаг 2: Бинарный поиск по коэффициенту безопасности
        int left = 0, right = 2 * n;
        int answer = 0;
        
        // Лямбда-функция для проверки достижимости с заданным лимитом
        java.util.function.Predicate<Integer> canReach = (limit) -> {
            // Проверка стартовой и конечной клеток
            if (dist[0][0] < limit || dist[n-1][n-1] < limit) {
                return false;
            }
            
            boolean[][] visited = new boolean[n][n];
            Queue<int[]> bfs = new LinkedList<>();
            bfs.offer(new int[]{0, 0});
            visited[0][0] = true;
            
            while (!bfs.isEmpty()) {
                int[] current = bfs.poll();
                int r = current[0], c = current[1];
                
                if (r == n - 1 && c == n - 1) {
                    return true;
                }
                
                for (int[] dir : dirs) {
                    int nr = r + dir[0], nc = c + dir[1];
                    if (nr >= 0 && nr < n && nc >= 0 && nc < n && 
                        !visited[nr][nc] && dist[nr][nc] >= limit) {
                        visited[nr][nc] = true;
                        bfs.offer(new int[]{nr, nc});
                    }
                }
            }
            return false;
        };
        
        // Бинарный поиск максимального допустимого limit
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (canReach.test(mid)) {
                answer = mid;
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return answer;
    }
}