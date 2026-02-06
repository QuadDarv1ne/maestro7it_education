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

# Python
class Solution:
    """
    Находит максимальную разность между последовательными элементами в отсортированной форме.
    Использует bucket sort для достижения O(n) времени.
    
    Подход:
    1. Находим min и max элементы
    2. Создаем корзины с размером (max - min) / (n - 1)
    3. Для каждой корзины храним только min и max
    4. Максимальный gap находится между корзинами, а не внутри
    
    Сложность по времени: O(n)
    Сложность по памяти: O(n)
    """
    
    def maximumGap(self, nums):
        n = len(nums)
        if n < 2:
            return 0
        
        # Находим min и max
        min_val = min(nums)
        max_val = max(nums)
        
        if min_val == max_val:
            return 0
        
        # Размер корзины
        bucket_size = max(1, (max_val - min_val) // (n - 1))
        bucket_count = (max_val - min_val) // bucket_size + 1
        
        # Инициализируем корзины [min, max]
        buckets = [[float('inf'), float('-inf')] for _ in range(bucket_count)]
        
        # Распределяем элементы по корзинам
        for num in nums:
            idx = (num - min_val) // bucket_size
            buckets[idx][0] = min(buckets[idx][0], num)
            buckets[idx][1] = max(buckets[idx][1], num)
        
        # Ищем максимальный gap между корзинами
        max_gap = 0
        prev_max = min_val
        
        for bucket_min, bucket_max in buckets:
            if bucket_min == float('inf'):
                # Пустая корзина
                continue
            
            max_gap = max(max_gap, bucket_min - prev_max)
            prev_max = bucket_max
        
        return max_gap