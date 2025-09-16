'''
 https://leetcode.com/problems/replace-non-coprime-numbers-in-array/description/?envType=daily-question&envId=2025-09-16
'''

import math
# from typing import List

class Solution:
    def replaceNonCoprimes(self, nums):
        """
        Заменяет не взаимно простые соседние числа в массиве на их НОК (наименьшее общее кратное)
        до тех пор, пока все соседние пары не станут взаимно простыми.
        
        Алгоритм использует стек для эффективной обработки массива:
        1. Берем каждое число из исходного массива
        2. Сравниваем его с верхним элементом стека
        3. Если НОД > 1 (числа не взаимно простые), заменяем их на НОК
        4. Повторяем шаг 2 с новым числом, пока возможно
        
        Args:
            nums (List[int]): Список целых положительных чисел.
        
        Returns:
            List[int]: Массив после всех возможных замен не взаимно простых чисел.
        
        Пример:
            Вход: [6, 4, 3, 2, 1]
            Выход: [12, 1]
        """
        def gcd(a, b):
            while b != 0:
                a, b = b, a % b
            return a

        stack = []
        for num in nums:
            while stack:
                g = gcd(stack[-1], num)
                if g > 1:
                    num = stack.pop() * num // g
                else:
                    break
            stack.append(num)
        return stack

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ:   https://t.me/hut_programmer_07  
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/  
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ  
# 6. YouTube канал: https://www.youtube.com/@it-coders  
# 7. ВК группа: https://vk.com/science_geeks