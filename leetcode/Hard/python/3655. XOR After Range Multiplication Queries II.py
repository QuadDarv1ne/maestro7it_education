"""
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
"""

# -*- coding: utf-8 -*-
"""
Решение задачи "XOR After Range Multiplication Queries II".

Метод: декомпозиция на квадратный корень (sqrt decomposition).

Аргументы:
    nums: исходный массив целых чисел
    queries: список запросов [l, r, k, v]

Возвращает:
    int: побитовый XOR всех элементов после обработки запросов

Алгоритм:
    1. Устанавливаем порог B = √n
    2. Запросы с k > B обрабатываем напрямую
    3. Запросы с k ≤ B группируем по (k, l % k) + разностный массив
    4. Применяем множители через префиксное произведение
    5. Возвращаем XOR всех элементов

Сложность:
    Время: O(q·√n + n·√n)
    Память: O(n + q)

Автор: Дуплей М.И. | Источник: https://github.com/QuadDarv1ne/
"""

from collections import defaultdict
import math

class Solution:
    MOD = 10**9 + 7
    
    def xorAfterQueries(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[List[int]]
        :rtype: int
        """
        n = len(nums)
        if n == 0:
            return 0
        
        # Порог декомпозиции (совместимо с любым Python 3)
        B = int(math.sqrt(n)) + 1
        
        # Копируем массив для модификации
        arr = nums[:]
        
        # Группировка малых запросов: (k, mod) -> список (pos_l, pos_r, v)
        small_queries = defaultdict(list)
        
        for q in queries:
            l, r, k, v = q[0], q[1], q[2], q[3]
            if k > B:
                # Большие k: прямое применение
                idx = l
                while idx <= r:
                    arr[idx] = (arr[idx] * v) % self.MOD
                    idx += k
            else:
                # Малые k: добавляем в группу
                mod = l % k
                pos_l = (l - mod) // k
                pos_r = (r - mod) // k
                small_queries[(k, mod)].append((pos_l, pos_r, v))
        
        # Обработка малых запросов через разностный массив
        for key, qlist in small_queries.items():
            k, mod = key[0], key[1]
            # Размер виртуального массива для данной (k, mod)
            size = (n - mod + k - 1) // k
            diff = [1] * (size + 2)
            
            # Применяем мультипликативные обновления в diff-массив
            for item in qlist:
                pos_l, pos_r, v = item[0], item[1], item[2]
                diff[pos_l] = (diff[pos_l] * v) % self.MOD
                # Модульная инверсия через малую теорему Ферма
                inv_v = pow(v, self.MOD - 2, self.MOD)
                diff[pos_r + 1] = (diff[pos_r + 1] * inv_v) % self.MOD
            
            # Префиксное произведение и применение к исходному массиву
            mult = 1
            for pos in range(size):
                mult = (mult * diff[pos]) % self.MOD
                idx = mod + pos * k
                if idx < n:
                    arr[idx] = (arr[idx] * mult) % self.MOD
        
        # Вычисляем финальный XOR
        result = 0
        for val in arr:
            result ^= val
        return result