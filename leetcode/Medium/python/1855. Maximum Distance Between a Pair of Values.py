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

class Solution:
    def maxDistance(self, nums1, nums2):
        """
        Находит максимальное расстояние между валидной парой индексов (i, j),
        где i <= j и nums1[i] <= nums2[j].
        
        Параметры:
        nums1: List[int] - первый невозрастающий массив
        nums2: List[int] - второй невозрастающий массив
        
        Возвращает:
        int - максимальное расстояние (j - i) или 0, если валидных пар нет
        """
        i = j = max_dist = 0
        len1, len2 = len(nums1), len(nums2)
        
        while i < len1 and j < len2:
            if nums1[i] <= nums2[j]:
                if i <= j:
                    max_dist = max(max_dist, j - i)
                j += 1
            else:
                i += 1
        return max_dist