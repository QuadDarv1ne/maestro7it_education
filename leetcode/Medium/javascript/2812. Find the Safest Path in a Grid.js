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
 * @param {number[][]} grid - Квадратная матрица n x n, где 1 - вор, 0 - пустая клетка
 * @return {number} - Максимальный возможный коэффициент безопасности пути
 */
var maximumSafenessFactor = function(grid) {
    const n = grid.length;
    
    // Шаг 1: BFS от всех воров для вычисления расстояний
    const dist = Array.from({length: n}, () => Array(n).fill(-1));
    const queue = [];
    
    // Инициализация очереди всеми ворами
    for (let r = 0; r < n; r++) {
        for (let c = 0; c < n; c++) {
            if (grid[r][c] === 1) {
                dist[r][c] = 0;
                queue.push([r, c]);
            }
        }
    }
    
    // Направления движения (вверх, вниз, влево, вправо)
    const dirs = [[0, 1], [0, -1], [1, 0], [-1, 0]];
    
    // Многопроходный BFS
    let head = 0;
    while (head < queue.length) {
        const [r, c] = queue[head++];
        
        for (const [dr, dc] of dirs) {
            const nr = r + dr, nc = c + dc;
            if (nr >= 0 && nr < n && nc >= 0 && nc < n && dist[nr][nc] === -1) {
                dist[nr][nc] = dist[r][c] + 1;
                queue.push([nr, nc]);
            }
        }
    }
    
    // Шаг 2: Бинарный поиск по коэффициенту безопасности
    let left = 0, right = 2 * n;
    let answer = 0;
    
    // Функция для проверки достижимости с заданным лимитом
    const canReach = (limit) => {
        // Проверка стартовой и конечной клеток
        if (dist[0][0] < limit || dist[n-1][n-1] < limit) {
            return false;
        }
        
        const visited = Array.from({length: n}, () => Array(n).fill(false));
        const bfs = [[0, 0]];
        visited[0][0] = true;
        
        let head = 0;
        while (head < bfs.length) {
            const [r, c] = bfs[head++];
            
            if (r === n - 1 && c === n - 1) {
                return true;
            }
            
            for (const [dr, dc] of dirs) {
                const nr = r + dr, nc = c + dc;
                if (nr >= 0 && nr < n && nc >= 0 && nc < n && 
                    !visited[nr][nc] && dist[nr][nc] >= limit) {
                    visited[nr][nc] = true;
                    bfs.push([nr, nc]);
                }
            }
        }
        return false;
    };
    
    // Бинарный поиск максимального допустимого limit
    while (left <= right) {
        const mid = Math.floor((left + right) / 2);
        if (canReach(mid)) {
            answer = mid;
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    
    return answer;
};