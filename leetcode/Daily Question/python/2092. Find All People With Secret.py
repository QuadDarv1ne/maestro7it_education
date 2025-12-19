'''
https://leetcode.com/problems/find-all-people-with-secret/?envType=daily-question&envId=2025-12-19

Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Find All People With Secret"

Сложность:
- Сортировка встреч: O(m log m)
- Обход блоков встреч: O(m + n)
'''

class Solution:
    def findAllPeople(self, n, meetings, firstPerson):
        # Сортируем по времени
        meetings.sort(key=lambda x: x[2])

        # Те, кто знает секрет (изначально 0 -> firstPerson)
        known = {0, firstPerson}

        i = 0
        m = len(meetings)

        while i < m:
            t = meetings[i][2]
            # Собираем все встречи c временем t
            group = []
            while i < m and meetings[i][2] == t:
                group.append(meetings[i])
                i += 1

            # Построим граф участников этой группы
            adj = {}
            participants = set()
            for x, y, _ in group:
                adj.setdefault(x, []).append(y)
                adj.setdefault(y, []).append(x)
                participants.add(x)
                participants.add(y)

            # Узнаем, кто из участников уже знает секрет
            queue = []
            for p in participants:
                if p in known:
                    queue.append(p)

            # BFS по этому временному подграфу
            visited = set(queue)
            while queue:
                cur = queue.pop()
                for nei in adj.get(cur, []):
                    if nei not in visited:
                        visited.add(nei)
                        queue.append(nei)

            # Все visited получают секрет
            known |= visited

        return list(known)
