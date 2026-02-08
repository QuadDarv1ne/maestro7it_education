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
    def containsNearbyAlmostDuplicate(self, nums, k, t):
        """
        Проверяет, есть ли два элемента с разностью ≤ t на расстоянии ≤ k
        
        Args:
            nums: список целых чисел
            k: максимальное расстояние между индексами
            t: максимальная разность между значениями
            
        Returns:
            bool: True если существует пара удовлетворяющая условиям
        """
        if t < 0 or k < 0:
            return False
            
        # Создаем словарь для ведер
        bucket_dict = {}
        bucket_size = t + 1  # Ширина ведра
        
        for i, num in enumerate(nums):
            # Вычисляем номер ведра
            bucket_id = num // bucket_size
            
            # 1. Проверяем текущее ведро
            if bucket_id in bucket_dict:
                return True
                
            # 2. Проверяем соседние ведра
            if bucket_id - 1 in bucket_dict and abs(num - bucket_dict[bucket_id - 1]) <= t:
                return True
                
            if bucket_id + 1 in bucket_dict and abs(num - bucket_dict[bucket_id + 1]) <= t:
                return True
                
            # Добавляем текущий элемент в ведро
            bucket_dict[bucket_id] = num
            
            # Удаляем элемент, который выходит за пределы окна k
            if i >= k:
                old_bucket_id = nums[i - k] // bucket_size
                del bucket_dict[old_bucket_id]
                
        return False