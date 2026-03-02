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

from collections import Counter
from typing import List

class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        """
        Возвращает пересечение двух массивов с учётом кратности элементов.
        Использует словарь частот для меньшего массива.
        
        Аргументы:
            nums1 (List[int]): первый массив целых чисел.
            nums2 (List[int]): второй массив целых чисел.
        
        Возвращает:
            List[int]: массив, содержащий общие элементы с учётом повторений.
        """
        # Для оптимизации памяти выбираем меньший массив для подсчёта частот
        if len(nums1) > len(nums2):
            # Убедимся, что nums1 — меньший
            nums1, nums2 = nums2, nums1
        
        # Строим частотный словарь для меньшего массива
        freq = Counter(nums1)
        
        result = []
        for num in nums2:
            # Если число есть в словаре и его счётчик > 0
            if freq.get(num, 0) > 0:
                result.append(num)
                freq[num] -= 1
                
        return result