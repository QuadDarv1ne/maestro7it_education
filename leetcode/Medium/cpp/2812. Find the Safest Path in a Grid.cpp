#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

class Solution {
public:
    /**
     * Находит максимальный коэффициент безопасности пути в сетке с ворами.
     * 
     * Коэффициент безопасности пути определяется как минимальное манхэттенское 
     * расстояние от любой клетки на пути до ближайшего вора.
     * 
     * Алгоритм:
     * 1. Многопроходный BFS от всех воров для вычисления расстояния до ближайшего вора
     * 2. Бинарный поиск по возможному значению коэффициента безопасности
     * 3. Проверка достижимости с использованием BFS/DFS
     * 
     * @param grid Квадратная матрица n x n, где 1 - вор, 0 - пустая клетка
     * @return Максимальный возможный коэффициент безопасности пути
     */
    int maximumSafenessFactor(vector<vector<int>>& grid) {
        int n = grid.size();
        
        // Шаг 1: BFS от всех воров для вычисления расстояний
        vector<vector<int>> dist(n, vector<int>(n, -1));
        queue<pair<int, int>> q;
        
        // Инициализация очереди всеми ворами
        for (int r = 0; r < n; ++r) {
            for (int c = 0; c < n; ++c) {
                if (grid[r][c] == 1) {
                    dist[r][c] = 0;
                    q.push({r, c});
                }
            }
        }
        
        // Направления движения (вверх, вниз, влево, вправо)
        vector<pair<int, int>> dirs = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
        
        // Многопроходный BFS
        while (!q.empty()) {
            auto [r, c] = q.front();
            q.pop();
            
            for (auto [dr, dc] : dirs) {
                int nr = r + dr, nc = c + dc;
                if (nr >= 0 && nr < n && nc >= 0 && nc < n && dist[nr][nc] == -1) {
                    dist[nr][nc] = dist[r][c] + 1;
                    q.push({nr, nc});
                }
            }
        }
        
        // Шаг 2: Бинарный поиск по коэффициенту безопасности
        int left = 0, right = 2 * n;
        int answer = 0;
        
        // Лямбда-функция для проверки достижимости с заданным лимитом
        auto canReach = [&](int limit) -> bool {
            // Проверка стартовой и конечной клеток
            if (dist[0][0] < limit || dist[n-1][n-1] < limit) {
                return false;
            }
            
            vector<vector<bool>> visited(n, vector<bool>(n, false));
            queue<pair<int, int>> bfs;
            bfs.push({0, 0});
            visited[0][0] = true;
            
            while (!bfs.empty()) {
                auto [r, c] = bfs.front();
                bfs.pop();
                
                if (r == n - 1 && c == n - 1) {
                    return true;
                }
                
                for (auto [dr, dc] : dirs) {
                    int nr = r + dr, nc = c + dc;
                    if (nr >= 0 && nr < n && nc >= 0 && nc < n && 
                        !visited[nr][nc] && dist[nr][nc] >= limit) {
                        visited[nr][nc] = true;
                        bfs.push({nr, nc});
                    }
                }
            }
            return false;
        };
        
        // Бинарный поиск максимального допустимого limit
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (canReach(mid)) {
                answer = mid;
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return answer;
    }
};