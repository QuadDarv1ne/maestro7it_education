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
public:
    bool hasValidPath(vector<vector<int>>& grid) {
        int m = grid.size(), n = grid[0].size();
        // delta для направлений 0: вверх, 1: вправо, 2: вниз, 3: влево
        int dirs[4][2] = {{-1, 0}, {0, 1}, {1, 0}, {0, -1}};
        
        // Предрасчёт допустимых направлений для каждого типа труб (1-6)
        vector<vector<int>> pipes = {
            {},          // заглушка, индекс 0 не используется
            {1, 3},      // тип 1: соединение (право, лево)
            {0, 2},      // тип 2: соединение (верх, низ)
            {2, 3},      // тип 3: соединение (низ, лево)
            {1, 2},      // тип 4: соединение (право, низ)
            {0, 3},      // тип 5: соединение (верх, лево)
            {0, 1}       // тип 6: соединение (верх, право)
        };
        
        vector<vector<bool>> visited(m, vector<bool>(n, false));
        queue<pair<int, int>> q;
        q.push({0, 0});
        visited[0][0] = true;
        
        while (!q.empty()) {
            auto [x, y] = q.front(); q.pop();
            if (x == m-1 && y == n-1) return true;
            
            int type = grid[x][y];
            for (int d : pipes[type]) {
                int nx = x + dirs[d][0], ny = y + dirs[d][1];
                // Проверка границ и посещения
                if (nx < 0 || nx >= m || ny < 0 || ny >= n || visited[nx][ny]) continue;
                
                int nextType = grid[nx][ny];
                // Проверка обратной совместимости
                for (int rd : pipes[nextType]) {
                    if (rd == (d ^ 2)) { // противоположное направление
                        visited[nx][ny] = true;
                        q.push({nx, ny});
                        break;
                    }
                }
            }
        }
        return false;
    }
};