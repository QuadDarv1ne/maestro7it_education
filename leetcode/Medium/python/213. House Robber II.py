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
    def rob(self, nums):
        """
        Находит максимальную сумму, которую можно украсть из домов, расположенных по кругу.
        
        Алгоритм:
        1. Если домов нет -> 0
        2. Если 1 дом -> его значение
        3. Если 2 дома -> максимум из двух
        4. Иначе:
           - Вариант 1: Грабим с 0 до n-2 (без последнего)
           - Вариант 2: Грабим с 1 до n-1 (без первого)
           - Берем максимум
        
        Сложность: O(n) время, O(1) память
        """
        
        # Базовые случаи
        n = len(nums)
        if n == 0:
            return 0
        if n == 1:
            return nums[0]
        if n == 2:
            return max(nums[0], nums[1])
        
        # Вспомогательная функция для линейного случая
        def rob_linear(arr):
            """Решает задачу House Robber I для линейного массива"""
            prev2 = 0  # dp[i-2]
            prev1 = 0  # dp[i-1]
            
            for num in arr:
                # Формула DP: dp[i] = max(dp[i-1], dp[i-2] + nums[i])
                current = max(prev1, prev2 + num)
                prev2, prev1 = prev1, current
            
            return prev1
        
        # Два сценария для кругового расположения
        # 1. Без последнего дома
        scenario1 = rob_linear(nums[:-1])
        
        # 2. Без первого дома
        scenario2 = rob_linear(nums[1:])
        
        # Возвращаем максимум
        return max(scenario1, scenario2)