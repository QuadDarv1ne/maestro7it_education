'''
https://leetcode.com/problems/merge-intervals/description/
'''

class Solution:
    def merge(self, intervals):
        """
        Объединяет все перекрывающиеся интервалы в массиве intervals.

        :param intervals: Список интервалов, каждый из которых представлен парой [start, end].
        :return: Список объединённых интервалов.
        """
        if not intervals:
            return []

        # Сортировка интервалов по начальной точке
        intervals.sort(key=lambda x: x[0])
        merged = [intervals[0]]

        for current in intervals[1:]:
            last = merged[-1]
            if current[0] <= last[1]:  # Есть перекрытие
                last[1] = max(last[1], current[1])  # Объединяем интервалы
            else:
                merged.append(current)  # Нет перекрытия, добавляем новый интервал

        return merged

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks