'''
https://leetcode.com/problems/successful-pairs-of-spells-and-potions/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
'''

import bisect

class Solution(object):
    def successfulPairs(self, spells, potions, success):
        """
        Решение задачи Successful Pairs of Spells and Potions.

        Идея:
        - Сортируем массив potions.
        - Для каждого spell вычисляем минимальное required = ceil(success / spell).
        - Используем бинарный поиск (bisect_left) в potions, чтобы найти первый элемент ≥ required.
        - Ответ = len(potions) − найденный индекс.
        Сложность: O((n + m) log m)
        """
        potions.sort()
        m = len(potions)
        result = []
        for spell in spells:
            # минимальное значение зелья, чтобы product >= success
            # required = ceil(success / spell), но аккуратно с целочисленными делениями
            # required = (success + spell - 1) // spell
            # но чтобы избежать переполнений, используем float или long
            if spell == 0:
                # если spell == 0, то никогда не будет успешной пары (если success > 0)
                result.append(0)
                continue
            # вычисляем пороговое potion
            # используем целочисленное деление, но корректно:
            req = (success + spell - 1) // spell
            # находим индекс первого potion >= req
            idx = bisect.bisect_left(potions, req)
            result.append(m - idx)
        return result

''' Полезные ссылки: '''
# 1. Telegram ❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. Telegram №1 @quadd4rv1n7
# 3. Telegram №2 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks