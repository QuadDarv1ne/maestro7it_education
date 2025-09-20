"""
https://leetcode.com/problems/implement-router/description/?envType=daily-question&envId=2025-09-20
"""

from collections import deque, defaultdict
import bisect

class Router:
    """
    Класс Router — модель маршрутизатора с ограниченной памятью.

    Атрибуты:
        memoryLimit: максимальное число пакетов, которые можно хранить
        queue: очередь пакетов (FIFO)
        seen: множество для проверки уникальности пакета
        destMap: словарь destination -> список timestamp
        startIndex: словарь destination -> индекс начала актуальных timestamp

    Методы:
        addPacket(source, destination, timestamp):
            Добавляет пакет, возвращает False если такой уже существует.
        forwardPacket():
            Удаляет и возвращает самый старый пакет, либо [] если пусто.
        getCount(destination, startTime, endTime):
            Возвращает количество пакетов для данного назначения в интервале времени.
    """

    def __init__(self, memoryLimit):
        self.memoryLimit = memoryLimit
        self.queue = deque()  
        self.seen = set()     
        self.destMap = defaultdict(list)       
        self.startIndex = defaultdict(int)     

    def addPacket(self, source, destination, timestamp):
        key = (source, destination, timestamp)
        if key in self.seen:
            return False
        if len(self.queue) == self.memoryLimit:
            self.forwardPacket()
        self.queue.append(key)
        self.seen.add(key)
        self.destMap[destination].append(timestamp)
        return True

    def forwardPacket(self):
        if not self.queue:
            return []
        s, d, t = self.queue.popleft()
        self.seen.remove((s, d, t))
        if self.destMap[d][self.startIndex[d]] == t:
            self.startIndex[d] += 1
        return [s, d, t]

    def getCount(self, destination, startTime, endTime):
        arr = self.destMap[destination]
        start = self.startIndex[destination]
        L = bisect.bisect_left(arr, startTime, start)
        R = bisect.bisect_right(arr, endTime, start)
        return R - L

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks