"""
Разделение квадратов II - решение на основе C++ кода

@param squares: List[List[int]] - квадраты [x, y, длина]
@return: float - минимальная y-координата линии, делящей площадь пополам

Сложность: O(n log n) время, O(n) память.

Алгоритм:
1. Сбор уникальных X-координат и создание дерева отрезков
2. Создание и сортировка событий (начало/конец квадратов)
3. Первый проход: вычисление общей площади
4. Второй проход: поиск y, где накопленная площадь = половина

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
"""

import bisect
# from typing import List

class SegmentTree:
    """Дерево отрезков для отслеживания покрытой ширины на оси X"""
    def __init__(self, xs):
        self.xs = xs  # Отсортированный список уникальных X-координат
        self.n = len(xs) - 1  # Количество отрезков между координатами
        self.cnt = [0] * (4 * self.n)  # Счетчик покрытий для каждого узла
        self.width = [0] * (4 * self.n)  # Покрытая ширина для каждого узла
    
    def _add(self, tree_idx, lo, hi, i, j, val):
        """
        Рекурсивное добавление значения к отрезку
        lo, hi - индексы в массиве xs (концы отрезков)
        i, j - координаты x (не индексы!)
        """
        # Проверяем, что отрезок [xs[lo], xs[lo+1]] не пересекается с [i, j]
        if j <= self.xs[lo] or self.xs[hi + 1] <= i:
            return
        
        # Если отрезок полностью покрывается [i, j]
        if i <= self.xs[lo] and self.xs[hi + 1] <= j:
            self.cnt[tree_idx] += val
        else:
            # Иначе рекурсивно обновляем детей
            mid = (lo + hi) // 2
            self._add(2 * tree_idx + 1, lo, mid, i, j, val)
            self._add(2 * tree_idx + 2, mid + 1, hi, i, j, val)
        
        # Пересчитываем покрытую ширину для узла
        if self.cnt[tree_idx] > 0:
            self.width[tree_idx] = self.xs[hi + 1] - self.xs[lo]
        elif lo == hi:
            self.width[tree_idx] = 0
        else:
            self.width[tree_idx] = self.width[2 * tree_idx + 1] + self.width[2 * tree_idx + 2]
    
    def add(self, i, j, val):
        """Добавляет значение к интервалу [i, j]"""
        if i < j:
            self._add(0, 0, self.n - 1, i, j, val)
    
    def get_covered_width(self):
        """Возвращает общую покрытую ширину"""
        return self.width[0]


class Solution:
    def separateSquares(self, squares):
        # 1. Собираем события и уникальные X-координаты
        events = []  # (y, delta, x_left, x_right)
        xs_set = set()
        
        for square in squares:
            x, y, l = square
            x_right = x + l
            events.append((y, 1, x, x_right))  # Начало квадрата
            events.append((y + l, -1, x, x_right))  # Конец квадрата
            xs_set.add(x)
            xs_set.add(x_right)
        
        # 2. Сортируем события и X-координаты
        events.sort()
        xs = sorted(xs_set)
        
        # 3. Вспомогательная функция для вычисления площади
        def get_area(events_list, xs_list):
            """Вычисляет общую площадь объединения квадратов"""
            tree = SegmentTree(xs_list)
            total_area = 0
            prev_y = 0
            
            for y, delta, xl, xr in events_list:
                covered_width = tree.get_covered_width()
                total_area += covered_width * (y - prev_y)
                tree.add(xl, xr, delta)
                prev_y = y
            
            return total_area
        
        # 4. Вычисляем общую площадь и половину
        total_area = get_area(events, xs)
        half_area = total_area / 2.0
        
        # 5. Второй проход для поиска разделяющей линии
        tree = SegmentTree(xs)
        accumulated = 0.0
        prev_y = 0
        
        for y, delta, xl, xr in events:
            covered_width = tree.get_covered_width()
            
            # Проверяем, не превысили ли мы half_area
            if covered_width > 0:
                area_gain = covered_width * (y - prev_y)
                if accumulated + area_gain >= half_area - 1e-12:
                    # Нашли интервал, где накопленная площадь достигнет half_area
                    return prev_y + (half_area - accumulated) / covered_width
            
            # Обновляем накопленную площадь и дерево
            accumulated += covered_width * (y - prev_y)
            tree.add(xl, xr, delta)
            prev_y = y
        
        # Если не нашли (все квадраты ниже линии), возвращаем последний y
        return prev_y