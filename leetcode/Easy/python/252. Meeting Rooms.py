'''
https://leetcode.com/problems/meeting-rooms/description/
'''

from typing import List

class Solution:
    def canAttendMeetings(self, intervals):
        """
        Проверяет, можно ли провести все встречи в одном помещении.

        Алгоритм:
        1. Сортируем встречи по времени начала.
        2. Проверяем перекрытия между соседними встречами.

        :param intervals: Список встреч [start, end]
        :return: True, если все встречи можно провести без пересечений, иначе False
        """
        intervals.sort(key=lambda x: x[0])
        for i in range(1, len(intervals)):
            if intervals[i][0] < intervals[i-1][1]:
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