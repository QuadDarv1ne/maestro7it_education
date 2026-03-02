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
    def firstUniqChar(self, s: str) -> int:
        """
        Возвращает индекс первого неповторяющегося символа в строке.
        Если такого символа нет, возвращает -1.

        Алгоритм:
        1. Подсчитываем частоту каждого символа с помощью массива на 26 элементов.
        2. Проходим по строке повторно и возвращаем индекс первого символа с частотой 1.

        Аргументы:
            s (str): строка из строчных латинских букв.

        Возвращает:
            int: индекс первого уникального символа или -1.
        """
        count = [0] * 26

        # Первый проход: подсчёт частот
        for ch in s:
            count[ord(ch) - ord('a')] += 1

        # Второй проход: поиск первого символа с частотой 1
        for i, ch in enumerate(s):
            if count[ord(ch) - ord('a')] == 1:
                return i

        return -1