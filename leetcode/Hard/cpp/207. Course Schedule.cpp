/**
 * https://leetcode.com/problems/course-schedule/description/
 */

#include <vector>
#include <unordered_map>
#include <unordered_set>
using namespace std;

class Solution {
public:
    /**
     * Определяет, можно ли пройти все курсы с учётом зависимостей.
     * Используется DFS для обнаружения циклов.
     * @param numCourses Количество курсов
     * @param prerequisites Список зависимостей [course, prereq]
     * @return true, если можно пройти все курсы, иначе false
     */
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        unordered_map<int, unordered_set<int>> graph;
        for (auto& prereq : prerequisites) {
            graph[prereq[0]].insert(prereq[1]);
        }

        vector<int> visited(numCourses, 0); // 0: unvisited, 1: visiting, 2: visited
        for (int i = 0; i < numCourses; ++i) {
            if (hasCycle(i, graph, visited)) return false;
        }
        return true;
    }

private:
    bool hasCycle(int node, unordered_map<int, unordered_set<int>>& graph, vector<int>& visited) {
        if (visited[node] == 1) return true;
        if (visited[node] == 2) return false;

        visited[node] = 1;
        for (int neighbor : graph[node]) {
            if (hasCycle(neighbor, graph, visited)) return true;
        }
        visited[node] = 2;
        return false;
    }
};

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/