'''
https://leetcode.com/problems/four-divisors/
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Four Divisors"

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
import math

class Solution:
    def sumFourDivisors(self, nums):
        """
        Находит сумму всех делителей для чисел, имеющих ровно 4 делителя.
        
        Args:
            nums: список целых чисел
            
        Returns:
            Сумма всех делителей чисел, имеющих ровно 4 делителя
            
        Алгоритм:
        1. Для каждого числа находим все его делители
        2. Если количество делителей равно 4, суммируем их
        3. Используем оптимизацию: перебираем делители до sqrt(num)
        4. Прерываем поиск, если найдено более 4 делителей
        """
        def get_divisors_sum(num):
            """
            Находит сумму делителей числа, если их ровно 4.
            Возвращает 0, если количество делителей не равно 4.
            """
            # Всегда есть делители 1 и само число
            divisors = {1, num}
            
            # Перебираем возможные делители до sqrt(num)
            for i in range(2, int(math.sqrt(num)) + 1):
                if num % i == 0:
                    divisors.add(i)
                    divisors.add(num // i)
                    
                    # Если уже больше 4 делителей, можно прекратить
                    if len(divisors) > 4:
                        return 0
            
            # Проверяем, что делителей ровно 4
            if len(divisors) == 4:
                return sum(divisors)
            return 0
        
        total_sum = 0
        
        for num in nums:
            total_sum += get_divisors_sum(num)
            
        return total_sum