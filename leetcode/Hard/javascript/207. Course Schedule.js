/**
 * https://leetcode.com/problems/course-schedule/description/
 */

/**
 * Определяет, можно ли пройти все курсы с учётом зависимостей.
 * Используется DFS для обнаружения циклов.
 *
 * @param {number} numCourses Количество курсов
 * @param {number[][]} prerequisites Список зависимостей [course, prereq]
 * @return {boolean} True, если можно пройти все курсы, иначе False
 */
var canFinish = function(numCourses, prerequisites) {
    const graph = Array.from({ length: numCourses }, () => []);
    for (const [course, prereq] of prerequisites) {
        graph[course].push(prereq);
    }

    const visited = new Array(numCourses).fill(0); // 0: unvisited, 1: visiting, 2: visited

    const dfs = (course) => {
        if (visited[course] === 1) return false;
        if (visited[course] === 2) return true;

        visited[course] = 1;
        for (const prereq of graph[course]) {
            if (!dfs(prereq)) return false;
        }
        visited[course] = 2;
        return true;
    }

    for (let i = 0; i < numCourses; i++) {
        if (visited[i] === 0 && !dfs(i)) return false;
    }
    return true;
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