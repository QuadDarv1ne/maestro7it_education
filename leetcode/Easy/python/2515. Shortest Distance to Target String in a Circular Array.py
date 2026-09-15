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

# from typing import List

class Solution(object):
    def closestTarget(self, words, target, startIndex):
        """
        :type words: List[str]
        :type target: str
        :type startIndex: int
        :rtype: int
        
        Возвращает кратчайшее расстояние от startIndex до любого вхождения target
        в циклическом массиве words. Если target отсутствует, возвращает -1.
        
        Алгоритм:
        1. Проходим по всем индексам массива
        2. Если находим target, вычисляем расстояние по кругу в обе стороны
        3. Берём минимум среди всех найденных расстояний
        
        Временная сложность: O(n)
        Пространственная сложность: O(1)
        """
        n = len(words)
        min_distance = float('inf')
        
        for i in range(n):
            if words[i] == target:
                # Расстояние по часовой стрелке (вправо)
                clockwise = (i - startIndex) % n
                # Расстояние против часовой стрелки (влево)
                counter_clockwise = (startIndex - i) % n
                # Кратчайшее расстояние до этого индекса
                distance = min(clockwise, counter_clockwise)
                # Обновляем глобальный минимум
                min_distance = min(min_distance, distance)
        
        return -1 if min_distance == float('inf') else min_distance