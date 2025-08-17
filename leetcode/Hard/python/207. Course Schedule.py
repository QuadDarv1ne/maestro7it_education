'''
https://leetcode.com/problems/course-schedule/description/
'''

# from typing import List
# from collections import defaultdict

class Solution:
    # def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
    def canFinish(self, numCourses, prerequisites):
        """
        Определяет, можно ли пройти все курсы с учётом зависимостей.
        Используется DFS для обнаружения циклов.

        :param numCourses: Количество курсов
        :param prerequisites: Список зависимостей [course, prereq]
        :return: True, если можно пройти все курсы, иначе False
        """
        graph = defaultdict(list)
        for dest, src in prerequisites:
            graph[dest].append(src)

        visited = [0] * numCourses  # 0: unvisited, 1: visiting, 2: visited

        def dfs(course):
            if visited[course] == 1:
                return False
            if visited[course] == 2:
                return True

            visited[course] = 1
            for prereq in graph[course]:
                if not dfs(prereq):
                    return False
            visited[course] = 2
            return True

        for i in range(numCourses):
            if visited[i] == 0 and not dfs(i):
                return False
        return True

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks