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
    def isUgly(self, n):
        """
        Проверяет, является ли число "некрасивым" (ugly number).
        
        Некрасивое число - это положительное целое число, простые множители которого 
        ограничены числами 2, 3 и 5.
        
        Параметры:
        n (int): Число для проверки
        
        Возвращает:
        bool: True, если число является некрасивым, иначе False
        
        Алгоритм:
        1. Числа ≤ 0 не являются некрасивыми
        2. 1 считается некрасивым числом
        3. Последовательно делим число на 2, 3 и 5, пока это возможно
        4. Если после всех делений остаётся 1, число некрасивое
        
        Примеры:
        >>> isUgly(6)    # 6 = 2 × 3
        True
        >>> isUgly(14)   # 14 = 2 × 7 (7 не входит в разрешённые множители)
        False
        
        Сложность:
        Время: O(log n) - на каждом шаге уменьшаем число
        Память: O(1) - используем константную память
        """
        if n <= 0:
            return False
        
        # Последовательно делим на разрешённые простые множители
        for factor in (2, 3, 5):
            while n % factor == 0:
                n //= factor
        
        # Если остался 1, значит других множителей нет
        return n == 1