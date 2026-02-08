"""
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
"""

import heapq
from collections import defaultdict

class Solution:
    def getSkyline(self, buildings):
        """
        Возвращает контур неба (skyline) для заданных зданий.
        
        Контур неба представляет собой список ключевых точек [[x1, y1], [x2, y2], ...],
        где каждая точка является началом горизонтального отрезка на высоте y.
        Последняя точка имеет высоту 0.
        В контуре нет двух последовательных точек с одинаковой высотой.
        
        Параметры:
        -----------
        buildings : list[list[int]]
            Список зданий, где каждое здание представлено как [left, right, height]
            left - координата X левой границы
            right - координата X правой границы  
            height - высота здания
            
        Возвращает:
        -----------
        list[list[int]]
            Список ключевых точек контура неба в формате [[x1, y1], [x2, y2], ...]
            
        Пример:
        --------
        >>> solution = Solution()
        >>> buildings = [[2,9,10],[3,7,15],[5,12,12],[15,20,10],[19,24,8]]
        >>> solution.getSkyline(buildings)
        [[2,10],[3,15],[7,12],[12,0],[15,10],[20,8],[24,0]]
        """
        if not buildings:
            return []
        
        # Создаем события: начало и конец зданий
        # Для начала здания используем отрицательную высоту для правильной сортировки
        events = []
        for left, right, height in buildings:
            events.append((left, height, 0))   # Событие начала (0)
            events.append((right, height, 1))  # Событие конца (1)
        
        # Сортируем события:
        # 1. По координате X
        # 2. По типу события (начало перед концом при одинаковом X)
        # 3. Для начала: выше здания первыми, для конца: ниже здания первыми
        events.sort(key=lambda x: (x[0], x[2], x[1] if x[2] == 1 else -x[1]))
        
        # Результат и структуры для отслеживания текущих высот
        result = []
        max_heap = [0]  # Максимальная куча (храним отрицательные значения для эмуляции max-heap)
        active_heights = defaultdict(int)  # Счетчик активных высот
        active_heights[0] = 1  # Уровень земли всегда активен
        
        # Обрабатываем все события
        for x, height, event_type in events:
            if event_type == 0:  # Событие начала здания
                heapq.heappush(max_heap, -height)
                active_heights[height] += 1
            else:  # Событие конца здания
                active_heights[height] -= 1
            
            # Удаляем неактивные высоты из кучи (ленивое удаление)
            while max_heap and active_heights[-max_heap[0]] == 0:
                heapq.heappop(max_heap)
            
            # Получаем текущую максимальную высоту
            current_max = -max_heap[0]
            
            # Добавляем точку в результат, если высота изменилась
            if not result or result[-1][1] != current_max:
                # Если уже есть точка с таким же X, обновляем ее
                if result and result[-1][0] == x:
                    result[-1][1] = max(result[-1][1], current_max)
                else:
                    result.append([x, current_max])
        
        # Объединяем последовательные точки с одинаковой высотой
        merged_result = []
        for point in result:
            if not merged_result or merged_result[-1][1] != point[1]:
                merged_result.append(point)
        
        return merged_result