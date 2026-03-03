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
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        vector<vector<int>> graph(numCourses);
        for (auto& pre : prerequisites) {
            graph[pre[1]].push_back(pre[0]); // prereq -> course
        }
        
        vector<int> state(numCourses, 0); // 0 unvisited, 1 visiting, 2 visited
        
        function<bool(int)> hasCycle = [&](int node) {
            if (state[node] == 1) return true;
            if (state[node] == 2) return false;
            
            state[node] = 1;
            for (int neighbor : graph[node]) {
                if (hasCycle(neighbor)) return true;
            }
            state[node] = 2;
            return false;
        };
        
        for (int i = 0; i < numCourses; i++) {
            if (hasCycle(i)) return false;
        }
        return true;
    }
};