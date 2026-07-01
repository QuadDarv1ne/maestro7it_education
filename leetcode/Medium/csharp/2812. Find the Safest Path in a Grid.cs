using System;
using System.Collections.Generic;

public class Solution {
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
    public int MaximumSafenessFactor(IList<IList<int>> grid) {
        int n = grid.Count;
        
        // Шаг 1: BFS от всех воров для вычисления расстояний
        int[][] dist = new int[n][];
        for (int i = 0; i < n; i++) {
            dist[i] = new int[n];
            Array.Fill(dist[i], -1);
        }
        
        Queue<(int, int)> q = new Queue<(int, int)>();
        
        // Инициализация очереди всеми ворами
        for (int r = 0; r < n; r++) {
            for (int c = 0; c < n; c++) {
                if (grid[r][c] == 1) {
                    dist[r][c] = 0;
                    q.Enqueue((r, c));
                }
            }
        }
        
        // Направления движения (вверх, вниз, влево, вправо)
        int[][] dirs = new int[][] { 
            new int[] {0, 1}, new int[] {0, -1}, 
            new int[] {1, 0}, new int[] {-1, 0} 
        };
        
        // Многопроходный BFS
        while (q.Count > 0) {
            var (r, c) = q.Dequeue();
            
            foreach (var dir in dirs) {
                int nr = r + dir[0], nc = c + dir[1];
                if (nr >= 0 && nr < n && nc >= 0 && nc < n && dist[nr][nc] == -1) {
                    dist[nr][nc] = dist[r][c] + 1;
                    q.Enqueue((nr, nc));
                }
            }
        }
        
        // Шаг 2: Бинарный поиск по коэффициенту безопасности
        int left = 0, right = 2 * n;
        int answer = 0;
        
        // Локальная функция для проверки достижимости с заданным лимитом
        bool CanReach(int limit) {
            // Проверка стартовой и конечной клеток
            if (dist[0][0] < limit || dist[n-1][n-1] < limit) {
                return false;
            }
            
            bool[][] visited = new bool[n][];
            for (int i = 0; i < n; i++) {
                visited[i] = new bool[n];
            }
            
            Queue<(int, int)> bfs = new Queue<(int, int)>();
            bfs.Enqueue((0, 0));
            visited[0][0] = true;
            
            while (bfs.Count > 0) {
                var (r, c) = bfs.Dequeue();
                
                if (r == n - 1 && c == n - 1) {
                    return true;
                }
                
                foreach (var dir in dirs) {
                    int nr = r + dir[0], nc = c + dir[1];
                    if (nr >= 0 && nr < n && nc >= 0 && nc < n && 
                        !visited[nr][nc] && dist[nr][nc] >= limit) {
                        visited[nr][nc] = true;
                        bfs.Enqueue((nr, nc));
                    }
                }
            }
            return false;
        }
        
        // Бинарный поиск максимального допустимого limit
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (CanReach(mid)) {
                answer = mid;
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return answer;
    }
}