'''
326. Power of Three (Python) by Dupley Maxim Igorevich
https://leetcode.com/problems/power-of-three/description/?envType=daily-question&envId=2025-08-13

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

class Solution:
    def isPowerOfThree(self, n):
        """
        Определяет, является ли число n степенью числа 3.

        Алгоритм:
        - Максимальная степень числа 3, которая помещается в 32-битное целое число, равна 3^19 = 1162261467.
        - Если n > 0 и 1162261467 делится на n без остатка, значит n является степенью числа 3.
        - Преимущество данного метода в том, что он не использует циклы и логарифмы, а работает за O(1).

        Параметры:
        n (int): Целое число для проверки.

        Возвращает:
        bool: True, если n является степенью числа 3, иначе False.

        Примеры:
        >>> Solution().isPowerOfThree(27)
        True
        >>> Solution().isPowerOfThree(0)
        False
        >>> Solution().isPowerOfThree(9)
        True
        """
        return n > 0 and 1162261467 % n == 0

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks