'''
https://leetcode.com/problems/n-repeated-element-in-size-2n-array/description/
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "N-Repeated Element in Size 2N Array"

Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
'''

# from typing import List

class Solution:
    def repeatedNTimes(self, nums):
        """
        Находит элемент, повторяющийся N раз в массиве размером 2N.
        
        Args:
            nums: массив длины 2N, содержащий N+1 уникальных элементов,
                  один из которых повторяется N раз
                  
        Returns:
            Элемент, повторяющийся N раз
            
        Алгоритм 1: Использование множества (O(n) по времени, O(n) по памяти)
        Алгоритм 2: Проверка соседних элементов (O(n) по времени, O(1) по памяти)
        """
        # Способ 1: Использование множества (простой и понятный)
        seen = set()
        for num in nums:
            if num in seen:
                return num
            seen.add(num)
        
        # Способ 2: Альтернативный - проверка соседних элементов
        # Этот способ использует тот факт, что в массиве длиной 2N
        # повторяющийся элемент должен встречаться как минимум
        # дважды на расстоянии не более 3 позиций
        
        # Для полноты решения, если первый способ не сработал:
        # (хотя по условию задачи всегда будет найден элемент)
        return -1