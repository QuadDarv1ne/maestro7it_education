'''
https://leetcode.com/problems/multiply-strings/description/
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
'''

class Solution:
    def minFlips(self, s):
        """
        Возвращает минимальное количество переворотов битов (type-2),
        необходимое для превращения строки в чередующуюся после любого числа
        циклических сдвигов (type-1).

        Алгоритм:
        - Удваиваем строку, чтобы учесть все циклические сдвиги.
        - Для каждого окна длины n считаем количество несовпадений с шаблоном
          '0101...' (начиная с 0). Используем префиксные суммы.
        - Минимум для окна = min(несовпадения, n - несовпадения).
        - Ответ — минимум по всем окнам.

        Параметры:
        s (str): исходная двоичная строка.

        Возвращает:
        int: минимальное количество переворотов.
        """
        n = len(s)
        t = s + s  # удвоенная строка для моделирования сдвигов
        # diff[j] = 1, если символ t[j] не совпадает с шаблоном (0 на чётных, 1 на нечётных)
        diff = [0] * (2 * n)
        for j, ch in enumerate(t):
            expected = '0' if j % 2 == 0 else '1'
            diff[j] = 1 if ch != expected else 0

        # Префиксные суммы для diff
        pref = [0] * (2 * n + 1)
        for j in range(2 * n):
            pref[j + 1] = pref[j] + diff[j]

        ans = n  # максимально возможное значение
        for i in range(n):
            flips = pref[i + n] - pref[i]  # несовпадения с шаблоном для окна [i, i+n-1]
            ans = min(ans, flips, n - flips)

        return ans