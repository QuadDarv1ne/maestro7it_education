'''
https://leetcode.com/problems/design-task-manager/description/?envType=daily-question&envId=2025-09-18
'''

import heapq

class TaskManager:
    """
    Менеджер задач.

    Порядок выбора задачи для выполнения:
      1) максимальный priority (больше лучше);
      2) при равных priority — максимальный taskId (больше лучше).
    execTop() возвращает userId выполненной задачи (и удаляет эту задачу).
    Если задач нет — возвращается -1.

    Реализация:
      - max-heap через heapq с кортежем (-priority, -taskId, taskId, userId).
      - словарь active: taskId -> (priority, userId) — хранит актуальные задачи.
      - при edit/add мы обновляем active и добавляем новую запись в heap.
      - при rmv просто удаляем запись из active; устаревшие записи пропускаются при execTop.
    """

    def __init__(self, tasks):
        """
        tasks: список записей [userId, taskId, priority]
        """
        self.heap = []     # элементы: (-priority, -taskId, taskId, userId)
        self.active = {}   # taskId -> (priority, userId)
        if tasks:
            for userId, taskId, priority in tasks:
                self.add(userId, taskId, priority)

    def add(self, userId, taskId, priority):
        """
        Добавить задачу.
        """
        self.active[taskId] = (priority, userId)
        heapq.heappush(self.heap, (-priority, -taskId, taskId, userId))

    def edit(self, taskId, newPriority):
        """
        Изменить приоритет задачи (если задача существует).
        """
        if taskId in self.active:
            _, userId = self.active[taskId]
            self.active[taskId] = (newPriority, userId)
            heapq.heappush(self.heap, (-newPriority, -taskId, taskId, userId))

    def rmv(self, taskId):
        """
        Удалить задачу (если есть).
        """
        if taskId in self.active:
            del self.active[taskId]

    def execTop(self):
        """
        Выполнить (удалить) и вернуть userId задачи с наивысшим приоритетом.
        Возвращает -1, если задач нет.
        """
        while self.heap:
            neg_pr, neg_tid, tid, uid = heapq.heappop(self.heap)
            if tid in self.active:
                cur_pr, cur_uid = self.active[tid]
                if cur_pr == -neg_pr and cur_uid == uid:
                    del self.active[tid]
                    return uid
        return -1

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks