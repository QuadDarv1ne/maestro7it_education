'''
Задача: Два лучших непересекающихся события (LeetCode #2054)
* https://leetcode.com/problems/two-best-non-overlapping-events/

Описание:
 * Дан массив событий events, где events[i] = [startTime_i, endTime_i, value_i].
 * Каждое событие имеет время начала, время окончания и ценность.
 * Необходимо выбрать не более двух непересекающихся событий, чтобы максимизировать сумму их ценностей.
 * События не пересекаются, если конец первого события строго меньше начала второго (включительно: end < start).
'''

import bisect
# from typing import List

class Solution:
    def maxTwoEvents(self, events):
        """
        Находит максимальную сумму ценностей не более чем двух непересекающихся событий.
        
        Args:
            events: List[List[int]] - события в формате [начало, конец, ценность]
            
        Returns:
            int - максимальная сумма ценностей
            
        Автор: Дуплей Максим Игоревич
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
        
        Сложность:
        - Время: O(n log n) из-за сортировки и бинарного поиска
        - Память: O(n) для хранения отсортированных массивов и префиксных максимумов
        """

        # Сортируем события по времени окончания
        events_sorted_by_end = sorted(events, key=lambda x: x[1])
        n = len(events_sorted_by_end)
        
        # Создаем массивы времен окончания и префиксных максимумов
        end_times = [0] * n
        prefix_max = [0] * n
        
        for i, (_, end, value) in enumerate(events_sorted_by_end):
            end_times[i] = end
            prefix_max[i] = max(prefix_max[i-1] if i > 0 else 0, value)
        
        # Инициализируем ответ максимальной ценностью одного события
        max_value = max(val for _, _, val in events)
        
        # Перебираем каждое событие как второе
        for start, _, value in events:
            # Находим индекс последнего события, которое заканчивается до start
            idx = bisect.bisect_left(end_times, start) - 1
            
            if idx >= 0:
                max_value = max(max_value, prefix_max[idx] + value)
        
        return max_value