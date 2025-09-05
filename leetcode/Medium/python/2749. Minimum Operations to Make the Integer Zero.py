'''
https://leetcode.com/problems/minimum-operations-to-make-the-integer-zero/description/?envType=daily-question&envId=2025-09-05
'''

class Solution:
    def makeTheIntegerZero(self, num1, num2):
        """
        Задача: найти минимальное количество операций, чтобы из num1 получить 0.
        В каждой операции выбирается i ∈ [0, 60], и выполняется вычитание:
            num1 = num1 - (2^i + num2)

        Условие:
        - Пусть k = количество операций.
        - Пусть target = num1 - k * num2.
        Тогда target должен быть представим как сумма ровно k степеней двойки.
        Это возможно, если:
            popcount(target) <= k <= target.

        Возвращает:
            Минимальное количество операций k, если возможно, иначе -1.
        """
        def popcount(x):
            return bin(x).count("1")

        for k in range(61):
            target = num1 - k * num2
            if target >= 0 and popcount(target) <= k <= target:
                return k
        return -1

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks