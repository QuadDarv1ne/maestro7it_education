/**
 * https://leetcode.com/problems/course-schedule/description/
 */

import java.util.*;

public class Solution {
    /**
     * Определяет, можно ли пройти все курсы с учётом зависимостей.
     * Используется DFS для обнаружения циклов.
     *
     * @param numCourses Количество курсов
     * @param prerequisites Список зависимостей [course, prereq]
     * @return true, если можно пройти все курсы, иначе false
     */
    public boolean canFinish(int numCourses, int[][] prerequisites) {
        Map<Integer, List<Integer>> graph = new HashMap<>();
        for (int[] prereq : prerequisites) {
            graph.computeIfAbsent(prereq[0], k -> new ArrayList<>()).add(prereq[1]);
        }

        int[] visited = new int[numCourses]; // 0: unvisited, 1: visiting, 2: visited

        for (int i = 0; i < numCourses; i++) {
            if (visited[i] == 0 && !dfs(i, graph, visited)) return false;
        }
        return true;
    }

    private boolean dfs(int course, Map<Integer, List<Integer>> graph, int[] visited) {
        if (visited[course] == 1) return false;
        if (visited[course] == 2) return true;

        visited[course] = 1;
        for (int prereq : graph.getOrDefault(course, new ArrayList<>())) {
            if (!dfs(prereq, graph, visited)) return false;
        }
        visited[course] = 2;
        return true;
    }
}

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