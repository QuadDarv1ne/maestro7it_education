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
    def longestPalindrome(self, s: str) -> int:
        """
        Возвращает максимальную длину палиндрома, который можно составить из букв строки.
        Используем подсчёт частот символов: берём все пары и, возможно, один центральный элемент.

        Аргументы:
            s (str): исходная строка из букв (учёт регистра).

        Возвращает:
            int: длина самого длинного палиндрома.
        """
        from collections import Counter
        freq = Counter(s)
        length = 0
        odd_exists = False

        for count in freq.values():
            # Добавляем все возможные пары
            length += (count // 2) * 2
            # Если есть нечётная частота, запоминаем
            if count % 2 == 1:
                odd_exists = True

        # Можно добавить один символ в центр, если была нечётная частота
        if odd_exists:
            length += 1

        return length