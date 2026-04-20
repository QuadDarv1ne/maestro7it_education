"""
Задача: Сложение двоичных строк (Add Binary)
https://leetcode.com/problems/add-binary/description/

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

Описание:
Даны две двоичные строки a и b, верните их сумму как двоичную строку.

Алгоритм:
- Используем поситочное сложение "столбиком" с переносом (carry).
- Идём с конца строк к началу.
- На каждом шаге складываем: bit_a + bit_b + carry.
- Результат бита: сумма % 2, новый carry: сумма // 2.
- В конце, если остался carry, добавляем '1' в начало.

Сложность:
- Время: O(max(len(a), len(b)))
- Память: O(max(len(a), len(b))) для результата.

Пример:
Input: a = "11", b = "1"
Output: "100"
"""

class Solution(object):
    def maxDistance(self, colors):
        """
        Находит максимальное расстояние между двумя домами с разными цветами.
        
        Условие:
        - Дома выстроены в линию, у каждого есть цвет (число).
        - Расстояние между домами i и j = |i - j|.
        - Нужно найти максимальное расстояние между двумя домами с РАЗНЫМИ цветами.
        
        Алгоритм:
        - Максимальное расстояние всегда будет достигаться с участием 
          крайнего левого (индекс 0) или крайнего правого (индекс n-1) дома.
        - Проходим слева направо: ищем самый дальний дом справа, 
          цвет которого отличается от colors[0].
        - Проходим справа налево: ищем самый дальний дом слева,
          цвет которого отличается от colors[n-1].
        - Берём максимум из двух найденных расстояний.
        
        Временная сложность: O(n), где n = len(colors)
        Пространственная сложность: O(1)
        
        Примеры:
        >>> Solution().maxDistance([1,1,1,6,1,1,1])
        3
        >>> Solution().maxDistance([1,8,3,8,3])
        4
        >>> Solution().maxDistance([0,1])
        1
        
        :type colors: List[int]
        :rtype: int
        """
        n = len(colors)
        max_dist = 0
        
        # Проход слева направо: ищем дом справа с цветом, отличным от первого
        for i in range(n - 1, -1, -1):
            if colors[i] != colors[0]:
                max_dist = max(max_dist, i)
                break  # нашли самый дальний, дальше не нужно
        
        # Проход справа налево: ищем дом слева с цветом, отличным от последнего
        for i in range(n):
            if colors[i] != colors[n - 1]:
                max_dist = max(max_dist, n - 1 - i)
                break  # нашли самый дальний
        
        return max_dist