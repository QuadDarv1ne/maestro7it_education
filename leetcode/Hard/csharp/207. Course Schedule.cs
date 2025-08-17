/**
 * https://leetcode.com/problems/course-schedule/description/
 */

using System;
using System.Collections.Generic;

public class Solution {
    /// <summary>
    /// Определяет, можно ли пройти все курсы с учётом зависимостей.
    /// Используется DFS для обнаружения циклов в графе зависимостей.
    /// </summary>
    /// <param name="numCourses">Количество курсов</param>
    /// <param name="prerequisites">Список зависимостей [course, prereq]</param>
    /// <returns>true, если можно пройти все курсы, иначе false</returns>
    public bool CanFinish(int numCourses, int[][] prerequisites) {
        var graph = new Dictionary<int, List<int>>();
        foreach (var prereq in prerequisites) {
            if (!graph.ContainsKey(prereq[0])) graph[prereq[0]] = new List<int>();
            graph[prereq[0]].Add(prereq[1]);
        }

        int[] visited = new int[numCourses]; // 0: не посещен, 1: в процессе, 2: посещен

        bool Dfs(int course) {
            if (visited[course] == 1) return false;
            if (visited[course] == 2) return true;

            visited[course] = 1;
            if (graph.ContainsKey(course)) {
                foreach (var prereq in graph[course]) {
                    if (!Dfs(prereq)) return false;
                }
            }
            visited[course] = 2;
            return true;
        }

        for (int i = 0; i < numCourses; i++) {
            if (visited[i] == 0 && !Dfs(i)) return false;
        }

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