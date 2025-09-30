'''
https://leetcode.com/problems/climbing-stairs/description/?envType=study-plan-v2&envId=top-interview-150

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

class Solution:
    def climbStairs(self, n):
        """
        Вычисляет число способов подняться на вершину лестницы из n ступеней, 
        если за один шаг можно подняться на одну или две ступени.

        Подход:
        Проблема сводится к числам Фибоначчи: ways[n] = ways[n-1] + ways[n-2].
        Используется динамическое программирование с O(1) доп. памятью:
        храним только два предыдущих значения.

        :param n: int — количество ступеней
        :return: int — число способов достижения n-й ступени
        Сложность:
        Время: O(n)
        Память: O(1)
        """
        if n <= 1:
            return 1
        first, second = 1, 2  # для n = 1 → 1, n = 2 → 2
        for _ in range(3, n + 1):
            first, second = second, first + second
        return first if n == 1 else second

''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks