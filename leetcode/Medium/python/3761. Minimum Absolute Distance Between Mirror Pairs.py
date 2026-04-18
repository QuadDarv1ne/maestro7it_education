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

class Solution:
    def minMirrorPairDistance(self, nums):
        """
        Находит минимальное расстояние между зеркальными парами в массиве.

        Зеркальная пара: индексы (i, j), где i < j и reverse(nums[i]) == nums[j].

        Алгоритм:
        1. Инициализируем `min_dist = infinity` и словарь `last_seen`.
        2. Идем по массиву с индексом `i` и значением `val`:
           a. Если `val` уже есть в `last_seen` (значит, ранее был элемент, 
              перевертыш которого равен `val`), обновляем `min_dist` 
              значением `i - last_seen[val]`.
           b. Вычисляем `rev = reverse(val)` и сохраняем `i` в `last_seen[rev]`
              (обновляя индекс последнего вхождения перевернутого числа).
        3. Возвращаем `min_dist`, если он был обновлен, иначе -1.
        """
        min_dist = float('inf')
        last_seen = {}
        
        for i, val in enumerate(nums):
            # 1. Проверка: является ли текущий элемент правой частью пары
            if val in last_seen:
                dist = i - last_seen[val]
                if dist < min_dist:
                    min_dist = dist
            
            # 2. Регистрация текущего элемента как будущей левой части
            # Переворот числа через строку
            rev = int(str(val)[::-1])
            last_seen[rev] = i
            
        return min_dist if min_dist != float('inf') else -1