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

class Solution {
public:
    /*
     * Обрабатывает запросы двух типов в обратном порядке:
     * 1: [1, x] — установить препятствие в точке x.
     * 2: [2, x, sz] — проверить, можно ли разместить блок размера sz на отрезке [0, x].
     */
    vector<bool> getResults(vector<vector<int>>& queries) {
        const int n = min(50000, static_cast<int>(queries.size()) * 3);
        vector<bool> ans;
        vector<int> tree(n + 1, 0); // Дерево Фенвика
        
        auto fenwickMaximize = [&](int i, int val) {
            while (i <= n) {
                tree[i] = max(tree[i], val);
                i += i & -i;
            }
        };
        
        auto fenwickGet = [&](int i) -> int {
            int res = 0;
            while (i > 0) {
                res = max(res, tree[i]);
                i -= i & -i;
            }
            return res;
        };
        
        // Собираем все препятствия (без дубликатов)
        set<int> obstacleSet;
        obstacleSet.insert(0);
        obstacleSet.insert(n);
        
        for (auto& q : queries) {
            if (q[0] == 1) {
                int x = q[1];
                // Проверяем, что x в допустимом диапазоне и не равен sentinel
                if (x > 0 && x < n) {
                    obstacleSet.insert(x);
                }
            }
        }
        
        vector<int> obstacles(obstacleSet.begin(), obstacleSet.end());
        
        // Начальное заполнение дерева
        for (size_t i = 1; i < obstacles.size(); ++i) {
            int x1 = obstacles[i - 1];
            int x2 = obstacles[i];
            fenwickMaximize(x2, x2 - x1);
        }
        
        // Обрабатываем запросы с конца
        for (int i = queries.size() - 1; i >= 0; --i) {
            if (queries[i][0] == 1) {
                int x = queries[i][1];
                
                // Пропускаем sentinel-значения
                if (x == 0 || x >= n) continue;
                
                auto it = lower_bound(obstacles.begin(), obstacles.end(), x);
                // Проверяем, что элемент существует и не является границей
                if (it != obstacles.end() && it != obstacles.begin() && next(it) != obstacles.end()) {
                    int leftObstacle = *std::prev(it);
                    int rightObstacle = *std::next(it);
                    
                    obstacles.erase(it);
                    fenwickMaximize(rightObstacle, rightObstacle - leftObstacle);
                }
            } else {
                int x = queries[i][1];
                int sz = queries[i][2];
                
                // Ищем последнее препятствие <= x
                auto it = upper_bound(obstacles.begin(), obstacles.end(), x);
                int leftObstacle = *std::prev(it);
                
                ans.push_back(fenwickGet(leftObstacle) >= sz || x - leftObstacle >= sz);
            }
        }
        
        reverse(ans.begin(), ans.end());
        return ans;
    }
};