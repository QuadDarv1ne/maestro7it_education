'''
https://leetcode.com/problems/make-sum-divisible-by-p/description/?envType=daily-question&envId=2025-11-30
Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X  
GitHub: https://github.com/QuadDarv1ne/  

Решение задачи "Make Sum Divisible by P"
'''

class Solution:
    def minSubarray(self, nums, p):
        """
        Находит минимальную длину подмассива, который нужно удалить, чтобы сумма оставшихся элементов была делима на p.
        
        Args:
            nums (list[int]): Входной массив чисел
            p (int): Делитель
            
        Returns:
            int: Минимальная длина подмассива для удаления, или -1 если невозможно
        """
        total_sum = sum(nums)
        remainder = total_sum % p
        
        # Если сумма уже делится на p, не нужно удалять подмассив
        if remainder == 0:
            return 0
            
        prefix_sum = 0
        prefix_map = {0: -1}  # Хранит остаток от деления префиксной суммы и индекс
        min_length = len(nums)
        
        for i, num in enumerate(nums):
            prefix_sum = (prefix_sum + num) % p
            target = (prefix_sum - remainder) % p
            if target in prefix_map:
                min_length = min(min_length, i - prefix_map[target])
            prefix_map[prefix_sum] = i
            
        return min_length if min_length < len(nums) else -1

'''
Полезные ссылки:
1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
2. Telegram №1 @quadd4rv1n7
3. Telegram №2 @dupley_maxim_1999
4. Rutube канал: https://rutube.ru/channel/4218729/
5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
6. YouTube канал: https://www.youtube.com/@it-coders
7. ВК группа: https://vk.com/science_geeks
'''