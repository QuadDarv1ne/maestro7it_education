"""
Задача: Минимальное количество коробок для перераспределения яблок (LeetCode #3074)

https://leetcode.com/problems/apple-redistribution-into-boxes/

Описание:
Даны две коллекции:
1. apple - список, где apple[i] представляет количество яблок в i-й корзине
2. capacity - список, где capacity[j] представляет вместимость j-й коробки

Необходимо найти минимальное количество коробок, достаточное для упаковки всех яблок
из всех корзин. Яблоки из разных корзин можно комбинировать в одной коробке.

Подход:
1. Вычисляем общее количество яблок (сумма массива apple)
2. Сортируем коробки по убыванию вместимости (жадная стратегия)
3. Берем коробки с наибольшей вместимостью до тех пор, пока их суммарная
   вместимость не станет >= общего количества яблок

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

Временная сложность: O(n log n) из-за сортировки, где n = len(capacity)
Пространственная сложность: O(1) (не считая входных данных)
"""

class Solution(object):
    def minimumBoxes(self, apple, capacity):
        """
        :type apple: List[int]
        :type capacity: List[int]
        :rtype: int
        """
        # Вычисляем общее количество яблок
        total_apples = sum(apple)
        
        # Сортируем коробки по убыванию вместимости
        capacity.sort(reverse=True)
        
        # Жадный алгоритм: берем самые вместительные коробки
        current_capacity = 0
        boxes_used = 0
        
        for box_capacity in capacity:
            boxes_used += 1
            current_capacity += box_capacity
            
            # Если набрали достаточную вместимость
            if current_capacity >= total_apples:
                return boxes_used
        
        # Теоретически недостижимо (гарантируется, что суммарной вместимости хватит)
        return boxes_used