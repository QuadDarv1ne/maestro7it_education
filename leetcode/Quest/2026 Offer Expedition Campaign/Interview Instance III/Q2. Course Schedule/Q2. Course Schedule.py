'''
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
'''

class Solution:
    def canFinish(self, numCourses, prerequisites):
        # Build adjacency list
        graph = [[] for _ in range(numCourses)]
        for course, prereq in prerequisites:
            graph[prereq].append(course)
        
        # 0 = unvisited, 1 = visiting, 2 = visited
        state = [0] * numCourses
        
        def has_cycle(node):
            if state[node] == 1:  # Currently in recursion stack -> cycle
                return True
            if state[node] == 2:  # Already fully processed
                return False
            
            state[node] = 1  # Mark as visiting
            for neighbor in graph[node]:
                if has_cycle(neighbor):
                    return True
            state[node] = 2  # Mark as fully processed
            return False
        
        # Check each course for cycles
        for course in range(numCourses):
            if has_cycle(course):
                return False
        return True