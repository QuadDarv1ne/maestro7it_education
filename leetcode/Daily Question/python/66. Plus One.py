'''
https://leetcode.com/problems/plus-one/description/
Автор: Дуплей Максим Игоревич - AGLA
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/

Решение задачи "Plus One"

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
    def plusOne(self, digits):
        """
        Увеличивает большое число, представленное массивом цифр, на единицу.
        
        Args:
            digits: массив цифр числа от старшего разряда к младшему
            
        Returns:
            Массив цифр результата увеличения на 1
            
        Алгоритм:
        - Идем с конца массива к началу
        - Если цифра < 9, увеличиваем ее на 1 и возвращаем результат
        - Если цифра = 9, устанавливаем ее в 0 и продолжаем
        - Если все цифры были 9, добавляем 1 в начало массива
        """
        n = len(digits)
        
        # Идем с конца массива (младшего разряда)
        for i in range(n - 1, -1, -1):
            if digits[i] < 9:
                # Если цифра меньше 9, просто увеличиваем ее
                digits[i] += 1
                return digits
            else:
                # Если цифра равна 9, устанавливаем 0 и продолжаем перенос
                digits[i] = 0
        
        # Если дошли сюда, значит все цифры были 9
        # Создаем новый массив с 1 в начале
        return [1] + digits